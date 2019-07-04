#import QRCode from pyqrcode
import pyqrcode
from pyqrcode import QRCode

# String which represent the QR code
# General syntax: pyqrcode.create(content, error='H', version=None, mode=None, encoding=None)

s = "www.ikwen.com/tsunami"

#Generate QR Code
url = pyqrcode.create(s)

# Create and save the png file naming "myqr.png"
url.svg("myqr.svg", scale=8)