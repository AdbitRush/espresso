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

PROMPT = (
    "A soft, out-of-focus minimalist background texture: a few scattered dark "
    "roasted coffee beans on a warm cream linen surface, lots of empty negative "
    "space, very subtle, muted, low contrast, gentle warm beige and soft brown "
    "tones, soft diffused natural light, calm and airy, tasteful, no text, no "
    "people, no logos. Suitable as a faint app background."
)

def generate():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key()}"
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
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
            img.save(OUT / "bg.jpg", "JPEG", quality=72, optimize=True)
            print("wrote", OUT / "bg.jpg", (OUT / "bg.jpg").stat().st_size, "bytes")
            return
    raise RuntimeError("no image: " + json.dumps(data)[:300])

if __name__ == "__main__":
    generate()
