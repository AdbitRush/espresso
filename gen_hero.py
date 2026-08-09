#!/usr/bin/env python
"""Cinematic hero plates for the espresso site.

The existing images/ are product shots on a bright counter — correct for the
picker tiles, wrong for a full-bleed hero. These are shot dark and wide, lit
from behind, with room in the frame for type to sit over them.

    python gen_hero.py            # generate the candidates
    python gen_hero.py --pick 2   # promote one to images/hero-cine.jpg
"""
import base64
import io
import json
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance

sys.path.insert(0, str(Path(__file__).resolve().parent))
# gen_images.generate() is (key, subject) and always writes a 640px square —
# right for the picker tiles, wrong for a 21:9 hero plate. Reuse only its key
# handling and call the API directly here.
from gen_images import api_key, MODEL, OUT  # noqa: E402


def generate(prompt, dst, size, quality=90):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"
           f":generateContent?key={api_key()}")
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    for part in data["candidates"][0]["content"]["parts"]:
        d = part.get("inlineData") or part.get("inline_data")
        if d and d.get("data"):
            img = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            img = img.resize(size, Image.LANCZOS)
            img.save(dst, "JPEG", quality=quality, optimize=True)
            return dst
    raise RuntimeError("no image in response")

STYLE = ("Cinematic still, anamorphic, shallow depth of field, dramatic low-key "
         "lighting with a warm amber rim light from behind, deep shadows, rich "
         "blacks, volumetric steam catching the light, fine film grain, shot on "
         "70mm, moody and premium, no text, no watermark, no faces.")

PLATES = {
    1: ("an extreme close-up of espresso extracting from a bottomless portafilter, "
        "a thick amber rope of coffee falling into a warm-lit cup, dark background, "
        "steam rising through a beam of light"),
    2: ("a dark moody barista counter at night, a single espresso cup lit by one warm "
        "overhead lamp, polished steel machine glinting in deep shadow, steam drifting"),
    3: ("a slow pour of milk into espresso forming latte art, shot from directly above, "
        "dark surface, single dramatic warm light, crema swirling"),
}


def grade(src, dst):
    """Slight contrast and desaturation so type stays readable over the top."""
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(.92)
    # crop to a wide cinematic ratio
    w, h = im.size
    target = 21 / 9
    nh = int(w / target)
    if nh < h:
        top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    im = im.resize((1920, int(1920 / target)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    return dst


def main():
    if "--pick" in sys.argv:
        n = int(sys.argv[sys.argv.index("--pick") + 1])
        src = OUT / f"_cine{n}.jpg"
        if not src.exists():
            sys.exit(f"{src} missing — generate first")
        out = grade(src, OUT / "hero-cine.jpg")
        print(f"promoted plate {n} -> {out} ({out.stat().st_size // 1024}kb)")
        return

    for n, subject in PLATES.items():
        dst = OUT / f"_cine{n}.jpg"
        if dst.exists():
            print(f"skip {dst.name}")
            continue
        generate(f"{subject}. {STYLE}", dst, (1400, 1400), quality=90)
        print(f"ok {dst.name} ({dst.stat().st_size // 1024}kb)")


if __name__ == "__main__":
    main()
