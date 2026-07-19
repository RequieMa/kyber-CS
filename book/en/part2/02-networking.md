---
title: "L2.2 · Computer Networking — System Calls That Leave the Machine"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# L2.2 · Computer Networking — System Calls That Leave the Machine

```
   Part 0  L2  software ↔ OS        (the big picture)
   Part 2  L2.1 operating systems
   Part 2  L2.2 networking         ◀ you are here
   Part 2  L2.3 databases
   Part 2  L2.4 distributed systems
```

**The question carried down:** We know the donut's browser face fetches
`donut.html` from a server somewhere. How does that actually work? How does
data leave one machine and arrive at another?

**The idea.** Networking is asking another computer's OS to do work — the same
pattern as a local system call, but over a wire. Your program calls one of its
own system calls (`send()` or `write()`), the OS turns that into electrical
signals on a cable, another computer's OS receives those signals, and hands the
data to the program waiting on the other end.

The whole Internet is this one pattern, repeated at scale.

## The Layered Model

The Internet is not one thing. It is a stack of agreements, each built on top
of the one below. This is called the **OSI model** (seven layers, in the
textbook) or the simpler **TCP/IP model** (four layers). We'll use the simpler
one:

```
   ┌─────────────────────────────────────────────────────────┐
   │  APPLICATION LAYER                                       │
   │  Your programs: HTTP, DNS, email, video calls           │
   │  "I want to fetch a web page"                            │
   ├─────────────────────────────────────────────────────────┤
   │  TRANSPORT LAYER                                         │
   │  TCP / UDP                                               │
   │  "I want reliable stream between two programs"          │
   ├─────────────────────────────────────────────────────────┤
   │  NETWORK LAYER                                           │
   │  IP (Internet Protocol)                                  │
   │  "I want to send a packet from one machine to another"  │
   ├─────────────────────────────────────────────────────────┤
   │  LINK LAYER                                              │
   │  Ethernet, Wi-Fi                                         │
   │  "I want to send a frame across one physical link"      │
   ├─────────────────────────────────────────────────────────┤
   │  PHYSICAL LAYER                                          │
   │  Cables, radio waves                                     │
   │  "I want to send voltage down this wire"                 │
   └─────────────────────────────────────────────────────────┘
```

Each layer provides a service to the one above it and asks for service from
the one below. The application layer doesn't care whether you're on Ethernet or
Wi-Fi. The link layer doesn't care whether you're fetching a web page or
streaming a video. Each layer only needs to keep one promise.

**The donut connection.** When the browser face calls `fetch("donut.html")`,
that one line of code triggers work at every single layer. Let's walk through
them, bottom to top.

## Layer 1: Physical — Voltage on a Wire

Deepest and simplest. The **physical layer** is about moving bits across a
medium — copper wire (Ethernet), fiber optic (light pulses), or radio (Wi-Fi).

A bit is a voltage. A 1 is one voltage; a 0 is another. The network card on
your computer changes the voltage on a wire, and the network card on the other
end reads it. That's it — the same game we discussed in Part 0 L5, just
stretched across a longer wire.

The physical layer has no idea what the bits mean. It never will. It just
shifts them.

## Layer 2: Link — One Hop at a Time

The **link layer** is the first layer that gives the bits structure. It wraps
bits into **frames**, each with a header that says "this frame is for device
with MAC address XX:XX:XX:XX:XX:XX."

A **MAC address** is a hardware identifier burned into every network interface
at the factory. It's like a serial number. When two devices are on the same
physical network (plugged into the same switch, or on the same Wi-Fi), the link
layer delivers frames directly between them using MAC addresses.

But the link layer only goes one hop. If your computer is in Shanghai and the
server is in San Francisco, the link layer gets the frame to your router, and
then it's done. Getting across the ocean is a job for the next layer.

## Layer 3: Network (IP) — Getting Across the Planet

The **network layer** solves the problem the link layer can't: how to send data
across multiple hops, through networks that don't know each other.

The Internet Protocol (IP) introduces **IP addresses** (like 192.168.1.42 for
IPv4, or 2001:db8::1 for IPv6). Every device on the Internet has an IP
address, at least temporarily. Your program sends a **packet** with a
destination IP address, and the network layer figures out how to get it there.

Routing is the algorithm that makes this work. Each router on the Internet
maintains a **routing table**: a map that says "to reach network X, send
packets to router Y." When a packet arrives at a router, the router looks at
the destination IP, consults its table, and forwards the packet to the next
router on the path. The packet hops from router to router until it reaches the
destination network.

```
   Your computer                      Server
       │                                ▲
       │  packet ──────────► router 1 ──┤
       │  (dest: server IP)   │         │
       │                       │         │
       │                       ▼         │
       │                     router 2 ───┤
       │                       │         │
       │                       ▼         │
       │                     router 3 ───┘
       │                       │
       │                       ▼
       │                    (packet arrives)
```

IP makes no promises. It is **best-effort delivery**: it will try to get your
packet there, but it may lose it, duplicate it, reorder it, or delay it. That
is not a bug — it's a deliberate design choice. Reliability is the next
layer's job.

> **One-breath aside.** Why _would_ you design a network layer that loses
> packets? Because making the network layer reliable means every router has to
> hold state about every connection — which fails when a router crashes. The
> Internet's design philosophy ("end-to-end principle") says: keep the core
> dumb and fast; put intelligence at the edges (your computer and the server).
> This is what makes the Internet resilient — a router in the middle can fail
> and the endpoints just retransmit.

## Layer 4: Transport (TCP) — Making Unreliable Reliable

The **transport layer** takes the unreliable packet stream from IP and turns
it into a reliable stream of data. The most important protocol here is **TCP**
(Transmission Control Protocol).

TCP gives you what looks like a pipe between two programs: data goes in one
end and comes out the other, in order, without gaps. Underneath, it's still
sending IP packets, but TCP adds three critical mechanisms:

**1. The three-way handshake.** Before any data flows, the two computers agree
to talk:

```
   Your computer                          Server
       │                                     │
       │  SYN ─────────────────────────────► │  "I'd like to connect"
       │                                     │
       │  ◄─────────────────────────── SYN+ACK│  "OK, I'm here"
       │                                     │
       │  ACK ─────────────────────────────► │  "Great, let's talk"
       │                                     │
       │  ===== connection established =====  │
       │  data flows both ways                │
```

**2. Acknowledgments and retransmission.** After sending a packet, the sender
waits for an **ACK** (acknowledgment) from the receiver. If no ACK arrives
within a timeout, the sender sends the packet again. The receiver reassembles
packets in the right order, even if they arrive out of order.

**3. Flow control and congestion control.** The receiver tells the sender "I
can only handle X bytes per second," and the sender respects that. When the
network is congested, TCP automatically slows down. This is why the Internet
doesn't collapse when millions of people start streaming video at once — TCP
backs off.

TCP also assigns **port numbers** (16-bit values like 80 for HTTP, 443 for
HTTPS, 22 for SSH). The IP address identifies the machine; the port number
identifies which program on that machine should get the data. Together they
form a **socket** — the endpoint of a connection.

> **One-breath aside.** There is also UDP (User Datagram Protocol), the other
> major transport protocol. UDP is just IP with port numbers — no handshake,
> no retransmission, no ordering. It's used for real-time applications
> (video calls, gaming) where a retransmitted packet arrives too late to be
> useful. The application layer handles reliability itself, or doesn't bother.
> The donut's browser face usually uses TCP, because web pages need every byte,
> but a live-streaming donut video feed might use UDP.

## Application Layer: What the User Sees

The top layer is where programs live — HTTP, DNS, SMTP (email), and thousands
more. These are the protocols your code actually calls.

### DNS — The Phonebook of the Internet

Before the browser can fetch `donut.html`, it needs the server's IP address.
You typed `example.com` — but the network layer needs `93.184.216.34`.

**DNS** (Domain Name System) is the phonebook. Your computer asks a DNS server:
"What is the IP address for `example.com`?" The DNS server looks it up (asking
other servers if needed — there's a hierarchy from root servers to TLD servers
to authoritative servers) and replies.

This is literally a phonebook distributed across thousands of machines, and it
is one of the most remarkable systems ever built. When you type a URL and the
page loads in under a second, DNS has performed a multi-hop query across the
planet to get you an IP address — and it does this for every resource on the
page.

```
   Your browser: "What's the IP for donut.example.com?"
        │
        ▼
   Local DNS cache: "Don't know, asking upstream..."
        │
        ▼
   ISP's DNS server: "Let me check... donut.example.com is at 203.0.113.42"
        │
        ▼
   Browser: "Got it! Now I can connect."
```

### HTTP — What Happens When You Fetch a Page

**HTTP** (HyperText Transfer Protocol) is the language web browsers and servers
speak. It is remarkably simple — just text requests and text responses.

When the donut's browser face fetches `donut.html`, this is what happens:

```
   Browser sends (over the TCP connection):
     GET /donut.html HTTP/1.1
     Host: donut.example.com
     Accept: text/html
     [blank line]

   Server replies:
     HTTP/1.1 200 OK
     Content-Type: text/html
     Content-Length: 4096
     [blank line]
     <html><body><h1>Spinning Donut</h1>
     <canvas id="donut"></canvas>
     <script src="donut.js"></script></body></html>
```

That's it. HTTP is a request-response protocol: ask for a resource, get it
back. HTTPS (the S is for Secure) wraps the same conversation in encryption
using TLS (Transport Layer Security), so nobody on the wire can read your
request or the server's response.

## The Full Trace: The Donut's Browser Face

Let's put it all together. When the browser face of your donut runs this
JavaScript:

```javascript
fetch('https://donut.example.com/donut.html')
  .then(response => response.text())
  .then(html => { /* render the page */ });
```

Here is the complete journey, layer by layer:

```
   APPLICATION LAYER (browser JavaScript):
      1.  fetch("https://...") is called.
      2.  Browser checks its local DNS cache for donut.example.com.
      3.  Cache miss → browser asks the OS to do a DNS lookup.
      4.  OS sends a DNS query (UDP packet) to the configured DNS server.
      5.  DNS server responds with IP: 203.0.113.42.
      6.  Browser constructs an HTTP GET request for /donut.html.
      7.  Browser asks the OS: "Open a TCP connection to 203.0.113.42:443."

   TRANSPORT LAYER (OS kernel, TCP):
      8.  OS sends a SYN packet to 203.0.113.42:443.
      9.  OS receives SYN+ACK from the server.
      10. OS sends ACK. Connection is established.
      11. OS hands the browser a socket — "here's your pipe."
      12. Browser writes HTTP request bytes into the socket.

   NETWORK LAYER (OS kernel, IP):
      13. OS wraps each TCP segment in an IP packet.
      14. Packet header: source=your IP, destination=203.0.113.42.
      15. OS looks at routing table: "To reach 203.0.113.42, send to router."

   LINK + PHYSICAL LAYERS (network card + cable):
      16. Network card wraps packet in an Ethernet frame.
      17. Frame header: source=your MAC, destination=router's MAC.
      18. Network card changes voltage on the wire. Electrons flow.

   ACROSS THE INTERNET (many hops):
      19. Router receives frame, strips link layer, reads IP destination.
      20. Router consults its routing table, forwards to next hop.
      21. This repeats 5–20 times across the planet.
      22. Final router: "203.0.113.42 is on my local network."
      23. Router sends frame to the server's network card.

   THE SERVER'S OS:
      24. Server's network card receives the frame.
      25. Server kernel reads IP packet, strips IP header.
      26. Server kernel reads TCP segment, sees port 443.
      27. Server kernel delivers the HTTP request to the web server process.

   THE SERVER APPLICATION:
      28. Web server reads "GET /donut.html".
      29. Web server reads the file from its file system.
      30. Web server constructs an HTTP response.
      31. Web server writes the response into the socket.

   THE RESPONSE COMES BACK:
      32. Same journey in reverse: TCP segments → IP packets → frames → voltages.
      33. Your OS receives the response, reassembles it, delivers it to the browser.
      34. Browser receives the HTML and starts rendering.
      35. Browser encounters <script src="donut.js">, requests that too.
      36. The donut appears in your browser tab.
```

From `fetch()` to a spinning donut: roughly 36 hops through two operating
systems, dozens of routers, and thousands of kilometers of cable. And it
happens in under a second.

## The Key Insight: Networking Is Just Remote System Calls

Here is the point that ties networking to everything else in this book.

When your program calls `write()` to a local file, it asks your OS to do work
on hardware you own. When your program calls `send()` to a network socket, it
asks your OS to package the data and send it to another machine — where that
machine's OS receives it and delivers it to a waiting program. That program
(like a web server) might call `read()` to handle your data, then `write()`
to send the response back.

**Networking is just system calls on two machines, connected by a wire.**

Everything you learned about the OS in L2.1 applies here: user space vs kernel
space, system calls as the boundary, the kernel managing the hardware. The
hardware is just farther away.

```
   Local system call:           Remote system call (networking):
   ┌─────────┐                  ┌─────────┐     ┌─────────┐
   │  your   │                  │  your   │     │ server  │
   │ program │                  │ program │     │ program │
   └────┬────┘                  └────┬────┘     └────┬────┘
        │  write()                    │  send()      │  read()
        ▼                              ▼              ▼
   ┌─────────┐                  ┌──────────────┐ ┌──────────────┐
   │   OS    │                  │  your OS     │ │  server OS   │
   │ (local) │                  │              │ │              │
   └─────────┘                  └──────┬───────┘ └──────┬───────┘
        │                              │                │
        │  disk/screen                 │  wire ────────► │
        ▼                              ▼                  ▼
     hardware                       hardware           hardware
```

The same boundary. The same pattern. Just extended across space.

## What to Read Next

| Resource | What it covers |
|---|---|
| **Computer Networking: A Top-Down Approach** (Kurose & Ross) | The standard textbook. Read Chapters 1–3 for the full layered model. |
| **"How DNS Works"** (a comic: `howdns.works` / `howhttps.works`) | Playful but technically accurate visual explanations of DNS and HTTPS. |
| **The TCP/IP Guide** (free online) | A thorough, approachable reference on every protocol in the stack. |
| **Wireshark** (tool -- install and capture packets) | See every layer in action: run `tcpdump` or Wireshark while the donut fetches its page, and watch the SYN/SYN+ACK/ACK exchange happen in real time. |
| **Inside this book: Part 0 L2** | The OS boundary you now know extends across the network. |

Understanding networking completes the picture: the donut's three faces don't
just talk to the local OS — the browser face extends that conversation across
the planet, using exactly the same system call pattern, just with more hops.
