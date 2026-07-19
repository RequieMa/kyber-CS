---
title: "Appendix B · The Donut Code Walkthrough"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# Appendix B · The Donut Code Walkthrough

> **Companion repository:** The spinning donut demo lives in a separate repo (TBD).
> Clone it and follow along. This appendix is a guided tour of the code — what each
> file does, how the three faces work, and where each piece sits on our L0–L5 map.

## Architecture at a Glance

```
demo/
├── donut_core.py          ← THE idea. Pure math, zero OS dependencies.
├── face_terminal.py        ← Terminal face: ASCII art via curses
├── face_desktop.py         ← Desktop face: launches the native window
├── desktop/                ← The Bridge pattern in action
│   ├── backend.py          ← Neutral currency (Frame, Event) + PlatformBackend ABC
│   ├── face.py             ← DesktopFace pipeline (pure software, no OS conditions!)
│   ├── backend_factory.py  ← The ONE spot that knows about platforms
│   └── backends/
│       ├── win32.py        ← Windows: talks to user32/gdi32 via ctypes
│       ├── cocoa.py        ← macOS stub (NotImplementedError → spec doc)
│       ├── x11.py          ← Linux stub (NotImplementedError → spec doc)
│       └── fake.py         ← FakeBackend for testing (no window needed)
└── web/
    └── donut.html          ← Browser face: re-implements donut_core in JavaScript
```

## The Core: `donut_core.py`

This is the single source of truth. Everything the donut IS lives here — and
nowhere else. Two pure functions:

```python
def brightness_grid(A: float, B: float, width: int, height: int) -> list[list[int]]:
    """Spin a torus by angles A, B; project to 2-D; return a grid of brightness values 0..11.
       Pure function: same (A,B,width,height) → same grid, every time. No side effects."""
    ...

def render_text(grid, ramp):
    """Turn a brightness grid into a string, using the given ramp."""
    ...
```

This is **L1 in code**: the idea is data (A, B, the grid) reshaped by rules
(rotation, projection, brightness). No screen, no OS, no window. Just math.

The `RAMPS` table at the bottom is the "art style knob" from Part 0:

```python
RAMPS = {
    "terminal": " .:-=+*#%@$",
    "desktop":  " ░░▒▒▓▓██",
    "browser":  [...],  # colors, not characters
}
```

## The Three Faces

### Terminal Face (`face_terminal.py`)

- Uses Python's `curses` library to draw directly in the terminal
- Calls `donut_core.brightness_grid()` → `render_text()` → writes the string to the terminal
- The system call: `curses` eventually calls `write()` — the OS puts characters on screen
- **L2 boundary:** the terminal face doesn't know it's asking the OS. `curses` hides that.

### Desktop Face (`face_desktop.py` + `desktop/`)

This is the teaching centerpiece for the **software/OS boundary** (L2).

The Bridge pattern separates what is *said* from how it is *done*:

- **`backend.py`** defines the neutral currency:
  - `Frame`: a grid of `Cell(glyph, color)` — what the face wants to show
  - `Event`: `QUIT`, `SPIN_UP`, `SPIN_DOWN` — what the user did
  - `PlatformBackend(ABC)`: exactly **four verbs** — `create_window`, `present`, `poll_events`, `destroy`
- **`face.py`** is `DesktopFace` — the entire rendering pipeline as pure software.
  There is deliberately NO `sys.platform` or OS conditional here. The face only
  speaks the neutral currency. The backend injection is the *only* door to the OS.
- **`backend_factory.py`** is the one spot that knows about platforms —
  `sys.platform == 'win32'` → `Win32Backend`, etc.
- **`backends/win32.py`** is the real implementation. It talks to Windows'
  user32.dll and gdi32.dll via Python's `ctypes`. `create_window` registers a
  window class and creates a native Win32 window. `present` iterates over the
  Frame's cells and calls GDI `SetTextColor`/`TextOutW` for each one. `poll_events`
  runs the Windows message pump (`PeekMessageW`) and translates `VK_LEFT`/`VK_RIGHT`
  into `SPIN_UP`/`SPIN_DOWN` events. All Win32 handles are acquired lazily (inside
  the verbs, not at module level) so the module imports cleanly on Linux for testing.

This is **L2 made physical**: the donut's idea (a grid of cells) crosses the OS
boundary through exactly four doors. Changing the backend changes *how* the OS is
asked, without changing the idea at all.

### Browser Face (`web/donut.html`)

- Re-implements `brightness_grid()` line-for-line in JavaScript
- Draws to an HTML `<canvas>` element
- The "system call" is the browser's Canvas API — which the browser translates
  into OS draw calls
- The deliberate teaching point: same math, different language, same result.
  Python and JavaScript diverge at L1, converge at L3 (`mul, mul, sub`).

## Mapping Code to Layers

| Code location | Layer | Why |
|---|---|---|
| `donut_core.py` | L1 | Pure idea: data + rules. No hardware. |
| `RAMPS` table | L1 | The "art style knob" — abstraction in code |
| `face_terminal.py` | L1→L2 | Translates idea → `write()` syscall (via curses) |
| `desktop/backend.py` | L2 | The OS boundary, shaped as an interface |
| `desktop/face.py` | L1→L2 | Pure software pipeline, injected with an OS door |
| `desktop/backends/win32.py` | L2 | Concrete OS conversation (GDI, user32) |
| `web/donut.html` | L1→L2 | Same idea, different language, same L2 boundary |
| *(Not in this repo)* | L3 | The CPU running `mul, mul, sub` |
| *(Not in this repo)* | L4 | The gates that build the adder |
| *(Not in this repo)* | L5 | The transistors switching the voltages |

## Running It

```bash
# Clone the companion repo (TBD)
git clone <donut-demo-repo-url>
cd donut-demo

# Terminal face
uv run python demo/face_terminal.py

# Desktop face (auto-selects backend for your OS)
uv run python -m demo.desktop

# Browser face — just open in a browser
open demo/web/donut.html
```

## The Point

This codebase exists to make the book's thesis *runnable*. You can set breakpoints
at the `present()` call, at the `write()` syscall, at the `brightness_grid()` pure
function, and watch the donut's journey through every layer. The code is small
enough to read in an afternoon, and every design decision (the Bridge pattern, the
four-verb backend interface, the lazy Win32 imports) exists to *teach* something
about the layer boundary it sits on.

> *The code is not the donut. The code is the donut's idea, waiting for a faithful
> mirror to make it spin.*
