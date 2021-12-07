import socket
import fcntl
import struct
import board
import digitalio
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from io import BytesIO
import cairosvg
import os.path

# set pins and init oled
RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

# clear screen
oled.fill(0)
oled.show()

# load fonts
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)


def get_icon(id, size=32):
    out = BytesIO()
    url = './icons/'+id+'.svg'
    if os.path.isfile(url):
        cairosvg.svg2png(url=url, write_to=out)  # convert svg to png
        return Image.open(out).resize((size, size)).convert('1')  # return resized image
    else:
        return Image.new("1", (32, 32))  # return empty image


while True:
    # openweather api request
    data = requests.get(
        url='https://api.openweathermap.org/data/2.5/onecall'
            '?appid=d3355b38ac0d56b2e91cefcd5fd744fb'   # should be changed to own api key
            '&units=metric'                             # units
            '&lang=de'                                  # referred language
            '&lat=54.788'                               # location (latitude)
            '&lon=9.43701',                             # location (longitude)
        timeout=5
    ).json()

    # display hourly data
    for step in [
        {'name': 'Jetzt:', 'data': data['current']},
        {'name': 'in einer Stunde:', 'data': data['hourly'][1]},
        {'name': 'in zwei Stunden:', 'data': data['hourly'][2]},
        {'name': 'in 3 Stunden:', 'data': data['hourly'][3]},
        {'name': 'in 6 Stunden:', 'data': data['hourly'][6]},
    ]:
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), step['name'], font=font3, fill=255)
        draw.text((0, 16), step['data']['weather'][0]['description'], font=font2, fill=255)
        draw.text((48, 32), str(step['data']['temp'])+'°C', font=font3, fill=255)
        draw.text((48, 48), str(step['data']['humidity'])+'%', font=font3, fill=255)
        image.paste(get_icon(step['data']['weather'][0]['icon']), (8, 32))

        oled.image(image)
        oled.show()
        time.sleep(2)

    # display daily data
    for step in [
        {'name': 'Morgen:', 'data': data['daily'][1]},
        {'name': 'Übermorgen:', 'data': data['daily'][2]},
        {'name': 'in 3 Tagen:', 'data': data['daily'][3]},
    ]:
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), step['name'], font=font3, fill=255)
        draw.text((0, 16), 'Morgens:', font=font2, fill=255)
        draw.text((0, 32), 'Mittags:', font=font2, fill=255)
        draw.text((0, 48), 'Abends:', font=font2, fill=255)
        draw.text((60, 16), str(step['data']['temp']['morn'])+'°C', font=font2, fill=255)
        draw.text((60, 32), str(step['data']['temp']['day'])+'°C', font=font2, fill=255)
        draw.text((60, 48), str(step['data']['temp']['eve'])+'°C', font=font2, fill=255)
        image.paste(get_icon(step['data']['weather'][0]['icon'], 16), (112, 16))
        image.paste(get_icon(step['data']['weather'][0]['icon'], 16), (112, 32))
        image.paste(get_icon(step['data']['weather'][0]['icon'], 16), (112, 48))

        oled.image(image)
        oled.show()
        time.sleep(5)
