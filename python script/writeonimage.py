import csv 
import json 

from PIL import Image, ImageDraw, ImageFont

def genimage():
    image = Image.open('download.png')

    
    draw = ImageDraw.Draw(image)

    fontsize = 30
    
    font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)    


    color = 'rgb(255, 0, 0)'
    draw.text((23,45), "rajat", fill=color, font=font)   
    image.save("result.png")
    draw.text((123, 145), "rajat@gmail.com", fill=color, font=font)   
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

# readfiles('records.csv')
genimage()



 
