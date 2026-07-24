#!/usr/bin/env python
"""Generate qr.svg pointing at the live app, so a desktop viewer can scan
it to open Espresso on their phone. Run after the URL changes.
    python make_qr.py
"""
import qrcode
from qrcode.image.svg import SvgPathImage

URL = "https://adbitrush.github.io/espresso/"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(image_factory=SvgPathImage)
img.save("qr.svg")
print("wrote qr.svg for", URL)
