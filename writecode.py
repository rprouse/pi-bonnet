from board import SCL, SDA, D4
import busio
import digitalio
from PIL import Image, ImageDraw
import adafruit_ssd1305

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(D4)

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1305 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, reset=oled_reset)

# Clear display.
disp.fill(0)
disp.show()

img = Image.open("images/WriteCode.png")
image = img.convert("1")
print(image.format, image.size, image.mode)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Display image.
disp.image(image)
disp.show()
