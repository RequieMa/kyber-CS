---
title: "1.1 · Programming Paradigms — Ways of Organizing Ideas"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# 1.1 · Programming Paradigms — Ways of Organizing Ideas

In Part 0, we established that **all software does is hold data and reshape it
according to rules**. That's true of every program ever written. But *how* you
organize the data and the rules — that's where paradigms come in.

A **programming paradigm** is a style of organizing code. It's not a feature of
the language; it's a way of thinking. Most languages support multiple paradigms,
and most real programs mix them. The paradigms differ in one fundamental
question: **what is the relationship between data and the code that operates on it?**

## Imperative Programming — "Do this, then that"

Imperative programming is the most direct translation of how a CPU works: a
sequence of instructions executed one after another. You tell the computer
*exactly what to do, step by step*.

```python
# Imperative: explicit steps, mutable state
x = 0
for i in range(10):
    x = x + i
print(x)
```

This is the paradigm you naturally reach for first. It maps directly to the
fetch–decode–execute cycle from Part 0 L3. Every `x = x + i` becomes a `load,
add, store` triplet in the CPU. Imperative code is the thinnest abstraction over
the hardware.

**The donut connection:** our `render()` function is imperative at heart — a
nested loop walking over every point on the torus, rotating it, projecting it,
recording brightness. Step by step, just like the CPU.

## Procedural Programming — "Group these steps into a named routine"

Procedural programming is imperative programming with **functions** (procedures).
You take a sequence of steps, give it a name, and call it from elsewhere. This
lets you reuse code and manage complexity through *decomposition* — breaking a
big problem into smaller, named sub-problems.

```python
def rotate_point(x, y, angle_a, angle_b):
    """Spin a 3-D point by two angles."""
    x = x * cos(angle_a) - y * sin(angle_a)
    return x, y

# Call it thousands of times
for theta in tube:
    for phi in ring:
        x, y = rotate_point(x, y, A, B)
```

Procedural programming introduced the critical idea of **abstraction**: once
`rotate_point` works, you never think about *how* it rotates again. You just call
it. This is the same abstraction principle that runs through our entire L0–L5
tower — each layer hides its details behind a name.

## Object-Oriented Programming — "Data and the code that operates on it belong together"

OOP groups data (attributes) and the functions that operate on that data
(methods) into **objects**. An object is a self-contained bundle: it knows things
and it can do things. The outside world interacts with it through a public
**interface** — messages you send to the object — without knowing how it works
inside.

```python
class Donut:
    def __init__(self):
        self.A = 1.0       # attribute: rotation angle
        self.B = 1.0       # attribute: rotation angle

    def spin(self, dA, dB):     # method: change state
        self.A += dA
        self.B += dB

    def render(self):           # method: produce a picture
        # ... rotation math here ...
        return brightness_grid
```

Where procedural programming asks "what steps happen?", OOP asks "what **things**
exist, and what can they do?" The donut isn't a bunch of variables and functions —
it's a `Donut` object with state and behavior. This maps to how humans naturally
categorize the world (nouns and verbs), which is why OOP became the dominant
paradigm for large-scale software.

OOP is the subject of [Chapter 1.2](02-oop.md). We'll go deep there.

## Functional Programming — "Data flows through pure transformations"

Functional programming (FP) takes a different stance: **avoid mutable state**.
Instead of changing data in place, you create new data by applying pure functions
to old data. A pure function always returns the same output for the same input
and has no side effects — it doesn't modify anything outside itself.

```python
# FP style: no mutation, pure functions composed together
def rotate(state, dA, dB):
    """Return a NEW state, don't mutate the old one."""
    return {"A": state["A"] + dA, "B": state["B"] + dB}

def render(state):
    """Pure function: state in, grid out."""
    # ... rotation math ...
    return brightness_grid

# Compose them
new_state = rotate(old_state, 0.1, 0.05)
frame = render(new_state)
```

FP's big idea is that mutable state is the source of most bugs. When any part of
the program can change any variable at any time, reasoning about the program
becomes combinatorially hard. Pure functions are *referentially transparent* —
you can replace a function call with its result and the program behaves exactly
the same. This makes FP code easier to test, reason about, and parallelize.

**The donut connection:** our `brightness_grid(A, B)` function is effectively
pure! Same `(A, B)` → same grid, every time. This is why we were able to send
the same grid to three different faces — the function has no hidden dependencies.
The donut is both OOP (a `Donut` object with state) and FP (a pure `render`
function) at the same time. Paradigms are not religions; they're tools.

## Declarative Programming — "Say what you want, not how to get it"

Declarative programming is the highest level of abstraction: you describe the
*desired result*, and the system figures out *how* to achieve it. SQL is the
canonical example:

```sql
SELECT name, age FROM users WHERE age > 18 ORDER BY name;
```

You didn't tell the database *how* to filter and sort — no loops, no comparisons,
no swap operations. You declared what you want, and the query planner (a very
sophisticated piece of software) figured out the optimal strategy.

HTML, CSS, regular expressions, and configuration files are all declarative.
You're stating constraints and desired outcomes, not step-by-step procedures.

## How They Fit Together

Most real systems mix paradigms:

```
┌────────────────────────────────────────────┐
│  DECLARATIVE  │  SQL queries, HTML, config  │  ← "what"
│  FUNCTIONAL   │  Pure data transformations  │  ← "data → data"
│  OOP          │  Objects with state+methods │  ← "things"
│  PROCEDURAL   │  Named, reusable steps      │  ← "named how"
│  IMPERATIVE   │  Step-by-step instructions  │  ← "how"
└────────────────────────────────────────────┘
```

Our donut program uses all of them:
- **Imperative/procedural:** the nested `for` loops in `render()`
- **OOP:** the `Donut` class bundling state and behavior
- **Functional:** `brightness_grid()` as a pure function
- **Declarative:** the `RAMPS` lookup table — "brightness 7 maps to this character"

The paradigms aren't competing. They're complementary lenses on the same
underlying truth: **data + rules**. Each paradigm just answers differently the
question of where to put the data and how to organize the rules.

> **One-breath aside.** The fact that all paradigms eventually compile down to the
> same `load, add, store, jump` instructions (Part 0 L3) is one of the deepest
> truths in computer science. The paradigms are *for humans* — they shape how we
> think about problems. The CPU doesn't care which one you used. This is
> abstraction at the highest level: multiple ways of organizing thought, all
> collapsing into the same stream of machine instructions.
