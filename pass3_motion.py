#!/usr/bin/env python
"""POLISH PASS 3 of 3 — MOTION ONLY. Typography and spacing are not touched.

    python pass3_motion.py          # apply
    python pass3_motion.py --undo

MEASURED FIRST, AND THE FIRST FINDING IS A BUG I SHIPPED

The makeover layer declares:

    .bk-reveal, .mk-rv { opacity:0; transform:translateY(16px) }
    .bk-reveal.in, .mk-rv.in { opacity:1; transform:none }

so every revealed block is invisible until JavaScript adds `.in`. When the
IntersectionObserver does not run, the content does not exist. That is not
hypothetical — it happened while testing this page: a backgrounded tab
suspends IntersectionObserver, and the entire machine picker rendered as an
empty band under its heading.

**Content must never require JavaScript in order to be visible.** The reveal
now fails open: everything is visible by default, and the hidden-then-animate
state is only armed once the script has run and confirmed it can animate.
If JS is broken, slow, blocked or throttled, the page is merely static —
never blank.

THE REST OF THE PASS

Durations and easings in use before this pass:

    .15s .18s .2s .25s .3s .5s .6s .8s   and   ease, ease-out,
    cubic-bezier(.2,.7,.3,1), cubic-bezier(.16,1,.3,1)

The same kind of interaction moved at a different speed depending on which
component you touched. Three tokens, matching the method's 200-300ms guidance:

    --m-fast 150ms   colour and border — should feel instant
    --m      220ms   hover transforms, shadows, chips
    --m-slow 320ms   reveals and larger movement

Nothing bounces: no easing here overshoots, and none is introduced.
prefers-reduced-motion disables all of it and forces the revealed state.

Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
START = "<!-- pass3:start -->"
END = "<!-- pass3:end -->"

STYLE = START + """
<style id="pass3-motion">
/* ══ PASS 3 — MOTION ONLY ══════════════════════════════════════════════ */
:root{ --m-fast:150ms; --m:220ms; --m-slow:320ms;
       --m-ease:cubic-bezier(.2,.7,.3,1); --m-out:cubic-bezier(.16,1,.3,1); }

/* FAIL OPEN. Visible by default; only hidden once JS has armed the reveal.
   The previous rule hid content unconditionally and relied on an observer to
   bring it back, which left an empty page whenever the observer did not run. */
.bk-reveal, .mk-rv{ opacity:1; transform:none; }
html.reveal-armed .bk-reveal:not(.in),
html.reveal-armed .mk-rv:not(.in){ opacity:0; transform:translateY(14px); }
.bk-reveal, .mk-rv{
  transition:opacity var(--m-slow) var(--m-out), transform var(--m-slow) var(--m-out);
}

/* one vocabulary for interaction */
.chip, .machine, .bk-cta, .cta, .tbtn, .taste-b, .gs-btn, .theme-btn,
.lang-btn, .fav-btn, .sync-btn, .reset-recipe, .pnav, button{
  transition:background-color var(--m) var(--m-ease),
             border-color var(--m) var(--m-ease),
             color var(--m-fast) var(--m-ease),
             transform var(--m) var(--m-ease),
             box-shadow var(--m) var(--m-ease);
}
.machine:hover, .chip:hover{ transform:translateY(-2px); }
.bk-cta:active, .cta:active, button:active{ transform:translateY(0) scale(.985); }

@media (prefers-reduced-motion: reduce){
  html.reveal-armed .bk-reveal:not(.in),
  html.reveal-armed .mk-rv:not(.in){ opacity:1!important; transform:none!important; }
  *, *::before, *::after{ animation:none!important; transition-duration:.01ms!important; }
}
</style>
""" + END

SCRIPT = START + """
<script id="pass3-motion-js">
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;   // stay visible

  var els = document.querySelectorAll('.bk-reveal, .mk-rv');
  if (!els.length) return;

  // Arm only now — before this line the content is visible, so a script that
  // never reaches here leaves a static page rather than a blank one.
  document.documentElement.classList.add('reveal-armed');

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, {rootMargin:'0px 0px -6% 0px', threshold:.05});
  els.forEach(function(el){ io.observe(el); });

  // Safety net: if nothing has revealed after 1.2s — throttled tab, observer
  // never firing, anything else — drop the armed state and show everything.
  setTimeout(function(){
    var shown = document.querySelectorAll('.bk-reveal.in, .mk-rv.in').length;
    if (!shown) document.documentElement.classList.remove('reveal-armed');
  }, 1200);
})();
</script>
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
        print(f"pass 3 removed ({n} blocks)")
        return 0
    html, _ = undo(html)
    html = html.replace("</head>", STYLE + "\n</head>", 1)
    html = html.replace("</body>", SCRIPT + "\n</body>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print("PASS 3 (motion) applied — reveals fail open, 3 duration tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
