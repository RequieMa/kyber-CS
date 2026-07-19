---
title: "L1 · Software — It's All Just Data and Rules"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L1 · Software — It's All Just Data and Rules

```
   L0  framing
 ▶ L1  SOFTWARE       ◀ you are here
   L2  software ↔ OS
   L3  instructions
   L4  digital logic
   L5  bits & physics
```

**The question carried down:** the three faces look nothing alike but spin
together. What do they *share*?

**The idea.** Here's the first big reveal, and it's true of *every* program ever
written — your browser, a video game, a bank's payroll system, the donut:

> **All software does is hold some data and reshape it according to rules.**

That's it. A browser holds the data of a web page and reshapes it into pixels. A
game holds the data of a world and reshapes it into the next frame. The donut
holds a tiny bit of data and reshapes it into a picture.

So what data does the donut hold? Almost nothing — just a few numbers:

```python
# The donut's entire "state" — everything the program needs to remember.
state = {
    "A": 1.0,   # how far it's rotated around one axis
    "B": 1.0,   # how far it's rotated around the other axis
    "pos": 50,  # where the donut sits in our shared world (0–100)
}
```

And the "rules" are a single function that turns that state into a picture. Not
into *light on a screen* — just into a grid of brightness values, pure data in,
pure data out:

```python
def render(state):
    """Turn the donut's state into a grid of brightness numbers.
       Same idea as the famous a1k0n.net 'donut math':
         1. walk around the surface of a torus (a ring)
         2. rotate every point by angles A and B
         3. project the 3-D points flat onto a 2-D grid
         4. record how much each spot faces the light
    """
    grid = new_blank_grid()
    for theta in around_the_tube():        # 1. the ring's tube
        for phi in around_the_ring():      #    the ring itself
            x, y, z = point_on_torus(theta, phi)
            x, y = rotate(x, y, state["A"], state["B"])   # 2. spin it
            sx, sy = project(x, y, z)                     # 3. flatten to screen
            grid[sy][sx] = brightness(theta, phi, state)  # 4. how lit?
    return grid          # <-- just numbers. no screen touched.
```

Read it as English, not as code: *for every point on the ring, spin it, flatten
it, and note how bright it should be.* The output is a grid of numbers like
`[[0, 0, 3, 7, 9, 7, 3, 0], …]`. **Brightness, not pixels.** Just data.

**Now — where do the three different faces come from?** This is the heart of the
whole document. The brightness grid is identical for all three. Each face only
differs in how it turns a brightness number into something visible — a tiny
lookup table called a *ramp*:

```python
TERMINAL_RAMP = " .:-=+*#%@$"          # brightness 0..10 → a character
DESKTOP_RAMP  = " ░░▒▒▓▓██"            # brightness 0..10 → a shaded block
BROWSER_RAMP  = [colors from dark→bright dots]   # brightness 0..10 → a colored dot

def paint(grid, ramp):
    for row in grid:
        for brightness in row:
            show(ramp[brightness])     # SAME grid, DIFFERENT ramp → different face
```

There's the answer to L0's mystery. The three faces share **the entire idea** —
the state and the `render` rules. They differ only in a **parameter**: which ramp
they paint with. Change one line of configuration and the terminal could look
like the browser. The idea is one thing; its appearance is a knob.

> This is *abstraction* in the flesh: "the donut" is a single idea that doesn't
> care whether it's drawn in characters, blocks, or dots.

**The donut at this layer.** We've now seen the whole donut as software: a little
state, a `render` rule, and a swappable art-style ramp. We will **freeze this
version** and never re-explain it — from here down we follow just *one thread*
through it.

**The cliffhanger.** Look again at `render`. It produced a grid of numbers and…
stopped. It never made the screen glow. `paint` called `show(...)` — but what is
`show`? A program can compute all the brightness numbers it likes, but
brightness lives in the program's own memory. **How does a number inside a
program become actual light on a physical screen?** The program, it turns out,
*cannot do that itself.* → **L2**

> **One-breath aside.** The choice of *how* to store the state — here a tiny
> dictionary, but it could be a list, a tree, a database — is the subject of
> *data structures* and *algorithms*, two of your first real courses. They ask:
> given the reshaping a program must do, what's the smartest way to hold the data?
