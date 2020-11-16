from django.shortcuts import render,redirect,HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os,csv,json,hashlib,shutil,base64
from datetime import datetime
from .models import csvdata,saveimage
from django.core.files.base import ContentFile

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def genkey():
    x = datetime.now()
    x = str(x)
    name = int(hashlib.sha256(x.encode('utf-8')).hexdigest(), 16) % 10**8
    return str(name)

def index(request):
    return render(request,"csv.html")

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
    return render(request,"index.html",{"secret":key,"headers":keys})

    

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
        fontsize = 30
        font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)
        color = 'rgb(0,0,0)'
        for j in config.keys():
            x = int(config[j]['x'])
            y = int(config[j]['y'])
            columnname = config[j]['column']
            message = data[i][columnname]
            draw.text((x, y), message, fill=color, font=font)
            img.save(resultpath+"/"+str(key)+str(i)+".png")
    downloadpath =  shutil.make_archive("media/"+key,"zip",resultpath)
    return render(request,"result.html",{"download":key})

def result(request):
    return render(request,"result.html")




 
