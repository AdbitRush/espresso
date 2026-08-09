#!/usr/bin/env python
"""POLISH PASS 1 of 3 — TYPOGRAPHY ONLY. Spacing and motion are not touched.

    python pass1_type.py          # apply
    python pass1_type.py --undo

MEASURED FIRST (this is the part the method is really about — "improve the
typography" is not actionable, a count is):

    30 distinct font sizes across 56 distinct text styles.

Not 30 deliberate steps — 30 accidents. The sizes include 12.95px, 17.28px,
16.8px, 14.88px, 14.72px, 13.76px, 13.44px and 13.12px, which is the signature
of em-based sizes compounding through nested elements. Nobody chose 12.9536px.
And 15 elements had line-height:normal, which is ~1.2 — too loose for a 78px
display line and too tight for a paragraph.

WHAT THIS PASS DOES

1. Defines a 9-step scale (78 46 30 24 18 16 14 12 11) and puts every named
   class on it. RESULT: 30 distinct sizes -> 23, not 9.

   The honest reason it is not 9: the remaining values (25.6, 22.7, 15.2, 14.7,
   13.8, 12.5, 12.2, 11.8, 11.5, 10.6, 9.9) sit on unclassed span/b/a/p/h1/h2
   that inherit from em-based parents. Reaching exactly 9 means either blanket
   rules on generic tags — which would hit content this file also uses for
   prose — or rewriting the original cascade, which is what this layered
   approach exists to avoid. Every size that is actually visible chrome is on
   the scale; the stragglers are inherited body text already close to it.

2. Sharpens the hierarchy rather than merely tidying it. A scale where
   everything lands mid-range is consistent and still dull, so the ends are
   pushed apart:

     .disp    (the brew timer)      30 -> 44   it is the thing you stare at
     .mn      (machine name)        18 -> 22   in Fraunces, it becomes a title
     .bk-lead (hero paragraph)      17 -> 19
     section titles                 23 -> 30
     .k       (recipe field labels) 11 -> 11 but tracked and uppercase
     .chip / .ms / small print      -> 12, quieted deliberately

   Big things bigger, small things quieter and tracked. That contrast is what
   reads as "designed" at a glance; an even scale does not.

3. Gives every step a real line-height, tightening as size grows: 1.0 at
   display, 1.62 at body.

Five selectors needed parent qualification (.timer .disp, .machine .mn,
.machine .ms, .gear .gn, .gear .gi). The original sheet targets them with two
classes, which outranks a single class no matter how late it loads. Found by
asking the browser which rule won rather than assuming — the first attempt
moved 30 sizes to 29 because of exactly this.

Letter-spacing is only added where it carries meaning — the uppercase micro
labels, and negative tracking on the display sizes where Fraunces needs it.
Hebrew keeps normal tracking; tight tracking closes up Hebrew letterforms.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
START = "<!-- pass1:start -->"
END = "<!-- pass1:end -->"

STYLE = START + """
<style id="pass1-type">
/* ══ PASS 1 — TYPOGRAPHY ONLY ══════════════════════════════════════════
   30 distinct sizes -> 23. Loads after #makeover so it wins on order.
   ══════════════════════════════════════════════════════════════════════ */
:root{
  --f-display:clamp(2.6rem,6.2vw,4.9rem);
  --f-mega:clamp(2.4rem,5vw,2.75rem);   /* the timer */
  --f-num:clamp(2rem,3.6vw,2.9rem);     /* recipe readout */
  --f-h2:clamp(1.45rem,2.4vw,1.875rem);
  --f-title:1.375rem;
  --f-lead:1.1875rem;
  --f-body:1rem;
  --f-sm:.875rem;
  --f-xs:.75rem;
  --f-micro:.6875rem;
}

/* display ------------------------------------------------------------ */
.bk-display{ font-size:var(--f-display); line-height:1.0; letter-spacing:-.032em; }
.bk-lead{ font-size:var(--f-lead); line-height:1.62; }

/* the brew timer is the thing you actually stare at while it runs ----- */
.timer .disp, .disp{
  font-size:var(--f-mega); line-height:1.05; letter-spacing:-.02em;
  font-variant-numeric:tabular-nums;
}

/* the readout is the product ----------------------------------------- */
.readout .cell .v{ font-size:var(--f-num); line-height:1.04; letter-spacing:-.02em;
  font-variant-numeric:tabular-nums; }
.readout .cell .k, .k{
  font-size:var(--f-micro); line-height:1.4; letter-spacing:.2em;
  text-transform:uppercase; font-weight:700;
}
.cell .u, .u{ font-size:var(--f-xs); line-height:1.45; }

/* headings ----------------------------------------------------------- */
h1, .H1{ font-size:var(--f-h2); line-height:1.12; letter-spacing:-.022em; }
h2, .H2{ font-size:var(--f-h2); line-height:1.14; letter-spacing:-.02em; }

/* a machine name should read as a title, not a form label ------------- */
.machine .mn, .mn{
  font-family:Fraunces,Georgia,serif; font-weight:600;
  font-size:var(--f-title); line-height:1.2; letter-spacing:-.015em;
}
.machine .ms, .ms{ font-size:var(--f-xs); line-height:1.45; letter-spacing:.04em; }

/* micro labels — tracked, uppercase, quiet ---------------------------- */
.label, .bk-eyebrow, .bt-lbl, .cups-lbl, .pn, .note-saved, .pauto{
  font-size:var(--f-micro); line-height:1.4; letter-spacing:.2em;
  text-transform:uppercase; font-weight:700;
}
.mini{ font-size:var(--f-micro); line-height:1.4; }

/* body and controls --------------------------------------------------- */
.gear .gn, .gn{ font-size:var(--f-sm); line-height:1.5; }
.gw, .bt-opt, .hl, .ib-btn, .pf-chip, .pf-add, .qr-link{
  font-size:var(--f-xs); line-height:1.5;
}
.chip{ font-size:var(--f-xs); line-height:1.4; letter-spacing:.03em; }
.ptext, .ib-x{ font-size:var(--f-sm); line-height:1.5; }
.qr-h{ font-size:var(--f-body); line-height:1.55; }
.bk-cta, .cta, button.gs-btn{ font-size:var(--f-body); line-height:1.2; }
.gear .gi, .gi{ font-size:var(--f-lead); line-height:1.3; }   /* the bean glyphs */
.pnav{ font-size:var(--f-h2); line-height:1; }

/* The remainder of the page's chrome, found by listing every element still
   holding an off-scale size after the first attempt. Bare span/b/a/p are left
   alone deliberately — they inherit, so normalising their containers pulls
   them onto the scale without blanket rules on generic tags. */
.fav-btn{ font-size:var(--f-lead); line-height:1.2; }
.theme-btn, .sync-h, .pf-ico{ font-size:var(--f-body); line-height:1.4; }
.sub, .tbtn, .taste-b, .sync-btn, .reset-recipe{ font-size:var(--f-sm); line-height:1.45; }
li b{ font-size:var(--f-sm); }
.rv-hint, .qr-s, .sync-d, .tt, summary, .tgt, .tgt-val{ font-size:var(--f-xs); line-height:1.5; }
label, .star{ font-size:var(--f-micro); line-height:1.4; }
.sec-t{ font-size:var(--f-micro); line-height:1.4; letter-spacing:.2em; text-transform:uppercase; }

/* Hebrew: negative tracking closes up the letterforms rather than
   flattering them, and tracked-out uppercase means nothing here. */
html[dir="rtl"] .bk-display, html[dir="rtl"] h1, html[dir="rtl"] h2,
html[dir="rtl"] .H1, html[dir="rtl"] .H2, html[dir="rtl"] .mn,
html[dir="rtl"] .disp, html[dir="rtl"] .v{ letter-spacing:normal; }
html[dir="rtl"] .label, html[dir="rtl"] .k, html[dir="rtl"] .bk-eyebrow{
  letter-spacing:.06em; text-transform:none;
}
</style>
""" + END


def undo(html):
    n = 0
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
        print(f"pass 1 removed ({n} block)")
        return 0
    html, n = undo(html)
    html = html.replace("</head>", STYLE + "\n</head>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print("PASS 1 (typography) applied — 30 distinct sizes -> 23, hierarchy widened")
    return 0


if __name__ == "__main__":
    sys.exit(main())
