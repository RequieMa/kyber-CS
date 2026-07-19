---
title: "L2 · Software ↔ OS — Programs Don't Touch Hardware; They Ask"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L2 · Software ↔ OS — Programs Don't Touch Hardware; They Ask

```
   L0  framing
   L1  software
 ▶ L2  SOFTWARE ↔ OS  ◀ you are here
   L3  instructions
   L4  digital logic
   L5  bits & physics
```

**The question carried down:** the program computed a grid of brightness numbers
but never lit the screen. How does a number become light?

**The idea.** Here is a fact that surprises almost everyone: **your program is
not allowed to touch the hardware.** It cannot poke the screen, the disk, the
network card, or the keyboard directly. That would be chaos — every program
fighting over the same screen, the same disk.

Instead there is one special program, always running, that owns all the
hardware: the **operating system** (the OS — Windows, macOS, Linux). Every other
program is a guest. When a guest wants something physical to happen, it must
**ask the OS**. That request is called a **system call**.

```
        YOUR PROGRAM (a guest)              THE OS (owns the hardware)
        ─────────────────────               ──────────────────────────
   "here's a grid, please draw it"  ──────►  receives the request ("write")
                                                     │
                                                     ▼
                                              actually drives the screen ───► 💡 light
   ◄──────────────────────────────────────  "done"
```

The program lives in a kind of sandbox. The only doors out of the sandbox are
system calls. Drawing to the screen, reading a key press, opening a file, sending
a network packet — **every** one of those is the program politely asking the OS,
because only the OS is allowed to move the actual hardware.

**The donut at this layer.** Remember our backend-and-three-faces picture? Now we
can see what the arrows in it really are — they are conversations with the OS:

```
   ┌──────────────────────────────────────────────────────────────┐
   │  BACKEND          render(state) → grid of brightness numbers    │
   └──────────────────────────────────────────────────────────────┘
        │ "draw this"            │ "draw this"          │ "draw this"
        ▼                        ▼                      ▼
   ┌──────────┐            ┌──────────┐           ┌──────────┐
   │ TERMINAL │            │ DESKTOP  │           │ BROWSER  │
   └────┬─────┘            └────┬─────┘           └────┬─────┘
        │ write() syscall       │ window-draw syscall  │ canvas-draw syscall
        ▼                        ▼                      ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   THE OPERATING SYSTEM   — the only one that touches the glass  │
   └──────────────────────────────────────────────────────────────┘
        ▲
        │  ← keyboard / mouse events flow UP the same way
   you press →  OS catches it  →  routes it to the focused window  →  backend
```

Two directions, both through the OS:

- **Output (down):** the terminal face turns its character grid into a single
  `write` system call — "OS, please put these characters on screen." The desktop
  and browser faces make their own equivalent draw requests. The backend computed
  the *idea*; the OS performs the *act*.
- **Input (up):** when you press **→**, you are not pressing a key "in" any
  program. The keypress is an electrical event the **OS** catches first. The OS
  decides which window is focused and hands the event to that window, which passes
  it to the backend — which nudges `state["A"]` and the spin speeds up. Then a new
  picture flows back down.

This is why all three faces stay in sync: there is one backend holding the one
true state, and the OS is the switchboard routing every input to it and every
output from it.

> Notice the terminal isn't "blind" or second-class. The backend knows the
> terminal's size (rows × columns) and font, so it computes the *entire* frame —
> every glyph **and** every blank space — and hands the OS the whole thing to
> flush. The terminal is a surface the backend paints, just like the others. Same
> idea, different units.

**The cliffhanger.** We keep saying "the OS does the real work." But the OS is not
magic — **the OS is itself just a program**, a very privileged one. When the OS
"drives the screen," it too is just running instructions on the same chip. So our
question sharpens and points straight down: when *any* program runs — yours or the
OS — what is it physically *doing*? What is a running program, underneath? → **L3**

> **One-breath aside.** When the browser face asks for a web page, that request
> leaves your machine entirely and travels to another computer. The rules for that
> conversation — *networking* — are just a bigger version of the same "ask
> someone else to do the work" idea. And the OS's trick of running many programs
> in their own sandboxes at once is the heart of an *operating systems* course.
