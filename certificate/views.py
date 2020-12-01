from django.shortcuts import render,redirect,HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os,csv,json,hashlib,shutil,base64
from datetime import datetime
from .models import csvdata,saveimage,fonts
from django.core.files.base import ContentFile
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

# Create your views here.

def handler404(request,exception):
    return render(request, '404.html')


def handler500(request):
    return render(request, '500.html')


def genkey():
    x = datetime.now()
    x = str(x)
    name = int(hashlib.sha256(x.encode('utf-8')).hexdigest(), 16) % 10**8
    return str(name)


def index(request):
    if(request.user.is_authenticated):
        return render(request,"csv.html")
    else:
        return render(request,"index.html")


def readata(request):
    csvFilePath = request.FILES["csv"]
    print(csvFilePath.name)
    name,extn = csvFilePath.name.split(".")
    if(extn!="csv"):
        return render(request,"csv.html",{"error":"The file type is not correct"})
    file_data = csvFilePath.read().decode("utf-8")
    file_data = file_data.strip("\n")
    file_data = file_data.strip(" ")
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
    obj = csvdata.objects.create(key=key,details=response)
    obj.save()
    fontfiles = fonts.objects.all()
    return render(request,"canvas.html",{"secret":key,"headers":keys,"fonts":fontfiles})



def writeonimage(request):
    image = request.POST["image"]
    config = request.POST["config"]
    config = json.loads(config)
    key = request.POST["key"]
    imagefile = ContentFile(base64.b64decode(image), name=key+".png")
    obj = saveimage.objects.create(photo=imagefile,key=key)
    obj.save()
    img = Image.open(os.getcwd()+'/certificate-generator/media/images/'+key+'.png')
    try:
        obj = csvdata.objects.get(key=key)
    except:
        return HttpResponse("Some error occured. Please try again later")
    data = obj.details
    resultpath=os.getcwd()+"/certificate-generator/media/result"+key
    os.mkdir(resultpath)
    for i in data.keys():
        img = Image.open(os.getcwd()+'/certificate-generator/media/images/'+key+'.png')
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
    downloadpath =  shutil.make_archive(os.getcwd()+"/certificate-generator/media/"+key,"zip",resultpath)
    return render(request,"result.html",{"download":key})



def addfont():
    folder  = os.getcwd()+"/certificate-generator/static/font"
    disp = []
    if(os.path.exists(folder)):
        lis = os.listdir(folder)
        for i in lis:
                name,extension = i.split(".")
                obj = fonts.objects.create(name=name,path=folder+"/"+str(i),fpath="/static/font/"+str(i))
                obj.save()

# def delfonts():
#     obj = fonts.objects.all()
#     for i in obj:
#         i.delete()



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
