from django.shortcuts import render,redirect,HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os
# Create your views here.

def index(request):
    return render(request,"index.html")

def writeonimage(request):
    
    image = Image.open('download.png')

    
    draw = ImageDraw.Draw(image)

    fontsize = int(input())
    
    font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)
    

    x, y= map(int,input("Enter the x and y corrdinate: ").split())


    color = 'rgb(255, 0, 0)'
    
    message = input("Enter your message: ")
    draw.text((x, y), message, fill=color, font=font)
    image.save("result.png")


 
