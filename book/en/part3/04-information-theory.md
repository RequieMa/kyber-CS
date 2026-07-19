---
title: Information Theory — What Even Is Information?
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# Information Theory — What Even Is Information?

```
    L0  framing                     ▲  "a donut"
    L1  software                    │  reshaping data
    L2  software ↔ OS               │  by asking the OS
    L3  instructions                │  which runs tiny commands
    L3  DEEP: ARCHITECTURE          │  how the CPU is built to run them
    L4  digital logic               │  built from gates
    THEORY OF COMPUTATION           │  what computation even IS
  ▶ INFORMATION THEORY              │  what information even IS
    L5  bits & physics              │  made of switching voltages
                                    └─── the deepest layer: the mathematics of surprise
```

**The question:** We've talked about bits, data, and voltages the whole way
down. But we've never stopped to ask: what, precisely, *is* information? Is a
file that's all zeros "smaller" than one with random data? Can we measure how
much information something contains? And can we send that information over a
noisy wire and still get it right on the other end?

**The idea.** In 1948, Claude Shannon — a 32-year-old engineer at Bell Labs —
published a paper called "A Mathematical Theory of Communication." It
single-handedly created the field of information theory. Shannon answered
questions nobody had thought to ask, and the answers are the foundation of
every piece of digital technology you use: compression, error correction,
cryptography, and even the way your phone talks to a cell tower.

Shannon's central insight is surprising and deep:

> **Information is not meaning. Information is surprise.**

A news headline you already predicted contains zero information. A lottery
result contains maximum information (for its length). A coin flip is 1 bit of
information. The fact that the sun will rise tomorrow is 0 bits of
information — it's completely predictable.

## Entropy — Measuring Information Content

Shannon defined **entropy** (borrowing the term from physics, where it means
"disorder") as the average amount of surprise in a source of information. The
more unpredictable a source, the higher its entropy.

A fair coin has 1 bit of entropy per flip: each outcome is equally surprising,
and it takes 1 bit to describe which one happened. A biased coin that lands
heads 99% of the time has very low entropy: you can predict "heads" most of the
time and be right, so each individual flip doesn't carry much new information.
A sequence of 10000 zeros has zero entropy: you already know the next symbol.

```
  Entropy = how many bits, on average, you need to describe an event

  Fair coin (50/50):             1.00 bit per flip
  Biased coin (90/10):           0.47 bits per flip
  Biased coin (99/1):            0.08 bits per flip
  Guaranteed outcome (100/0):    0.00 bits per flip
```

**The donut at this layer.** The donut's `render()` output is a grid of
brightness values. Each frame is similar to the previous one — the donut has
only rotated a few degrees. Most of the grid is the same from frame to frame.
That means the *difference* between two consecutive frames has very low
entropy: most cells are unchanged. A donut video could be compressed
enormously by sending only the *differences* between frames — which is exactly
what video compression (MPEG, H.264) does. The entropy of the raw frames is
high (many distinct brightness values), but the entropy of the *frame-to-frame
change* is very low. That's information theory in action.

> **One-breath aside.** Shannon borrowed the word "entropy" from physics, but
> the connection is real, not just poetic. In thermodynamics, entropy measures
> how many microscopic arrangements correspond to the same macroscopic state.
> In information theory, entropy measures how many bits you need to describe
> the next symbol. Both quantify "uncertainty," and the equations are
> mathematically identical. This is not a coincidence — it reflects a deep
> unity between information and physics that we're still exploring.

## Encoding — Representing Information Efficiently

If information is surprise, then an efficient encoding should use fewer bits
for predictable content and more bits for surprising content. This is the idea
behind **variable-length encoding**, and it's everywhere.

### Huffman Coding

David Huffman, as a graduate student in 1951, found an optimal way to do this.
His algorithm builds a tree where the most frequent symbols get the shortest
codes, and the least frequent symbols get the longest ones.

Consider the brightness ramp in the terminal donut:

```
  Brightness:  0   1   2   3   4   5   6   7   8   9  10
  Frequency:  40% 25% 15% 10%  5%  3%  1%  0.5% 0.3% 0.1% 0.1%
```

If we encoded each brightness with a fixed 4-bit code (enough for 0–10), every
pixel would take 4 bits. But Huffman coding would assign:

```
  Brightness 0:  "0"       (1 bit, because it's common)
  Brightness 1:  "10"      (2 bits)
  Brightness 2:  "110"     (3 bits)
  ...
  Brightness 10: "11111110" (8 bits, because it's rare)
```

On average, a pixel might use 2.3 bits instead of 4. For a 50×50 grid that's
saving 4,250 bits per frame. The donut looks exactly the same — the *information
content* is the same — but the representation is 40% smaller.

This is how `zip` files work, how JPEG compression starts, how every modern
codec saves space. They all exploit the same principle: some symbols are more
predictable than others, so give them shorter codes.

## Compression — Lossless vs Lossy

Compression comes in two flavors, and they answer different questions.

**Lossless compression** (zip, PNG, FLAC): the decompressed data is *bit-for-bit
identical* to the original. Every brightness value in the grid is exactly
restored. This is mandatory for text, source code, and executable programs —
a single bit error in a program changes the behavior entirely.

**Lossy compression** (JPEG, MP3, H.264): the decompressed data is *close
enough* to the original but not identical. Some information is thrown away
because humans won't notice it. This is what makes a 10-minute donut video
compressible from gigabytes to megabytes.

The donut's three faces are a perfect illustration of lossy encoding:

```
  Original data:  a grid of continuous brightness values (0.0 to 1.0)
                  (infinite precision — theoretically infinite bits per pixel)

  Terminal face:  maps brightness to 12 ASCII characters
                  (lossy: ~3.6 bits per pixel)
                  Result: the donut is recognizable but blocky

  Desktop face:   maps brightness to 8 shaded block characters
                  (less lossy: ~4 bits per pixel)
                  Result: smoother, but still a discrete ramp

  Browser face:   maps brightness to colored dots with antialiasing
                  (least lossy: ~24 bits per pixel with RGB color)
                  Result: near-continuous appearance
```

**The same underlying grid of brightness values is the "information."** The
three faces are different *encodings* of that information — each one
compressing the original continuous brightness into a discrete set of symbols,
with progressively less loss. Information theory tells us exactly how much
information is lost in each encoding. The terminal face loses some information
(you can't distinguish brightness 0.42 from brightness 0.45 if they map to the
same character), but it preserves the *structure* — you can still see the donut
shape and its rotation.

## Error Correction — Sending Bits Over a Noisy Channel

All the encoding in the world is useless if the bits get corrupted during
transmission. And they *will* get corrupted. Wires have electrical noise,
wireless signals have interference, memory chips have cosmic ray strikes
(genuinely — a stray alpha particle can flip a bit in RAM, and it happens a few
times per gigabyte per month).

Shannon also addressed this: how do you send information over a noisy channel
so that the receiver can detect (and fix) errors?

The fundamental technique is **redundancy**. You add extra bits that are
mathematically related to the data bits. If some bits get flipped, the receiver
can reconstruct the original data.

### Parity

The simplest error detection: add one extra bit (the **parity bit**) that makes
the total number of 1s in the data even (even parity) or odd (odd parity). If a
single bit flips during transmission, the parity won't match, and the receiver
knows something went wrong.

```
  Data:        1 0 1 1 0 0 1    (four 1s — already even)
  Parity bit:  0
  Transmitted: 1 0 1 1 0 0 1 0

  (After a single-bit error:
   Received:   1 0 1 0 0 0 1 0  — five 1s, odd — ERROR!)
```

Parity is simple but limited: it can detect an odd number of errors, but it
can't *correct* them or detect an even number. For correction, you need more
structure.

### Hamming Codes

Richard Hamming (a colleague of Shannon's at Bell Labs) invented codes that can
both detect *and correct* a certain number of errors. His trick: add multiple
parity bits, each covering a subset of the data bits, overlapping in a clever
pattern so that a flipped bit causes a unique pattern of parity failures (the
*syndrome*) that identifies exactly which bit is wrong.

A (7,4) Hamming code takes 4 data bits and adds 3 parity bits. It can correct
any single-bit error in the 7-bit block. That's the mathematical minimum for
single-error correction.

### Hamming Distance

The **Hamming distance** between two bit strings is the number of positions
where they differ. `10110` and `10010` have Hamming distance 1 (they differ in
the third bit). The importance: if you design your valid code words to be at
least distance d apart, a received word can be corrupted by up to d-1 bits and
still be closer to the correct code word than to any other.

- Distance 1: no error detection (any single-bit error turns into another valid
  code word).
- Distance 2: single-bit error detection (parity).
- Distance 3: single-bit error correction (Hamming codes).
- Distance 4: single-bit correction + double-bit detection.
- And so on.

**The donut at this layer.** Every single bit traveling from the donut's
`render()` output to your screen is protected by error-correcting codes.
Modern RAM uses **ECC (Error-Correcting Code)** — typically a variant of
Hamming code — to fix single-bit errors and detect double-bit errors. When the
OS writes the donut's brightness grid to the screen, the data moves over a bus
that uses parity or CRC (Cyclic Redundancy Check) for error detection. The
CPU's internal buses use error-correcting codes too.

You never see this, but the donut would occasionally glitch — a wrong pixel, a
flash of incorrect brightness — if error correction didn't exist. A cosmic ray
hitting the wrong memory cell could turn a 1 into a 0, changing the donut's
appearance. Error correction prevents that silently, continuously, for every
frame rendered since the first pixel lit up.

> **One-breath aside.** The most dramatic example of error correction in action
> is the Voyager spacecraft, now more than 15 billion miles from Earth. Its
> radio signal is so faint that the carrier power is about 10⁻¹⁶ watts — the
> energy of a snowflake landing on the ground, per second. The data is encoded
> with a powerful convolutional code and then a Reed-Solomon code. Together,
> they allow the receiver to reconstruct the original message even with a raw
> bit error rate above 5%. Without information theory, Voyager would be utterly
> silent. Your donut has a much easier journey — data moves inches or feet, not
> light-hours — but the same mathematics protects both.

## The Shannon Limit — The Ceiling of Communication

Here is Shannon's most stunning result. Given a noisy channel (say, a wire
with random interference that flips 1% of bits), there is a maximum rate at
which you can send information reliably — the **channel capacity**. If you try
to send faster than this limit, no amount of clever error correction can get
your data through intact. Below the limit, you can make the error rate
arbitrarily small by using enough redundancy.

The implication: **perfect communication over a noisy channel is possible, but
only up to a hard mathematical ceiling.** Shannon proved this ceiling exists;
he even calculated it for common channel types. But his proof was
_non-constructive_ — it showed that good codes exist, without saying how to
find them. Finding codes that approach the Shannon limit has been a 70-year
engineering quest. Modern codes (LDPC codes, turbo codes) come within
fractions of a percent of the limit, making satellite communication, 5G, and
WiFi possible at their current speeds.

**The donut at this layer.** Every time the donut's data moves between
chips — from RAM to CPU, from CPU to GPU, over the USB cable to your
monitor — it's hitting these theoretical limits. The engineers who designed
your laptop's memory bus chose a speed that balances data rate against error
rate, targeting the Shannon limit for that physical channel. If they pushed the
bus faster, errors would spike and the error correction would soak up the
gains. The donut's smooth 60 fps is a product of both compute speed and
information-theoretic limits on data transport.

> **One-breath aside.** Shannon's noisy-channel coding theorem is one of the
> few results in computer science that is both provably true *and* a practical
> limit that hardware engineers bump into daily. It's not a "maybe" or a
> heuristic. It's a brick wall, with the same logical certainty as the
> Pythagorean theorem. If someone claims a communication system that exceeds
> the Shannon limit for its channel, they are provably wrong, no matter how
> clever the scheme.

## The Donut as an Information Channel

Let's put it together. The donut pipeline is an information channel:

```
  Source:  the donut's state {A, B, pos}
     │
     ▼
  Encoder: render() produces a grid of brightness values
     │        (raw information: ~24 bits per pixel × 2500 pixels = 60,000 bits)
     ▼
  Encoding 1:  brightness → terminal ramp  (12 symbols per cell)
     │        (lossy compression: ~3.6 bits per pixel)
     ▼
  Encoding 2:  grid → write() syscall
     │        (framed into packets with error detection)
     ▼
  Channel:  system bus, RAM, GPU, display cable
     │        (noisy — protected by ECC and parity)
     ▼
  Decoder:  monitor receives pixels
     │        (interpreted as light)
     ▼
  Destination:  your eye
```

At each step, information is encoded, sometimes compressed (lossily), sometimes
protected against errors. The *meaning* (the donut rotating) survives all these
encoding stages unchanged. The *representation* changes completely at each step.

This is exactly what we saw in Part 0: the donut is one idea expressed through
multiple faces. Information theory gives us the language to describe that. The
"information" is the donut state — the surprise of which pixel lights up next.
Everything else — ramps, encodings, error-correcting codes — is about
representing and preserving that surprise across a noisy physical channel.

## Where to Go Next

- **"Information Theory: A Tutorial Introduction"** (James V. Stone) — a
  gentle, intuitive introduction that requires almost no math. The best place to
  start if this chapter sparked your interest.
- **"The Information: A History, A Theory, A Flood"** (James Gleick) — a
  beautiful narrative history of information theory, from African talking drums
  to Shannon's original paper to modern information overload. Not a textbook,
  but it gives you the cultural and scientific context.
- **"Elements of Information Theory"** (Cover and Thomas) — the standard
  graduate textbook. Comprehensive, rigorous, and remarkably readable for what
  it is. Chapters 2–5 cover entropy, compression, and the noisy-channel coding
  theorem that proves error correction can work up to the Shannon limit.
- **Shannon's original 1948 paper** — "A Mathematical Theory of Communication."
  Readable even now, and a masterpiece of clear exposition. Available free
  online from Bell Labs.
- **The video book "But What Is Entropy?"** (3Blue1Brown on YouTube) —
  excellent visual intuition for what entropy means, with clear animations.
  Watch before diving into Cover and Thomas.
