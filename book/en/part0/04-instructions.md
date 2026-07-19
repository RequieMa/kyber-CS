---
title: "L3 · Instructions — A Program Is a List of Tiny Commands"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L3 · Instructions — A Program Is a List of Tiny Commands

```
   L0  framing
   L1  software
   L2  software ↔ OS
 ▶ L3  INSTRUCTIONS   ◀ you are here
   L4  digital logic
   L5  bits & physics
```

**The question carried down:** the OS is also just a program. So what *is* a
running program, physically? What does "running" mean?

**The idea.** A running program is a **list of tiny instructions** that a chip
(the **CPU**) carries out one after another, mindlessly, billions per second.
Each instruction is almost insultingly simple: *add these two numbers, copy this
number over there, compare these, jump to a different spot in the list.* That's
the entire vocabulary. Everything — the donut, the OS, your browser — is built
from millions of these tiny steps.

The CPU runs them in a loop so simple it has a name, the **fetch–decode–execute
cycle**:

```
          ┌─────────────────────────────────────────────┐
          │                                               │
          ▼                                               │
   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐  │
   │  1. FETCH    │──►│ 2. DECODE    │──►│ 3. EXECUTE    │──┘
   │ get the next │   │ what kind of │   │ actually do  │
   │ instruction  │   │ command is   │   │ it (add,     │
   │ from memory  │   │ this?        │   │ copy, jump)  │
   └─────────────┘   └─────────────┘   └──────────────┘
        (… and repeat, billions of times per second …)
```

That loop is the heartbeat of every computer that has ever existed.

**Now we follow our single thread down.** Back in L1, the donut's `render`
function spun each point with a line of rotation math. Let's grab **one line** of
it — just one — and never let go:

```python
x = x * cosA - y * sinA      # ← THE thread. we follow this line to the bottom.
```

To you, that's one line. To the CPU, even this is too big — it must be broken into
several instructions. Here it is in **assembly**, which is the human-readable name
for the CPU's actual instructions (don't memorize it — just feel the *grain*):

```asm
    mul   r1, x, cosA      ; r1 = x * cosA       (a multiply)
    mul   r2, y, sinA      ; r2 = y * sinA       (another multiply)
    sub   x,  r1, r2       ; x  = r1 - r2        (a subtract)
```

Three instructions for one line of math. The `r1`, `r2` are **registers** — a
handful of tiny slots inside the CPU where it keeps the numbers it's working on
*right now*. The CPU fetches `mul`, decodes "ah, a multiply," executes it; then
the next; then the next. Spin the donut one frame and the CPU runs this little
trio thousands of times.

> **The two languages converge here.** Our donut is written in Python for the
> terminal and desktop, and in JavaScript for the browser — two languages that
> look quite different on the page. But that same rotation line, in *either*
> language, comes down to the same kind of `mul, mul, sub`. The high-level
> language is for *humans*; underneath, it collapses to the CPU's tiny vocabulary.
> This is the hourglass beginning to pinch: **the three faces and even the two
> languages are starting to look the same down here.**

**The donut at this layer.** The donut's smooth spinning is revealed to be the
fetch–decode–execute loop grinding through `mul, mul, sub` (and thousands of
friends) every single frame. The animation *is* the cycle, made visible.

**The cliffhanger.** The CPU "executes" `sub` — it subtracts. But the CPU is a
sliver of silicon with no fingers and no idea what a number is. **How does a piece
of silicon actually subtract two numbers?** → **L4**

> **One-breath aside.** Turning your readable `x = x*cosA - y*sinA` into those
> `mul/mul/sub` instructions is the job of a *compiler* (or, for Python/JS, an
> *interpreter*) — and how to do that well is its own deep course. *Theory of
> computation* sits near here too, asking the grand question: what can *any* list
> of instructions possibly compute, and what can it never compute?
