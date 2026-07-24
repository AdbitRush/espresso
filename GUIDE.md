# ☕ Espresso — Complete Guide

Everything this app does, how to use it, and how it's built. Written for Or's kit
(Varia VS3 · DeLonghi Dedica · moka pot · cold brew · filter).

---

## 1. Where it lives

| Link | Use it for |
|---|---|
| **https://adbitrush.github.io/espresso/** | The public link — **share this**. GitHub-hosted, so nobody sees your server. Best for installing on a phone (HTTPS). |
| **https://espresso.178-105-148-72.sslip.io/** | Your server (HTTPS). Same app; this one runs the cloud-sync API. |
| **http://178.105.148.72:8899/** | Your server by raw IP:port (plain HTTP). |
| **https://github.com/AdbitRush/espresso** | The code. |

All three run the **same app** — the only difference is the address people see.

---

## 2. Quick start

1. Open the link.
2. **Pick a machine** (Dedica, Moka pot, Cold brew, Filter, Milk foam) — each tile has a photo.
3. **Pick a drink.**
4. Read the **grind number + dose/yield/time**, follow the **animated steps**, use the **built-in timer**.
5. Tell it how it tasted in **Rate this cup**, and it helps you dial in.

---

## 3. The grind numbers (important)

- The **Varia VS3 dial is 0–9.9** (finer = lower number).
- **Espresso is a fine grind** — near the bottom of the dial.
- Your **basket** decides the espresso number:
  - **Stock (pressurized)** basket → around **2.5**.
  - **Unpressurized (modded)** basket → around **0.8** (finer). *(This is the one you use.)*
- Coarser methods climb from there: **moka ≈ 5.0 · V60 ≈ 6.5 · French press ≈ 8 · cold brew ≈ 9**.

> These are **starting points**. The shot is the real judge: aim for **14 g in → ~28 g out in
> 25–30 s**, tasting balanced. **Sour/fast → grind finer (lower). Bitter/slow → coarser (higher).**

### The Basket toggle
On any Dedica drink there's a **Basket** switch (Stock / Unpressurized). It's a **global** choice —
flip it once and **every espresso drink** updates its grind number, the **prep/tamp step**, and the
**shot animation** (unpressurized shows a bottomless-portafilter pour; stock shows the two-spout shot).

---

## 4. Machines & drinks

- **Dedica (espresso):** Espresso · Americano · Cappuccino · Latte · Flat white · Cortado · Macchiato · Iced latte · Iced americano · Espresso shakerato.
- **Moka pot:** Moka coffee *(the moka's "espresso" — a moka can't pull a true 9-bar shot)* · Moka americano · Moka cappuccino.
- **Cold brew:** Concentrate · Smooth · Iced cold-brew latte · Cold-brew tonic.
- **Filter:** V60 pour-over · French press.
- **🥛 Milk foam:** Steam wand basics · Cappuccino foam · Latte microfoam · Flat white · By hand (frother/press) · **Latte art (heart & rosetta)** · **Milk alternatives** (oat/soy/almond).

Each drink shows a **photo**, a **machine-readout** (grind/dose/yield/time), a **dial-in hint**,
**animated step-by-step** with a timer, and **gear that helps** (with the *why*).

---

## 5. Personalising it

### Your recipe (per drink)
Override **any number** — grind, dose, yield, time — with your own value. The readout shows your value
with a **green dot**. Use the **− / +** buttons on grind to nudge finer/coarser as you dial by taste.
**↺ Reset to default** clears your overrides for that drink.

### Rate this cup
After a shot, tap a **star rating** (1–5) and a **taste** (🍋 sour / ✅ just right / 🔥 bitter):
- It **logs the shot** with the grind you used.
- After a couple of cups it **suggests a grind change** (sour → finer, bitter → coarser) with a one-tap **Apply**.
- A **grind-trend sparkline** shows your grind across recent shots, each marked by its taste colour, so
  you can watch yourself converge on the sweet spot.

### Favourites & Surprise
Star any drink (☆ → ★) for a quick-access strip at the top. **🎲 Surprise me** jumps to a random drink.

### Profiles (multiple users)
The **👤 bar** lets you switch between users (e.g. "Me" and a friend) or add one with **+ New user**.
Each profile keeps its **own** favourites, notes, ratings, custom recipes, and sync code — so a friend
on your phone doesn't mix into your data.

---

## 6. Saving to the cloud (sync)

At the bottom, **Sync across devices**:
1. Type a **sync code** (any 3–40 letters/numbers) and a **PIN** (defaults to **3944**).
2. **Save to cloud** stores your favourites, notes, ratings and custom recipes on the server.
3. On another device, enter the **same code + PIN** and tap **Load**.

It **auto-saves** on changes once a code is set, and **auto-loads** on startup. The **PIN is enforced
on the server**, so a code alone can't read your data. Share code + PIN to give someone your setup.

*(Sync needs the server online; the app itself still works fully offline.)*

---

## 7. Install it like an app (PWA)

Turns the website into a home-screen app — fullscreen, works **offline**, nothing to download.
- **iPhone (Safari):** Share → *Add to Home Screen*.
- **Android/desktop Chrome:** tap the **Install** banner.
- The **🖼️ button** in the header cycles the background texture (beans → coffee rings → burlap → off).
- **◐** toggles light/dark; **עברית / EN** switches language (full Hebrew + RTL).

---

## 8. For developers / maintenance

**Stack:** one self-contained `index.html` (HTML + CSS + vanilla JS, no build step). Served static;
`server.py` adds the sync API. Bilingual EN/HE, PWA (`sw.js`, `manifest.webmanifest`).

**Key files**
| File | What |
|---|---|
| `index.html` | The whole app — data (`MACHINES`, `HE_DRINKS`), scenes (inline-SVG animations), render + logic. |
| `server.py` | Static server **+** `GET/POST /api/state/<code>` sync API (PIN-locked, CORS open). |
| `sw.js` | Service worker — offline shell, network-first for HTML. Bump `V` to force-update. |
| `make_icons.py` | Regenerate app icons (PWA). |
| `make_qr.py` | Regenerate `qr.svg` (points at the Pages URL). |
| `gen_images.py` | Gemini image generator — drink heroes + machine tiles (`python gen_images.py <keys…>`). |
| `gen_bg.py` | Gemini background textures (`bg`, `bg2`, `bg3`). |
| `images/` | Generated JPGs (drink heroes, machine tiles, backgrounds) + icons. |

**Data model (localStorage), namespaced per profile:** `espresso.<profile>.favs`,
`espresso.<profile>.note.<machine/drink>` (holds `{grind,dose,yield,time,text}`),
`espresso.<profile>.log.<machine/drink>`, `espresso.<profile>.synccode` / `.syncpin`.
Globals: `espresso.theme`, `espresso.lang`, `espresso.basket`, `espresso.bgi`, `espresso.profile`.

**Deploy**
```bash
# from the repo
git add -A && git commit -m "…" && git push        # GitHub Pages auto-deploys (~1 min)
ssh root@178.105.148.72 "git -C /root/repos/espresso pull"   # update the server
# server.py changed? also: systemctl restart espresso
```
The server runs as the `espresso` systemd unit (`python3 server.py`, port 8899,
`ESPRESSO_DATA_DIR=/root/repos/espresso_data`), fronted by Caddy for HTTPS. Auto-starts on reboot.

**Regenerate images** (needs `GOOGLE_API_KEY`): `python gen_images.py` / `python gen_bg.py`.

---

*Grind numbers are starting points — trust the shot, not the sheet. Enjoy. ☕*
