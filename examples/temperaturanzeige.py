import board, digitalio, glob, time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

path = "/sys/bus/w1/devices/"
sensor_path = glob.glob(path + "28*")[0]
sensor_data_path = sensor_path + "/w1_slave"

def read_temperature():
  file = open(sensor_data_path, "r")
  rows = file.readlines()
  file.close()
  return rows

def get_temperature_in_degree():
  rows = read_temperature()
  while rows[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    rows = read_temperature()
  equals_pos = rows[1].find('t=')
  if equals_pos != -1:
      temp_string = rows[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0
      return temp_c

oled.fill(0)
oled.show()

while True:
  image = Image.new("1", (oled.width, oled.height))
  draw = ImageDraw.Draw(image)

  draw.text((0, 0), "Temperatur:", font=font2, fill=255)
  draw.text((0, 30), str(get_temperature_in_degree())+"°C", font=font, fill=255)

  oled.image(image)
  oled.show()

  time.sleep(1)
