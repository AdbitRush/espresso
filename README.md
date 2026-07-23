# ☕ Espresso

A single-page brewing guide tuned to **my exact kit**. Pick a machine, pick a drink — it gives you the **Varia VS3 grind number**, the dose/yield/time readout, every step, a built-in brew timer, and the gear that actually helps.

No build, no dependencies. Just open `index.html` (or the live page) on your phone in the kitchen.

## The kit it's built for

| Device | Role | Notes |
|---|---|---|
| **Varia VS3** | Grinder | Grind settings are shown as `full-turns.dial` starting points (e.g. `1.8` = 1 turn + 8). |
| **DeLonghi Dedica** | Espresso | **51 mm** pressurized basket — grind runs a touch coarser than a true espresso machine. |
| **Moka pot** (makineta) | Stovetop | Medium-fine, salt-like grind; no pressure needed. |
| **Cold brew** | Immersion | No machine — very coarse grind, 14–16 h fridge steep, then strain. |

## Grind quick-reference (VS3 starting points)

| Drink | Machine | Grind | Dose → Yield | Time |
|---|---|---|---|---|
| Espresso / milk drinks | Dedica | **1.8** | 14 g → 28 g | 25–30 s |
| Flat white (tighter) | Dedica | **1.7** | 14 g → 26 g | 25–30 s |
| Moka coffee | Moka pot | **3.2** | fill basket → full pot | ~4–5 min |
| Cold brew concentrate | Immersion | **5.5** | 100 g → 500 ml | 16 h steep |

> These are **starting points**. Taste the shot, then move the grind ±0.2:
> sour & fast → **finer**; bitter, slow or choking → **coarser**.

## Features

- **Machine → drink** picker with a machine-readout recipe card (grind / dose / yield / time).
- **Step-by-step** method per drink, incl. milk texturing notes for the Dedica wand.
- **Built-in timer** with a target marker (shot time / moka time).
- **Gear that helps** per drink — with the *why*, and the 51 mm tamper flagged as essential.
- Light/dark theme, remembers your last pick, works offline.

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
