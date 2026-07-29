# HANDOFF — espresso

**Updated:** 2026-07-30 · **Repo:** https://github.com/AdbitRush/espresso · **Branch:** main
**Read this first, then `UPGRADES.md`** (owner request inbox). `GUIDE.md` is the
full user-facing guide; `README.md` is the kit + grind reference. This file is
only what you need to *operate* the thing.

---

## Live right now

| | URL | Notes |
|---|---|---|
| **Public link — share this** | https://adbitrush.github.io/espresso/ | GitHub Pages. HTTPS, best for installing on a phone. Static only: **cloud sync still talks to the VPS** (CORS is open for exactly this). |
| **VPS copy** | https://espresso.178-105-148-72.sslip.io | Same app **plus** the sync API. Caddy → `localhost:8899`. |
| VPS by IP:port | http://178.105.148.72:8899 | Plain HTTP, same process, no TLS. |
| In the hub | ABRI ONE → Life apps → Espresso | http://178.105.148.72:9000 |

No auth anywhere — it's a brew guide. The only private thing is the sync blob,
and that's PIN-locked server-side (below).

---

## Deployment

Two copies. `git push` deploys Pages in ~1 min; the VPS **pulls itself once a day**.

```bash
git add -A && git commit -m "…" && git push     # Pages: automatic
# want the VPS now instead of waiting for the nightly pull:
ssh root@178.105.148.72 /root/bin/espresso-pull.sh
```

### The nightly pull
| | |
|---|---|
| Script | `/root/bin/espresso-pull.sh` — pulls `--ff-only`, and **restarts the unit only if `server.py` changed** (`index.html` is read per request, `server.py` is held in memory) |
| **Schedule** | `/etc/cron.d/espresso-pull` — **daily 04:17 UTC**. The file has one marked line to edit; examples for hourly / every-15-min are in the comment right above it |
| Log | `/var/log/espresso-pull.log` — one line per actual change, plus any failure. Silent when there's nothing new |

*Why it exists:* on 2026-07-30 the VPS was found serving `fa3702a` while `main`
was `88fac31` — five days stale, still showing the self-contradictory iced-latte
step that `88fac31` fixed. Pages was current the whole time, so nothing looked
broken. Silent drift is this project's failure mode; the cron closes it.

A same-day change still won't be live until 04:17 UTC. If you need it out now,
run the script by hand (above), then **verify both copies match**:
```bash
curl -s https://adbitrush.github.io/espresso/ | wc -c
curl -s https://espresso.178-105-148-72.sslip.io/ | wc -c    # must match
```

### The unit
```
/etc/systemd/system/espresso.service   enabled → survives reboot
WorkingDirectory=/root/repos/espresso
ExecStart=/usr/bin/python3 server.py     PORT=8899
ESPRESSO_DATA_DIR=/root/repos/espresso_data      ← outside the served dir, on purpose
```
Caddy (`/root/caddy/Caddyfile`, a **Docker** container — not a systemd service)
terminates TLS for `espresso.<sslip>` and gzips. Reload it with
`docker exec caddy caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile`.

---

## The sync API (`server.py`)

The only server-side logic in the whole project. Static file serving plus:

| Route | Behaviour |
|---|---|
| `GET /api/state/<code>` | the blob, or `{}` if that code was never used (no PIN needed for an empty one) |
| `POST /api/state/<code>` | `{pin, data}` — **the first write claims the PIN**; later writes with a wrong PIN get 403 |

- Codes must match `^[A-Za-z0-9_-]{3,40}$`; bodies cap at 512 KB.
- Legacy blobs without a `pin` key are treated as unlocked and migrate on next write.
- CORS is wide open (`*`) so the Pages copy can sync here. That is deliberate.
- The PIN is the *only* thing protecting a blob, it travels in a header, and the
  blob sits on disk as plain JSON. Fine for favourites and grind notes; don't
  put anything real in there.

**`/root/repos/espresso_data` is currently empty — cloud sync has never been used
against this server.** The code path is untested with real data; treat the first
real save/load as a live test.

---

## Gotchas

- **`sw.js` is a service worker with a cache version `V` (now `espresso-v4`).**
  HTML is network-first, so app changes land immediately — but **every other
  asset is stale-while-revalidate**. Change an image or an icon without bumping
  `V` and installed phones keep the old one. Bump `V` when assets change.
- **Grind numbers are the whole point and they are opinions.** They were
  recalibrated three times (`dc73adb` → `34550d8` → `4ad83e8`). The Varia VS3
  dial is 0–9.9, finer = lower; the **basket toggle** (stock/pressurized ≈ 2.5 vs
  unpressurized ≈ 0.8) rewrites every Dedica espresso number, the prep/tamp step,
  and the shot animation at once. Don't "fix" one drink in isolation.
- **EN and HE step arrays must stay the same length** — the language toggle
  indexes them in parallel. `88fac31` had to add a step to both sides.
- **Hebrew + numbers need bidi isolation.** The timer target rendered backwards
  until the numeric part got its own `direction:ltr` span. Same trap anywhere a
  digit sits inside Hebrew text.
- One file, no build: `index.html` is ~148 KB of HTML + CSS + vanilla JS with the
  data (`MACHINES`, `HE_DRINKS`) and the inline-SVG scenes in it. There is no
  bundler to hide behind and no tests — changes get verified by opening it.
- Image generation (`gen_images.py`, `gen_bg.py`) needs `GOOGLE_API_KEY`. The 34
  JPGs in `images/` are committed, so you only need the key to regenerate.

---

## Recent work

- `88fac31` — iced-latte steps reordered so the sweetener goes in **before** the
  milk (the old wording told you to add syrup "before the milk" in a step that
  ran after the milk was already poured); timer Hebrew legibility; count-up /
  count-down toggle, defaulting to counting **down** to the target.
- `fa3702a` — moka default 5.0 + **⤓ use this grind for all [machine]**.
- `1999646` / `8b5534e` — grind-trend sparkline in *Rate this cup*; − / + grind
  stepper and ↺ reset-to-default, synced with custom overrides.
- `c94de4a` — per-drink custom recipe overrides + bottomless-portafilter animation.

---

## Open / next

- [x] ~~The VPS pull is manual~~ — fixed 2026-07-30: nightly cron at 04:17 UTC,
      schedule editable in `/etc/cron.d/espresso-pull` (see Deployment).
- [ ] Cloud sync has **zero real usage** (data dir empty). Do one save + load
      across two devices before trusting it.
- [ ] **This repo is public.** Nothing secret is in it today, and the sync PIN
      default (`3944`, documented in `GUIDE.md`) is client-side and therefore
      public by nature anyway — but don't let a real credential land here. The
      VPS admin details belong in the private repos.
- [ ] No `UPGRADES.md`-driven work queued yet; the file exists as an empty inbox.
- [ ] `sw.js` is still on `espresso-v4` — if the next change touches `images/`,
      remember it needs a bump.
- [ ] The app is a single 148 KB `index.html`. It's fine, but the next big feature
      is the point where splitting the data (`MACHINES`/`HE_DRINKS`) out into its
      own file starts paying for itself.
