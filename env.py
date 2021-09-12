
# sudo pip3 install adafruit-circuitpython-ssd1305
# sudo pip3 install adafruit-circuitpython-ms8607

import time
from board import SCL, SDA, D4
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305
from adafruit_ms8607 import MS8607

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(D4)

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the MS8607 temperature, pressure and humidity sensor
sensor = MS8607(i2c)

# Create the SSD1305 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, reset=oled_reset)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
font = ImageFont.truetype('./fonts/PixeloidSans.ttf', 9)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Write three lines of text.
    draw.text((x, top + 0), "Pressure: %.2f hPa" % sensor.pressure, font=font, fill=255)
    draw.text((x, top + 12), "Temperature: %.2f C" % sensor.temperature, font=font, fill=255)
    draw.text((x, top + 24), "Humidity: %.2f %% rH" % sensor.relative_humidity, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(1)

