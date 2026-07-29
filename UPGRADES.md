# 🚀 UPGRADES — espresso (brew guide)

**What this is:** a running inbox of upgrades / changes you (the owner) want made to
**espresso**. Drop requests here anytime — the next AI coding session reads this file
right after `HANDOFF.md` and implements the top unchecked items.

## For the owner (Or)
- Add anything you want changed under **📥 Requested** below — one line each, plain language.
- Rough is fine (e.g. "the moka steps are too long", "add cortado to the moka", "make the
  timer bigger"). No need to be technical.
- Priority: put the most important at the top, or tag it `[P0]` / `[P1]`.
- Taste notes count as requests: "espresso comes out sour at 2.5" is a real bug here.

## For the next AI session — PROTOCOL (do this)
1. Read `HANDOFF.md` (current state) **then this file**.
2. Work the top unchecked `- [ ]` items in **📥 Requested** (respect `[P0]` > `[P1]` > rest).
3. For each finished item: change it to `- [x]`, move it into **✅ Done** with the date + a
   one-line note (commit hash if useful). Verify it per this repo's own rules before claiming
   done — that means **opening the app**, and for anything bilingual, checking EN *and* HE.
4. If a request is unclear or risky, leave it unchecked and add a `> Q:` line asking the owner.
5. Commit + push, **and pull on the VPS** (`ssh root@178.105.148.72 "git -C /root/repos/espresso pull"`)
   — Pages auto-deploys, the server does not. Keep this file the single source of truth for
   "what to build next here."

---

## 📥 Requested  (newest / highest-priority at top)

- [ ] _(nothing queued yet — owner adds items here)_

---

## ✅ Done

- _(none yet)_
