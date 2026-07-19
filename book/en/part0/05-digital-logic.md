---
title: "L4 · Digital Logic — Instructions Are Built from Gates"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L4 · Digital Logic — Instructions Are Built from Gates

```
   L0  framing
   L1  software
   L2  software ↔ OS
   L3  instructions
 ▶ L4  DIGITAL LOGIC  ◀ you are here
   L5  bits & physics
```

**The question carried down:** the CPU executes `sub` — how does silicon
actually subtract?

**The idea.** Numbers inside the CPU are written in **binary** — strings of 1s
and 0s. And arithmetic on them is built from absurdly simple decision-makers
called **logic gates**. A gate takes one or two 1/0 inputs and produces one 1/0
output, following a fixed rule. There are only a few kinds:

```
   AND  → 1 only if BOTH inputs are 1       OR  → 1 if EITHER input is 1
   ┌───────────────┐                        ┌───────────────┐
   │ a  b │ out      │                        │ a  b │ out     │
   │ 0  0 │  0       │                        │ 0  0 │  0      │
   │ 0  1 │  0       │                        │ 0  1 │  1      │
   │ 1  0 │  0       │                        │ 1  0 │  1      │
   │ 1  1 │  1       │                        │ 1  1 │  1      │
   └───────────────┘                        └───────────────┘

   XOR  → 1 if the inputs DIFFER            NOT → flips it: 0→1, 1→0
   ┌───────────────┐
   │ a  b │ out      │
   │ 0  0 │  0       │
   │ 0  1 │  1       │
   │ 1  0 │  1       │
   │ 1  1 │  0       │
   └───────────────┘
```

That's the entire toolkit. From *just these*, you can build arithmetic. Watch.

**Following our thread:** the CPU's `sub` (and its sibling `add`) is built from a
small circuit called a **full adder** — a gadget that adds two binary digits plus
a "carry" from the previous column, exactly the way you add numbers by hand,
carrying the 1. One column looks like this:

```
        a ──┐
            ├──[ XOR ]──────────────► sum   (the digit you write down)
        b ──┘        └──[ XOR ]─► with carry-in
                                                       ┌─[ AND ]─┐
        a ──[ AND ]── b  ───────────────────────────►─┤  OR     ├─► carry-out
        carry-in ─[ AND ]─ (a XOR b) ──────────────►──┘         │   (the 1 you carry)
                                                       └─────────┘
```

Don't worry about wiring it perfectly in your head. The point is the *shape of
the claim*: **`sum` is just an XOR, `carry` is just some ANDs and an OR.** Adding
is gates. Subtracting is adding with one number flipped (a NOT plus a trick). To
add two 32-bit numbers, you chain 32 of these full adders in a row, each passing
its carry to the next — a **ripple** — and you've built the part of the CPU that
ran our `sub`.

And where does the steady rhythm come from — fetch, decode, execute, fetch,
decode, execute? A **clock**: an electrical pulse ticking billions of times a
second. Every tick, the gates settle on their answers and **registers** (built
from gates that can *hold* a value) latch the result so it's ready for the next
tick. The donut's whole animated spin is paced by that tick.

**The donut at this layer.** That one subtraction from our thread —
`sub x, r1, r2` — is now fully demystified: it's a row of full adders, made of
XOR/AND/OR gates, latching their answer on a clock tick. The donut spins because
millions of these gates flicker in lockstep, every tick, every frame.

> **The hourglass is at its narrowest here.** There is no "terminal donut" or
> "browser donut" at this depth. There is no Python or JavaScript. There is just
> a subtract, built from gates, identical no matter which face you were looking
> at. The art styles diverged at the top; down here everything has converged into
> one mechanism.

**The cliffhanger.** A gate outputs a 1 or a 0. We've been writing "1" and "0"
this whole time as if they were obvious. But a chip is a physical object. **What
*is* a 1? What is a gate physically made of?** → **L5**

> **One-breath aside.** Designing these circuits so they're fast, small, and
> correct is *digital design* and *computer architecture* — courses where you'll
> build a working CPU from gates yourself. It's less magic than it sounds, and
> more satisfying.
