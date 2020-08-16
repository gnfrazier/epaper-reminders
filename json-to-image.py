
import codecs
from PIL import Image

import imgkit

def current_hourly_to_html(c,h):

    # h is the same as formatted_hourly from the weather api.
    
    cur_temp_cell = '<td class="large" rowspan="2">{}°</td>'.format(c['cur_temp'])
    cur_humidity_cell = '<td class="large" rowspan="2">{}﹪</td>'.format(c['cur_temp'])
    cur_time_cell = '<td class="small" rowspan="2">{}</td>'.format('Upd:<br>23:00')
    
    
    hours = [2,5,8,11,14]
    time = cur_temp_cell
    temp = ''
    wind = cur_humidity_cell
    wind_dir = ''
    conditions = ''
    precip_percent = cur_time_cell
    for i in hours:


        if h[i]['precip_percent']!=' ':
            formatted_precip = h[i]['precip_percent']+'﹪'
        else:
            formatted_precip = ''

        cell = "<td>{}</td>".format(h[i]['hour'],)
        time = time + cell
        cell = "<td>{}°</td>".format(h[i]['temp'],)
        temp = temp + cell
        cell = "<td>{}{}</td>".format(h[i]['wind'],h[i]['wind_dir'].lower())
        wind = wind + cell
        #cell = "<td>{}</td>".format(h[i]['wind_dir'],)
        #wind_dir = wind_dir + cell
        cell = "<td>{}</td>".format(h[i]['conditions_icon'],)
        conditions = conditions + cell
        cell = "<td>{}</td>".format(formatted_precip,)
        precip_percent = precip_percent + cell

    rows  = [time,
            temp,
            wind,
            #wind_dir,
            conditions,
            precip_percent,  
                ]    
    head = '''<html><head><meta charset="utf-8"/>
            <style>
            td {
                  text-align: center;
                  border: 1px;

                  border-spacing: 0;
                  border-style: hidden hidden hidden solid;
                  padding: 3px;
                }
            td.large {
                font-size: 20px;
                border-style: hidden hidden hidden hidden;
            
                }
            td.small {
                font-size: 10px;
                border-style: hidden hidden hidden hidden;
                }
            </style>
            </head>
            <body style="background-color:white;">'''
    table = '<table>'    

    for row in rows:
        table = table + '<tr>' + row + '</tr>'

    table = table + '</table>'

    tail = '</body></html>'

    page = head + table

    return page

def html_to_jpg(html_page,file_name):
    
    html_name = file_name + '.html'
    jpg_name = file_name + '.jpg'
    
    with codecs.open(html_name,'w', "utf-8-sig") as file:
        file.write(html_page)
    
    output = imgkit.from_file(html_name,jpg_name)
    
    im = Image.open(jpg_name)

    return im


def table_crop_hourly_2in7(uncropped_image):

    # total image size W,H 264, 176
    image_dim = (264,176)

    # Offset of the table, leaves a right panel
    hourly_table_left = 76
    
    (left, upper, right, lower) = (10, 0, image_dim[0]-hourly_table_left, image_dim[1])
    
    im_crop = uncropped_image.crop((left, upper, right, lower))
    
    return im_crop


def crop_hourly_2in7(uncropped_image):

    # total image size W,H 264, 176
    image_dim = (264,176)


    
    (left, upper, right, lower) = (5, 0, image_dim[0]+5, image_dim[1])
    
    im_crop = uncropped_image.crop((left, upper, right, lower))
    
    return im_crop


def current_hourly_json_to_jpg(current_cond, formatted_hourly):
    
    hourly_html = current_hourly_to_html(current_cond,formatted_hourly)
    
    uncropped = html_to_jpg(hourly_html, 'hourly_table')  
    
    cropped_table = crop_hourly_2in7(uncropped)
    
    return cropped_table
