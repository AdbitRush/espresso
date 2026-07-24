#!/usr/bin/env python
"""Generate appetizing hero images for each drink via Gemini 2.5 Flash Image
("Nano Banana"), in one consistent style, and save them under images/.
Reads GOOGLE_API_KEY from the abri-brain .env.

    python gen_images.py            # all drinks
    python gen_images.py espresso   # just one (key = machine_drink or drink)
"""
import base64, io, json, os, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
ENV = Path(r"C:\Users\AdBitRush\Documents\AdbitRush 22\2026\abri-brain\.env")
MODEL = "gemini-2.5-flash-image"
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

def api_key():
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"]
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("GOOGLE_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no GOOGLE_API_KEY")

# consistent style so every drink looks like one set
STYLE = ("Professional overhead-to-45-degree product photograph, warm cream and "
         "amber tones, soft natural window light, minimal cozy specialty-coffee "
         "styling on a warm stone surface, shallow depth of field, high detail, "
         "appetizing, no text, no watermark, no hands.")

DRINKS = {
    "dedica_espresso": "a freshly pulled double espresso in a small ceramic cup with thick golden crema",
    "dedica_americano": "an americano in a clear glass, espresso poured over hot water with floating crema",
    "dedica_cappuccino": "a cappuccino in a ceramic cup with a thick milk-foam cap and light cocoa dusting",
    "dedica_latte": "a caffe latte in a tall glass with silky steamed milk and a thin latte-art leaf",
    "dedica_flatwhite": "a flat white in a small ceramic cup with glossy microfoam and fine latte art",
    "dedica_cortado": "a cortado in a small gibraltar glass, equal espresso and warm milk, minimal foam",
    "dedica_macchiato": "an espresso macchiato in a small cup, espresso marked with a single dollop of foam",
    "dedica_icedlatte": "an iced latte in a tall glass with big ice cubes, cold milk and espresso swirling",
    "dedica_icedamericano": "an iced americano in a tall glass full of ice with dark coffee and crema",
    "dedica_shakerato": "an espresso shakerato in a chilled coupe glass, frothy foamy shaken iced espresso",
    "moka_moka": "rich stovetop moka-pot coffee in a small cup beside an aluminium moka pot",
    "moka_mokaamericano": "a moka-pot americano in a mug, strong stovetop coffee lengthened with water",
    "moka_mokacap": "a moka-pot cappuccino in a cup with hand-frothed milk foam and cocoa",
    "cold_concentrate": "cold-brew coffee concentrate in a glass bottle and a glass over ice, dark and smooth",
    "cold_smooth": "smooth cold brew poured over ice in a tall glass, clear and refreshing",
    "cold_icedlatte": "an iced cold-brew latte in a tall glass, cold milk poured over cold brew and ice",
    "cold_tonic": "a cold-brew tonic in a tall glass, layered coffee over fizzy tonic with a citrus twist",
    "filter_v60": "a V60 pour-over brewing into a glass carafe, clean bright filter coffee, gooseneck kettle",
    "filter_frenchpress": "a French press full of coffee beside a mug of full-bodied brew",
    "milkfoam_steamwand": "a stainless steel milk pitcher being steamed by an espresso machine wand, glossy silky microfoam swirling, wisps of steam",
    "milkfoam_cappuccino": "a cappuccino with a thick airy milk foam cap and a light dusting of cocoa in a ceramic cup",
    "milkfoam_latte": "pouring glossy silky microfoam into a latte forming latte art, a leaf or heart, close up",
    "milkfoam_flatwhite": "a flat white in a small cup with tight shiny microfoam and fine latte art",
    "milkfoam_handfroth": "a glass of warm milk being frothed by a handheld electric milk frother, airy foam forming",
    "milkfoam_latteart": "a barista pouring a rosetta latte art into a coffee cup, top-down close up, elegant white fern pattern",
    "milkfoam_alt": "a frothy oat milk latte in a glass beside a plain carton of barista oat milk, plant-based, warm tones",
    # machine-tile thumbnails
    "machine_dedica": "a slim stainless-steel DeLonghi Dedica style espresso machine on a warm kitchen counter, front product photo",
    "machine_moka": "a classic aluminium moka pot stovetop espresso maker, product photo",
    "machine_cold": "a tall glass jar of dark cold-brew coffee concentrate with a lid, product photo",
    "machine_filter": "a white ceramic V60 pour-over dripper with a paper filter on a glass carafe, product photo",
    "machine_milkfoam": "a stainless-steel milk frothing pitcher holding glossy white microfoam, product photo",
}

def generate(key, subject):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"
           f":generateContent?key={api_key()}")
    prompt = f"{subject}. {STYLE}"
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    for part in data["candidates"][0]["content"]["parts"]:
        d = part.get("inlineData") or part.get("inline_data")
        if d and d.get("data"):
            raw = base64.b64decode(d["data"])
            img = Image.open(io.BytesIO(raw)).convert("RGB")
            # square-crop + resize to keep the app light
            s = min(img.size)
            img = img.crop(((img.width - s) // 2, (img.height - s) // 2,
                            (img.width + s) // 2, (img.height + s) // 2)).resize((640, 640), Image.LANCZOS)
            out = OUT / f"{key}.jpg"
            img.save(out, "JPEG", quality=82, optimize=True)
            return out
    raise RuntimeError("no image in response: " + json.dumps(data)[:300])

if __name__ == "__main__":
    keys = sys.argv[1:] or list(DRINKS)
    for k in keys:
        if k not in DRINKS:
            print("skip unknown", k); continue
        for attempt in range(3):
            try:
                out = generate(k, DRINKS[k]); print("ok", out, out.stat().st_size, "bytes"); break
            except Exception as e:
                print(f"  {k} attempt {attempt+1} failed: {str(e)[:160]}"); time.sleep(3)
