#!/usr/bin/python3
# -*- coding:utf-8 -*-

from PIL import Image,ImageDraw,ImageFont

import epd2in7b

if __name__ == "__main__":
    epd = epd2in7b.EPD()

    epd.init()
    epd.Clear()
