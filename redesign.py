#!/usr/bin/env python
"""Apply the design refactor to index.html as an additive override layer.

This is a single 148KB hand-written file with no build step, powering an
installable PWA with a service worker and a cloud sync API. Rewriting its CSS
in place would risk the sync contract, the offline cache, the Hebrew RTL mode
and the dark theme for a purely visual gain.

So the refactor is layered instead: one <style> block appended after the
existing one, one hero section inserted, one small motion script. Every rule
here overrides rather than replaces, which keeps the diff readable and makes
the whole thing revertible by deleting three marked blocks.

    python redesign.py          # apply
    python redesign.py --undo   # remove it again

Idempotent.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

START = "<!-- bateshka:start -->"
END = "<!-- bateshka:end -->"

# ---------------------------------------------------------------- styles ---
STYLE = """
<style id="bateshka">
/* ============================================================
   Design refactor — additive layer. Overrides only; the original
   cascade above is untouched. Delete the three bateshka blocks to
   revert completely.
   ============================================================ */

:root{
  /* Fluid type scale. clamp() rather than breakpoints so the display
     sizes track the viewport instead of jumping at arbitrary widths. */
  --fs-display: clamp(2.6rem, 7vw, 5.25rem);
  --fs-h2:      clamp(1.5rem, 2.6vw, 2.25rem);
  --fs-lead:    clamp(1.02rem, 1.5vw, 1.3rem);
  --fs-eyebrow: .72rem;

  /* Spacing rhythm. The original sections butted together at ~22px;
     these give the page room to breathe without feeling sparse. */
  --sp-section: clamp(3.5rem, 7vw, 7rem);
  --sp-block:   clamp(1.5rem, 3vw, 2.75rem);

  /* Elevation ramp — the original had a single --shadow. */
  --e1: 0 1px 2px rgba(60,40,20,.05), 0 2px 8px rgba(60,40,20,.04);
  --e2: 0 2px 6px rgba(60,40,20,.07), 0 12px 32px rgba(60,40,20,.09);
  --e3: 0 6px 18px rgba(60,40,20,.10), 0 28px 60px rgba(60,40,20,.14);

  --shell: 1120px;
  --ease: cubic-bezier(.2,.7,.3,1);
}
[data-theme="dark"]{
  --e1: 0 1px 2px rgba(0,0,0,.4), 0 2px 8px rgba(0,0,0,.3);
  --e2: 0 2px 6px rgba(0,0,0,.45), 0 12px 32px rgba(0,0,0,.4);
  --e3: 0 6px 18px rgba(0,0,0,.5), 0 28px 60px rgba(0,0,0,.55);
}

/* ---- shell -------------------------------------------------------------
   Was max-width:680px, which left roughly two thirds of a desktop viewport
   empty. The reading column stays narrow where narrow is correct; only the
   layout gets the extra room. */
.wrap{ max-width: var(--shell) !important; padding: 22px clamp(18px,4vw,40px) 120px !important; }
.wrap > section, .wrap > .sync-card, .wrap > .qr-card{ margin-top: var(--sp-section); }

/* ---- typography --------------------------------------------------------
   Display type gets negative tracking, which Fraunces needs at large sizes;
   body copy gets a longer measure and looser leading. */
h1, h2, h3, .bk-display{ letter-spacing: -.022em; }
.bk-display{
  font-family:"Fraunces", serif;
  font-size: var(--fs-display);
  line-height: .96;
  font-weight: 700;
  margin: 0;
  text-wrap: balance;
}
.bk-lead{
  font-size: var(--fs-lead);
  line-height: 1.6;
  color: var(--ink-soft);
  max-width: 46ch;
  margin: 1.1rem 0 0;
}
.bk-eyebrow{
  font-family:"JetBrains Mono", monospace;
  font-size: var(--fs-eyebrow);
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--crema);
  margin: 0 0 1rem;
  display: block;
}

/* ---- hero --------------------------------------------------------------
   Asymmetric: type occupies the left 7 columns, an overlapping image stack
   the right 5. Collapses to type-only on small screens, where the stack
   would just be noise. */
.bk-hero{
  display: grid;
  grid-template-columns: 7fr 5fr;
  gap: clamp(1.5rem, 4vw, 4rem);
  align-items: center;
  padding: clamp(2rem, 6vw, 5.5rem) 0 var(--sp-block);
}
.bk-hero-copy{ min-width: 0; }
.bk-cta-row{ display:flex; gap:.7rem; flex-wrap:wrap; margin-top: 1.8rem; }
.bk-cta{
  display:inline-flex; align-items:center; gap:.5rem;
  font: 600 .95rem/1 "Archivo", system-ui, sans-serif;
  padding: .85rem 1.4rem; border-radius: 999px;
  background: var(--crema); color:#fff8ef; text-decoration:none;
  border: 0; cursor: pointer;
  box-shadow: var(--e1);
  transition: transform .22s var(--ease), box-shadow .22s var(--ease), background .22s var(--ease);
}
.bk-cta:hover{ transform: translateY(-2px); box-shadow: var(--e2); background: var(--crema-bright); }
.bk-cta.ghost{
  background: transparent; color: var(--ink);
  border: 1.5px solid var(--hair);
}
.bk-cta.ghost:hover{ background: var(--card); border-color: var(--crema); }

/* Overlapping image stack — the "depth" the flat grid was missing. */
.bk-stack{ position: relative; aspect-ratio: 1/1; }
.bk-stack img{
  position:absolute; border-radius: 18px; object-fit: cover;
  box-shadow: var(--e3); border: 1px solid var(--hair);
}
.bk-stack img:nth-child(1){ width:70%; height:70%; top:0; right:0; z-index:2; }
.bk-stack img:nth-child(2){ width:52%; height:52%; bottom:4%; left:0; z-index:3; }
.bk-stack img:nth-child(3){ width:40%; height:40%; top:38%; right:6%; z-index:1; opacity:.9; }

/* ---- machine picker ----------------------------------------------------
   Was repeat(4,1fr) with five tiles, so the fifth sat alone on its own row.
   A six-column grid takes 3+3 then 2+2+2 — no orphan, and the first two read
   as primary. */
@media (min-width: 900px){
  .machines{
    grid-template-columns: repeat(6, 1fr) !important;
    gap: 14px !important;
  }
  .machines > *:nth-child(1),
  .machines > *:nth-child(2){ grid-column: span 3; }
  .machines > *:nth-child(n+3){ grid-column: span 2; }
  .machines > *:nth-child(1) .hero,
  .machines > *:nth-child(2) .hero{ aspect-ratio: 16/9; }
}
.machines > *{
  transition: transform .24s var(--ease), box-shadow .24s var(--ease);
}
.machines > *:hover{ transform: translateY(-3px); box-shadow: var(--e2); }

/* ---- section headings --------------------------------------------------- */
.step-label, .steplabel{ letter-spacing: .16em !important; }

/* ---- scroll reveal ------------------------------------------------------
   Opacity+translate only, both compositor-friendly. Elements start visible
   and are hidden by script, so the page still reads with JS disabled. */
.bk-reveal{ opacity: 0; transform: translateY(18px); }
.bk-reveal.bk-in{
  opacity: 1; transform: none;
  transition: opacity .55s var(--ease), transform .55s var(--ease);
}

/* ---- responsive --------------------------------------------------------- */
@media (max-width: 899px){
  .bk-hero{ grid-template-columns: 1fr; padding-top: 1.5rem; }
  .bk-stack{ display: none; }
}
@media (max-width: 420px){
  :root{ --fs-display: clamp(2.1rem, 11vw, 2.9rem); }
  .wrap{ padding-left: 16px !important; padding-right: 16px !important; }
  .bk-cta{ flex: 1 1 auto; justify-content: center; }
}

@media (prefers-reduced-motion: reduce){
  .bk-reveal{ opacity: 1 !important; transform: none !important; }
  .machines > *:hover, .bk-cta:hover{ transform: none; }
  *{ transition-duration: .01ms !important; }
}

/* ============================ polish pass ============================ */

/* The header was floating in the middle of the page with no anchor. Give it
   a hairline and let the hero sit up against it instead of drifting. */
header{
  border-bottom: 1px solid var(--hair);
  padding-bottom: 18px !important;
  margin-bottom: 0 !important;
}
.bk-hero{ padding-top: clamp(1.75rem, 4vw, 3.5rem) !important; }

/* Step labels were 11px grey text doing the work of a section heading.
   Give them a rule and real presence without shouting. */
.step, .steplabel, .step-label,
.wrap > .lbl, .lbl{
  display: flex !important;
  align-items: center;
  gap: .9rem;
  font-family: "JetBrains Mono", monospace;
  font-size: .7rem !important;
  letter-spacing: .2em !important;
  text-transform: uppercase;
  color: var(--ink-soft) !important;
  margin: var(--sp-block) 0 1rem !important;
}
.step::after, .steplabel::after, .step-label::after, .lbl::after{
  content: ""; flex: 1 1 auto; height: 1px;
  background: linear-gradient(90deg, var(--hair), transparent);
}

/* Cards: deepen the resting state and make the hover feel intentional
   rather than a generic lift. */
.machines > *{
  border-radius: 16px !important;
  overflow: hidden;
  box-shadow: var(--e1);
  border: 1px solid var(--hair);
  background: var(--card);
}
.machines > *:hover{ border-color: color-mix(in oklab, var(--crema) 45%, var(--hair)); }
.machines .hero{ overflow: hidden; }
.machines .hero img{
  transition: transform .5s var(--ease);
  will-change: transform;
}
.machines > *:hover .hero img{ transform: scale(1.045); }

/* The two feature cards read as plain boxes; give them the same elevation
   language as everything else. */
.qr-card, .sync-card{
  border-radius: 18px !important;
  box-shadow: var(--e2) !important;
  border: 1px solid var(--hair) !important;
  padding: clamp(1.25rem, 3vw, 2rem) !important;
}

/* Empty state — "Pick a machine first ↑" was bare text on the page. */
#drinks:empty, .empty-hint{
  color: var(--ink-soft);
  font-style: italic;
}

/* Footer was crowding the last card. */
footer{
  margin-top: var(--sp-section) !important;
  padding-top: var(--sp-block) !important;
  border-top: 1px solid var(--hair);
  color: var(--ink-soft);
}

/* Focus ring — the original relied on the browser default, which the warm
   palette washes out. Needed for keyboard use and for accessibility. */
:where(button, a, input, [tabindex]):focus-visible{
  outline: 2px solid var(--crema);
  outline-offset: 3px;
  border-radius: 8px;
}
</style>
"""

# ------------------------------------------------------------------ hero ---
HERO = """
<section class="bk-hero" id="bkHero">
  <div class="bk-hero-copy">
    <span class="bk-eyebrow" data-i18n-bk="eyebrow">Grind · dose · time</span>
    <h2 class="bk-display" data-i18n-bk="title">Pull a better shot<br>than yesterday.</h2>
    <p class="bk-lead" data-i18n-bk="lead">Exact grind numbers and step-by-step recipes for the kit you
      already own — the Varia VS3, the Dedica, a moka pot on the hob. No guesswork, no scales envy.</p>
    <div class="bk-cta-row">
      <button class="bk-cta" type="button" id="bkStart" data-i18n-bk="cta1">Start with your machine</button>
      <button class="bk-cta ghost" type="button" id="bkSurprise" data-i18n-bk="cta2">Surprise me</button>
    </div>
  </div>
  <div class="bk-stack" aria-hidden="true">
    <img src="images/dedica_espresso.jpg" alt="" loading="eager" width="600" height="600">
    <img src="images/milkfoam_latteart.jpg" alt="" loading="lazy" width="600" height="600">
    <img src="images/filter_v60.jpg" alt="" loading="lazy" width="600" height="600">
  </div>
</section>
"""

# ----------------------------------------------------------------- motion ---
SCRIPT = """
<script id="bateshka-motion">
/* Scroll reveal + hero wiring. Progressive enhancement: if this never runs,
   nothing is hidden and every control still works. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Hero buttons reuse the controls that already exist rather than
  // duplicating their logic.
  var start = document.getElementById('bkStart');
  if (start) start.addEventListener('click', function () {
    var m = document.getElementById('machines');
    if (m) {
      m.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      var first = m.querySelector('button, [role=button], .machine');
      if (first && first.focus) setTimeout(function(){ first.focus({preventScroll:true}); }, reduce ? 0 : 450);
    }
  });
  var surprise = document.getElementById('bkSurprise');
  if (surprise) surprise.addEventListener('click', function () {
    var existing = document.getElementById('surprise') ||
                   document.querySelector('[id*="surprise" i], [class*="surprise" i]');
    if (existing && existing.click) existing.click();
  });

  if (reduce || !('IntersectionObserver' in window)) return;

  var targets = document.querySelectorAll(
    '.bk-hero-copy, .bk-stack, #machines, .qr-card, .sync-card, #favWrap');
  if (!targets.length) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('bk-in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });

  targets.forEach(function (el, i) {
    el.classList.add('bk-reveal');
    el.style.transitionDelay = Math.min(i * 60, 240) + 'ms';
    io.observe(el);
  });
})();
</script>
"""


def undo(html):
    return re.sub(re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)


def main():
    html = INDEX.read_text(encoding="utf-8")

    if "--undo" in sys.argv:
        out = undo(html)
        INDEX.write_text(out, encoding="utf-8")
        print("reverted" if out != html else "nothing to revert")
        return

    if START in html:
        html = undo(html)
        print("re-applying over the previous layer")

    # 1. styles — immediately after the existing stylesheet closes
    i = html.find("</style>")
    if i == -1:
        sys.exit("no </style> found")
    i += len("</style>")
    html = html[:i] + f"\n{START}\n{STYLE.strip()}\n{END}\n" + html[i:]

    # 2. hero — straight after the header
    j = html.find("</header>")
    if j == -1:
        sys.exit("no </header> found")
    j += len("</header>")
    html = html[:j] + f"\n{START}\n{HERO.strip()}\n{END}\n" + html[j:]

    # 3. motion — last thing before </body>
    k = html.rfind("</body>")
    if k == -1:
        sys.exit("no </body> found")
    html = html[:k] + f"\n{START}\n{SCRIPT.strip()}\n{END}\n" + html[k:]

    INDEX.write_text(html, encoding="utf-8")
    print(f"applied — index.html now {len(html):,} bytes")


if __name__ == "__main__":
    main()
