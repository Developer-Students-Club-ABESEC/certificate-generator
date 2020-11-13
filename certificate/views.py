from django.shortcuts import render,redirect,HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os,csv,json

# Create your views here.

def index(request):
    return render(request,"csv.html")

def readata(request):
    csvFilePath = request.FILES["csv"]
    file_data = csvFilePath.read().decode("utf-8")
    print(file_data)
    data = file_data.split("\n")
    keys = data[0].split(",")
    keys[-1] = keys[-1][:-1]
    response = []
    for i in range(1,len(data)):
        temp = data[i].split(",")
        dic = {}
        for i in range(len(keys)):
            if("\r" in temp[i]):
                temp[i] = temp[i][:-1]
            dic[keys[i]] = temp[i]
        response.append(dic)
    print(response)

    return render(request,"index.html",{"records":response,"headers":keys})


def writeonimage(request):
    image = request.POST["image"]

    fontsize = 30
    font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)
    

    x, y= map(int,input("Enter the x and y corrdinate: ").split())


    color = 'rgb(255, 0, 0)'
    
    message = input("Enter your message: ")
    # draw.text((x, y), message, fill=color, font=font)
    image.save("result.png")


 
