---
title: L3 Deep · Computer Architecture — The CPU and Its World
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L3 Deep · Computer Architecture — The CPU and Its World

```
    L0  framing                     ▲  "a donut"
    L1  software                    │  reshaping data
    L2  software ↔ OS               │  by asking the OS
  ▶ L3  instructions    ─────────────┤  which runs tiny commands
    L3  DEEP: ARCHITECTURE          │  how the CPU is built to run them
    L4  digital logic               │  built from gates
    L5  bits & physics              │  made of switching voltages
                                    └─── you are here: expanding L3
```

**The question:** In Part 0 we saw that a running program is a list of
instructions — `mul, mul, sub` — being fetched, decoded, and executed billions
of times per second. But the CPU is a physical object. How is it *organized* to
do this? What parts does it need?

**The idea.** Every modern computer (your laptop, your phone, the server that
served this page) is built around the same fundamental design, invented in the
1940s and so elegant that we've never left it. It's called the stored-program
concept, and it's usually associated with John von Neumann, though many people
contributed.

The insight is disarmingly simple:

> The program and the data live in the **same memory**, and the CPU reads both
> through the same mechanism.

Before this, computers were programmed by rewiring them — plugboards, patch
cables, physical switches. To change the program, you rewired the machine. Von
Neumann said: put the program *in memory*, right alongside the numbers it
operates on. The CPU reads it like any other data.

That one idea — stored-program — is why you can run a donut, a spreadsheet,
and a web browser on the same hardware without touching a single wire.

## The Von Neumann Architecture

Let's draw the machine. It has exactly three parts:

```
                          ╔═══ CONTROL UNIT ═══╗
                          ║                     ║
     ┌──────────┐         ║  ┌───┐              ║
     │          │         ║  │ PC│  (program    ║
     │  MEMORY  │ ◄───────║  │   │   counter)   ║
     │          │  data   ║  └───┘              ║
     │  (holds  │  bus    ║  ┌───┐              ║
     │  program ║         ║  │ IR│  (instruction║
     │  + data) │         ║  │   │   register)  ║
     │          │         ║  └───┘              ║
     └────┬─────┘         ║                     ║
          │ address bus   ║                     ║
          │               ╚═════════════════════╝
          │                      │
          │                      ▼
          │               ┌──────────────┐
          │               │     ALU      │
          └──────────────►│              │
                          │  (arithmetic │
                          │   / logic)   │
                          └──────┬───────┘
                                 │
                          ┌──────▼───────┐
                          │  REGISTERS   │
                          │  (r1, r2, …) │
                          └──────────────┘
```

Three components, connected by *buses* — bundles of wires that carry data,
addresses, and control signals from one part to another.

1. **Memory (RAM):** a giant array of numbered slots. Each slot holds one byte
   (8 bits). Slot 0, slot 1, …, slot billions. The program and its data share
   this space. The donut's `state["A"]`, the brightness grid, the instruction
   `mul r1, x, cosA` — all of them live here when not actively being worked on.

2. **The CPU (the processor):** the engine. It has sub-parts we'll unpack in a
   moment: the control unit, the ALU, and the registers.

3. **I/O (input/output):** everything that connects the computer to the outside
   world — keyboard, mouse, screen, disk, network card. The CPU talks to them
   through the same bus system, but I/O is special: it's how the donut's
   brightness grid gets from memory to your screen, and how your keypress
   (`→` speed-up) gets from the keyboard back to the program.

**The donut at this layer.** Your donut program sits in memory. The
instructions `mul, mul, sub` occupy a contiguous block. The state `{A, B, pos}`
sits in another block. The brightness grid that `render()` produces is a third
block. They're all just bytes in the same giant array. The CPU traverses the
instruction block, reading each command and shuffling data between the other
blocks and its own registers.

> **One-breath aside.** Von Neumann's design is so dominant that we sometimes
> forget there are alternatives. The *Harvard architecture* keeps program
> memory separate from data memory — each with its own bus. It's faster in some
> ways (you can fetch an instruction and load data simultaneously) but less
> flexible. Many embedded microcontrollers (like the ones in your microwave)
> use a Harvard design. Modern laptop CPUs are *modified Harvard* — they look
> Von Neumann to the programmer but act like Harvard under the hood for speed.

## Inside the CPU: Fetch, Decode, Execute

In Part 0 (L3) we saw the loop in broad strokes. Now let's fill in exactly
what happens during each step.

**Step 1: Fetch.** The control unit looks at a special register called the
**Program Counter (PC)**, which holds the memory address of the *next*
instruction. It sends that address to memory via the address bus, and memory
sends the instruction back via the data bus. This instruction lands in another
special register: the **Instruction Register (IR)**. The PC then increments
automatically — it now points to the instruction after this one.

**Step 2: Decode.** The control unit examines the bits in the IR. It's looking
at the *opcode* — the part of the instruction that says "this is a `mul`" or
"this is a `sub`." The control unit has a small decoder circuit that activates
the right pathways: "Ah, `sub` means I need to connect the ALU's subtract mode,
and the operands are in registers r1 and r2."

**Step 3: Execute.** The ALU (Arithmetic Logic Unit) does the actual work. For
`sub x, r1, r2`, the ALU receives r1 and r2 as inputs, subtracts them, and
places the result back in register x. The ALU doesn't know it's subtracting for
a donut — it just performs the operation the control unit tells it to.

Then the cycle repeats. The control unit reads the (updated) PC, fetches the
next instruction from that address, and so on forever. The entire universe of
computing is this loop.

```
  FETCH ──► DECODE ──► EXECUTE ──► (repeat, billions/sec)
   │           │           │
   │           │           ▼
   │           │     ┌─────────────┐
   │           │     │  our donut: │
   │           │     │  mul r1..   │
   │           │     │  mul r2..   │
   │           │     │  sub x..    │
   │           │     └─────────────┘
   ▼           ▼
  ┌────┐    ┌────┐
  │ PC │    │ IR │
  │  → │    │sub │
  └────┘    └────┘
```

**The donut at this layer.** Let's trace our `sub x, r1, r2` through the
cycle. At the start of the cycle, the PC holds, say, address 19304 — the
address of `sub` in memory. The fetch sends address 19304 to RAM, and RAM
returns the bits for `sub x, r1, r2`. The PC ticks to 19305, pointing at the
next instruction. The decode looks at the opcode bits, sees "subtract," and
routes r1 and r2 to the ALU. The ALU subtracts. The result goes to x. Done.
The whole thing takes maybe 0.3 nanoseconds.

Now imagine: the donut's `render` function loops over every point on the torus.
For each point, it computes a rotation, which involves... our `mul, mul, sub`.
For each point, the CPU hits this trio roughly 1000 times per frame. At 60
frames per second, that's 60,000 `mul, mul, sub` trios per second, each one
waltzing through the fetch-decode-execute cycle. The whole computer is just
this loop, nested in time.

## The Memory Hierarchy — Why Speed Costs

Here's a fact that will haunt every programmer: memory is not one thing. It's a
*ladder*, and each rung is a different technology with a different tradeoff.

```
          REGISTERS           ◄──   ~1 cycle (0.3 ns)    size: ~1 KB
            │                       cost: $$$$/byte
            ▼
          L1 CACHE             ◄──   ~3 cycles           size: ~32 KB
            │
            ▼
          L2 CACHE             ◄──   ~10 cycles          size: ~256 KB
            │
            ▼
          L3 CACHE             ◄──   ~40 cycles          size: ~8 MB
            │
            ▼
          MAIN MEMORY (RAM)    ◄──   ~200 cycles         size: ~16 GB
            │
            ▼
          DISK (SSD/HDD)       ◄──   ~10,000,000 cycles  size: ~1 TB
```

The CPU registers are right inside the chip — they're the fastest thing in
existence. A register access takes one clock cycle. But there are only a few
dozen of them. Then comes cache: small amounts of ultra-fast memory built into
the CPU itself. L1 is fastest and smallest; L3 is slower but bigger. Below
that, main memory (RAM) is comparatively glacial. Disk is a million times
slower.

Why this pyramid? Because *fast memory is expensive and hot*. Building 1 TB of
L1 cache would melt your laptop and cost more than a house. So engineers build
a tiny amount of fast memory and a large amount of slow memory, and rely on a
trick called **locality**:

- **Temporal locality:** if you accessed a memory address, you'll probably
  access it again soon. (The donut reads `state["A"]` every single frame.)
- **Spatial locality:** if you accessed one address, you'll probably access its
  neighbors soon too. (The donut's instructions are stored sequentially — after
  `mul`, the next `mul` is right next to it in memory.)

The cache hardware notices these patterns automatically. When your program asks
for address X, the cache grabs not just X but a whole chunk of X's neighbors
and keeps them nearby. If your program's data access pattern is predictable,
the cache will have what you need already loaded, most of the time.

**The donut at this layer.** The donut's state — `A`, `B`, `pos` — is tiny,
just three numbers. They fit in the registers, or at worst L1 cache. That's why
your laptop can spin the donut at 60 fps without breaking a sweat. The
brightness grid, by contrast, is big — thousands of numbers. That lives in main
memory. The CPU is constantly fetching chunks of it through the cache hierarchy:
pull the grid row from RAM into L3, then L2, then L1, operate on it, write
back. Every 'mul, mul, sub' in the render loop triggers this data journey
alongside the instruction journey.

Now imagine the donut was poorly written, with `state["A"]` scattered across
the grid calculation in a way that jumps around memory unpredictably (what we'd
call *cache-unfriendly*). The same program would crawl, because every
instruction would find the cache cold — a *cache miss* — and the CPU would
spend hundreds of cycles waiting on RAM.

## Pipelining: The Assembly Line

The fetch-decode-execute cycle, as described above, seems sequential: do step
1, then step 2, then step 3, then start the next instruction. That would mean
each instruction takes 3 cycles, and the CPU is idle for 2/3 of its time (each
sub-unit is used only 1/3 of the time).

Pipelining fixes this the same way a factory does: overlap the work.

```
  Without pipeline:
   INST 1:     [FETCH] [DECODE] [EXECUTE]
   INST 2:                          [FETCH] [DECODE] [EXECUTE]
   INST 3:                                               [FETCH] [DECODE] [EXECUTE]

  With pipeline:
   INST 1:     [FETCH] [DECODE] [EXECUTE]
   INST 2:             [FETCH] [DECODE] [EXECUTE]
   INST 3:                     [FETCH] [DECODE] [EXECUTE]
   INST 4:                             [FETCH] [DECODE] [EXECUTE]
```

While instruction 1 is being executed, instruction 2 is being decoded, and
instruction 3 is being fetched — all three at the same time, on three different
parts of the CPU. The throughput triples. The CPU finishes one instruction per
cycle, even though each instruction takes three cycles to complete.

**The donut at this layer.** Our `mul, mul, sub` trio is exactly the kind of
simple, sequential code that pipelines love. While the first `mul` is executing
in the ALU, the second `mul` is being decoded, and the next instruction after
that (whatever follows `sub` in the loop) is being fetched. The donut's tight
loop of arithmetic instructions keeps the pipeline full and the CPU busy.

But not all code pipelines well. Consider what happens with a branch — an "if"
statement:

```asm
    cmp   r1, r2         ; compare r1 with r2
    beq   label          ; if equal, jump to label
    mul   r3, r4, r5     ; otherwise, keep going
```

The CPU fetches `cmp`, decodes it, executes it. It fetches `beq`, decodes it.
Now it needs to execute `beq` — but `beq` might or might not jump. The pipeline
has already started fetching the next instruction. If it guessed wrong, it has
to flush the pipeline (discard the partially-completed work) and start over
from the correct address. This is a **branch misprediction**, and it costs ~15
cycles of wasted work.

Modern CPUs are surprisingly good at predicting branches (they learn patterns:
"this loop usually runs 100 times" or "this comparison almost always goes the
same way"). But branches still create hiccups. The donut's render loop is
nearly branch-free — it's mostly straight-line math — which is part of why it
runs so smoothly.

> **One-breath aside.** The classic donut math by a1k0n uses a clever trick:
> it precomputes `sin` and `cos` of A and B once per frame, then uses them for
> every point. This is a *spatial locality* win (the sin/cos values stay in
> registers or L1 cache) and a *computational redundancy* win (no repeated trig
> calls). The donut is not just a cute demo — it's a demonstration of how
> making data flow predictably unlocks the CPU's full speed.

## Instruction Set Architecture (ISA) — The CPU's Contract

Different CPUs speak different languages. The vocabulary a CPU understands is
its **Instruction Set Architecture (ISA)** — the complete list of instructions
it can execute: `add`, `sub`, `mul`, `load`, `store`, `branch`, and so on. The
ISA is a boundary:

> **Above the ISA:** compilers and programmers write code.
> **Below the ISA:** CPU engineers build hardware that implements those
> instructions.

The ISA is the contract between software and hardware. As long as a compiler
produces instructions from the ISA, any CPU implementing that ISA will run the
code. This is why you can run the same Windows program on an Intel chip from
2010 or 2025 — they both speak x86.

Here are the three major ISA families you'll encounter:

- **x86 / x86-64 (Intel, AMD):** the dominant ISA for laptops, desktops, and
  servers. It's a Complex Instruction Set Computer (CISC) — it has hundreds of
  instructions, some quite elaborate. The x86 ISA is ancient (1978, the Intel
  8086) and has been extended again and again, making it... let's say
  *historically layered*. Modern x86 chips translate these complex instructions
  into simpler internal micro-operations behind the scenes — a trick that keeps
  backward compatibility while getting modern performance.

- **ARM (Apple Silicon, Qualcomm, most phones):** the dominant ISA for mobile
  devices. ARM is a Reduced Instruction Set Computer (RISC) — fewer, simpler
  instructions. Each instruction does less but can run faster. ARM was designed
  for low power consumption, which is why it powers your phone. In 2020, Apple
  switched their Macs from x86 to ARM, proving that a RISC chip can now match
  or beat CISC at every measure.

- **RISC-V (pronounced "risk-five"):** an open, free ISA. Unlike x86 and ARM,
  which are owned by companies and require licenses, RISC-V is open — anyone
  can build a chip that speaks it. It's still young (the specification was
  finalized in 2019) but is generating enormous interest in academia and
  industry. Think of it as Linux to x86's Windows: free, open, and gaining
  ground.

**Why do ISAs differ?** It's a constant tension. CISC (x86) packs more work
into each instruction, which can make programs shorter (fewer bytes of code,
less memory used). RISC (ARM, RISC-V) keeps instructions simple so they run
faster, can be pipelined more easily, and consume less power. There is no right
answer; the tradeoff shifts depending on whether you're building a cloud server
or a smartwatch.

**The donut at this layer.** Our `mul, mul, sub` instructions are RISC-style
simple — each one does one thing. On an x86 chip, the compiler *might* emit a
single `FMA` (fused multiply-add) instruction that does both the multiply and
the subtract in one shot. On ARM, it might emit three separate instructions.
The donut's behavior is the same either way — the math is the same — but the
byte sequences are different. The ISA is the language; the donut's idea is the
same thought expressed in that language.

## Microarchitecture vs. ISA — The Same Language, Different Accents

One more distinction is worth making, because it reveals how engineering works
in practice.

The **ISA** is what the programmer sees: the list of instructions, the register
names, the memory model. It's the contract. The **microarchitecture** is how
the CPU *implements* that contract internally — the pipeline depth, the cache
sizes, the branch predictor design, the number of execution units.

Two CPUs can implement the same ISA with completely different microarchitectures.
Intel's Core i5 and AMD's Ryzen 5 both speak x86-64, but their internal designs
are wildly different. Intel might use a 14-stage pipeline with a particular
branch predictor; AMD might use a 17-stage pipeline with a different cache
hierarchy. The same program runs identically on both (same ISA), but at
different speeds — because the microarchitecture differs.

This is the engineering freedom inside the ISA's boundaries. The ISA defines
*what* you can say; the microarchitecture defines *how fast* you can say it.

**The donut at this layer.** The donut runs on any x86 CPU — a 2015 Intel chip
and a 2025 AMD chip both execute the same `mul, mul, sub` instructions. But on
the newer chip, with its larger caches and deeper pipeline, the donut might
render twice as fast. The donut doesn't change; the engine under it does.

## Interrupts and Exceptions — How the CPU Handles Surprises

The fetch-decode-execute loop is beautifully regular, but real computers aren't.
The keyboard sends a keypress, the disk finishes a read, the donut divides by
zero. How does the CPU handle these interruptions to its rhythm?

**Interrupts** are external events: a hardware device (keyboard, disk, timer)
signals the CPU that it needs attention. The CPU finishes its current
instruction, then instead of fetching the next one, it saves its state (the PC
and registers) and jumps to a special **interrupt handler** — a small program
registered by the OS. The handler deals with the device, then restores the
CPU's saved state, and the interrupted program resumes as if nothing happened.

**Exceptions** are internal: the program itself does something the CPU can't
handle in the normal flow. Division by zero, accessing invalid memory, an
undefined instruction. The CPU catches these and transfers to an exception
handler. The handler might fix the problem (if possible), kill the offending
program, or crash the system.

**The donut at this layer.** While your donut spins, an interrupt fires every
~1 millisecond from the system timer. The CPU suspends the donut's
fetch-decode-execute loop, runs the OS's scheduler, checks if another program
needs the CPU, and resumes the donut. The donut never notices — but its smooth
60 fps animation depends on the OS getting these timer interrupts to wake up
and tell the donut "time for the next frame."

If the donut's `render()` loop ran forever without interruption (an infinite
loop in user code), the scheduler interrupt would *preempt* it — forcibly
pausing the donut so other programs get CPU time. This is the foundation of
multitasking.

## Modern Trends: Multi-Core, GPUs, Accelerators

A single CPU core, pipelined and cache-laden, can run billions of instructions
per second. But transistors have stopped shrinking at the rate they used to (a
trend called the end of Dennard scaling), so we can't just make each core
faster. Instead, we add more cores.

**Multi-core CPUs.** A modern laptop chip has 4–16 cores, each containing its
own ALU, registers, and L1/L2 cache, sharing L3 cache and memory. The OS can
run different programs on different cores simultaneously. The donut could, in
principle, be parallelized: one core computes the top half of the grid while
another computes the bottom. But that requires writing the program to be safe
for parallelism — a deep and tricky topic.

**GPUs (Graphics Processing Units).** A GPU is a different beast: thousands of
small, simple cores designed to do the same operation on many data points at
once. The donut's render loop — "for every point on the torus, do the same
rotation math" — is a perfect GPU workload. A GPU could process all 1000 points
simultaneously instead of one at a time. This is why GPUs don't just render
donuts; they train neural networks: same operation, many data points.

**Specialized accelerators (TPUs, NPUs).** Google's Tensor Processing Unit
(TPU) and the Neural Processing Units (NPUs) in modern phones are chips
designed for one specific class of computation (matrix multiplication for
neural networks). They can't run your donut at all — they only accelerate
matrix math. But they do that *extremely* well, and the CPU delegates that work
to them.

**The donut at this layer.** The donut as written runs on one CPU core, one
instruction at a time, in a pipelined loop. That's plenty for this toy. But if
the donut had to render 10,000 tori at once (a scene in a video game), the CPU
would struggle — and the GPU would take over. The architecture of the machine
determines where different types of work belong.

## Where to Go Next

- **nand2tetris** (Noam Nisan and Shimon Schocken) — you build a computer from
  NAND gates all the way up through an operating system. Part 5 of that course
  covers exactly this chapter's material: building the CPU and understanding the
  fetch-decode-execute cycle in hardware. Start here if you want to *build*
  what you just read.
- **CSAPP: Computer Systems: A Programmer's Perspective** (Bryant and
  O'Hallaron) — Chapters 4 and 5 cover processor architecture and optimizing
  program performance with the memory hierarchy in mind. This is the definitive
  text for understanding how architecture affects your code.
- **"Computer Architecture: A Quantitative Approach"** (Hennessy and Patterson)
  — the classic textbook. Dense but comprehensive. Patterson won a Turing Award
  partly for his work on RISC, which you met above.
- **"The Anatomy of a Donut"** (a1k0n.net) — retrace the original donut code
  with new eyes. Now that you know about caches and pipelines, notice *why* the
  donut code is structured the way it is: all the trig precomputed, all the
  loops tight, no branches in the inner loop.
