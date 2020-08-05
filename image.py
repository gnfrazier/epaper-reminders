
from PIL import Image,ImageDraw,ImageFont

try: # this is for quick developement only
    import epd2in7b
    raspi = True
    
except:
    
    import matplotlib.pyplot as plt
    raspi = False
    
    
    # The folliwing line is useful in Jupyter notebook
    %matplotlib inline



if raspi:
    epd = epd2in7b.EPD()

    epd.init()
    epd.Clear()

    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
 
    
else:
    blackimage = Image.new('1', (298, 126), 255)  # 255: clear the frame
    redimage = Image.new('1', (298, 126), 255)  # 255: clear the frame
    HBlackimage = Image.new('1', (264, 126), 255)  # 298*126
    HRedimage = Image.new('1', (264, 126), 255)  # 298*126    



font_path = "usr/share/fonts/truetype/"

font24 = ImageFont.truetype('usr/share/fonts/truetype/droid/DroidSans.ttf', 24) #24 Chars across the screen
font18 = ImageFont.truetype('usr/share/fonts/truetype/droid/DroidSans.ttf', 18)

drawblack = ImageDraw.Draw(HBlackimage)
drawred = ImageDraw.Draw(HRedimage)
drawblack.text((10, 0), 'hello world', font = font24, fill = 0)
drawblack.text((10, 30), 'abcdefghijklmnopqrstu', font = font24, fill = 0)
drawblack.text((10, 60), 'abcdefghijklmnopqrstu', font = font24, fill = 0)
drawblack.text((10, 90), 'abcdefghijklmnopqrstu', font = font24, fill = 0)

#drawblack.text((150, 0), 'another line', font = font24, fill = 0)    
#drawblack.line((20, 50, 70, 100), fill = 0)
#drawblack.line((70, 50, 20, 100), fill = 0)
#drawblack.rectangle((20, 50, 70, 100), outline = 0)    
drawred.line((165, 50, 165, 100), fill = 0)
drawred.line((140, 75, 190, 75), fill = 0)
drawred.arc((140, 50, 190, 100), 0, 360, fill = 0)
drawred.rectangle((80, 50, 130, 100), fill = 0)
drawblack.rectangle((0, 0, 264, 126), outline = 0, width= 2)    

# plt.imshow(drawblack)
if raspi:
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))

else:
    display(HBlackimage)
