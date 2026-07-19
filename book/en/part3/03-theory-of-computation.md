---
title: Theory of Computation — What Can Be Computed at All?
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# Theory of Computation — What Can Be Computed at All?

```
    L0  framing                     ▲  "a donut"
    L1  software                    │  reshaping data
    L2  software ↔ OS               │  by asking the OS
    L3  instructions                │  which runs tiny commands
    L3  DEEP: ARCHITECTURE          │  how the CPU is built to run them
    L4  digital logic               │  built from gates
  ▶ THEORY OF COMPUTATION           │  what computation even IS
    L5  bits & physics              │  made of switching voltages
                                    └─── a new layer: the mathematical ceiling
```

**The question behind all questions:** We've descended through the stack and
seen every layer: the program, the OS, the CPU, the gates, the transistors. But
there's a layer *above* even the hardware, yet *underneath* everything: the
mathematical layer. What *is* computation, fundamentally? Not "how does this
specific chip do it," but "what can ANY possible computing system do?" And the
answer is both awe-inspiring and sobering.

**The idea.** Computer science has a hidden ceiling. Above it, some problems
exist that no computer — no matter how fast, no matter how much memory, no
matter how cleverly designed — can ever solve. And below it, even among the
problems that *can* be solved, some are so expensive that they might as well be
impossible.

This chapter is a guided tour of that ceiling.

## Turing Machines — The Simplest Possible Computer

In 1936, Alan Turing was thinking about the same question we're asking: "What
is computation?" He invented a model so simple it seems almost silly. It's
called the **Turing machine**, and it has exactly these parts:

1. An **infinite tape**, divided into cells. Each cell holds one symbol (say,
   a 0 or a 1, or a blank).
2. A **head** that can read the symbol under it, write a new symbol, and move
   left or right one cell.
3. A **state machine** — a small set of states and a table of rules: "If you're
   in state A and reading a 1, write a 0, move right, and enter state B."

That's it. The entire machine. A tape, a head, and a few rules.

And here is the claim:

> **Anything that can be computed at all — in any programming language, on any
> hardware, in any universe with any physics — can be computed by this absurdly
> simple tape-and-head machine.**

That claim, the **Church-Turing thesis**, is the foundational belief of
computer science. It has never been disproven. Every programming language ever
invented — Python, C, JavaScript, Lisp, even the weird esoteric ones — is
*Turing-complete*, meaning it can simulate any Turing machine. And a Turing
machine can simulate any of them.

```
  ┌───────────────────────────────────────────────────────┐
  │                     THE TAPE                          │
  │  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐     │
  │  │ 1 │ 0 │ 1 │ 1 │ 0 │ 1 │ 0 │ 0 │ 1 │ 0 │   │ …  │
  │  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘     │
  │         ▲                                             │
  │         │                                             │
  │       HEAD                                           │
  │    ┌──────┐                                           │
  │    │ read, │  "if state = 4 and symbol = 0:           │
  │    │ write,│   write 1, move right, state = 7"        │
  │    │ move  │                                          │
  │    └──────┘                                          │
  │         │                                             │
  │    ┌────▼─────┐          ┌───────────────────────┐   │
  │    │  STATES  │  ───►    │  TRANSITION TABLE     │   │
  │    │  0..n    │          │  if state 3, see 1 →   │   │
  │    └──────────┘          └───────────────────────┘   │
  └───────────────────────────────────────────────────────┘
```

**The donut at this layer.** The donut's `render()` function computes a grid of
brightness values. By the Church-Turing thesis, a Turing machine could compute
this same grid. It would, of course, be agonizingly slow — the Turing machine
moves one cell at a time along an imaginary tape, while your laptop's CPU
operates on entire 64-bit words in a single cycle. But the *output* would be
exactly the same. The donut's math (the rotation using sin and cos) is
computable to arbitrary precision — you can approximate the trig functions to
as many decimal places as you like, given enough tape. The CPU is just an
*impossibly fast* Turing machine.

This is the heart of abstraction: the idea of the donut exists in the
mathematical layer, independent of the hardware. The Turing machine proves it;
the CPU realizes it.

> **One-breath aside.** Is every possible machine equivalent to a Turing
> machine? Probably. But the question isn't settled for *quantum computers*.
> Quantum computation might solve certain problems faster than any Turing
> machine could (not different problems — same problems, faster). Whether this
> means quantum computers are "more powerful" in principle, or just faster, is
> an open question in quantum complexity theory. Most researchers suspect the
> latter: quantum computers probably don't expand the *set* of solvable
> problems, just the *speed* of solving some of them.

## Finite State Machines — The Simplest Model

Before the Turing machine, there's an even simpler model: the **finite state
machine (FSM)**. It has states and transitions, like the Turing machine's
control unit, but *no tape* — no memory of the past beyond the current state.

An FSM is the computational model of a traffic light, a vending machine, a
simple text parser, or a regular expression. It reads input symbols one at a
time and changes state based on them. It cannot "remember" things that require
arbitrary storage.

```
            ┌───────────────────────┐
            │                       │
            │     READING "1"       │◄──── read 0 ─────┐
            │     (counting odd)    │                   │
            │                       ├── read 1 ────┐   │
            └───────────────────────┘              │   │
                    │                              │   │
                    │ read 0                        │   │
                    │                              │   │
                    ▼                              │   │
            ┌───────────────────────┐              │   │
            │                       │◄─────────────┘   │
            │     READING "0"       ├── read 1 ────────┘
            │     (counting even)   │
            │                       │
            └───────────────────────┘
```

This FSM toggles between "even" and "odd" every time it reads a 1. Feed it a
binary string, and its final state tells you whether the number of 1s is even
or odd. That's all it can do — it has *no memory* of the specific sequence, only
of the parity.

FSMs are fundamental because they appear everywhere: in digital circuits
(coordinating when to fetch vs. decode), in network protocols (three-way
handshake: SYN, SYN-ACK, ACK), in compilers (recognizing keywords in your
source code). And they're the foundation of **regular expressions**, which are
just text patterns that an FSM can recognize.

**The donut at this layer.** The control unit of the CPU that runs the donut is
a finite state machine. Its states are "fetch," "decode," "execute." The input
is the clock tick. On each tick, it transitions: fetch → decode → execute →
fetch. That three-state FSM, repeated billions of times, is what drives every
instruction the donut executes.

## Decidability — The First Ceiling

Now we get to the unsettling part. Turing proved that some problems are
mathematically uncomputable — a Turing machine (and therefore any computer)
cannot solve them, no matter how much time or tape you give it.

The most famous example is the **Halting Problem**: given a description of any
program and its input, determine whether that program will *eventually stop*
(halts) or run *forever* (loops).

Imagine you wrote a Python program:

```python
while True:
    pass  # this loop runs forever
```

It's obvious to a human that this never halts. But now consider:

```python
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
```

(This is the Collatz conjecture: nobody knows whether this loop always
eventually reaches 1 for any input.)

A "halting-checker" program would need to decide, for *any* program and input,
whether it halts. Turing proved this is impossible. His proof is a masterpiece
of self-reference: if such a checker existed, you could feed it a program that
does the opposite of what the checker predicts, creating a paradox. (Like a
barber who shaves everyone who doesn't shave themselves — who shaves the
barber?)

The practical implication: **there is no general-purpose bug-finding tool.**
No tool can automatically determine whether any program has an infinite loop,
or crashes for some input, or is correct for all inputs. Some of these questions
are provably undecidable. That's not a limit on current tools — it's a limit on
computation itself.

**The donut at this layer.** The donut's render loop is trivially halting:
it iterates over a finite grid of points, computes, and terminates. But a
more ambitious donut — one that *generated* infinite procedural patterns
forever, streaming new frames indefinitely — would be a program whose halting
behavior is interesting: it *shouldn't* halt, by design, because it's an
animation. A halting-checker would say "this program loops forever" and that
would be *correct*. The undecidability of the Halting Problem isn't about
confusion — it's about the impossibility of a general algorithm that gets the
right answer for *all* programs.

> **One-breath aside.** The Halting Problem proof is the most important
> negative result in computer science, but undecidability is everywhere.
> Hilbert's tenth problem (is there an algorithm to determine whether any
> Diophantine equation has integer solutions?), the equivalence problem for
> context-free grammars (do two grammars generate the same language?), and
> Post's correspondence problem are all undecidable. The set of undecidable
> problems is infinite and far larger than the set of decidable ones. Most
> statements about programs — "is this correct?" "will this crash?" — are
> undecidable in general.

## P vs NP — The Second Ceiling

The Halting Problem is about problems that can't be solved *at all*. But there's
a different boundary: problems that can be solved *in principle* but might take
*unimaginably long*.

A problem is in **P** (polynomial time) if it can be solved in a reasonable
amount of time — the runtime grows as `n`, `n^2`, or `n^3` with the problem
size. Sorting a list, finding the shortest path on a map, and doing arithmetic
are all in P.

A problem is in **NP** (nondeterministic polynomial time) if a proposed solution
can be *checked* quickly, even though finding the solution might be hard. The
archetype is the **traveling salesman**: given a list of cities, find the
shortest route that visits each exactly once. Nobody knows how to solve this
for 100 cities without checking an astronomical number of routes — but if you
hand me a route, I can quickly verify "yep, that visits all cities" and tell you
its length.

The big open question — the P vs NP problem — is:

> Is every problem whose solution can be checked quickly (NP) also solvable
> quickly (P)?

Or, more bluntly: **Is finding as easy as verifying?**

Most computer scientists believe the answer is NO: there are problems that are
genuinely hard to solve but easy to check. But nobody has *proven* it. The Clay
Mathematics Institute has offered a $1 million prize for the proof, and it's
one of the seven Millennium Prize Problems. If P = NP (finding is as easy as
checking), encryption as we know it would collapse, drug discovery would be
trivial, and many logistical nightmares would vanish. If P ≠ NP (finding is
harder), we need to accept that some important problems will always need clever
approximation, not exact solution.

**The donut at this layer.** The donut's render is in P — it takes O(n) time
where n is the number of grid points. The rotation math (multiply, subtract) is
constant-time per point. So the donut runs in linear time, easily. But now
imagine a different problem: "Find the optimal arrangement of 10,000 donuts on
a conveyor belt to minimize manufacturing time." That sounds like an NP-hard
problem. You could quickly check an arrangement someone gives you (NP), but
finding the optimal one might be intractable. The donut's physics is easy. The
donut factory's logistics might be impossible.

## P, NP, and the Art of Reduction

One of the most important ideas in complexity theory is **reduction**: showing
that problem A can be transformed into problem B, so that solving B gives you
the answer to A for free. If you can reduce A to B, and B is "easy" (in P),
then A is also easy. Conversely, if A is "hard" (NP-complete), and A reduces to
B, then B is at least as hard as A.

The set of **NP-complete** problems is the most famous class in all of computer
science. They are the hardest problems in NP: if you find a polynomial-time
solution to *any one* of them, you've proven P = NP. They include:

- **SAT (Boolean satisfiability):** given a logical formula with AND/OR/NOT,
  is there an assignment of true/false to the variables that makes it true?
- **Traveling salesman:** find the shortest route visiting all cities.
- **Graph coloring:** can you color a map with k colors so no two adjacent
  regions share a color?
- **Knapsack:** given items with weights and values, what's the most valuable
  set that fits in a fixed-capacity bag?

These problems look different, but they're secretly the same hardness. You can
reduce SAT to traveling salesman, and traveling salesman to graph coloring. The
entire NP-complete family is connected through reductions.

**The donut at this layer.** The donut's rendering is easy (linear time). But
if the donut suddenly had to *decide* something NP-complete — like finding the
optimal set of 5000 points on the torus to minimize shading artifacts — it
would stall. That problem might be NP-complete, solvable only by exhaustively
checking an exponential number of subsets. The donut would freeze, hung on an
impossible computation. This is the boundary between what a CPU can do
practically, vs. what it can do in principle.

### Polynomial vs. Exponential — The Practical Wall

The difference between P and NP is the difference between *growth rates*:

- **Polynomial:** `n`, `n^2`, `n^3` — double your input size, the runtime
  doubles (or quadruples, or multiplies by 8). Manageable.
- **Exponential:** `2^n`, `n!` — double your input size, the runtime
  multiplies by a factor of `2^n`. Catastrophic.

For n=100: an `n^3` algorithm does 1,000,000 operations (trivial). A `2^n`
algorithm does 1,267,650,600,228,229,401,496,703,205,376 operations (still
running when the Sun dies). That's the NP wall. Hard problems aren't "hard" in
the sense of requiring cleverness — they're hard in the sense of requiring
more time than the age of the universe, even for modest-sized inputs.

This is why we use approximation algorithms (get "close enough" answers
quickly) and heuristics (educated guesses that usually work) for hard
problems. The donut's render can be exact; many real-world problems cannot.

## The Chomsky Hierarchy — A Map of Computability

Linguist Noam Chomsky classified languages (both human and programming) into
four levels of expressive power, and it directly mirrors the hierarchy of
computational models we've been discussing. Each level can recognize a broader
class of patterns than the one before it, at the cost of needing more
computational resources:

| Level | Grammar type | Computational model | Example |
|---|---|---|---|
| Type 3 | Regular | Finite state machine | CSV file, simple text patterns |
| Type 2 | Context-free | Pushdown automaton (FSM + stack) | JSON, balanced parentheses, most programming languages |
| Type 1 | Context-sensitive | Linear-bounded automaton | Some natural language constructions |
| Type 0 | Recursively enumerable | Turing machine | Any programming language |

Your donut code is level 2 (context-free, like most programming languages). But
when executed, it exercises the full Turing-complete power of the underlying
machine. The Chomsky hierarchy is a staircase: each level can do everything the
levels below can do, plus more. The Turing machine sits at the top, able to
recognize any language in the hierarchy.

## Connecting to the Donut — One Last Time

Let's close with the deepest connection between the spinning donut and the
theory of computation.

The donut, as a mathematical idea, is a **computable function**: a mapping from
input (the state variables `A`, `B`, `pos`) to output (a brightness grid). The
Church-Turing thesis says: there exists a Turing machine that computes this
function. The CPU that actually runs the donut is a physical realization of
that Turing machine — faster, with finite memory, but equivalent in
computational power.

When you watch the donut spin, you are watching a computable function being
evaluated in real time. The rotation math (sin and cos approximated by Taylor
series or lookup tables) is computable to any precision you desire — you just
need more tape (more memory) and more time. The animation is a sequence of
computable outputs, each one produced from the previous state by the same set
of rules.

And here is the beautiful part: because the donut is computable, you could
*prove* properties about it. You could prove that the brightness at a given
point depends on `A` in a continuous way. You could prove that the animation
never produces the same frame twice (if `A` and `B` are not rational multiples
of π). You could prove that the donut always looks like a donut and never turns
into a cube. These are theorems, not just empirical observations — and they
hold on any Turing-complete machine, from your laptop to a hypothetical
Babbage-style mechanical computer.

The donut isn't just code. It's mathematics, made physical.

## Where to Go Next

- **"Introduction to the Theory of Computation"** (Michael Sipser) — the
  textbook. Readable, rigorous, and the standard entry point. Chapters 1–4
  cover everything in this chapter and more. This is where you'll first prove
  the undecidability of the Halting Problem yourself.
- **"Computability and Logic"** (Boolos, Burgess, and Jeffrey) — a more
  philosophical treatment that connects computability to logic and the
  foundations of mathematics. Good if the Halting Problem made you wonder about
  the nature of mathematical truth.
- **"Godel, Escher, Bach"** (Douglas Hofstadter) — a literary masterpiece that
  weaves Gödel's incompleteness theorems (related to undecidability), art, and
  music into a single fabric. Not a textbook, but a meditation on the same
  themes.
- **"Computational Complexity: A Modern Approach"** (Arora and Barak) — the
  definitive text for P vs NP and beyond. Graduate-level, but the first few
  chapters are accessible after Sipser.
- **nand2tetris, Part II** (chapters 6–12) — covers the practical side: how to
  build a compiler and a simple operating system. Shows that theoretical
  computability translates directly into engineering.
