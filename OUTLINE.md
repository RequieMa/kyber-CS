# kyber-CS — Book Outline

> **Narrative spine:** "How does that actually happen?" — a top-down descent through the
> abstraction stack, following one spinning donut from idea to electrons.
>
> **Thesis:** Software is abstracted ideas. Hardware is the faithful mirror of instructions.
>
> **Running example:** a spinning 3-D donut, rendered three ways (terminal / desktop window /
> browser) from one shared backend. Code lives in a separate repo (TBD); kyber-CS references it
> as the book's central demonstration.

---

## Part 0 · Bird's-Eye — One Continuous Descent

The map chapter. A self-contained 30-minute read that walks the full stack L0→L5→Synthesis
before any chapter dives deep. Adapted from `tutorial/CS/CS-syllabus.md`.

| # | Chapter | Layer | Question answered |
|---|---------|-------|-------------------|
| 0.0 | How to Read This | — | What kind of book this is, who it's for, how to use it |
| 0.1 | Framing: What Even Is a Computer? | L0 | Hardware = doer, Software = plan & material |
| 0.2 | Software: It's All Just Data and Rules | L1 | The three faces share one `render` idea; art style is just a parameter |
| 0.3 | Software ↔ OS: Programs Don't Touch Hardware | L2 | System calls, sandboxes, the OS as switchboard |
| 0.4 | Instructions: A Program Is a List of Tiny Commands | L3 | fetch–decode–execute, `x*cosA - y*sinA` → `mul, mul, sub` |
| 0.5 | Digital Logic: Instructions Are Built from Gates | L4 | Full adder = XOR + AND + OR; the clock; the hourglass narrows |
| 0.6 | Bits & Physics: A 1 Is a Voltage, a Gate Is a Switch | L5 | Transistor = electrically-controlled switch; photons to your eye |
| 0.7 | Synthesis: The Climb Back Up | — | The hourglass shape; abstraction as the whole game |

---

## Part 1 · Software — The Top of the Hourglass (L1 expanded)

Where ideas are weightless and infinitely recombinable. Data + rules, organized.

| # | Chapter | Status | Notes |
|---|---------|--------|-------|
| 1.1 | Programming Paradigms | ❌ missing | Imperative, OOP, FP, declarative — when and why each exists |
| 1.2 | Object-Oriented Programming | ✅ draft exists | `book/draft/oop/` — mindmap→overview→inherit→SOLID→design patterns→decoupling→frameworks (needs condensing) |
| 1.3 | Data Structures & Algorithms | ✅ draft exists | `book/draft/data-structure-algo/ds_al.ipynb` — needs text narrative |
| 1.4 | Languages & Compilers | ❌ missing | Python/JS/C converge to the same `mul, mul, sub` — the hourglass pinch |
| 1.5 | Software Engineering | ❌ missing | Testing, version control, CI/CD, the craft beyond the code |

### Existing draft materials mapping

- `book/draft/oop/` — 9 files covering OOP end-to-end. Use as backbone of ch.1.2, trim to ~3 sub-chapters.
- `book/draft/data-structure-algo/ds_al.ipynb` — Jupyter notebook, needs prose wrapper.
- `book/draft/computer-basis/basis.md` — L0 material, overlaps with Part 0.1; merge or place as appendix.

---

## Part 2 · Systems — The Boundary (L2 expanded)

Everything that happens at the "ask" boundary — OS, networking, databases, distribution.
This is the widest Part and the core of a CS education.

| # | Chapter | Status | Notes |
|---|---------|--------|-------|
| 2.1 | Operating Systems | ❌ missing | Processes, memory, file systems, concurrency, the kernel boundary |
| 2.2 | Computer Networking | ❌ missing | TCP/IP, HTTP, DNS, from a keypress to a remote server and back |
| 2.3 | Databases | ❌ missing | Relational model, SQL, transactions, ACID, NoSQL tradeoffs |
| 2.4 | Distributed Systems | ❌ missing | CAP theorem, consensus, fault tolerance, the cloud as a computer |

---

## Part 3 · Hardware — The Bottom of the Hourglass (L3–L5 expanded)

Where everything converges to one mechanism. Gates, circuits, architecture, physics.

| # | Chapter | Status | Notes |
|---|---------|--------|-------|
| 3.1 | Computer Architecture | ❌ missing | Von Neumann, CPU design, memory hierarchy, pipelining, caching |
| 3.2 | Digital Logic Design | ❌ missing | From NAND to ALU — the nand2tetris arc |
| 3.3 | Theory of Computation | ❌ missing | Turing machines, decidability, P vs NP, the limits of "computable" |
| 3.4 | Information Theory | ❌ missing | Shannon entropy, encoding, compression, error correction |

---

## Appendices

| # | Appendix | Status | Notes |
|---|----------|--------|-------|
| A | CS Timeline | ✅ draft exists | `book/en/en-timeline.md` + `book/zh/zh-timeline.md` — 1822→2014 |
| B | The Donut Code Walkthrough | ❌ TBD | Reference to sibling repo; annotated listing of `donut_core.py` + three faces |
| C | How to Use This Book (course tracks) | ❌ missing | "I'm a beginner" vs "I'm refreshing" vs "I'm teaching" — suggested paths |
| D | Further Reading by Layer | ❌ missing | CS50, nand2tetris, CSAPP, CLRS, etc. — keyed to each Part |

---

## Global notes

### Language strategy
- **English (`book/en/`):** primary text. Part 0 adapted from `CS-syllabus.md`.
- **中文 (`book/zh/`):** companion notes. Part 0 adapted from `CS-syllabus.zh-notes.md`.
  Chinese track is a condensed paraphrase, not a line-by-line translation — keep this approach
  for all chapters.

### Running example
- The spinning donut demo lives in a **separate repo** (TBD). `kyber-CS` references it with
  code snippets and figures; the reader clones the demo repo to run it.
- Part 0 is readable without running the code. Parts 1–3 optionally invite the reader to
  experiment.

### Writing order (per CLAUDE.md: "Finish one book before starting the next")
1. **Part 0** — adapt from `tutorial/CS/CS-syllabus.md` → ship as the first complete increment
2. **Part 1** — condense existing OOP draft + expand DSA; ship
3. **Part 2** — write OS/networking/databases/distributed; ship
4. **Part 3** — write architecture/logic/theory/information; ship
5. **Appendices** — timeline polish, donut walkthrough (once demo repo exists), course tracks

### Missing vs. existing
- **Existing draft material:** OOP (9 files), DSA (1 notebook), computer-basis (1 file),
  timeline (EN + ZH), zhihu answers/articles (reference only)
- **Missing and must-write:** OS, networking, databases, distributed systems, architecture,
  digital logic, theory of computation, information theory, programming paradigms,
  languages & compilers, software engineering

---

## Relationship to other kyber-* books

```
kyber-maths     →  the mathematical foundation (calculus, linear algebra, probability, stats)
kyber-CS        →  the computational stack (this book)
kyber-physics   →  forces, flows, motion — physics for cybernetic systems
kyber-ml        →  learning systems — where maths + CS + physics converge
```

`kyber-CS` assumes `kyber-maths` as prerequisite (or at least co-requisite) for Parts 2–3.
Part 0 and Part 1 require only high-school algebra.
