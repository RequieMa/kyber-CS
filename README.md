<sub>🌐 <b>English</b> · <a href="README-cn.md">中文</a></sub>

# Kyber CS

> *Computer Science, from bits to distributed systems — built for the cybernetics stack.*

[![Ko-fi](https://img.shields.io/badge/Support-ko--fi-FF5E5B?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/requiema)
[![Afdian](https://img.shields.io/badge/Support-爱发电-946CE6?style=flat)](https://afdian.com/a/requiema)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Jupyter Book](https://img.shields.io/badge/Jupyter_Book-🔧-blue)](https://jupyterbook.org/)

<br>

[Quick Start](#quick-start) · [What's Here](#whats-here) · [Structure](#repository-structure)

---

## Quick Start

```bash
git clone https://github.com/RequieMa/kyber-CS
cd kyber-CS
uv sync && uv run jupyter book build
```

### Word Count Tool

Track chapter word counts:

```bash
uv run python tools/wordcount.py              # list all chapters with word counts
uv run python tools/wordcount.py --lang en    # English chapters only
uv run python tools/wordcount.py --lang zh    # Chinese chapters only
```

The tool strips markdown syntax, code blocks, math, and directives — counting only
plain-text words. Draft content (`book/draft/`) is excluded by default.

---

## What's Here

<!-- | Chapter | Content | Status |
|---------|---------|--------|
| 1 · Data Structures & Algorithms | Complexity analysis, arrays, trees, graphs, dynamic programming | 🚧 Draft |
| 2 · Computer Architecture | Digital logic, CPU design, memory hierarchy, instruction sets | 🚧 Draft |
| 3 · Operating Systems | Processes, memory management, file systems, concurrency | 🚧 Draft |
| 4 · Networking | Protocol stacks, TCP/IP, routing, application-layer protocols | 🚧 Draft |
| 5 · Databases | Relational models, indexing, transactions, distributed databases | 🚧 Draft |
| 6 · Programming Languages | Parsing, type systems, compilation, runtime semantics | 🚧 Draft |
| 7 · Distributed Systems | Consensus, replication, fault tolerance, CAP theorem | 📋 Planned |
| 8 · Theory of Computation | Automata, computability, complexity classes, cryptography | 📋 Planned | -->

---

## Repository Structure

```
kyber-CS/
├── book/
│   ├── en/                   # English chapters (ready for build)
│   ├── zh/                   # 中文章节
│   └── draft/                # Content under development
├── tools/
│   └── wordcount.py          # Chapter word count tracker
├── about.md                  # About the book and author
├── contact.md                # Contact information
├── privacy.md                # Privacy policy
├── terms.md                  # Terms of service
├── myst.yml                  # MyST configuration
├── pyproject.toml            # Project metadata & dependencies
└── README.md
```

---

## Connect

<div align="center">

| | | |
|---|---|---|
| 📧 | Email | [mazengou@gmail.com](mailto:mazengou@gmail.com) |
| 🌐 | Personal Site | [requiema.github.io](https://requiema.github.io) |
| 📝 | dev.to | [dev.to/requiema](https://dev.to/requiema) |
| 𝕏 | X | [x.com/mazengou](https://x.com/mazengou) |
| 👾 | Reddit | [u/Leather_Rip7919](https://www.reddit.com/user/Leather_Rip7919/) |
| 🔖 | 掘金 | [juejin.cn/user/76300220645242](https://juejin.cn/user/76300220645242) |
| 📦 | Gitee | [gitee.com/requiema](https://gitee.com/requiema) |
| 📖 | 知乎 | [zhihu.com/people/consilivm](https://www.zhihu.com/people/consilivm) |
| 🎬 | Bilibili | 镇魂曲麦 |
| 📱 | 公众号 | 镇魂曲麦 |

</div>
