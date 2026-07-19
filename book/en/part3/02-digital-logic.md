---
title: L4 Deep · Digital Logic — How Gates Build the Machine
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L4 Deep · Digital Logic — How Gates Build the Machine

```
    L0  framing                     ▲  "a donut"
    L1  software                    │  reshaping data
    L2  software ↔ OS               │  by asking the OS
    L3  instructions                │  which runs tiny commands
    L3  DEEP: ARCHITECTURE          │  how the CPU is built to run them
  ▶ L4  DIGITAL LOGIC   ─────────────┤  built from gates
    L4  DEEP: DIGITAL LOGIC         │  how gates build everything
    L5  bits & physics              │  made of switching voltages
                                    └─── you are here: expanding L4
```

**The question carried down:** In Part 0 (L4), we saw that the CPU's `sub`
instruction is built from logic gates — ANDs, ORs, XORs, NOTs — wired into a
ripple-carry adder. But that was just one circuit. How do gates build
*everything else* in a computer? Memory, control, the whole CPU?

**The idea.** Logic gates are the Lego bricks of the digital world. You only
have a few kinds, but you can wire them to do anything: add numbers, compare
values, choose paths, and — most remarkably — *remember* a value. The last one
is where real magic starts.

## Why Binary? A Quick Refresher

Before we open any gates, let's be honest about why we use just two symbols:

> A computer uses binary because two voltages are trivially distinguishable.

In a transistor, the "gate" voltage is either high enough to switch the
transistor on, or it isn't. With ten symbols (our decimal 0–9), you'd need ten
different voltage levels, and distinguishing them would be expensive, noisy, and
unreliable. With two levels, you just need one simple threshold: above 0.7 V is
a "1"; below 0.3 V is a "0." The physics is forgiving.

That's the entire reason. Not because binary is mathematically natural (though
binary arithmetic is simple). Not because it's elegant. Because it's cheap and
reliable to build with real wires and real electrons.

So a number like 42 in decimal becomes `101010` in binary — the same quantity,
just written with two symbols instead of ten. The CPU stores it as eight wires
(the common byte), each either high (1) or low (0). All of computing is
shuffling those wire voltages.

## From Transistors to Gates — A Quick Review

From Part 0 L5, we know that a transistor is a switch controlled by a voltage.

```
          gate (control)
            │
            ▼
   in ──────●──────► out
```

When the gate voltage is HIGH, the switch closes and current flows: out = in.
When the gate voltage is LOW, the switch opens: out = disconnected.

Wire two of these switches in a particular pattern and you get an AND gate:
current flows from both inputs to output only when both control voltages are
high. Wire them differently and you get OR, NOT, NAND, NOR, XOR. All of them
are just patterns of transistors.

But you don't need all of them. It turns out that **any** logic circuit can be
built from **NAND gates alone** — a single type of gate. NAND is "NOT AND": it
outputs a 1 unless both inputs are 1. This is the theoretical foundation of
nand2tetris: from one gate you reconstruct all the others, then the ALU, then
the CPU, then the computer. One primitive, recursively stacked.

```
  NAND gate:
    a  b │ out
    0  0 │  1
    0  1 │  1
    1  0 │  1
    1  1 │  0
```

> **One-breath aside.** The fact that one gate type is universal is not just a
> neat textbook fact — it's how real chips are designed. In the early days,
> designers used many gate types. Today, chip design uses standard-cell
> libraries that are heavily NAND- or NOR- based, because regularity makes
> fabrication easier, smaller, and more reliable. The question "what is the
> simplest possible self-sufficient building block" is the same question that
> drives the entire *theory of computation* chapter ahead of us.

## Combinational Logic — Gates Without Memory

The circuits we saw in Part 0 (the full adder) are **combinational**: the
output depends only on the current inputs. There is no history. Change the
inputs, wait a few nanoseconds for the voltages to propagate through the gates,
and the outputs stabilize to the new answer.

And you can build a *lot* with just combinational logic.

### Decoders

A decoder is a circuit that takes a binary number and activates one of several
output lines. A 3-to-8 decoder takes 3 input bits (representing numbers 0–7)
and activates exactly one of 8 outputs.

```
  3-bit input   │  active output (only one is 1)
  ──────────────┼──────────────────────────────────
  000           │  out0 = 1
  001           │  out1 = 1
  010           │  out2 = 1
  ...           │  ...
  111           │  out7 = 1
```

Decoders are everywhere. The control unit uses one to decode the instruction
opcode (the fetch-decode-execute's "what is this instruction?" step). Memory
uses one to select which byte to read from a given address. A keyboard uses one
to figure out which key was pressed.

### Multiplexers (MUX)

A multiplexer selects one of several inputs. Think of a railroad switch: two
tracks come in, one track goes out, and a control signal picks which incoming
track connects to the outgoing track.

A 2-to-1 MUX has two data inputs (A and B), one selector (S), and one output:
if S=0, output = A; if S=1, output = B.

```
   S ──┐
       ├─►  out = A when S=0, B when S=1
  A ───┤
  B ───┘
```

MUXes are the CPU's routing fabric. The ALU uses them to decide "are we adding
or subtracting?" The register file uses them to decide "which register should
we read right now?" The CPU is, in many ways, a sea of multiplexers connecting
gates to registers under the control unit's direction.

### The ALU — Putting It All Together

The ALU is a combinational circuit — a big one — that performs all the
arithmetic and logical operations the CPU supports: add, subtract, AND, OR,
XOR, compare, shift left, shift right.

```
                        ┌─────────────────────────────────────────────┐
  input_a (32 wires)───►│                                             │
                        │                    ALU                      │
  input_b (32 wires)───►│                                             │
                        │                                             │
  opcode (4 wires) ─────┤  if opcode=0: output = a + b               │
                        │  if opcode=1: output = a - b               │──► result (32 wires)
                        │  if opcode=2: output = a AND b             │
                        │  if opcode=3: output = a OR b              │──► flags (zero, negative, overflow)
                        │  ...                                       │
                        └─────────────────────────────────────────────┘
```

Inside, the opcode controls a set of multiplexers that route `a` and `b`
through different gate networks. For add, they go through the full-adder chain.
For AND, they bypass the adder and go through a row of AND gates. The MUX at
the end selects which subcircuit's output to send forward.

**The donut at this layer.** Every `mul, mul, sub` in our donut's render loop
passes through the ALU. The `sub` sets the opcode to 1. The 32-bit adder chain
(inverted inputs for subtraction) ripples, and 0.3 nanoseconds later the result
appears. The ALU doesn't know it's computing a donut coordinate. It just takes
two numbers and opcode, produces one number. Faithfully, mindlessly.

### Comparators and Shifters — More Building Blocks

The ALU also handles operations beyond arithmetic. A **comparator** takes two
binary numbers and determines if they're equal, or which is larger. It's built
from XOR gates (to detect bit-by-bit equality) cascaded through ANDs. If every
pair of bits matches, the comparator outputs 1. This is how the CPU checks
"did the loop counter reach zero yet?" — the condition that exits the donut's
render loop when all grid points have been processed.

A **shifter** moves all bits left or right: `0110` shifted left by 1 becomes
`1100` (multiply by 2), shifted right becomes `0011` (divide by 2). A shifter
is essentially a row of multiplexers, each selecting between "pass the bit
through" or "pass the bit from the neighbor." The donut's `render()` doesn't
use shifting explicitly, but the compiler may use shifts to optimize
multiplication by small constants — replacing `x * 8` with `x << 3` because a
shift is faster than a multiply.

### Propagation Delay — Why Gates Take Time

Every gate takes a small but real amount of time to produce its output after
its inputs change. This is **propagation delay**, measured in picoseconds
(trillionths of a second). For a simple AND gate, it might be 50 ps. For a
complex chain of gates (like our 32-bit adder), the delays add up.

This is the critical constraint on all digital design. The longest path through
the circuit — the *critical path* — determines the maximum clock speed. The
adder chain we traced above is the critical path of the ALU. The ALU's path
through the full CPU is the critical path of the whole processor. The donut's
speed, the frame rate, everything — bounded by how fast the slowest path
through the gates can settle.

Engineers spend enormous effort shortening critical paths. They redesign
adders (carry-lookahead instead of ripple), they reorder circuits, they
insert pipeline stages (breaking long paths into shorter ones). Every
nanosecond matters, and every nanosecond is a war against propagation delay.

## Sequential Logic — Gates That Remember

Here is where the world changes. Every circuit we've built so far forgets the
moment its inputs change. But a computer needs to *remember*: the current state
of the donut (A, B, the brightness grid contents), the program counter (where we
are in the instructions), the registers. If everything forgot every cycle, we
couldn't compute anything multi-step.

The solution is a circuit that feeds back to itself — the output is connected
back to the input through a gate, creating a loop that holds its value.

### The SR Latch

The simplest memory element is the **SR latch** (Set-Reset):

```
         ┌───┐
    S ───┤   ├──► Q
         │NOR├──┐
      ┌──┤   │  │
      │  └───┘  │
      │         │
      │  ┌───┐  │
      │  │   │  │
      └──┤NOR├──┘
         │   ├──► Q̅ (not-Q)
    R ───┤   │
         └───┘
```

When S=1, the latch enters "set" state: Q becomes 1 and stays 1 even after S
goes back to 0. When R=1, it "resets": Q becomes 0 and stays 0. When both are
0, the latch *remembers its last value*.

Two NOR gates, cross-wired. That's the birth of memory in hardware. From this
humble 2-transistor loop, all of storage grows.

### The D Flip-Flop — Clocked Memory

The SR latch is useful but undisciplined: it changes whenever S or R changes. A
computer needs memory that only changes at specific moments — when the clock
ticks. Enter the **D flip-flop**:

```
  CLK ──┐
        ├────────────► Q updates to D on the clock's rising edge
   D ───┤
        │
         └── (a few gates that sample D only at the clock edge)
```

The D flip-flop captures the value of D at the exact moment the clock rises
from 0 to 1, and holds it until the next rising edge. Now we have
**synchronous memory** — everything updates together, in lockstep.

This is the clock we introduced in Part 0. Every register in the CPU is a bank
of D flip-flops. Every state variable in the donut (`A`, `B`, `pos`) is stored
in memory cells that are, at their core, just cleverly wired flip-flops.

## The Clock: Heartbeat of the Machine

A clock is just a wire that alternates between 0 and 1 at a fixed frequency:
3 GHz means it ticks 3 billion times per second. Each tick defines a moment
when flip-flops capture their inputs and present stable outputs for the next
stage.

The clock enforces discipline:

1. At the rising edge, registers present their values.
2. The values flow through combinational logic (gates, adders, MUXes).
3. The logic outputs stabilize after some delay (the propagation delay).
4. At the *next* rising edge, the next set of registers captures the results.
5. Repeat.

This is why every CPU has a maximum clock speed. The clock period must be long
enough for the combinational logic to settle. If the logic takes 0.5 ns to
settle, you can't clock faster than 2 GHz (1/0.5 ns). If you try — that's
overclocking — the next flip-flop may capture a half-settled value, causing a
compute error that looks like a crash or corruption.

**Setup time** is the minimum time before the clock edge that a flip-flop's
input must be stable. **Hold time** is the minimum time after the clock edge it
must stay stable. Violate either, and the flip-flop enters a *metastable*
state — not 0, not 1, but something in between, with unpredictable results.

**The donut at this layer.** The donut's spin speed is fundamentally tied to
this clock. A faster clock means more `mul, mul, sub` cycles per second, which
means more grid points computed per frame, which means a smoother or faster
animation. But the clock can't go arbitrarily fast — the adder's ripple delay
sets the limit. To get faster without raising the clock frequency, engineers
invented the **carry-lookahead adder**, which computes carries in parallel
instead of waiting for the ripple. The donut's frame rate is, in a real sense,
limited by how fast bits can propagate through gates.

> **One-breath aside.** Overclocking works sometimes because chip manufacturers
> set conservative clock speeds to guarantee operation across all chips, all
> temperatures, all voltages. A particular chip might tolerate a 10% faster
> clock — it's just that not all chips in the batch can. This is also why
> overclocking requires better cooling: heat increases propagation delays
> (electrons move slower in hotter silicon), so an overclocked chip that works
> at 25 C might fail at 80 C. The donut would glitch, then freeze.

## Finite State Machines in Hardware

Remember the finite state machine from the theory of computation? Here it is in
hardware form. An FSM in a digital circuit has three parts:

1. **State register:** a bank of D flip-flops that holds the current state.
2. **Next-state logic:** combinational gates that compute the next state from
   the current state and the inputs.
3. **Output logic:** combinational gates that compute the outputs from the
   current state (and possibly the inputs).

```
               inputs ──────►┌─────────────────┐
                              │  NEXT-STATE     │
                              │  LOGIC          │
                              │  (combinational)│
                              └────────┬────────┘
                                       │ next state
                                       ▼
                              ┌────────────────┐
                              │  STATE REGISTER│◄──── clock
                              │  (D flip-flops)│
                              └────────┬────────┘
                                       │ current state
                                       │
                  ┌────────────────────┤
                  │                    │
                  ▼                    ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  OUTPUT LOGIC    │  │  NEXT-STATE      │
        │  (combinational) │  │  (fed back)      │
        └────────┬─────────┘  └──────────────────┘
                 │
                 ▼ outputs
```

The CPU's control unit is exactly this: a finite state machine that cycles
through fetch, decode, execute, and back to fetch. The state register holds
"which phase are we in." The next-state logic checks "did the clock just tick?"
The output logic says "if we're in decode, activate the opcode decoder and
prepare the ALU." All of this is built from the same gates we've been
exploring.

**The donut at this layer.** The control unit FSM is what coordinates the
donut's instruction flow. While the ALU is busy subtracting for one
instruction, the control unit's next-state logic has already computed that the
next tick should move from execute back to fetch. The FSM's output logic has
readied the program counter to send the next address. The FSM ticks, the
fetch-decode-execute wheel turns, and the donut's computation advances by one
instruction. The control unit FSM is the conductor; the ALU and registers are
the orchestra.

### Synchronous vs. Asynchronous Design

Nearly every digital circuit today is **synchronous**: driven by a single
global clock, with all state changes happening on the clock edge. This is the
design we've been describing. It's simple, predictable, and debuggable.

**Asynchronous** circuits have no global clock. Each stage signals the next
when it's done ("handshaking"). These are harder to design (you have to worry
about race conditions and glitches) but can be faster and use less power —
because each stage starts immediately when ready, not when the next clock tick
arrives.

There's been research interest in asynchronous design for decades, but almost
all commercial CPUs are synchronous. The donut's CPU runs on a clock, and that
clock ticks, and that's what makes the whole thing predictable.

## Following the Donut's `sub` Through the Full Adder Chain

Let's trace our single instruction — `sub x, r1, r2` — through the actual
circuit, bit by bit.

Assume `r1` holds the number 5 (binary `0101`) and `r2` holds 3 (binary
`0011`). Subtraction is addition of the two's complement: we invert all bits of
`r2` (making it `1100`) and add 1. The full chain for 4 bits (for simplicity;
real CPUs use 32 or 64):

```
   bit position:   3      2      1      0
                   ↓      ↓      ↓      ↓
  r1:              0      1      0      1
  inverted r2:     1      1      0      0
  carry in:        0      0      0      1   ← start with carry-in = 1 (for two's complement)

  Full adder 0:    a=1, b=0, carry-in=1   → sum=0, carry-out=1
  Full adder 1:    a=0, b=0, carry-in=1   → sum=1, carry-out=0
  Full adder 2:    a=1, b=1, carry-in=0   → sum=0, carry-out=1
  Full adder 3:    a=0, b=1, carry-in=1   → sum=0, carry-out=1

  Result: 0010 = 2  ✓  (5 - 3 = 2)
```

Each full adder is 5 gates (two XORs, two ANDs, one OR). The 4-bit add we just
did used 20 gates plus the NOTs for the inversion. A 32-bit add uses 160 gates
for the adders plus 32 NOTs for the inversion. The donut's `sub` fires this
cascade of 160+ gates every time it executes.

And the result ripples from bit 0 all the way to bit 31 — the carry ripples
through all 32 adders in sequence. At the end, if bit 31 produced a carry, the
result overflowed (the donut coordinates wrapped around — probably a glitch).

This is why subtraction isn't "free." It costs gate delays, nanoseconds, and
energy. The donut's render loop can't avoid it — every rotation is a
subtraction — but understanding that cost is what lets engineers optimize it.

## The nand2tetris Arc — From NAND to Computer

There is a beautiful learning path that mirrors exactly what we've done in
Part 0 and this chapter. It's called **nand2tetris** (short for "From NAND to
Tetris"). The premise: start with one NAND gate as your only primitive, and
build everything step by step:

1. NAND → NOT, AND, OR, XOR (1 gate type, now you have all)
2. Gates → half adder, full adder, ALU (now you can compute)
3. ALU + flip-flops → registers, memory (now you can store)
4. ALU + registers + control → CPU (now you can execute instructions)
5. CPU + memory → a working computer (now you can run programs)
6. Computer + assembly → an assembler (now you can write programs)
7. Assembler → a compiler (now you can write in a high-level language)
8. Compiler → an operating system (now you can run multiple programs)
9. Everything → Tetris (see: the course's title)

What nand2tetris makes visible is that **nothing** is added between step 1 and
step 9 except *wiring*. No new physics. No new primitives. Just more and more
gates, connected in more and more elaborate patterns. The computer is a
tower of abstraction built entirely on one gate type.

**The donut at this layer.** If you followed nand2tetris, you would build a
computer that could, in principle, run the donut's render. The circuit that
computes our `sub` would be exactly the circuit you design in project 3. The
ALU you build in project 2 is the ALU that the donut's `mul, mul, sub` passes
through. The computer you build in project 5 is executing those instructions,
60 times a second, for as long as you watch.

## What You Can't Build Solely from Gates (and Why That Matters)

Gates can compute any finite function. But they cannot:

- **Infinite storage.** You can't build unbounded memory from gates alone — you
  need physical structures (DRAM capacitors, SRAM cells) that leak and need
  refreshing. Gates can *address* memory but can't *be* all of it.
- **Infinite loops without a clock.** A purely combinational circuit with no
  flip-flops cannot "loop" — it has no memory of previous states. To repeat the
  same computation, you need sequential logic and a clock to manage the state.
- **Self-modification.** A circuit made of gates is a circuit made of gates.
  It can't rewire itself (though *FPGAs* — Field Programmable Gate Arrays —
  come close: you can reconfigure their wiring at runtime).

These aren't limitations of gates per se; they're the boundaries of the
*finite-state model*. And that boundary points straight at our next chapter.
Some questions live *above* the hardware — in the realm of what can and cannot
be computed at all, regardless of how many gates you build.

## Where to Go Next

- **nand2tetris** (Noam Nisan and Shimon Schocken) — the canonical path from
  NAND to a working computer. Chapters 1–5 cover everything in this chapter in
  project form, where you actually build the circuits.
- **"Code: The Hidden Language of Computer Hardware and Software"** (Charles
  Petzold) — a brilliant, accessible walk from telegraph relays to CPUs,
  building every concept from scratch. Starts with flashlights and ends with
  Windows. This is the gentlest possible version of this chapter.
- **"The Art of Electronics"** (Horowitz and Hill) — the engineer's bible for
  actual circuit design. Chapters 8–12 cover digital logic from the transistor
  level up. Dense but definitive.
- **CSAPP** (Bryant and O'Hallaron), Chapter 3 — goes a level deeper into how
  a specific CPU (x86-64) implements its instruction set, with real gate-level
  descriptions of adders and multipliers.
