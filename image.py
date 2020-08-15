
#!/usr/bin/python3
# -*- coding:utf-8 -*-


import json
from PIL import Image,ImageDraw,ImageFont

import weather

with open('conditions_key.json','r') as file:
    
    condition_keys = json.load(file)

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
    
    h_black_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    h_red_image = Image.new('1', (epd.height, epd.width), 255)  # 298*126    
 
    
else:
    
    h_black_image = Image.new('1', (298, 176), 255)  # 298*126
    h_red_image = Image.new('1', (298, 176), 255)  # 298*126    


font24 = ImageFont.truetype(font_path, 24) #24 Chars across the screen
font18 = ImageFont.truetype(font_path, 18)

line_pos = {
            0:(97, 0),
            1:(97, 28),
            2:(97, 56),
            3:(97, 84),
            4:(97, 112),
            5:(97, 140),
            }



test_string = 'abcdefghijklmnopqrstuv'
test_string = 'ABCEEFGHIJKLMNOPQRST'
test_string = "| 23 | 10 | 20  W |"
header      = "| HR | tp | W dir"
print(len(test_string))

formatted_hourly = get_hourly()

print(formatted_hourly)

drawblack = ImageDraw.Draw(h_black_image)
drawred = ImageDraw.Draw(h_red_image)

drawblack.text((97, 0), header, font = font24, fill = 0)
for pos in list(line_pos.keys())[1:]:
    
    
    line = "| {} | {} | {}  {} " .format(formatted_hourly[pos]['hour'],
         formatted_hourly[pos]['temp'],
         formatted_hourly[pos]['conditions_icon'],
         formatted_hourly[pos]['precip_percent'])
    print(line)
    drawblack.text(line_pos[pos], line, font = font24, fill = 0)

'''drawblack.text((97, 0), header, font = font24, fill = 0)
drawblack.text((97, 28), test_string, font = font24, fill = 0)
drawblack.text((97, 56), test_string, font = font24, fill = 0)
drawblack.text((97, 84), test_string, font = font24, fill = 0)
drawblack.text((97, 112), test_string, font = font24, fill = 0)
drawblack.text((97, 140), test_string, font = font24, fill = 0)'''


drawblack.rectangle((0, 0, 264, 176), outline = 0, width= 2)    

# plt.imshow(drawblack)
if raspi:
    epd.display(epd.getbuffer(h_black_image), epd.getbuffer(h_red_image))

else:
    display(h_black_image)
