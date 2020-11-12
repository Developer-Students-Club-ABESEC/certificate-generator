

from PIL import Image, ImageDraw, ImageFont


image = Image.open('download.png')

 
draw = ImageDraw.Draw(image)

fontsize = int(input())
 
font = ImageFont.truetype('C:/Windows/Fonts/Calibri.ttf', size=fontsize)
 

x, y= map(int,input("Enter the x and y corrdinate: ").split())


color = 'rgb(255, 0, 0)'
 
message = input("Enter your message: ")
draw.text((x, y), message, fill=color, font=font)
image.save("result.png")


 
