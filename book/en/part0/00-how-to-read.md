---
title: How to Read This Book
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# How to Read This Book

You are about to start studying computer science. Before the formal courses
arrive — with their separate names like *algorithms*, *operating systems*,
*architecture* — this book hands you the **map** they all live on.

The map has one shape: a **descent**. We start at the top, inside software you
already use every day, and we keep asking the same stubborn question:

> *"Okay… but how does **that** actually happen?"*

Every answer reveals a layer underneath. We follow the question all the way
down — from a spinning shape on your screen to the electrons in a chip — and then
climb back up once to see the whole thing at a glance.

## The One Big Idea

> **Software is abstracted ideas. Hardware is the faithful mirror of instructions.**

Everything in this book is one long demonstration of that single sentence.

## How to Use This Book

- **No programming experience is assumed.** If you're comfortable with high
  school algebra (sines, cosines, a little geometry), you have enough.
- **Part 0 is the map.** Read it in one sitting (~30 minutes). It walks the full
  stack from idea to electrons, using a single running example. Everything in
  Parts 1–3 is an expansion of something you first meet here.
- **The code is optional.** Snippets are there to make ideas concrete. Read them
  if they help; skim them if they don't. Nothing later depends on you running
  them — but a companion repository (TBD) lets you run the spinning donut yourself.
- **Each chapter stands on the one before it.** The descent is cumulative. If you
  skip ahead, you'll miss the question the current chapter is answering.

## One Example Carries the Whole Journey

Here is a small program you can picture clearly. It draws a **spinning donut** —
a 3-D torus, rotating in space, shaded so it looks solid:

```
                  $$@@@@@@
              $$@@@@%%%%%%%%@@
           ##@@%%%%++++++++%%%%@
          #@@%%++++======++++%%@@
         #@%%++===---------==++%%@
         #@%++==---::::::---==++%@#
         #@%++==--:::  :::--==++%@#
          @%%++==--:::::--==+++%@#
          #@@%%++====----===++%%@#
            @@%%%%++++++++%%%%@@
              @@@@%%%%%%%%@@@$
                  @@@@@@$$
```

Now the twist that makes it our perfect guide. We run this donut on **three
completely different screens at the same time**:

```
   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
   │   TERMINAL       │   │   DESKTOP WINDOW │   │   BROWSER TAB    │
   │   (text only)    │   │   (a real app)   │   │   (a web page)   │
   │                  │   │                  │   │                  │
   │   $$@@@@@@        │   │   ░▒▓██▓▒░       │   │   ●●◐◐○○· ·      │
   │  @@%%++==%%@      │   │  ▒▓███████▓      │   │  ◐○· · · ·○◐     │
   │  @%++--::--+%@    │   │  ▓████████▓▒     │   │  ○· glowing ·○   │
   │   @%%++==%%@      │   │   ░▒▓██▓▒░       │   │   ●◐○· ·○◐●      │
   │                  │   │                  │   │                  │
   │  ← ASCII glyphs   │   │  ← shaded blocks │   │  ← colored dots  │
   └─────────────────┘   └─────────────────┘   └─────────────────┘
        face #1                face #2               face #3
```

Three windows that look **nothing alike**. One is made of typewriter characters,
one of shaded blocks, one of glowing colored dots. You can press **← / →** to
spin the donut faster or slower, or drag it with the mouse — and all three react
together, perfectly in sync.

And here is the arrangement we'll keep coming back to. There is **one brain**
behind the three faces:

```
        ┌───────────────────────────────────────────────┐
        │   THE BACKEND  (one program, the "brain")       │
        │                                                 │
        │   • THE donut math — ONE copy, ONE idea         │
        │   • the donut's state: position + spin angles   │
        │   • listens to ALL your input (keys, mouse)     │
        │   • tells each face exactly what to show        │
        └───────────────────────────────────────────────┘
              │  "here is the picture"     │      │
              ▼                            ▼      ▼
       ┌────────────┐          ┌────────────┐  ┌────────────┐
       │  TERMINAL  │          │  DESKTOP   │  │  BROWSER   │
       │  draws it  │          │  draws it  │  │  draws it  │
       │  as text   │          │ as blocks  │  │  as dots   │
       └────────────┘          └────────────┘  └────────────┘
```

The backend owns the **idea**. Each face owns only its **art style**.

That picture is going to explain all of computer science to you. Keep it in mind.
**Our driving question:** these three windows look nothing alike — so *what could
they possibly share?*

Let's descend.
