---
title: "L2.1 · Operating Systems — The Program That Owns the Hardware"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L2.1 · Operating Systems — The Program That Owns the Hardware

```
   Part 0  L2  software ↔ OS        (the big picture)
   Part 2  L2.1 operating systems  ◀ you are here
   Part 2  L2.2 networking
   Part 2  L2.3 databases
   Part 2  L2.4 distributed systems
```

**The question carried down:** Part 0 told us that programs _ask_ the OS to do
anything real — draw to the screen, read a file, send a packet. But what _is_
the OS? What does it actually _do_ all day?

**The idea.** The operating system is a program — but a very special one. It is
the one program that is allowed to touch the hardware, and it spends its entire
existence saying _no_ to other programs until they ask politely.

```
   ┌───────────────────────────────────────────────────────────┐
   │                  THE OPERATING SYSTEM                        │
   │                                                             │
   │   ┌─────────────────────────────────────────────────────┐   │
   │   │  KERNEL  (the privileged core — runs in "kernel mode") │   │
   │   │                                                       │   │
   │   │  Process scheduler ── virtual memory manager         │   │
   │   │  File system driver ── device drivers                │   │
   │   │  System call dispatcher                              │   │
   │   └─────────────────────────────────────────────────────┘   │
   │                                                             │
   │     ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
   │     │  your    │  │ browser  │  │  music   │  │  system  │ │
   │     │ terminal │  │          │  │  player  │  │  daemon  │ │
   │     └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
   │       ▲               ▲            ▲               ▲       │
   │       │  each lives in its own sandbox ("user space")      │
   └───────────────────────────────────────────────────────────┘
```

Every other program — your terminal, your browser, the donut — is a guest.
It runs in a restricted mode called **user space**. Only the kernel runs in
**kernel space**, where the hardware is accessible. That split is enforced
by the CPU itself: if a user-space program tries to execute a privileged
instruction, the CPU refuses and hands control to the kernel.

> **One-breath aside.** This user/kernel split is not just a software
> convention — the CPU has a special bit in its status register that tracks
> which mode it's in. When that bit says "kernel," the CPU allows
> instructions that access hardware directly. When it says "user," those
> instructions cause a trap — an automatic jump to the kernel. So the
> boundary is physical: the chip itself enforces it. See Part 0 L3 for how
> this works at the instruction level.

## What the OS Actually Does

The OS has four big jobs. Every one of them matters for understanding how our
donut actually runs. If we think of the donut as a play, the OS is the
theater: it manages the stage (processes), keeps actors from bumping into each
other (memory), stores the script (file system), and runs the lights and
sound (device drivers). The show doesn't happen without the theater.

### A Quick History: Why Operating Systems Exist

In the earliest computers (1940s–1950s), there was no OS. You loaded a
program by plugging cables or feeding punched cards, ran it until it finished,
and then the machine sat idle until a human loaded the next program. The
computer was expensive: millions of dollars. The human was cheap.

The operating system was invented to solve one problem: **keep the expensive
computer busy.** Early OSes simply loaded the next program automatically when
the current one finished (batch processing). Then they added the ability to
_run multiple programs at once_ (multiprogramming) so that when one program
waited for the disk, the CPU could work on another. Then they added interactive
time-sharing (the 1960s), so that many people could use the same computer from
different terminals. And finally, the personal computer (1980s) put the OS on
every desk.

Your laptop's OS (Linux, macOS, Windows) is the direct descendant of these
1960s time-sharing systems. The OS is still doing the same thing: keeping the
machine busy, managing resources, and letting many programs coexist. The
donut, your browser, your music player, and a hundred system services — all
sharing one CPU, one memory, one disk — is exactly the problem the OS was
built to solve.

### 1. Process Management

A **process** is a running program — one instance of your terminal, one browser
tab, one copy of the donut. Each process has its own memory, its own open
files, its own position in the code. It _thinks_ it has the whole machine to
itself.

How does a process get created? When you double-click the donut icon, the
OS's file system finds the donut executable, reads its header (which says "I
need this much memory" and "start at this instruction"), carves out a fresh
address space, loads the code into memory, sets up the stack and heap, and
transfers control to the program's entry point. From the program's
perspective, it suddenly exists with `main()` already running. Behind the
scenes, the OS did a dozen bookkeeping operations to make that look simple.

But your computer may have 200 processes running and only 4 or 8 CPU cores.
How do they all run at once? They don't — they **take turns**.

The OS contains a piece of software called the **scheduler**. It divides time
into tiny slices — typically about 10–100 milliseconds — and gives each process
a slice. After the slice ends, the scheduler _preempts_ the process (forces it
to pause), saves its state (every register value, the program counter, the
stack pointer), loads the next process's saved state, and hands it the CPU.

This happens thousands of times per second. To a human, it looks like
everything is running simultaneously. To the CPU, only one thing runs at a
time, and the scheduler is the traffic cop.

There are many scheduling algorithms, each suited to different situations.
A **round-robin** scheduler gives every process a turn in a fixed order —
fair, but not efficient if one process is more important. A **priority**
scheduler lets high-priority processes (like the audio player that must not
stutter) run before low-priority ones (like the background updater). Most
modern OSes use a **multi-level feedback queue**: processes start in a high-
priority queue and get demoted if they use up their time slice, which
naturally separates interactive programs (short bursts, high priority) from
CPU-heavy batch jobs (long bursts, low priority). The donut's terminal face,
which mostly waits for you to press a key, stays high-priority and responsive,
while a background video renderer sinks to the bottom queue and runs whenever
there's spare time.

```
   TIME ──────────────────────────────────────────────────────────►

   Process A  ████████░░░░████████░░░░████████░░░░████████░░░░
   Process B  ░░░░████████░░░░████████░░░░████████░░░░████████
   Process C  ░░░░░░░░████████░░░░████████░░░░████████░░░░░░░░

   ▲ the scheduler picks which process runs on each tick
```

**Threads** are like lighter-weight processes. A single process can have
multiple threads, all sharing the same memory and files but each with its own
stack and its own program counter. Think of a process as a house and threads as
the people inside it — they share the kitchen but each has their own room. The
donut's three faces (terminal, desktop, browser) could each run in a different
thread of the same process, sharing the backend state directly.

### 2. Memory Management

Every process thinks it owns all the RAM. Your donut program thinks it has
address 0 through 4 billion, all to itself. The terminal also thinks it owns
address 0 through 4 billion.

This is a lie — a very useful lie called **virtual memory**.

The OS, with help from a piece of hardware called the **MMU** (Memory
Management Unit), creates a fake address space for every process. When the
process reads or writes to "address 42," the MMU looks up a **page table** and
translates that to a real physical address, which may be anywhere in actual RAM.

```
   Process A's view:        MMU translation:        Physical RAM:
   ┌──────────────────┐    ┌─────────────┐         ┌──────────────┐
   │   page 0          │───►│ page table  │───────►│  frame 7     │
   │   page 1          │───►│ for A       │───┐    ├──────────────┤
   │   ...             │    └─────────────┘   │    │  frame 2     │
   └──────────────────┘                      │    ├──────────────┤
                                              └───►│  frame 12    │
   Process B's view:                                 └──────────────┘
   ┌──────────────────┐    ┌─────────────┐
   │   page 0          │───►│ page table  │───────►│  frame 5     │
   │   page 1          │───►│ for B       │───┐    ├──────────────┤
   │   ...             │    └─────────────┘   │    │  frame 9     │
   └──────────────────┘                       └───►│  frame 3     │
                                                      └──────────────┘
```

Memory is divided into chunks called **pages** (typically 4 KB each). Each
page of a process's virtual address space maps to a **frame** of physical
memory. Not every virtual page needs to be in RAM at once — if a process
accesses a page that isn't loaded, the MMU signals a **page fault**, and the
OS loads it from disk (called "swapping"). This is how you can run programs
that need more memory than your computer physically has.

**The donut connection.** When the donut's `render()` function writes to its
brightness grid, it's writing to virtual addresses. The MMU translates those
writes to real RAM. The OS ensures the donut's memory doesn't leak into the
browser's memory or vice versa. Each face of the donut is isolated —
processes can't see each other's data unless the OS explicitly allows it.

### 3. File Systems

Files are how data persists after a program ends. A **file system** is the OS's
system for storing, organizing, and retrieving files on disk.

The Unix file system is a tree of **directories** (folders) and files, starting
from the root `/`. Every file has metadata stored in a structure called an
**inode**: who owns it, what permissions it has, when it was created, and
most importantly, which disk blocks hold the file's data.

```
   Directory                Inode table                  Disk blocks
   ┌────────────┐          ┌──────────────┐            ┌────┐
   │ donut/     │─────────►│ inode 1001   │            │  ...  │
   │   .        │          │ type: dir    │            ├────┤
   │   ..       │          │ entries:     │───────────►│ file │
   │   src/     │          │   .   → 1001 │            │ data │
   └────────────┘          │   ..  →  999 │            ├────┤
                           │   src → 2002 │            │  ...  │
   ┌────────────┐          └──────────────┘            └────┘
   │ donut/src/ │          ┌──────────────┐
   │   donut.c  │─────────►│ inode 3003   │
   └────────────┘          │ type: file   │
                           │ size: 12 KB  │───────────►│  ...  │
                           │ blocks: [... ]│            ├────┤
                           └──────────────┘            │ code │
                                                        └────┘
```

The famous Unix principle "**everything is a file**" means that mice, keyboards,
screens, network connections, and even running processes are represented as
files in the file system. You can read from the keyboard by reading the file
`/dev/input/keyboard`. The donut's terminal face writes to `/dev/tty` — which
is a file. This unification is powerful: the same `read()` and `write()`
system calls work on everything.

> **One-breath aside.** Modern file systems (ext4, NTFS, APFS) are themselves
> astonishingly complex — they use B-trees for fast lookups, journaling to
> survive crashes, and copy-on-write to avoid corruption. But from the OS's
> perspective, they all present the same interface: `open`, `read`, `write`,
> `close`. The OS abstracts the hardware; the file system abstracts the disk.

### 4. Device Drivers

A **device driver** is a kernel module that knows how to talk to a specific
piece of hardware — your graphics card, your network card, your SSD. The
kernel speaks to drivers through a standard interface, and each driver speaks
to its device through the device's private protocol (often by talking to
registers in memory-mapped I/O space, as described in Part 0 L5).

When the donut's desktop face asks the OS to draw a pixel, the OS hands that
request to the graphics driver, which knows exactly which register to write to
on your specific GPU to make that pixel glow. The donut program never needs
to know what GPU you have — the OS and its drivers handle that.

## System Calls Revisited: Tracing the Donut's `write()`

Let's follow exactly what happens when the donut's terminal face calls
`write()`. This is the payoff — you now know enough to see the whole path.

```
   User space (the donut):
      1.  The donut's paint() function calls show().
      2.  show() formats the brightness grid into a string of characters.
      3.  show() calls printf(), which calls write(fd, buffer, size).
      4.  write() executes a special CPU instruction: "syscall" or "int 0x80".
      5.  The CPU switches to kernel mode and jumps to the kernel's syscall handler.

   Kernel space (the OS):
      6.  The kernel reads the syscall number (1 = write on Linux).
      7.  It validates the file descriptor fd — is this process allowed to write here?
      8.  It follows fd to the terminal device's file structure.
      9.  It calls the terminal driver's write function.
      10. The driver tells the GPU or terminal emulator to display the characters.
      11. The kernel returns control to user space, switching the mode bit back.
      12. The donut resumes, thinking it just "drew to screen."

   Physical (the hardware):
      13. The GPU reads pixels from its framebuffer memory.
      14. The display controller scans those pixels 60 times per second.
      15. Voltage on the display cable changes.
      16. A liquid crystal twists, or an LED glows. Light comes out.
```

That is 16 steps between a number in the donut's memory and actual light on
your screen. Steps 1–3 are the donut's own code. Step 4 is the boundary. Steps
5–11 are the OS. Steps 13–16 are pure physics.

Every system call — every `read`, `open`, `send`, `recv` — follows the same
pattern: trap into the kernel, validate, dispatch, do the work, return.

## The Three Faces, Revisited

Earlier in Part 0, we saw that the three faces of the donut make different
system calls:

- **Terminal face** → `write(fd, char_grid, size)` — write a string of
  characters to the terminal device.
- **Desktop face** → a window-system draw call (like X11's `XDrawString` or
  Wayland's `wl_surface_attach`) — a more complex set of system calls that
  talk to the compositor and GPU driver.
- **Browser face** → canvas draw calls via the browser's rendering engine,
  which itself talks to the OS through yet different interfaces — plus a
  `connect()` and `send()` call to fetch `donut.html` over the network.

Three completely different system call sequences. But they share the same
structure: **ask the OS**, **wait for the OS to do it**, **get back control**.
This is the universal pattern at L2. Every program, in every language, on
every operating system, touches hardware through this one bottleneck.

## What to Read Next

| Resource | What it covers |
|---|---|
| **CSAPP** (Computer Systems: A Programmer's Perspective, Chapters 8–10) | The definitive deep dive on processes, virtual memory, and system-level I/O. The `write()` trace above is a simplified version of CSAPP's treatment. |
| **Harvard CS50's Week 4** ("Memory") | A more approachable introduction to pointers, addresses, and how programs see memory — a good warm-up before tackling virtual memory in detail. |
| **"Three Easy Pieces"** (OSTEP — free online textbook) | The best full-length operating systems textbook. Chapters on scheduling, virtual memory, and file systems are especially good. |
| **Inside this book: Part 0 L3** | What happens at the instruction level when the kernel takes over — the CPU's interrupt handling, privilege levels, and context switching. |
| **Minix 3** (a tiny OS you can actually read) | Real, readable OS code. The original inspiration for Linux. Booting it in a VM and reading the scheduler is an education. |

Understanding the OS is the key that unlocks everything else in systems
programming. Every networking call, every database query, every distributed
system eventually goes through the kernel — and now you know what it does when
it gets there.
