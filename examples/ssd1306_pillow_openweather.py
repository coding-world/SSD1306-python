import socket
import fcntl
import struct
import board
import digitalio
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RESET_PIN = digitalio.DigitalInOut(board.D4)

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

oled.fill(0)
oled.show()

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

while True:
    data = requests.get(
        url='https://api.openweathermap.org/data/2.5/onecall'
            '?appid=c240bdf114f959cfc34a442b85c426bd'
            '&units=metric'
            '&lang=de'
            '&lat=54.788'
            '&lon=9.43701',
        timeout=5
    ).json()

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
        draw.text((0, 20), step['data']['weather'][0]['description'], font=font2, fill=255)
        draw.text((0, 40), str(step['data']['temp'])+'°C', font=font3, fill=255)
        draw.text((60, 40), str(step['data']['humidity'])+'%', font=font3, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(2)

    for step in [
        {'name': 'Morgen:', 'data': data['daily'][1]},
        {'name': 'Übermorgen:', 'data': data['daily'][2]},
        {'name': 'in 3 Tagen:', 'data': data['daily'][3]},
    ]:
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), step['name'], font=font3, fill=255)
        draw.text((0, 20), 'Morgens:', font=font2, fill=255)
        draw.text((0, 35), 'Mittags:', font=font2, fill=255)
        draw.text((0, 50), 'Abends:', font=font2, fill=255)
        draw.text((80, 20), str(step['data']['temp']['morn'])+'°C', font=font2, fill=255)
        draw.text((80, 35), str(step['data']['temp']['day'])+'°C', font=font2, fill=255)
        draw.text((80, 50), str(step['data']['temp']['eve'])+'°C', font=font2, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(5)
