#!/usr/bin/env python
"""Complete visual makeover — an additive layer that sits after `redesign.py`.

Why a second layer instead of editing the first: `redesign.py` is already
applied and revertible on its own, and index.html is a 180KB hand-written file
carrying a service worker, a sync contract, Hebrew RTL and a dark theme.
Stacking a second marked block keeps both independently removable and keeps the
diff readable.

    python makeover.py          # apply
    python makeover.py --undo   # remove just this layer

────────────────────────────────────────────────────────────────────────────
THE BRIEF (written down first, because adjectives are not a design direction)

Audience      Someone standing in their kitchen holding a phone, who owns a
              Dedica or a moka pot and wants the right numbers in four seconds.
              Not a shopper. They already own the gear.

The one action  Machine → drink → exact grind, dose and time. Everything on the
              page either moves them along that path or gets out of the way.

Quality bar   An editorial coffee journal — Kinfolk, Monocle, a serious roaster's
              print catalogue. Photography does the talking, type is quiet and
              confident, nothing decorative.

Ban list      No muddy grey-brown. No emoji as interface icons. No generic
              drop-shadowed cards. No centred-everything. No border radius over
              14px on content. No animation that bounces. No decorative gradient
              that is not light behaving like light.

WHAT ACTUALLY CHANGES, AND WHY

1. Palette. The page was a washed grey-brown that read as "unfinished dark
   theme" rather than a decision. Replaced with a real espresso palette: an
   almost-black roast, warm cream, and copper as the single accent. One accent,
   used sparingly, is what separates designed from decorated.

2. The header floated in a lighter band above the hero, so the page opened with
   a 90px strip of nothing. It now sits on the image, transparent, and gains a
   surface only once you scroll past the hero.

3. Photography discipline. There are 37 images generated at different times
   under different lighting, and they did not read as one set. They now share a
   treatment — a slight desaturation, a touch of contrast, and a warm multiply
   wash — so the page looks shot rather than assembled. This is the single
   highest-leverage change and it costs nothing.

4. One drink photo was rendering 704px tall and overflowing the viewport.
   Images now carry fixed aspect ratios and a viewport cap.

5. The recipe numbers — grind, dose, time — were small cells in a row. They are
   the entire reason the site exists, so they are now the largest non-display
   type on the page, set in tabular figures so the digits stop shifting as they
   change.

6. Section labels ("1 · Machine") were ordinary small text. They are now tracked
   editorial markers with a hairline rule, which is what gives a page the sense
   that someone set it rather than stacked it.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

START = "<!-- makeover:start -->"
END = "<!-- makeover:end -->"

STYLE = START + """
<style id="makeover">
/* ═══════════════════════════════════════════════════════════════════
   MAKEOVER — additive. Loads after #bateshka, overrides only.
   Remove this whole block to revert.
   ═══════════════════════════════════════════════════════════════════ */

/* ── 1. palette ────────────────────────────────────────────────────
   Was a washed grey-brown that read as an unfinished dark theme. This
   is a roast: near-black with red in it, warm cream, copper accent. */
:root{
  --roast:#0C0806;
  --roast-2:#151009;
  --roast-3:#1F1710;
  --cream:#F5EEE4;
  --cream-2:#D8CCBC;
  --ash:#9C8B7B;
  --copper:#C87B3C;
  --copper-lo:rgba(200,123,60,.14);
  --hair:rgba(245,238,228,.10);
  --shell:1240px;
  --ease:cubic-bezier(.2,.7,.3,1);
  --t:200ms; --t-slow:320ms;
}
[data-theme="dark"], html[data-theme="dark"] body{
  --bg:var(--roast); --panel:var(--roast-2); --ink:var(--cream);
}
[data-theme="dark"] body{
  background:
    radial-gradient(1200px 700px at 78% -8%, rgba(200,123,60,.10), transparent 60%),
    radial-gradient(900px 600px at 8% 12%, rgba(120,70,30,.07), transparent 62%),
    var(--roast);
  color:var(--cream);
}

/* ── 2. photography ────────────────────────────────────────────────
   37 images made at different times under different light. A shared
   treatment is what makes them read as one shoot instead of a folder.
   Highest-leverage change on the page, and it costs nothing. */
.machine .mic, .card img, .shot img, img.hero-img, .gi img{
  filter:saturate(.9) contrast(1.06) brightness(.98);
}
.machine, .shot, .card{ position:relative; }
.machine::after, .shot::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(180deg, rgba(12,8,6,0) 42%, rgba(12,8,6,.55) 100%);
  mix-blend-mode:multiply; border-radius:inherit;
}

/* No image may exceed the viewport. One drink photo was rendering 704px
   tall and pushing everything below the fold. */
img{ max-height:62vh; object-fit:cover; }
.machine .mic{ aspect-ratio:4/3; height:auto; width:100%; object-fit:cover; }

/* ── 3. header sits ON the hero ────────────────────────────────────
   It was in a lighter band above it, so the page opened with 90px of
   nothing. Transparent over the image; gains a surface after scroll. */
header{
  position:absolute; inset-inline:0; top:0; z-index:40;
  background:transparent!important; border-bottom:1px solid transparent!important;
  backdrop-filter:none!important;
  transition:background var(--t) var(--ease), border-color var(--t) var(--ease),
             backdrop-filter var(--t) var(--ease);
  /* A soft top scrim so the wordmark stays readable over any photograph even
     if no scroll state ever applies. Degrading to "unreadable" is not an
     option; degrading to "slightly less crisp" is. */
  -webkit-mask-image:none;
  text-shadow:0 1px 14px rgba(0,0,0,.55);
}
html.mk-scrolled header{
  position:fixed;
  background:rgba(12,8,6,.72)!important;
  border-bottom:1px solid var(--hair)!important;
  backdrop-filter:blur(14px) saturate(1.2)!important;
}
/* Preferred path: no JavaScript at all. A scroll-driven animation ties the
   header's surface directly to scroll position, so it cannot be broken by a
   missing listener, a throttled tab, or the app rewriting class names. The
   observer below is only a fallback for engines without scroll timelines. */
@supports (animation-timeline: scroll()){
  header{
    position:fixed;
    animation:mk-header-surface linear both;
    animation-timeline:scroll(root block);
    animation-range:120px 420px;
  }
  @keyframes mk-header-surface{
    from{ background-color:rgba(12,8,6,0); border-bottom-color:transparent; }
    to  { background-color:rgba(12,8,6,.78); border-bottom-color:rgba(245,238,228,.10); }
  }
  html.mk-scrolled header{ backdrop-filter:blur(14px) saturate(1.2)!important; }
}
.brand .mark{ box-shadow:0 6px 22px rgba(200,123,60,.34); }

/* ── 4. hero ───────────────────────────────────────────────────────
   Full-bleed, and the type lockup pinned low-left the way a title card
   sits, rather than floating in the middle of the frame. */
/* Do NOT touch .bk-hero::before — that is where the photograph lives
   (url(images/hero-cine.jpg), z-index 0). The scrim is already on ::after.
   Redefining ::before here is exactly how I blanked the hero the first time. */
.bk-hero{
  min-height:min(92vh,860px); margin-top:0!important;
  border-radius:0; overflow:hidden;
}
/* Pinned low-left against the shell, the way a title card sits — it was
   floating centre-ish because the copy block had a max-width and auto margins. */
.bk-hero-copy{
  position:relative; z-index:2;
  width:min(var(--shell),100%); max-width:none;
  margin-inline:auto;
  padding-inline:clamp(20px,5vw,48px);
  padding-bottom:clamp(2.25rem,6vh,4.5rem);
}
.bk-hero-copy > *{ max-width:min(56ch,760px); }
.bk-eyebrow{
  font-family:Archivo,system-ui,sans-serif; font-size:.7rem; font-weight:700;
  letter-spacing:.24em; text-transform:uppercase; color:var(--copper);
  display:inline-flex; align-items:center; gap:.8em;
}
.bk-eyebrow::before{ content:""; width:34px; height:1px; background:var(--copper); opacity:.85; }
.bk-display{
  font-family:Fraunces,Georgia,serif; font-weight:600;
  font-size:clamp(2.5rem,6.1vw,5rem); line-height:.96; letter-spacing:-.03em;
  text-wrap:balance; margin:.28em 0 .34em;
}
.bk-lead{
  font-size:clamp(1.02rem,1.35vw,1.22rem); line-height:1.62;
  color:var(--cream-2); max-width:54ch;
}

/* ── 5. section markers ────────────────────────────────────────────
   "1 · Machine" was ordinary small text. Tracked marker plus a hairline
   is what makes a page look set rather than stacked. */
.label, .label-row > .label, .sec-t{
  font-family:Archivo,system-ui,sans-serif; font-size:.7rem!important;
  font-weight:700; letter-spacing:.22em; text-transform:uppercase;
  color:var(--ash); display:flex; align-items:center; gap:1em;
  padding-bottom:.9em; margin-bottom:1.5em;
  border-bottom:1px solid var(--hair);
}
.label::after, .sec-t::after{ content:""; flex:1 1 auto; }

/* ── 6. the numbers are the product ────────────────────────────────
   Selector is .readout .cell .v, not .cell .v: the original sheet has
   .cell.grind .v at 1.55rem, which outranks a two-class selector. */
/*
   Grind, dose and time are why anyone opens this. They were small cells
   in a row. Tabular figures so digits stop shifting as values change. */
.cell{
  background:linear-gradient(180deg,rgba(245,238,228,.045),rgba(245,238,228,.015));
  border:1px solid var(--hair); border-radius:14px;
  padding:1.15rem 1rem; text-align:center;
}
.cell .k{
  font-size:.66rem; letter-spacing:.2em; text-transform:uppercase;
  color:var(--ash); font-weight:700;
}
.readout .cell .v{
  font-family:Fraunces,Georgia,serif; font-weight:600;
  font-size:clamp(2rem,3.6vw,2.9rem); line-height:1.04; color:var(--cream);
  font-variant-numeric:tabular-nums; letter-spacing:-.02em; display:block;
  margin-top:.18em;
}
.cell .u{ font-size:.8rem; color:var(--ash); letter-spacing:.02em; }

/* ── 7. tiles ──────────────────────────────────────────────────────
   Were app cards with heavy borders. Editorial tiles: the photograph
   carries it, the caption sits quietly underneath. */
.machine{
  border:1px solid var(--hair)!important; border-radius:14px; overflow:hidden;
  background:var(--roast-2); box-shadow:none!important;
  transition:transform var(--t) var(--ease), border-color var(--t) var(--ease);
}
.machine:hover{ transform:translateY(-3px); border-color:rgba(200,123,60,.42)!important; }
.machine.on, .machine[aria-pressed="true"]{
  border-color:var(--copper)!important;
  box-shadow:0 0 0 1px var(--copper), 0 18px 44px rgba(0,0,0,.5)!important;
}
.machine .mn{
  font-family:Fraunces,Georgia,serif; font-weight:600; font-size:1.12rem;
  letter-spacing:-.012em; color:var(--cream);
}
.machine .ms{ font-size:.78rem; color:var(--ash); letter-spacing:.04em; }

.chip{
  border:1px solid var(--hair); background:rgba(245,238,228,.04);
  color:var(--cream-2); border-radius:999px; letter-spacing:.02em;
  transition:background var(--t) var(--ease), border-color var(--t) var(--ease), color var(--t) var(--ease);
}
.chip:hover{ border-color:rgba(200,123,60,.45); color:var(--cream); }
.chip.on{ background:var(--copper-lo); border-color:var(--copper); color:var(--cream); }

/* ── 8. motion ─────────────────────────────────────────────────────
   Reveals only, and only once. Nothing overshoots. */
.bk-reveal, .mk-rv{
  opacity:0; transform:translateY(16px);
  transition:opacity var(--t-slow) var(--ease), transform var(--t-slow) var(--ease);
}
.bk-reveal.in, .mk-rv.in{ opacity:1; transform:none; }

@media (prefers-reduced-motion: reduce){
  .bk-reveal, .mk-rv{ opacity:1!important; transform:none!important; transition:none!important; }
  header{ transition:none!important; }
}

/* ── 9. mobile ─────────────────────────────────────────────────────
   375px is the check that matters; most of this is read one-handed. */
@media(max-width:768px){
  .bk-hero{ min-height:min(86vh,720px); }
  .bk-display{ font-size:clamp(2.4rem,10.5vw,3.4rem); }
  .cell{ padding:.9rem .7rem; }
  .readout .cell .v{ font-size:clamp(1.7rem,7.5vw,2.2rem); }
  img{ max-height:52vh; }
}
</style>
""" + END

SCRIPT = START + """
<script id="makeover-js">
(function(){
  // Header earns a surface once the hero is behind you.
  //
  // Deliberately NOT a scroll listener: this page never fires scroll events on
  // window (verified — a probe listener counted zero while window.scrollY was
  // changing), so the obvious implementation silently did nothing. An
  // IntersectionObserver on the hero is reliable here, and it is the better
  // approach regardless: no handler running on every frame.
  //
  // The flag also lives on <html> rather than <body>, because the app rewrites
  // body.className as it renders and was wiping it.
  var hero = document.getElementById('bkHero');
  if (hero && 'IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      document.documentElement.classList.toggle('mk-scrolled', !es[0].isIntersecting);
    }, {rootMargin:'-90px 0px 0px 0px', threshold:0}).observe(hero);
  }

  // Reveal once, then stop observing — re-animating on every pass is the
  // thing that makes scroll-reveal feel cheap.
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {rootMargin:'0px 0px -8% 0px', threshold:.06});
    document.querySelectorAll('.bk-reveal, .mk-rv').forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('.bk-reveal, .mk-rv').forEach(function(el){ el.classList.add('in'); });
  }
})();
</script>
""" + END


def undo(html):
    out, n = [], 0
    while True:
        i = html.find(START)
        if i == -1:
            break
        j = html.find(END, i)
        if j == -1:
            break
        html = html[:i] + html[j + len(END):]
        n += 1
    return html, n


def main():
    html = INDEX.read_text(encoding="utf-8")

    if "--undo" in sys.argv:
        html, n = undo(html)
        INDEX.write_text(html, encoding="utf-8")
        print(f"removed {n} makeover block(s)")
        return 0

    html, n = undo(html)                      # idempotent: strip, then re-add
    if "</head>" not in html:
        raise SystemExit("no </head> found")
    html = html.replace("</head>", STYLE + "\n</head>", 1)
    if "</body>" not in html:
        raise SystemExit("no </body> found")
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print("makeover applied" + (f" (replaced {n} existing block(s))" if n else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
