#!/usr/bin/env python
"""Generate the espresso-cup app icons (crema→copper tile + white cup).
Run once to (re)build the PNGs referenced by the manifest & apple-touch-icon.
    python make_icons.py
"""
from PIL import Image, ImageDraw

TOP = (244, 191, 112)   # crema-bright
BOT = (192, 125, 67)    # copper
STROKE = (255, 248, 239)


def gradient(size):
    col = Image.new("RGB", (1, size))
    for y in range(size):
        t = y / (size - 1)
        col.putpixel((0, y), tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))
    return col.resize((size, size))


def sheen(img, size):
    """Soft top-left highlight."""
    ov = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(ov)
    cx, cy, r = size * 0.30, size * 0.14, size * 0.75
    for i in range(24):
        rr = r * (1 - i / 24)
        a = int(90 * (i / 24))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=a)
    white = Image.new("RGB", (size, size), (255, 255, 255))
    img.paste(white, (0, 0), ov)
    return img


def draw_cup(img, size):
    d = ImageDraw.Draw(img, "RGBA")
    cb = size * 0.58
    off = (size - cb) / 2
    oy = off + size * 0.035
    s = cb / 26.0
    def P(u, v):
        return (off + u * s, oy + v * s)
    w = max(2, round(1.7 * s))

    # cup body: flat top, rounded bottom
    x1, y1 = P(5.2, 10.5)
    x2, y2 = P(16.4, 19.6)
    r = 4.6 * s
    d.rounded_rectangle([x1, y1, x2, y2], radius=r, outline=STROKE, width=w,
                        fill=(255, 255, 255, 46))
    # square off the top two corners so it reads as a cup rim
    d.rectangle([x1, y1, x2, y1 + r], outline=None, fill=None)
    d.line([P(5.2, 10.5), P(16.4, 10.5)], fill=STROKE, width=w)

    # handle (right half arc)
    hb = [P(13.5, 11.0), P(19.3, 16.8)]
    d.arc([hb[0][0], hb[0][1], hb[1][0], hb[1][1]], start=-90, end=90, fill=STROKE, width=w)

    # saucer
    d.line([P(4.3, 20.4), P(17.2, 20.4)], fill=STROKE, width=w)
    # rounded caps
    cap = w / 2
    for (u, v) in [(4.3, 20.4), (17.2, 20.4)]:
        cx, cy = P(u, v)
        d.ellipse([cx - cap, cy - cap, cx + cap, cy + cap], fill=STROKE)

    # steam
    sw = max(2, round(1.4 * s))
    for u in (10.0, 14.0):
        d.line([P(u, 6.4), P(u - 0.6, 4.8), P(u + 0.4, 3.0)], fill=(255, 248, 239, 220),
               width=sw, joint="curve")
    return img


def make(size, path):
    img = gradient(size).convert("RGB")
    img = sheen(img, size)
    img = draw_cup(img, size)
    img.save(path)
    print("wrote", path, size)


if __name__ == "__main__":
    make(512, "icon-512.png")
    make(192, "icon-192.png")
    make(180, "apple-touch-icon.png")
    make(32, "favicon-32.png")
