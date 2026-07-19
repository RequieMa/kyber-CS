---
title: "L5 · Bits & Physics — A 1 Is a Voltage; a Gate Is a Switch"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L5 · Bits & Physics — A 1 Is a Voltage; a Gate Is a Switch

```
   L0  framing
   L1  software
   L2  software ↔ OS
   L3  instructions
   L4  digital logic
 ▶ L5  BITS & PHYSICS ◀ you are here  (the floor)
```

**The question carried down:** what *is* a 1, physically? What is a gate made of?

**The idea — and the floor.** We've reached the bottom. Underneath the gates
there is no more computer science, only physics. And it turns out the answer is
almost comically humble:

> **A 1 is a high voltage. A 0 is a low voltage.** That's all a bit is — whether
> a certain wire is electrically "high" or "low" right now.

And a gate? A gate is built from **transistors**, and a transistor is just a tiny
electrically-controlled **switch**:

```
        a transistor = a switch operated by electricity

            control ("gate")
                  │
                  ▼
        in ───────●───────► out
                  │
        when control is HIGH (a "1"):  the switch is CLOSED → current flows → out is 1
        when control is LOW  (a "0"):  the switch is OPEN   → no current   → out is 0
```

That is the entire foundation. Wire a few switches together so that current only
gets through when *both* controls are high, and you've built an AND gate. A few
more switches make OR, NOT, XOR. Stack those into adders (L4). Stack adders into a
CPU (L3). Let the CPU run instructions (L3). Wrap the privileged ones in an OS
(L2). Let programs ask the OS (L2). Let a program reshape data (L1). And the data
it reshapes can be a spinning donut (L0).

**The donut at this layer.** Follow our thread to its very end. That one result
bit of our subtraction — the top bit of `x` after `sub x, r1, r2` — is, at this
instant, **a voltage on a wire** inside the chip, held high or low by a few
transistors switching. Multiply that by millions of bits, and the result is a
grid of brightness numbers. That grid becomes a request to the OS, which sets the
voltages driving your screen's pixels (or the dots that form a character's shape),
and those pixels emit **photons** — actual light — that land in your eye as a
spinning donut.

```
   one transistor switching
         │
         ▼  (a few of them)
   a logic gate                ← L5/L4 boundary: physics becomes logic
         │
         ▼  (chained)
   an adder → the `sub`        ← L4/L3
         │
         ▼  (millions, on a clock)
   the CPU running instructions ← L3
         │
         ▼  (one privileged program among many)
   the OS serving requests     ← L2
         │
         ▼  (a guest asking)
   your program reshaping data ← L1
         │
         ▼
   a donut, spinning, in light ← L0
```

Physics doesn't know about donuts. It only holds voltages, faithfully, exactly as
the instructions demand. The meaning — "this is a donut" — lives entirely in the
layers above. **The hardware is a perfect, mindless mirror.**

We've hit the floor. Now let's climb back up and see what we built.
