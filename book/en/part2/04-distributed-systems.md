---
title: "L2.4 · Distributed Systems — When One Computer Isn't Enough"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L2.4 · Distributed Systems — When One Computer Isn't Enough

```
   Part 0  L2  software ↔ OS        (the big picture)
   Part 2  L2.1 operating systems
   Part 2  L2.2 networking
   Part 2  L2.3 databases
   Part 2  L2.4 distributed systems ◀ you are here
```

**The question carried down:** Everything we've looked at so far lives on one
machine — one CPU, one OS, one disk. What changes when we connect a thousand
machines and ask them to act as one?

**The idea.** A distributed system is a collection of independent computers
that appears to the user as a single coherent system. Google appears to be one
web site, but it runs on millions of machines. YouTube appears to be one video
player, but it spans data centers on every continent.

The hard truth: **distributed systems are fundamentally different from
single-machine systems.** Every assumption that holds on one machine breaks
when you connect two.

## The Donut, Scaled

Our donut runs on one machine. One backend, three faces, all on your laptop.
Nothing is shared, nothing fails unexpectedly, and everything is instant.

Now imagine a million people want to watch the same donut spin in perfect sync.
They should all see the same `A` and `B` at the same time. When one person
presses **→** to speed it up, everyone sees the change within a fraction of a
second.

This is a distributed systems problem. Here is why it is hard:

```
   Naive approach:                   The reality:
   ┌──────────────────────┐          ┌──────────────────────┐
   │  One server sends    │          │  Network is slow      │
   │  state to all viewers│          │  Some viewers are     │
   │  every frame.        │          │  behind. Messages     │
   │  Works like a TV     │          │  get lost. People     │
   │  broadcast.          │          │  press → at the       │
   │                      │          │  same time. What      │
   │  Problem solved?     │          │  happens? Chaos.      │
   └──────────────────────┘          └──────────────────────┘
```

Every difficulty in distributed systems comes down to one thing: **you cannot
rely on anything.** You cannot rely on the network being fast, the other
machine being up, or two events happening in the same order on different
machines.

## The Fallacies of Distributed Computing

In the 1990s, researchers at Sun Microsystems codified the **eight fallacies
of distributed computing** — assumptions that beginners make and experts know
are false. Here are the most important ones:

**1. The network is reliable.** It isn't. Packets get lost, cables get cut,
routers crash. A distributed system must handle the network failing at any
moment.

**2. Latency is zero.** It isn't. Reading from RAM on the same machine takes
~100 nanoseconds. Sending a packet to a server across the country takes ~50
milliseconds. That's 500,000 times slower. Distributed systems must be
designed _around_ this fact — every remote call is an eternity.

**3. Bandwidth is infinite.** It isn't. Moving data between machines is
expensive. Sending the full history of every donut frame to every viewer
would saturate any network immediately.

**4. The network is secure.** It isn't. Anything you send can be read or
modified by anyone between you and the destination.

**5. Topology doesn't change.** It does. Servers are added, removed, upgraded.
A good distributed system handles this without downtime.

**6. There is one administrator.** There isn't. Different machines may be
owned by different organizations, with different policies and failure modes.

**7. Transport cost is zero.** It isn't. Serializing data, compressing it,
sending it, receiving it, deserializing it — all of this costs CPU time and
power.

**8. The network is homogeneous.** It isn't. Some viewers are on gigabit
Ethernet, some on spotty 3G. Your system must work for all of them.

> **One-breath aside.** These fallacies sound pessimistic, but they're
> empowering. Once you accept them, you stop designing for the ideal case and
> start designing for the _worst_ case — which is the only case that
> eventually happens at scale. The Internet itself is the proof that it's
> possible: every day, billions of machines that assume nothing about each
> other somehow cooperate.

## The CAP Theorem

The CAP theorem is the most important result in distributed systems. It says:
a distributed data system can guarantee at most two of these three properties:

- **Consistency:** Every read sees the most recent write. All viewers see the
  same donut state at the same time.
- **Availability:** Every request gets a response (even if it's not the most
  recent data). The donut keeps spinning even if some servers are down.
- **Partition tolerance:** The system continues to work even if the network
  splits (a "partition") — the servers in one data center can't talk to the
  servers in another.

The theorem says: if the network splits (which it will — see fallacy #1), you
_must_ choose between consistency and availability. You cannot have both.

```
         Consistency
             │
             │  ✦  CA systems (rare — they can't survive partitions)
             │     Traditional relational DBs, single-site only
             │
             │
    ┌────────┴────────┐  CP systems (consistent but may refuse requests)
    │                  │  Banking: better to refuse a withdrawal than
    │                  │  show a wrong balance
    │                  │
    │                  │
    Availability ──────┴────── Partition Tolerance
                        │
                        │  AP systems (available but possibly stale)
                        │  Social media: better to show an old donut
                        │  state than to show nothing
                        │
                        │
```

For the million-viewer donut: if the network between data centers gets cut,
do you:

- **CP:** Stop updating the donut for viewers on one side of the cut until
  the network heals? (They see a frozen donut, but it's correct.)
- **AP:** Let each side show its own slightly different version of the donut?
  (The donut keeps spinning, but viewers on different sides see different
  angles until the network heals.)

There is no right answer. It depends on what you're building. A flight
control system chooses CP. A multiplayer game often chooses AP.

## Consensus: Getting Machines to Agree

The most fundamental problem in distributed systems is **consensus**: getting
multiple machines to agree on something. What was the donut's state at exactly
12:00:00 UTC? Which viewer pressed **→** first? Which server should handle
each request?

Consensus is harder than it sounds because machines can fail, messages can be
lost, and messages can be delayed. A naive approach ("just vote") fails
because a failed machine votes "no" and a delayed message arrives after the
vote is over.

Two algorithms have become standard solutions:

**Paxos** (Leslie Lamport, 1989) was the first practical consensus algorithm.
It works in rounds: one machine is the "proposer" who suggests a value, and
a group of "acceptors" vote on it. If a majority accepts, the value is
decided. Paxos handles failures because a value is only decided when a
_quorum_ — a majority — agrees. A minority of failed machines cannot block the
decision.

Paxos is notoriously difficult to understand (even Lamport struggled to
explain it — his original paper used an analogy about a parliament on an
ancient Greek island). In practice, a newer algorithm called **Raft** has
largely replaced it for new systems.

**Raft** (Diego Ongaro, 2013) breaks consensus into three sub-problems:

1. **Leader election.** The machines pick one leader. If the leader fails,
   the remaining machines detect it (through timeouts) and elect a new one.
2. **Log replication.** The leader receives all updates, writes them to its
   own log, and sends copies to the followers. When a majority confirms they
   have the update, the leader commits it.
3. **Safety.** If a leader fails during replication, the new leader checks
   which updates were actually committed and fills any gaps before accepting
   new ones.

The result: a group of machines that behave like one reliable machine, even
though any individual machine can fail at any time. Tools like **etcd** and
**Consul** implement Raft, and they are the backbone of cloud infrastructure.

When a million people watch the donut, a Raft-based system could maintain one
authoritative donut state across multiple servers. If one server dies, the
others seamlessly take over. The donut never stops spinning.

## The Cloud: Someone Else's Computer

The **cloud** (AWS, Google Cloud, Azure) is the practical embodiment of
distributed systems. When you upload the donut to a cloud provider, here's
what happens:

- Your donut runs on one of millions of virtual machines in a data center
  somewhere.
- The cloud provider handles the networking, storage, power, cooling, and
  physical security.
- If the machine your donut is running on fails, the provider automatically
  starts it on another machine.
- If your donut becomes popular (hello, million viewers), you add more
  machines, and a **load balancer** distributes viewers across them.

From the cloud provider's perspective, they are running a distributed system
at enormous scale. From yours, you are calling APIs to create virtual
machines, databases, and load balancers — which is just asking someone else's
OS to do work, at a higher level.

```
   ┌──────────────────────────────────────────────────────────┐
   │  YOUR APPLICATION                                         │
   │  "I want the donut to run on 20 machines"                │
   │                                                           │
   │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐      │
   │  │ D │ │ D │ │ D │ │ D │ │ D │ │ D │ │ D │ │ D │      │
   │  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘      │
   │                                                           │
   │  ┌──────────────────────────────────────────────────┐    │
   │  │  CLOUD PROVIDER'S DISTRIBUTED SYSTEM              │    │
   │  │  "I will run your containers, handle failures,   │    │
   │  │   scale up/down, route traffic, store data"      │    │
   │  └──────────────────────────────────────────────────┘    │
   │                                                           │
   │  ┌──────────────────────────────────────────────────┐    │
   │  │  PHYSICAL DATA CENTER                             │    │
   │  │  "Here are 100,000 servers, network, power"      │    │
   │  └──────────────────────────────────────────────────┘    │
   └──────────────────────────────────────────────────────────┘
```

## MapReduce: Bring the Computation to the Data

One of the most influential ideas in distributed computing is **MapReduce**,
popularized by Google in 2004. It solves a specific problem: how do you
process enormous datasets (petabytes) across thousands of machines when
moving the data is too expensive?

The answer is the opposite of what seems natural. Instead of moving all the
data to one machine and processing it there, you **send the processing code
to where the data already lives**.

```
   Traditional approach:                MapReduce approach:

   Data ──────────► One big machine     Machine 1 ──► processes its chunk
        (expensive to move)             Machine 2 ──► processes its chunk
                                        Machine 3 ──► processes its chunk
                                        Machine 4 ──► processes its chunk
                                             │
                                             │ (just the tiny results move)
                                             ▼
                                      One machine combines results
```

MapReduce has two phases:

- **Map:** Each machine reads its local chunk of data and produces a set of
  key-value pairs. For the donut: each machine processes the spin logs stored
  on its own disk and emits `(user_id, total_spin_degrees)`.
- **Reduce:** The machines shuffle the key-value pairs so all values for the
  same key land on the same machine. Then each machine combines them. Result:
  the total spin degrees per user.

This pattern appears everywhere in modern systems. Hadoop is the open-source
MapReduce implementation. Spark is its faster successor. Even SQL databases
use the same map/reduce idea internally for parallel queries.

## Bringing It All Together: The Million-Viewer Donut

Let's design the million-viewer donut as a distributed system. What does it
need?

```
   MILLION-VIEWER DONUT ARCHITECTURE

                         ┌─────────────────────┐
                         │  DNS + Load Balancer  │
                         │  "Send each viewer    │
                         │   to the nearest      │
                         │   available server"   │
                         └──────┬──────────────┘
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                   ▼
   ┌──────────────────┐ ┌──────────────┐  ┌──────────────┐
   │  Raft Cluster     │ │  Cache (AP)  │  │  Cache (AP)  │
   │  (CP — the donut  │ │  Serve state │  │  Serve state │
   │   state is the    │ │  to viewers  │  │  to viewers  │
   │   source of truth)│ │  FAST        │  │  FAST        │
   └──────────────────┘ └──────────────┘  └──────────────┘
              │
              ▼
   ┌─────────────────────┐
   │  Database (CP)      │
   │  "Record every spin, │
   │   every event, for   │
   │   replay & analysis" │
   └─────────────────────┘
```

The key insight: the million-viewer donut is not one system — it's _several
systems_ working together, each making different CAP tradeoffs:

- **Raft cluster** (the backend): CP — guarantees a single, consistent donut
  state. If one machine fails, the cluster picks a new leader. The donut
  doesn't stop.
- **Cache layer:** AP — serves the current state to viewers as fast as
  possible. May be slightly stale (a few milliseconds behind), but viewers
  won't notice. If a cache server fails, viewers go to another one.
- **Database:** CP — every frame is recorded exactly once, in order. If the
  database is temporarily unavailable, the frames buffer in a queue and are
  written when it recovers.

The distributed donut is not one program. It is a constellation of programs,
each with a different job, communicating across the network — tolerating
failures, managing latency, and making the tradeoffs that CAP requires.

## The Thread That Connects

Every layer we've studied feeds into this one:

- **The OS (L2.1)** provides the basic sandbox — each machine runs its own
  OS, its own processes, its own virtual memory.
- **Networking (L2.2)** connects the machines — system calls that leave the
  machine, carrying packets between the sandboxes.
- **Databases (L2.3)** give the system memory that persists — but now that
  memory is distributed across machines, and CAP says we must choose.
- **Distributed systems (L2.4)** is all of the above, plus the understanding
  that every promise a single machine can make is contingent on the network
  keeping its own promises — which it won't, always.

The deepest lesson of distributed systems is also the simplest: **the
network is the weakest link, and everything you build must be designed around
that fact.** Once you accept it, you can build systems that survive crashed
machines, cut cables, and overloaded routers — and to the user, they look
like one donut, spinning peacefully, unbothered by the chaos underneath.

## What to Read Next

| Resource | What it covers |
|---|---|
| **"Designing Data-Intensive Applications"** (Kleppmann) | The single best book on distributed systems for practitioners. Chapters on replication, partitioning, transactions, and consensus are transformative. |
| **"The Raft Paper"** (ongaro.github.io/raft) | The original Raft paper is unusually readable — it's written to be understood, not just cited. |
| **"Fallacies of Distributed Computing"** (various sources) | The original Sun Microsystems paper. Every engineer should memorize these. |
| **MIT 6.824** (free online course, now 6.5840) | Stanford's CS244b is also excellent. Both involve implementing Raft from scratch — one of the most educational experiences in CS. |
| **Inside this book: L2.2 (Networking)** | The foundation — distributed systems start where networking leaves off. |

Distributed systems is the capstone of the systems stack. From one program
asking its OS to draw a character, to a million viewers watching the same
donut across a planet — the pattern is the same. It just needs more machines,
more patience, and a healthy respect for network partitions.
