#!/usr/bin/env python
"""Generate a subtle app background (images/bg.jpg) via Gemini 2.5 Flash Image.
Muted and low-contrast so the app content stays readable on top.
    python gen_bg.py
"""
import base64, io, json, os, urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent
ENV = Path(r"C:\Users\AdBitRush\Documents\AdbitRush 22\2026\abri-brain\.env")
MODEL = "gemini-2.5-flash-image"
OUT = ROOT / "images"; OUT.mkdir(exist_ok=True)

def api_key():
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"]
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("GOOGLE_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no GOOGLE_API_KEY")

COMMON = (" lots of empty negative space, very subtle, muted, low contrast, warm "
          "beige and soft brown tones, soft diffused light, calm, tasteful, no text, "
          "no people, no logos. Suitable as a faint app background.")
BGS = {
    "bg":  "A soft out-of-focus minimalist texture: a few scattered dark roasted coffee beans on a warm cream linen surface." + COMMON,
    "bg2": "A soft minimalist texture of faint coffee-cup rings and light stains on warm off-white paper." + COMMON,
    "bg3": "A soft minimalist texture of a woven burlap coffee-sack surface in warm natural beige." + COMMON,
}

def generate(name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key()}"
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
            img = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            # fade it out so it reads as a faint texture, and keep the file small
            img = ImageEnhance.Contrast(img).enhance(0.85)
            img = ImageEnhance.Color(img).enhance(0.9)
            img = img.resize((1200, 1200), Image.LANCZOS)
            out = OUT / (name + ".jpg")
            img.save(out, "JPEG", quality=72, optimize=True)
            print("wrote", out, out.stat().st_size, "bytes")
            return
    raise RuntimeError("no image: " + json.dumps(data)[:300])

if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(BGS)
    for n in names:
        if n in BGS:
            generate(n, BGS[n])
