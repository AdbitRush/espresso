# ☕ Espresso

A single-page brewing guide tuned to **my exact kit**. Pick a machine, pick a drink — it gives you the **Varia VS3 grind number**, the dose/yield/time readout, every step, a built-in brew timer, and the gear that actually helps.

No build, no dependencies. Just open `index.html` (or the live page) on your phone in the kitchen.

## The kit it's built for

| Device | Role | Notes |
|---|---|---|
| **Varia VS3** | Grinder | Grind shown as the **dial number** (~0–20 scale, finer = lower). Espresso `0.2–3.3`, moka `3.1–7.8`, cold brew `10.1–19.6` per the [Honest Coffee Guide](https://honestcoffeeguide.com/varia-vs3-gen-2-grind-settings/) Gen 2 chart. |
| **DeLonghi Dedica** | Espresso | **51 mm** pressurized basket — grind runs a touch coarser than a true espresso machine. |
| **Moka pot** (makineta) | Stovetop | Medium-fine, salt-like grind; no pressure needed. |
| **Cold brew** | Immersion | No machine — very coarse grind, 14–16 h fridge steep, then strain. |
| **Filter** | V60 / French press | Manual brews off the grinder — medium (V60) to coarse (press). |

## Grind quick-reference (Varia VS3 — dial 0–9.9, finer = lower)

VS3 espresso range is **0.2–3.3** (Honest Coffee Guide). Pick your **basket** in the app: **stock/pressurized → ~2.5**, **unpressurized (modded) → ~0.8**. Everything stays within the 0–9.9 dial.

| Drink | Machine | Grind (dial) | Dose → Yield | Time |
|---|---|---|---|---|
| Espresso / cappuccino / macchiato | Dedica | **2.5** | 14 g → 28 g | 25–30 s |
| Latte / iced / shakerato | Dedica | **2.4** | — | 25–30 s |
| Flat white / cortado (ristretto) | Dedica | **2.2–2.3** | 14 g → 26 g | 25–30 s |
| Americano / iced americano (long) | Dedica | **2.8–2.9** | 14 g → 28 g+ | 25–30 s |
| Moka coffee | Moka pot | **4.8** | fill basket → full pot | ~4–5 min |
| V60 pour-over | Filter | **6.5** | 20 g → 320 g | ~3 min |
| French press | Filter | **11** (turn 2 · 1.0) | 30 g → 450 g | ~8 min |
| Cold brew | Immersion | **13–15** (turn 2 · 3–5) | 100 g → 500 ml | 14–16 h |

> These are **starting points** — taste, then nudge: sour & fast → **finer** (lower);
> bitter, slow or choking → **coarser** (higher). On a **pressurized** basket use ~2.5;
> if you run a modded **unpressurized** basket, go finer (~0.8–1.5).

## Features

- **Machine → drink** picker with a machine-readout recipe card (grind / dose / yield / time).
- **Illustrated animated step player** — each step plays a hand-drawn SVG scene; prev/next, dot progress, auto-play.
- **🥛 Milk foaming guide** — a dedicated method with steam-wand basics + foam styles per drink (cappuccino / latte / flat white) and a by-hand option; animated steps + photos, same as the coffee recipes.
- **Built-in timer** with a target marker (shot time / moka time).
- **User profiles** — switch between users (e.g. "Me" / a friend) from the top bar; each has its own favorites, notes, ratings, and cloud sync code/PIN. Add a user inline with "+ New user".
- **★ Favorites** — star any drink; a quick-access strip pins them at the top (per user).
- **Your recipe** — override any number per drink (grind, dose, yield, time) with your own preference; a **− / +** grind stepper nudges finer/coarser (0.1 steps) as you dial by taste; the readout shows your value with a green dot; **↺ Reset to default** clears it. Saved per drink + user and **synced across devices**. Plus free notes.
- **Basket-specific shot animation** — the unpressurized basket shows a bottomless-portafilter pour (converging streams) instead of the two-spout shot.
- **Rate this cup** — a 1–5 **star quality rating** plus a one-tap taste log (sour / just right / bitter) per shot. Tracks avg/best over all cups; after a couple it spots the pattern and suggests a grind change with a one-tap **Apply** (sour→finer, bitter→coarser, step scaled to the brew method), or tells you it's dialed in.
- **🎲 Surprise me** — jumps to a random drink.
- **Share / deep links** — every drink has its own URL (`…/#dedica/cappuccino`); the share button uses the native share sheet on mobile or copies the link. Opening a shared link lands right on that recipe.
- **Gear that helps** per drink — with the *why*, and the 51 mm tamper flagged as essential.
- **Installable PWA** — add to your home screen, runs fullscreen and **offline** (service worker + app icons).
- **Bilingual EN / עברית** with full RTL — every drink, step, and gear item translated; toggle in the header.
- **QR code** on the page — scan from desktop to open it on your phone (`make_qr.py` regenerates it).
- **Cloud sync** — pick a sync code and save your favorites, notes & ratings to the server, then load them on any device or share the code. Auto-saves on change; works from the GitHub Pages copy too (CORS). Runs on the server build (`server.py`), which also serves the static app.
- **Basket toggle** (Dedica) — stock/pressurized vs unpressurized; a global choice that reshuffles the grind on every espresso drink at once.
- **Photo machine tiles** — each method (Dedica, moka, cold brew, filter, milk) shows a generated photo for easy visual picking.
- The basket toggle also changes the **prep step**: pressurized = light tamp; unpressurized = WDT-distribute + firm level tamp.
- Light / dark coffee theme + a **🖼️ background button** that cycles through a few textures (beans, coffee rings, burlap) and off; remembers your last pick, language, basket, and background.

## Install on your phone

Open **https://adbitrush.github.io/espresso/**, then:
- **iPhone (Safari):** Share → *Add to Home Screen*.
- **Android (Chrome):** tap the **Install** banner, or menu → *Install app*.

It then opens like a native app and works with no signal. Icons are generated by `make_icons.py` (run it to rebuild them).

## Run it

```bash
# just open the file
open index.html        # macOS
start index.html       # Windows
```

Or serve it and hit it from your phone on the same Wi-Fi:

```bash
python -m http.server 8080
```

## Publish (GitHub Pages)

Settings → Pages → Deploy from branch → `main` / root. Then it's live at
`https://adbitrush.github.io/espresso/`.

---

*Grind numbers are opinions, not gospel — dial them to your beans.*
