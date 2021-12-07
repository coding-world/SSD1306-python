import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from random import randint
import RPi.GPIO as gpio
import digitalio
import time
import board

# define pins
gpio.setmode(gpio.BCM)
channel = 23
gpio.setup(channel, gpio.IN, pull_up_down=gpio.PUD_UP)

RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

# clear display
oled.fill(0)
oled.show()

# import font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 64)

# print ?
imageBegin = Image.new("1", (oled.width, oled.height))
ImageDraw.Draw(imageBegin).text((40, 0), "?", font=font, fill=255)
oled.image(imageBegin)
oled.show()

# generate images
numbers = []
for i in range(1, 7):
    image = Image.new("1", (oled.width, oled.height))
    ImageDraw.Draw(image).text((40, 0), str(i), font=font, fill=255)
    numbers.append(image)

while True:
    if gpio.input(channel) == 0:
        while True:
            oled.image(numbers[randint(0, 5)])
            oled.show()
            time.sleep(0.01)
            if gpio.input(channel) == 1:
                oled.image(numbers[randint(0, 5)])
                oled.show()
                time.sleep(0.5)
                break
