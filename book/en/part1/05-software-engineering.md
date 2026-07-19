---
title: "1.5 · Software Engineering — The Craft Beyond the Code"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# 1.5 · Software Engineering — The Craft Beyond the Code

Writing code that works — once, on your machine, while you're watching — is easy.
Writing code that works correctly, stays working as the system grows, and can be
understood and modified by other people (including your future self) — that's
**software engineering**. It's the difference between a shed and a skyscraper.

## Why "Just Writing Code" Isn't Enough

In 1975, Frederick Brooks published *The Mythical Man-Month*, a book based on his
experience managing IBM's OS/360 — a project that consumed 5,000 person-years and
became known as "the most terrifying software development project in history."
His central observation:

> Adding more programmers to a late project makes it later.

Why? Because programmers don't just write code — they communicate, coordinate,
review, test, debug, and integrate. The overhead of coordination grows faster
than the work each additional person contributes. A team of 10 isn't 10× faster
than one person; it might be 3× faster, at 20× the communication cost.

Brooks' insight is that **the hard part of software isn't writing code. It's
managing complexity across time, people, and changing requirements.**

## Testing — Proving It Works

Testing is not debugging. **Debugging** is finding and fixing a known problem.
**Testing** is systematically searching for unknown problems before they reach
users. This distinction, first made by Glenford Myers in 1979, turned testing
into a discipline.

### Levels of Testing

| Level | What it tests | Example from the donut |
|---|---|---|
| **Unit test** | A single function or class in isolation | `test that brightness_grid(0,0) returns a non-empty grid` |
| **Integration test** | Multiple units working together | `test that DesktopFace.run() calls backend.present()` |
| **End-to-end test** | The whole system, as a user would use it | `launch donut, press →, verify all three faces spin faster` |

The donut demo has 29 unit tests. They verify that `brightness_grid()` produces
correct values, that the `Frame` class enforces bounds, that `FakeBackend` records
frames correctly, and that the `DesktopFace` pipeline calls the backend in the
right order. These tests run in under a second and catch regressions before they
reach human eyes.

### Why Tests Matter for You

When you're learning, tests serve a different purpose: they let you experiment
without fear. Change the rotation math, run the tests — if they pass, you haven't
broken the donut. Tests are a safety net that makes refactoring (improving code
without changing behavior) possible.

## Version Control — The Undo Button for Code

**Git** (created by Linus Torvalds in 2005 for Linux kernel development) is the
universal tool for tracking changes to code. Every change is a **commit** — a
snapshot of the entire project at a point in time, with a message explaining why.

Key concepts:
- **Repository:** the project's complete history, stored locally
- **Commit:** a saved snapshot with a message
- **Branch:** a parallel timeline of changes. Work on a feature without affecting
  the main codebase.
- **Merge:** bring changes from one branch into another
- **Remote:** a copy of the repository on another machine (GitHub, GitLab)

The killer feature of Git isn't storing code — it's enabling collaboration.
Multiple people can work on different features in parallel branches, and Git
provides the tools to merge their work together, detect conflicts, and trace
every line of code back to who wrote it and why.

## Debugging — The Art of Finding Why

Debugging is the systematic process of:
1. **Reproduce** the bug consistently
2. **Isolate** the minimal conditions that trigger it
3. **Identify** the root cause (not just the symptom)
4. **Fix** the cause
5. **Verify** the fix doesn't break anything else

The most powerful debugging tool is the scientific method: form a hypothesis
about what's wrong, design a test that would confirm or refute it, run the test,
repeat. Print statements and debuggers are just ways of gathering evidence.

The donut's Win32 backend development (documented in the companion repo's
Plan.md) is a debugging case study: two 64-bit pointer truncation bugs that only
appeared on real Windows hardware. The fix was explicit ctypes `argtypes`/`restype`
declarations. The debugging process: reproduce on Windows, isolate to the
WNDPROC callback, identify the `c_long` vs `c_ssize_t` mismatch, fix, verify
with the pipeline smoke test.

## The Development Lifecycle

Software isn't built in one pass. Modern development follows an iterative cycle:

```
   ┌──────────────────────────────────────┐
   │                                      │
   ▼                                      │
  Plan  ──►  Code  ──►  Test  ──►  Deploy ──┘
                       ▲          │
                       └──────────┘
                       (if tests fail)
```

**Continuous Integration (CI)** automates this: every time you push code, a CI
server checks out the latest version, runs the full test suite, and reports the
results. If tests fail, the team is notified immediately. This prevents the
"works on my machine" problem and catches integration issues early.

**Continuous Deployment (CD)** extends CI: if tests pass, the code is
automatically deployed to production. This reduces the time between writing code
and users benefiting from it from weeks to minutes.

## Communication — The Real Hard Problem

Brooks identified two kinds of complexity in software:
- **Essential complexity:** inherent to the problem itself. You can't make a
  donut renderer simpler than the rotation math requires.
- **Accidental complexity:** created by the way we build software. Bad interfaces,
  poor documentation, tangled dependencies.

Most of software engineering is fighting accidental complexity. The tools (tests,
version control, CI/CD, design patterns) are weapons in that fight. But the most
important skill is **communication**: writing clear commit messages, documenting
*why* a decision was made (not just what the code does), and designing interfaces
that make the right thing easy and the wrong thing hard.

> **One-breath aside.** Brooks' *The Mythical Man-Month* is still in print 50
> years later for a reason. Its observations about team dynamics, estimation, and
> the nature of software complexity haven't aged. If you read one book about
> software engineering that isn't about code, make it that one.

## Connecting Back to the Donut

The donut demo is small enough to be understood in an afternoon. But it
demonstrates software engineering principles in miniature:

- **Testing:** 29 unit tests covering the pure pipeline, fake backend, and
  factory logic. The Win32 backend has smoke tests that run on real Windows.
- **Version control:** every checkpoint in the desktop face's development is
  documented in `Plan.md` with `[x]` markers.
- **Interface design:** the four-verb `PlatformBackend` API is a study in
  minimalism. It's exactly the boundary that testing and portability need, and
  nothing more.
- **Separation of concerns:** the face doesn't know about the OS, the backend
  doesn't know about the donut, the factory is the only place that knows about
  platforms.

These aren't just academic principles. They're why the donut works on three
different screens, on three different operating systems, in two different
languages, with a test suite that runs in under a second. Good engineering is
what makes complexity manageable.
