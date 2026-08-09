# How we build these sites

The method from Romario (@bateshkaaa),
[the thread](https://x.com/bateshkaaa/status/2079218516150862086), written out
in full — plus what actually happened when it was applied to this repo, because
the gap between the method and the practice is where the work is.

The claim: agencies charge $8,000–$12,000 and three weeks for a marketing site.
The same site is one afternoon. Most people still get template-looking output
because they type *"build me a beautiful website"* and pray — and the model
defaults to safe: Inter, a purple gradient, three feature cards.

> **The $10K look comes from constraints, not vibes.**

That one line is the whole method. Everything below is machinery for supplying
constraints.

---

## Part 1 — Load the design brain (15 min)

The model's default taste is a $500 template. Skills change that. A skill is a
folder with a `SKILL.md` that gets read before any design decision.

```
npm install -g @anthropic-ai/claude-code
claude                       # log in
```

Then install two skills — either drop the folders into `.claude/skills/`, or
just paste the links and ask for them to be installed:

```
install github.com/anthropics/skills/tree/main/skills/frontend-design
install github.com/nextlevelbuilder/ui-ux-pro-max-skill
```

Structure ends up as `.claude/skills/frontend-design/SKILL.md`. Restart, then
`/skills` to confirm. No API, no config.

## Part 2 — Steal the direction (20 min)

**Adjectives do not work.** "Make it premium" produces nothing. Screenshots work.

1. Open Awwwards and Dribbble. Search the niche — "SaaS landing", "portfolio",
   "law firm".
2. Pick **3** sites. Not ten — more references confuse the model.
3. Screenshot the hero, one content section, and the footer of each. Nine
   images, saved as `ref-1.png`, `ref-2.png`, `ref-3.png`.
4. Hand them over with exactly this line:

> Match the typography scale, spacing rhythm, and motion of these references.
> Do not copy the layouts.

The "do not copy" clause matters. Without it you get a lookalike of ref-1.

## Part 3 — The build prompt (5 min to write, ~6 to run)

One message, five blocks:

| Block | Example |
|---|---|
| **Audience** | "This site is for freelance photographers charging $2K+ per shoot." |
| **The 1 action** | "Every page pushes toward booking a call. One CTA, repeated." |
| **References** | "Use ref-1.png, ref-2.png, ref-3.png as the quality bar." |
| **Stack** | "Astro, Tailwind, deployed to Cloudflare Pages. Static, fast, no CMS." |
| **Ban list** | "Banned: purple gradients, emoji as icons, Inter as the display font, generic stock-photo placeholders, centered-everything layouts." |

First working version in 4–6 minutes. It will be ~70% there. Nobody ships v1.

## Part 4 — The polish pass (1–2 hours) — **this is the $10K part**

Agencies bill 40% of the project here. Three passes, **as three separate
messages**, in this order:

1. **Typography only** — "Review every heading and body size. Establish a strict
   type scale. Fix line-height and letter-spacing. Touch nothing else."
2. **Spacing only** — "Audit vertical rhythm section by section. Double the
   whitespace where sections feel cramped. Touch nothing else."
3. **Motion only** — "Add scroll-reveal and hover states. Subtle. 200–300ms.
   Nothing bounces."

> Ask for all three at once and you get one dimension done well and two badly.

Then the mobile check: **"Show me every page at 375px width and fix what
breaks."** 60%+ of traffic is a phone. Agencies also check this last — they just
don't mention it.

## Part 5 — Ship (15 min, $0/month)

`git init`, commit, push. Cloudflare Pages → connect repo → build `npm run
build`, output `dist`. Add the domain; DNS propagates in minutes.

## The realistic curve

Site 1 takes 6 hours and looks like $3K. Site 3 takes 3 hours and looks like
$7K. By site 5 it is a 2-hour pipeline.

> You'll end up with a solid website — not a perfect one. Ship it. Find one
> thing to improve each day.

---

# What actually happened here

Applied to `fashionhotspot.site` and this repo. The method is sound. These are
the parts it doesn't warn you about.

### Parts 1–3 don't apply to a site that exists

Most real work is on a live site, not a blank folder. Part 4 is the part that
transfers, and it is the valuable part anyway.

### The passes only work if you measure first

"Establish a strict type scale" is not actionable until you know what you have.
Measuring fashionhotspot found **17 distinct font sizes across 39 text styles** —
including 23px *and* 24px, 13px *and* 13.5px. Nobody can see those differences;
they just double the cost of every future change. That is a finding you can act
on. "The typography could be better" is not.

Same for spacing: nine different section paddings, four sections whose own top
and bottom disagreed, one with 44px above and **10px** below.

### Measuring also tells you what to leave alone

The audit said the letter-spacing was already em-based and consistent
(-0.035em at 64px, -0.03em at 36px, -0.02em at 28px). I had assumed it needed
fixing. It didn't. Likewise `prefers-reduced-motion` was already handled well.

**Two of the three passes found something I would otherwise have "fixed" and
made worse.** A pass that changes nothing is a successful pass.

### The ban list should be written for *this* site

The generic list (no purple gradients, no emoji icons) is a starting point.
The useful version names this project's actual failure modes. For espresso:

> No muddy grey-brown. No emoji as interface icons. No generic drop-shadowed
> cards. No centred-everything. No border radius over 14px on content. No
> animation that bounces. No decorative gradient that isn't light behaving
> like light.

### The highest-leverage change is usually photography, not layout

Espresso has 37 images generated at different times under different lighting.
They did not read as one set. A shared treatment — slight desaturation, a
touch of contrast, a warm multiply wash — did more for "expensive" than any
type change, and cost nothing.

### 375px is where it actually breaks

The mobile check found the homepage scrolling sideways: 427px of content in a
356px viewport. Horizontal scroll is the loudest broken signal a phone site can
give.

Two traps:

- **Windows will not make a browser window 375px wide.** The first attempt
  reported a 1265px viewport and found nothing. Test in a real 375px iframe.
- **Fixing width by wrapping a row makes it worse.** Sixteen filter pills at a
  44px tap target wrapped into five rows: 503px of buttons before the first
  product. A row that is too wide should *scroll*, not stack.

### Verify in the state the user sees

Several bugs this session were phantoms:

- A tab that is backgrounded suspends `requestAnimationFrame`,
  IntersectionObserver and scroll events. Code that looked broken was fine —
  `document.hidden` was `true`.
- An iframe served a cached page, so a working CSS fix looked like it had
  failed, and `!important` got added chasing it.
- A build writes to `docs/` and syncs through a `/tmp` clone, so the
  checked-out copy looks stale until the pull script runs.

Check `document.visibilityState` and cache-bust before believing a fix failed.

### Prefer solutions that cannot break

The espresso header needed a surface once you scroll past the hero. A scroll
listener is the obvious answer and could not be verified in a hidden tab. A CSS
scroll-driven animation (`animation-timeline: scroll()`) ties it directly to
scroll position with no JavaScript, no listener, and nothing for a throttled
tab or a class-rewriting app to break. The observer stays only as a fallback.

When a visual state can be expressed in CSS, express it in CSS.

---

## The checklist

```
□ Write the brief down first: audience, the one action, quality bar, ban list
□ Three references, not ten. "Match the scale and rhythm. Do not copy layouts."
□ MEASURE before each pass — count the sizes, the paddings, the durations
□ Pass 1: typography.  Only.
□ Pass 2: spacing.     Only.
□ Pass 3: motion.      Only.
□ A pass that finds nothing is a good pass. Don't invent work.
□ 375px in a real 375px viewport, not a resized window
□ Rows scroll, they don't stack
□ Confirm the tab is visible before believing anything is broken
□ Ship. One improvement a day.
```

---

# Worked example: the three passes on espresso

Run as three separate passes, each measured before it was written. Each is its
own file and each reverts on its own (`python passN_*.py --undo`).

## Pass 1 — typography (`pass1_type.py`)

**Measured:** 30 distinct font sizes across 56 text styles — including 12.95px,
17.28px, 14.88px, 13.76px. Those are not decisions, they are `em` units
compounding through nested elements. 15 elements had `line-height: normal`.

**Done:** a 9-step scale, and the hierarchy widened rather than merely tidied —
brew timer 30→44px, machine name 18→22px in Fraunces, micro labels tracked and
uppercased at 11px. Big things bigger, small things quieter. An even scale is
consistent and still dull; the contrast is what reads as designed.

**Result: 30 → 23**, not 9. Honest reason: the stragglers sit on unclassed
`span`/`b`/`a`/`h1` inheriting from `em`-based parents, and reaching 9 needs
blanket rules on generic tags or a rewrite of the original cascade.

**Trap:** the first attempt moved 30 → 29. Five selectors (`.timer .disp`,
`.machine .mn`, `.machine .ms`, `.gear .gn`, `.gear .gi`) are two-class in the
original sheet, which outranks a one-class override no matter how late it
loads. Found by asking the browser which rule won — not by reading CSS.

## Pass 2 — spacing (`pass2_spacing.py`)

**Measured:** six block paddings — `0/18`, `51/0`, `11/11`, `0/0`, `32/32`,
`38/0` — four asymmetric, three top-heavy with *zero* underneath, so blocks
ended by colliding with what followed. Four different grid gaps (10/12/14/16).
Section labels separated by 0, 22 or 24px depending which one you hit.

**Done:** one section rhythm, `clamp(46px, 6vw, 78px)` above every numbered
section, with a hairline rule so the rhythm is visible rather than merely
present. One gap. Symmetric padding on an 8px grid.

**Result:** every section now at a uniform 76.8px. Page 5047 → 5648px. This was
the biggest visible change of the three — the steps stopped touching and
started reading as steps.

## Pass 3 — motion (`pass3_motion.py`)

**Measured:** eight durations (.15 → .8s) and four easings mixed arbitrarily.

**And a bug I had shipped in the makeover layer:**

```css
.bk-reveal { opacity: 0 }        /* JS adds .in to bring it back */
```

Every revealed block was invisible until JavaScript ran. Not hypothetical — a
backgrounded tab suspends IntersectionObserver, and the entire machine picker
rendered as an empty band under its heading.

> **Content must never require JavaScript in order to be visible.**

The reveal now *fails open*: visible by default, hidden only once the script has
run and armed it, plus a 1.2s safety net that un-arms if nothing ever revealed.
If JS is blocked, slow or throttled the page is static — never blank.

Three tokens: 150ms colour, 220ms hover, 320ms reveals. Nothing overshoots.

## What the passes cost and returned

| | |
|---|---|
| Measuring first | Turned "improve the typography" into "30 sizes, 5 of them outranked" |
| Doing them separately | Pass 3 found a blank-content bug that a combined pass would have buried |
| Verifying each | Two passes appeared to work and hadn't — 30→29, and reveals |
| Zero API spend | All CSS and existing photography |
