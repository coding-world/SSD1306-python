import socket, fcntl, struct, board, digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RESET_PIN = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=RESET_PIN)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack("256s", str.encode(ifname[:15])),
        )[20:24]
    )

TEXT=""
try:
    TEXT = get_ip_address("eth0")
except IOError:
    try:
        TEXT = get_ip_address("wlan0")
    except IOError:
        TEXT = "kein Netzwerk!"

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

draw.text((0, 0), "Hello World :D", font=font, fill=255)
draw.text((0, 30), "Deine IP ist:", font=font, fill=255)
draw.text((0, 46), TEXT, font=font, fill=255)

oled.image(image)
oled.show()
