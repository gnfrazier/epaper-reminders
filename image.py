
#!/usr/bin/python3
# -*- coding:utf-8 -*-



from PIL import Image,ImageDraw,ImageFont

try: # this is for quick developement only
    import epd2in7b
    raspi = True
    
    font_path = '/usr/share/fonts/opentype/linux-libertine/LinBiolinum_R.otf'

    
except:
    
    import matplotlib.pyplot as plt
    raspi = False
    # font_path = "/usr/share/fonts/truetype/clear-sans/ClearSans-Regular.ttf"
    
    # The folliwing line is useful in Jupyter notebook
    # %matplotlib inline

font_path = '/usr/share/fonts/opentype/linux-libertine/LinBiolinum_R.otf'

if raspi:
    epd = epd2in7b.EPD()

    epd.init()
    epd.Clear()

    # blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    # redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    h_black_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    h_red_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
 
    
else:
    # blackimage = Image.new('1', (298, 126), 255)  # 255: clear the frame
    # redimage = Image.new('1', (298, 126), 255)  # 255: clear the frame
    h_black_image = Image.new('1', (298, 176), 255)  # 298*126
    h_red_image = Image.new('1', (298, 176), 255)  # 298*126    





font24 = ImageFont.truetype(font_path, 24) #24 Chars across the screen
font18 = ImageFont.truetype(font_path, 18)

#    font24 = ImageFont.load_default()
#    font18 = ImageFont.load_default()

test_string = 'abcdefghijklmnopqrstuv'
test_string = 'ABCEEFGHIJKLMNOPQRST'
test_string = "Fuck it! We'll Do it Live!"
print(len(test_string))

drawblack = ImageDraw.Draw(h_black_image)
drawred = ImageDraw.Draw(h_red_image)
drawblack.text((10, 0), test_string, font = font24, fill = 0)
drawblack.text((10, 28), test_string, font = font24, fill = 0)
drawblack.text((10, 56), test_string, font = font24, fill = 0)
drawblack.text((10, 84), test_string, font = font24, fill = 0)
drawblack.text((10, 112), test_string, font = font24, fill = 0)
drawblack.text((10, 140), test_string, font = font24, fill = 0)


drawblack.rectangle((0, 0, 264, 176), outline = 0, width= 2)    

# plt.imshow(drawblack)
if raspi:
    epd.display(epd.getbuffer(h_black_image), epd.getbuffer(h_red_image))

else:
    display(h_black_image)
