# Display useful information on my CyberDeck Bonnet
#
# Toggles between Temperature, Pressure, Humidity screen then
# system stats like memory and CPU

import time
import subprocess
from board import SCL, SDA, D4
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305
from adafruit_ms8607 import MS8607

def env(draw, font, sensor):

    # Write three lines of text.
    draw.text((0, -2 + 0), "Temperature: %.2f C" % sensor.temperature, font=font, fill=255)
    draw.text((0, -2 + 12), "Pressure: %.2f hPa" % sensor.pressure, font=font, fill=255)
    draw.text((0, -2 + 24), "Humidity: %.2f %% rH" % sensor.relative_humidity, font=font, fill=255)

def stats(draw, font):

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.0f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.

    draw.text((0, -2 + 0), "IP: " + IP, font=font, fill=255)
    draw.text((0, -2 + 8), CPU, font=font, fill=255)
    draw.text((0, -2 + 16), MemUsage, font=font, fill=255)
    draw.text((0, -2 + 25), Disk, font=font, fill=255)

def main():
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
  font = ImageFont.truetype('./fonts/PixeloidSans.ttf', 9)

  count = 0

  while True:

      # Draw a black filled box to clear the image.
      draw.rectangle((0, 0, width, height), outline=0, fill=0)

      if count % 10 >= 5:
        env(draw, font, sensor)
      else:
        stats(draw, font)

      count += 1

      # Display image.
      disp.image(image)
      disp.show()
      time.sleep(1)

if __name__ == "__main__":
  main()
