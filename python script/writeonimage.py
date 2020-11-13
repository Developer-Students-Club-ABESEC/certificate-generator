import csv 
import json 

from PIL import Image, ImageDraw, ImageFont

def genimage():
    image = Image.open('download.png')

    
    draw = ImageDraw.Draw(image)

    fontsize = int(input())
    
    font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)
    

    x, y= map(int,input("Enter the x and y corrdinate: ").split())


    color = 'rgb(255, 0, 0)'
    
    message = input("Enter your message: ")
    draw.text((x, y), message, fill=color, font=font)
    image.save("result.png")

def readfiles(csvFilePath):
    data = {} 
    keylist = []
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
        i = 0

        for rows in csvReader:
            key = i
            data[key] = dict(rows)
            i+=1
        for i in data[0].keys():
            keylist.append(i)
    print(data,keylist,sep="\n")

readfiles('records.csv')



 
