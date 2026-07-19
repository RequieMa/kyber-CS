---
title: "1.3 · Data Structures & Algorithms — How to Hold and Reshape Data"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# 1.3 · Data Structures & Algorithms — How to Hold and Reshape Data

In Part 0 L1, we said all software does is **hold data and reshape it according
to rules**. The "rules" part gets the glory — algorithms! — but the "hold" part
is equally important. The choice of *how* you store the data determines what you
can do with it, and how fast.

## The Equation

Niklaus Wirth, the creator of Pascal, titled one of his books with the most famous
equation in computer science:

> **Algorithms + Data Structures = Programs**

He wasn't being reductive. He was naming the two halves of every program:
- **Data structures** are how you organize information in memory.
- **Algorithms** are the procedures that reshape that information.

The two are inseparable. A brilliant algorithm on the wrong data structure is
slow. The right data structure with a naive algorithm is still slow. You design
them together.

## Data Structures — The Shapes Data Takes

### Arrays and Lists

The simplest structure: a contiguous block of memory holding elements in order.
**Random access** is instant — `grid[i][j]` is one multiplication and one
addition for the CPU. But inserting in the middle is expensive: everything after
must shift.

```python
# Array: fast read, slow insert-in-middle
grid = [[0] * 80 for _ in range(24)]   # 24 rows × 80 columns
grid[10][40] = 7                        # instant — just math
```

Our donut's brightness grid is a 2-D array. The render function writes brightness
values to `grid[y][x]`, and the paint function reads them back. Arrays are the
natural structure when you know the size in advance and need random access.

A **linked list** trades random access for fast insertion: each element points to
the next. To find element 100, you walk through 99 pointers. But to insert in the
middle, you only change two pointers.

### Stacks and Queues

A **stack** is a last-in-first-out (LIFO) structure. Push onto the top; pop from
the top. It's the structure behind function calls: when `render()` calls
`rotate()`, the CPU pushes the return address onto the call stack.

A **queue** is first-in-first-out (FIFO). Enqueue at the back; dequeue from the
front. It's the structure behind event handling: the OS queues up keyboard events,
and the program dequeues them one at a time. Our donut's `poll_events()` is
reading from a queue the OS maintains.

### Hash Tables

A hash table (dictionary, map, associative array) is the swiss army knife of data
structures: you give it a **key**, it gives you back the **value** in constant
time. Under the hood, a hash function converts the key to an array index:

```python
state = {"A": 1.0, "B": 1.0, "pos": 50}
state["A"]      # hash("A") → index → 1.0 — instant
```

Our donut's state is a dictionary. For three keys, any structure would work. For
three million keys? Hash tables are the only structure that gives you O(1) lookup.

### Trees

A tree is a hierarchical structure: a root node, branches, leaves. Trees model
anything with nested containment: file systems (folders within folders), HTML
pages (elements within elements), organization charts.

A **binary search tree** keeps elements sorted: everything in the left subtree is
smaller, everything in the right is larger. Searching is O(log n) — you eliminate
half the tree at each step.

### Graphs

A graph is nodes connected by edges. Trees are a special case (no cycles). Graphs
model networks: social graphs, road maps, the internet itself. Graph algorithms
(finding shortest paths, detecting communities) are among the most practically
useful in all of CS.

## Algorithms — The Rules for Reshaping Data

### What "Fast" Means: Big-O Intuition

An algorithm's speed isn't measured in seconds — that depends on the hardware.
It's measured in *how the work grows as the input grows*. This is **Big-O
notation**:

| Notation | Name | What it means |
|---|---|---|
| O(1) | Constant | Same speed regardless of input size. Hash table lookup. |
| O(log n) | Logarithmic | Each step halves the problem. Binary search. |
| O(n) | Linear | Work grows proportionally to input. Scanning an array. |
| O(n log n) | Linearithmic | Slightly worse than linear. Fast sorting algorithms. |
| O(n²) | Quadratic | Double the input → quadruple the work. Nested loops. |
| O(2ⁿ) | Exponential | Each additional item doubles the work. Brute-force. |

Our donut's `render()` function has nested loops over theta and phi — that's
O(n²) in the number of sample points. For a 80×24 terminal grid, that's fine. For
a 4K display at 60fps? You'd need a more efficient approach (like a GPU shader).

### Sorting

Sorting is the most studied problem in computer science. The best
comparison-based sorts run in O(n log n) — quicksort, mergesort, heapsort.

The deep insight: you can't sort *n* items by comparing them pairwise in fewer
than O(n log n) operations. This is a **lower bound** — a proof that no algorithm
can do better. Knowing what *can't* be done is as important as knowing what can.

### Searching

Given a sorted array, **binary search** finds an element in O(log n): check the
middle, eliminate half, repeat. For a million elements, that's ~20 comparisons
instead of ~500,000 on average.

But searching isn't just about finding a value. **Graph search** — finding a path
from A to B — is what powers GPS navigation, network routing, and game AI.
Breadth-first search (BFS) explores outward in rings; depth-first search (DFS)
goes as deep as possible before backtracking.

### Recursion — A Function That Calls Itself

Recursion is a function that calls itself on a smaller version of the same
problem. It's the natural way to process trees (each subtree is itself a tree)
and the elegant way to express divide-and-conquer algorithms (quicksort,
mergesort).

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Recursion maps directly to the call stack (that LIFO structure). Each recursive
call pushes a new frame onto the stack. When the base case is reached, the stack
unwinds. Understanding recursion is understanding the call stack — which is L2
territory.

## The Donut's Data Structures

Our donut program uses almost every fundamental structure:

| Structure | Where in the donut | Why |
|---|---|---|
| 2-D Array | Brightness grid `grid[y][x]` | Random access by coordinates |
| Dictionary | `state = {"A": 1.0, "B": 1.0}` | Named access to state |
| List | `RAMPS` lookup table | Indexed by brightness level |
| Queue | OS event queue → `poll_events()` | FIFO input handling |
| Stack | Call stack during `render()` → `rotate()` → `project()` | Function calls |

The donut is simple enough that any data structure would work. But the *pattern* —
choosing the right structure for the access pattern — is universal. A database
index is a B-tree for the same reason the brightness grid is an array: the access
pattern determines the structure.

> **One-breath aside.** The study of data structures and algorithms is where
> computer science most directly touches mathematics. A course in *Design and
> Analysis of Algorithms* will formalize Big-O, teach you to prove correctness,
> and introduce you to the deep theory: what can be computed efficiently, and
> what (probably) can't. That's the bridge to Part 3's theory of computation.
