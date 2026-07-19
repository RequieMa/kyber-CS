---
title: "L2.3 · Databases — When Programs Need to Remember"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L2.3 · Databases — When Programs Need to Remember

```
   Part 0  L2  software ↔ OS        (the big picture)
   Part 2  L2.1 operating systems
   Part 2  L2.2 networking
   Part 2  L2.3 databases           ◀ you are here
   Part 2  L2.4 distributed systems
```

**The question carried down:** Programs run, produce data, and stop. The data
disappears. How do we make data survive across restarts, across crashes, across
years? Every program you've seen so far — the donut included — treats data as
something that exists only while the program is running. But the world doesn't
work that way. Your bank balance, your email, your YouTube watch history,
every like, every comment — all of it outlives the programs that created it.

**The idea.** A database is a program that _remembers_. It sits between your
application and the disk, managing the messy reality of storage so your
program doesn't have to. It answers two questions that every serious program
eventually asks: "how do I save data so I can find it later?" and "how do I
keep that data correct when many things are happening at once?"

## The Donut's Missing Feature

Remember the donut's state from Part 0 L1? It was tiny:

```python
state = {
    "A": 1.0,       # rotation angle around one axis
    "B": 1.0,       # rotation angle around the other axis
    "pos": 50,      # position on screen (0-100)
}
```

This lives in memory. When the program stops — you close the window, the
computer shuts down, the power flickers — that state is gone. When you start
the donut again, it starts from `A=1.0, B=1.0, pos=50` as if nothing ever
happened.

Now suppose you wanted more. You want to record _every single spin_ — every
state, every frame — and then replay the donut's entire history, or analyze
which angles people prefer, or find the most popular position. Suddenly "it
lives in memory" is not enough. You need something that persists.

That's a database. The donut's state is so small that a text file would work
just fine — but the _problems_ a database solves (saving data, finding it
fast, keeping it consistent) are the same at every scale, from a donut log to
YouTube's entire video catalog.

## Why Not Just Use a File?

You _could_ save the donut's state to a file:

```
# donut_state.txt
A=1.0  B=1.0  pos=50  timestamp=2026-07-19T12:00:01
A=1.1  B=1.0  pos=50  timestamp=2026-07-19T12:00:02
A=1.1  B=1.1  pos=50  timestamp=2026-07-19T12:00:03
...
```

This works! For one program writing one stream of data, a file is fine. In
fact, many database systems are built on top of files — they just add a lot
of structure and safety around them. But problems appear quickly as your needs
grow:

- **Finding data.** If you saved 10 million frames and want "all frames where
  `A` was between 2.0 and 2.5," you'd have to read every line. At 60 frames
  per second, 10 million frames is about two days of donut spinning — plausible
  for a weekend art project. Scanning every file for a specific value is called
  a **full table scan**, and it's the slowest thing a database can do.
- **Multiple writers.** If two copies of the donut both write to the same file,
  they'd overwrite each other. The file would become garbage.
- **Consistency.** What if the power fails in the middle of writing one line?
  The file might contain `A=1.0  B=` and nothing else — half a record.
- **Structure.** As your data gets more complex (multiple donuts, user
  preferences, comments on frames), a flat file becomes impossible to manage.

A database is a program that handles all of these problems. It sits between
your code and the file system, managing reads, writes, search, consistency,
and concurrency.

## The Relational Model

The most widely used kind of database is the **relational database**. It was
invented by Edgar Codd at IBM in 1970, and the core idea is deceptively
simple: **organize data into tables with rows and columns, and use relationships
between tables to represent the world.**

Let's design a database for the donut. Instead of one flat log file, we split
the data into tables:

```
   ┌─────────────────────────────────────────────────────┐
   │  Table: spins                                        │
   ├──────┬──────┬──────┬──────┬──────────────────────────┤
   │  id  │  A   │  B   │  pos │  timestamp               │
   ├──────┼──────┼──────┼──────┼──────────────────────────┤
   │  1   │ 1.0  │ 1.0  │  50  │ 2026-07-19 12:00:01     │
   │  2   │ 1.1  │ 1.0  │  50  │ 2026-07-19 12:00:02     │
   │  3   │ 1.1  │ 1.1  │  50  │ 2026-07-19 12:00:03     │
   │  4   │ 1.2  │ 1.1  │  51  │ 2026-07-19 12:00:04     │
   └──────┴──────┴──────┴──────┴──────────────────────────┘

   ┌──────────────────────────────────────────────────────┐
   │  Table: users                                        │
   ├──────┬──────────┬──────────────────┬──────────────────┤
   │  id  │  name    │  email           │  created_at      │
   ├──────┼──────────┼──────────────────┼──────────────────┤
   │  1   │  Alice   │ alice@ex.com     │ 2026-01-15       │
   │  2   │  Bob     │ bob@ex.com       │ 2026-03-20       │
   └──────┴──────────┴──────────────────┴──────────────────┘
```

Notice the relationship: if each spin was created by a user, we could add a
`user_id` column to the `spins` table. That's the "relational" part — separate
tables connected by shared values.

## SQL: Speaking to the Database

To talk to a relational database, you use **SQL** (Structured Query Language,
pronounced "sequel" or "S-Q-L"). SQL is **declarative**: you say _what_ you
want, not _how_ to get it.

```sql
-- Find all spins where the donut was especially fast
SELECT timestamp, A, B
FROM spins
WHERE A > 3.0 AND B > 2.5
ORDER BY timestamp DESC
LIMIT 10;
```

Read this as: "Give me the timestamps and angles of the 10 fastest spins,
sorted most recent first." You don't tell the database how to search — you
just describe the result. The database figures out the fastest way to find it.

Other common operations:

```sql
-- Insert a new spin (the donut does this every frame)
INSERT INTO spins (A, B, pos, timestamp)
VALUES (1.5, 2.0, 55, '2026-07-19 12:00:05');

-- How many spins did each user record?
SELECT users.name, COUNT(spins.id) AS spin_count
FROM users JOIN spins ON users.id = spins.user_id
GROUP BY users.name;
```

SQL is the language of data. It's used everywhere — which is why it's worth
learning even if you never become a database administrator.

> **One-breath aside.** SQL was invented in the 1970s and looks like it. But
> its age is a feature, not a bug. Every database system — PostgreSQL, MySQL,
> SQLite, Oracle, SQL Server — speaks some version of SQL. You can learn it
> once and use it across all of them. Newer languages (like NoSQL query
> languages) are often just SQL with different syntax and fewer features.

## Indexes: Finding Things Fast

Without an index, finding a row in a table means scanning every single row.
For 10 donut frames that's nothing. For 10 billion frames, it's impossible.

An **index** is a separate data structure that the database maintains to make
lookups fast. The most common type is a **B-tree** (balanced tree), which lets
the database find a value in logarithmic time — roughly 30 reads to find
anything among a billion rows, instead of scanning the whole billion.

Here's the intuition: a B-tree is like a phonebook. If you want to find
"Smith" in a billion-name phonebook:

- Open to the middle. You hit "M." Smith is after M — skip the first half.
- Open to the middle of the remaining half. You hit "R." Still before Smith.
- Open again. "T." Too far — go back.
- A few more halvings and you're at "S" → "Sm" → "Smi" → "Smith."

The database does the same with B-trees: each node in the tree tells it which
branch to follow, and the tree stays balanced (which is the "B" part) no matter
how many rows you add or remove. A B-tree with `n` entries has a depth of
roughly `log(n)`. For a billion rows, that's about 30 levels. Every read is
30 tiny comparisons instead of a billion. That is the difference between a
query that takes microseconds and one that takes minutes.

In practice, modern B-tree nodes are much wider than one comparison — a node
might hold hundreds of key-pointer pairs, fitting in a single disk block
(usually 4–16 KB). This makes the tree very short and wide: a billion-row
index might be only 3–4 levels deep, because each node holds hundreds of
entries. The database reads one block from disk per level, and each read is
a single `O(1)` disk seek. Result: even a massive table can be searched in
3–4 disk reads, which is fast enough for interactive queries.

```sql
-- Create an index on the A column of the spins table
CREATE INDEX idx_spins_A ON spins(A);

-- Now this query takes milliseconds instead of hours:
SELECT * FROM spins WHERE A BETWEEN 2.0 AND 2.5;
```

The downside: indexes make writes slightly slower (the database has to update
the index tree when you insert a row). But they make reads dramatically faster.
In practice, you index the columns you search or sort by, and leave the rest.

## Transactions and ACID

Here is the hardest problem databases solve. Imagine two people both try to
book the last seat on a flight. The airline's database has:

```
   Table: seats
   ┌──────┬──────────┬──────────┐
   │  id  │  flight  │  booked  │
   ├──────┼──────────┼──────────┤
   │ 42A  │  BA249   │  false   │
   └──────┴──────────┴──────────┘
```

If both customers click "Book" simultaneously, the database might do this:

```
   Request 1 reads: seat 42A is not booked → true
   Request 2 reads: seat 42A is not booked → true    ← both see "free"
   Request 1 writes: set seat 42A to booked
   Request 2 writes: set seat 42A to booked           ← double-booked!
```

This is a **race condition**, and it's exactly the same class of problem we
saw in the L2.1 scheduling discussion — two things happening at once,
interfering with each other.

Databases solve this with **transactions** and the **ACID** properties.
A transaction is a group of operations that the database treats as "all or
nothing." ACID stands for:

- **Atomicity.** Either all the operations in a transaction happen, or none
  of them do. If the power fails halfway through, the database undoes
  everything. No half-written records.
- **Consistency.** The database never violates its own rules. If you said
  "every spin must have a user_id," the database enforces it.
- **Isolation.** Each transaction runs as if it were alone. The database
  prevents the double-booking scenario above — it locks the row so the second
  request waits until the first is done.
- **Durability.** Once a transaction is committed, it stays committed — even
  through a power failure. The data is safely on disk.

```sql
BEGIN TRANSACTION;

-- All or nothing
UPDATE seats SET booked = true WHERE id = '42A' AND flight = 'BA249';
INSERT INTO bookings (user_id, seat_id) VALUES (1, '42A');

COMMIT;
```

If two requests run this transaction at the same time, the database ensures
that only one succeeds. The other either gets an error or waits. No
double-booking.

Now apply this to the donut: if two users both pressed **→** at the exact
same moment to change the spin speed, the donut's state update `A += 0.1`
could lose one of the updates. A transaction prevents that.

## NoSQL: When the Relational Model Doesn't Fit

Relational databases are powerful, but they're not the answer to every
problem. Starting around 2005, a new class of databases emerged called
**NoSQL** (Not Only SQL).

Relational databases assume your data has a fixed **schema** — you define
tables and columns before inserting data. NoSQL databases relax this in
different ways:

**Document stores** (like MongoDB) store JSON-like documents, each of which
can have different fields. Good for data that doesn't fit neatly into rows
and columns — user profiles with optional fields, for example.

```json
{
  "user": "alice",
  "donut_preferences": {
    "speed": "fast",
    "color_scheme": "neon",
    "last_spin": "2026-07-19T12:00:00Z"
  }
}
```

**Key-value stores** (like Redis) are the simplest possible database: store a
value by its key. Blazingly fast, but you can only look up by key. The donut's
state `A=1.0, B=1.0, pos=50` is a perfect fit for a key-value store (and Redis
could serve the donut state to thousands of viewers in real time).

**Wide-column stores** (like Cassandra) and **graph databases** (like Neo4j)
cover other niches.

NoSQL databases typically sacrifice one or more ACID guarantees for
performance or scalability. They are "eventually consistent" instead of
"immediately consistent" — which works fine for a donut that updates 60 times
per second, but not for that last airplane seat.

> **One-breath aside.** The "NoSQL vs SQL" debate is often overblown. Modern
> databases are converging: PostgreSQL now supports JSON columns, many NoSQL
> databases support transactions, and the best architecture often uses both —
> PostgreSQL for bookings (needs ACID) and Redis for donut state (needs speed).
> There is no One True Database. There are only tradeoffs.

## The Donut, Revisited: When Would You Need a Database?

The donut's state is tiny — three numbers. A database for three numbers is
absurd. But let's push the donut to the edge:

- **Recording every frame for replay analysis.** Every spin, every angle,
  every position, for a year. At 60 frames per second, that's about 1.9
  billion rows. A file can't handle that. A database with an index on
  `timestamp` can.
- **Multi-player donut.** Thousands of people each control their own donut
  on a shared screen. Every donut's state, every user's preferences, every
  configuration — this is a relational problem: `users` table, `donuts`
  table, `spins` table, joined by relationships.
- **Leaderboard.** Whose donut has spun the most total degrees? The database
  answers in milliseconds with an `ORDER BY total_degrees DESC LIMIT 10`.
- **Caching the current state for millions of viewers.** A single server
  can't handle millions of connections. But a key-value cache (Redis) in
  front of a relational database can: the cache serves the current state to
  viewers instantly, and the database stores the history reliably.

The database pattern emerges naturally as soon as your program needs to
_remember_ in a way that survives the program itself, and needs to _find_
among things it remembered.

## What to Read Next

| Resource | What it covers |
|---|---|
| **"Use the Index, Luke"** (free online book) | The best practical guide to database indexing — teaches you to think in terms of index access paths. |
| **SQLite** (tool -- `sqlite3` is on almost every machine) | The simplest database to experiment with. Create the `spins` table above, insert a million rows, and practice `SELECT` queries. |
| **"Designing Data-Intensive Applications"** (Kleppmann) | The definitive book on databases and distributed data systems — readable and deep. |
| **PostgreSQL Tutorial** (free online) | PostgreSQL is the gold standard of open-source relational databases. Learning it teaches you everything about the relational model. |
| **Inside this book: L2.4 (Distributed Systems)** | What happens when your database outgrows one machine? |

The database is your program's memory that lasts. Like human memory, it's
imperfect — transactions try to keep it accurate, indexes make it fast, and
NoSQL accepts a little fuzziness in exchange for speed. But the basic question
is always the same: when this program stops, what should it remember?
