from django.shortcuts import render,redirect,HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os,csv,json,hashlib,shutil,base64
from datetime import datetime
from .models import csvdata,saveimage,fonts
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def genkey():
    x = datetime.now()
    x = str(x)
    name = int(hashlib.sha256(x.encode('utf-8')).hexdigest(), 16) % 10**8
    return str(name)


def dispfonts():
    lis = fonts.objects.values_list("name",flat=True)
    return lis

def index(request):
    if(request.user.is_authenticated):
        return render(request,"csv.html")
    else:
        return render(request,"index.html")
        

def readata(request):
    csvFilePath = request.FILES["csv"]
    file_data = csvFilePath.read().decode("utf-8")
    data = file_data.split("\n")
    keys = data[0].split(",")
    keys[-1] = keys[-1][:-1]
    response = {}
    for i in range(1,len(data)):
        temp = data[i].split(",")
        dic = {}
        for j in range(len(keys)):
            if("\r" in temp[j]):
                temp[j] = temp[j][:-1]
            dic[keys[j]] = temp[j]
        response[i] = dic
    key = genkey()
    print(key)
    obj = csvdata.objects.create(key=key,details=response)
    obj.save()
    fonts = dispfonts()
    return render(request,"canvas.html",{"secret":key,"headers":keys,"fonts":fonts})

    

def writeonimage(request):
    image = request.POST["image"]
    config = request.POST["config"]
    config = json.loads(config)
    key = request.POST["key"]
    imagefile = ContentFile(base64.b64decode(image), name=key+".png")
    obj = saveimage.objects.create(photo=imagefile,key=key)
    obj.save()
    img = Image.open(os.getcwd()+'/media/images/'+key+'.png')
    try:
        obj = csvdata.objects.get(key=key)
    except:
        return HttpResponse("Some error occured. Please try again later")
    data = obj.details
    resultpath="media/result"+key
    os.mkdir(resultpath)
    for i in data.keys():
        img = Image.open(os.getcwd()+'/media/images/'+key+'.png')
        draw = ImageDraw.Draw(img)
        for j in config.keys():
            x = int(config[j]['x'])
            y = int(config[j]['y'])
            columnname = config[j]['column']
            message = data[i][columnname]
            fontsize = int(config[j]['size'])
            fontstyle = config[j]['style']
            color = config[j]['color']
            obj = fonts.objects.get(name=fontstyle)
            path = obj.path
            font = ImageFont.truetype(path, size=fontsize)
            draw.text((x, y), message, fill=color, font=font)
            img.save(resultpath+"/"+str(key)+str(i)+".png")
    downloadpath =  shutil.make_archive("media/"+key,"zip",resultpath)
    return render(request,"result.html",{"download":key})

def result(request):
    return render(request,"result.html")

def addfont():
    folder  = "./fonts/font"
    disp = []
    if(os.path.exists(folder)):
        lis = os.listdir(folder)
        for i in lis:
            try:
                name,extension = i.split(".")
                obj = fonts.objects.create(name=name,path=folder+"/"+str(i))
                obj.save()
                print("added "+i)
            except:
                pass



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

