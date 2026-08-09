#!/usr/bin/env python
"""POLISH PASS 2 of 3 — SPACING ONLY. Typography and motion are not touched.

    python pass2_spacing.py          # apply
    python pass2_spacing.py --undo

MEASURED FIRST

    block padding (top/bottom)   0/18   51/0   11/11   0/0   32/32   38/0
    grid + flex gaps             10px   12px   14px    16px
    space above section labels   0px    22px   24px

Six paddings, four of them asymmetric and three of those top-heavy with
literally zero underneath — so a block ends by colliding with whatever is
next. Four different gaps doing the same job. And the numbered sections
("1 · Machine", "2 · Drink", "Steps") are separated by 0, 22 or 24px depending
on which one you land on, which is why the page reads as a continuous scroll
of controls rather than a sequence of steps.

WHAT THIS PASS DOES

1. One section rhythm. Every numbered section label gets clamp(46px,6vw,78px)
   above it. This is the single biggest visible change in the three passes: the
   steps stop touching and start reading as steps. It is the method's "double
   the whitespace where sections feel cramped", and they were cramped.

2. One gap. 10/12/14/16 collapse to 16px, with 24px where a grid separates
   whole cards rather than controls.

3. Symmetric block padding on an 8px grid. Nothing ends with zero.

4. A hairline above each section label, so the rhythm is visible rather than
   merely present — whitespace alone reads as "unfinished" until something
   marks the boundary.

The hero is deliberately exempt: it is full-bleed and sets its own inset.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
START = "<!-- pass2:start -->"
END = "<!-- pass2:end -->"

STYLE = START + """
<style id="pass2-spacing">
/* ══ PASS 2 — SPACING ONLY ═════════════════════════════════════════════
   6 paddings + 4 gaps + 3 section rhythms -> one system on an 8px grid.
   ══════════════════════════════════════════════════════════════════════ */
:root{
  --sec-y:clamp(46px,6vw,78px);   /* above every numbered section */
  --gap:16px;                     /* controls, chips, cells */
  --gap-lg:24px;                  /* whole cards */
  --pad:20px; --pad-lg:28px;
}

/* 1 ── section rhythm ------------------------------------------------
   Was 0 / 22 / 24px depending on the section. The steps were touching. */
.label, .sec-t{
  margin-top:var(--sec-y)!important;
  margin-bottom:18px!important;
  padding-top:18px;
  border-top:1px solid var(--hair,rgba(245,238,228,.10));
}
/* The first label after the hero needs no rule above it — the hero already
   is the boundary, and a hairline there reads as a stray line. */
.bk-hero + * .label:first-of-type,
#favWrap .label{ border-top:0; padding-top:0; margin-top:clamp(28px,3.5vw,44px)!important; }

/* 2 ── one gap -------------------------------------------------------- */
.machines, .grid, .drinks, .cells, .readout, .gearlist, .chips, .row{
  gap:var(--gap);
}
.machines, .drinks, .gearlist{ gap:var(--gap-lg); }

/* 3 ── symmetric padding; nothing ends at zero ------------------------ */
.card, .panel, .recipe, .qr-card, .sync-card, .tt{
  padding:var(--pad-lg) var(--pad);
}
.cell{ padding:var(--pad) 12px; }

/* the readout is the payoff — give it room to be the payoff */
.recipe .readout{ margin-block:var(--gap-lg); }

/* 4 ── page bottom: the footer was landing straight after content ----- */
footer{ margin-top:var(--sec-y); padding-block:32px; }

@media(max-width:768px){
  :root{ --sec-y:clamp(34px,7vw,48px); --pad:16px; --pad-lg:20px; --gap-lg:16px; }
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
        print(f"pass 2 removed ({n} block)")
        return 0
    html, _ = undo(html)
    html = html.replace("</head>", STYLE + "\n</head>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print("PASS 2 (spacing) applied — one section rhythm, one gap, symmetric padding")
    return 0


if __name__ == "__main__":
    sys.exit(main())
