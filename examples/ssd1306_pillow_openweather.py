import socket
import fcntl
import struct
import board
import digitalio
import requests
import time
import os.path
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from io import BytesIO
import cairosvg

# set pins and init oled
RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

# clear screen
oled.fill(0)
oled.show()

# load fonts
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)


def get_icon(id, size=32):
    url = './icons/'+id+'.svg'
    if os.path.isfile(url):
        return Image.open(
            BytesIO(cairosvg.svg2png(url=url))  # convert svg to png
        ).resize((size, size)).convert('1')  # return resized image
    else:
        return Image.new("1", (size, size))  # return empty image


while True:
    # openweather api request
    data = requests.get(
        url='https://api.openweathermap.org/data/2.5/onecall'
            '?appid=d3355b38ac0d56b2e91cefcd5fd744fb'   # should be changed to own api key
            '&units=metric'                             # units
            '&lang=de'                                  # referred language
            '&lat=54.788'                               # location (latitude)
            '&lon=9.43701',                             # location (longitude)
        timeout=10
    ).json()

    # display hourly data
    for step in [
        {'title': 'Jetzt:', 'data': data['current']},
        {'title': 'in einer Stunde:', 'data': data['hourly'][1]},
        {'title': 'in zwei Stunden:', 'data': data['hourly'][2]},
        {'title': 'in 3 Stunden:', 'data': data['hourly'][3]},
        {'title': 'in 6 Stunden:', 'data': data['hourly'][6]},
    ]:
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), step['title'], font=font3, fill=255)
        draw.text((0, 16), step['data']['weather'][0]['description'], font=font2, fill=255)
        draw.text((48, 32), str(step['data']['temp']) + '°C', font=font3, fill=255)
        draw.text((48, 48), str(step['data']['humidity']) + '%', font=font3, fill=255)
        image.paste(get_icon(step['data']['weather'][0]['icon']), (8, 32))

        oled.image(image)
        oled.show()
        time.sleep(4)

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), 'nächste Tage', font=font3, fill=255)
    for i in range(1, 4):
        draw.text((24, 16 * i), str(data['daily'][i]['temp']['day'])[:4] + '°C', font=font2, fill=255)
        draw.text((76, 16 * i), str(data['daily'][i]['temp']['night'])[:4] + '°C', font=font2, fill=255)
        image.paste(get_icon(data['daily'][i]['weather'][0]['icon'], 16), (0, 16 * i))

    oled.image(image)
    oled.show()
    time.sleep(8)
