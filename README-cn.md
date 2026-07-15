<sub>🌐 <a href="README.md">English</a> · <b>中文</b></sub>

# Kyber CS

> *从比特到分布式系统的计算机科学——为控制论技术栈而建。*

[![Ko-fi](https://img.shields.io/badge/Support-ko--fi-FF5E5B?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/requiema)
[![Afdian](https://img.shields.io/badge/Support-爱发电-946CE6?style=flat)](https://afdian.com/a/requiema)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Jupyter Book](https://img.shields.io/badge/Jupyter_Book-🔧-blue)](https://jupyterbook.org/)

<br>

[快速开始](#快速开始) · [能做什么](#能做什么) · [目录结构](#目录结构)

---

## 快速开始

```bash
git clone https://github.com/RequieMa/kyber-CS
cd kyber-CS
uv sync && uv run jupyter book build
```

### 字数统计工具

追踪每章字数：

```bash
uv run python tools/wordcount.py              # 列出所有章节及字数
uv run python tools/wordcount.py --lang zh    # 仅中文章节
uv run python tools/wordcount.py --lang en    # 仅英文章节
```

工具会剔除 markdown 语法、代码块、数学公式和指令 — 仅统计纯文本字数。
草稿目录（`book/draft/`）默认排除。

---

## 能做什么 / 这里有什么

<!-- | 章节 | 内容 | 状态 |
|------|------|------|
| 1 · 数据结构与算法 | 复杂度分析、数组、树、图、动态规划 | 🚧 草稿 |
| 2 · 计算机体系结构 | 数字逻辑、CPU 设计、存储层次、指令集 | 🚧 草稿 |
| 3 · 操作系统 | 进程管理、内存管理、文件系统、并发 | 🚧 草稿 |
| 4 · 计算机网络 | 协议栈、TCP/IP、路由、应用层协议 | 🚧 草稿 |
| 5 · 数据库系统 | 关系模型、索引、事务、分布式数据库 | 🚧 草稿 |
| 6 · 编程语言 | 语法分析、类型系统、编译、运行时语义 | 🚧 草稿 |
| 7 · 分布式系统 | 共识算法、复制、容错、CAP 定理 | 📋 计划中 |
| 8 · 计算理论 | 自动机、可计算性、复杂度类、密码学 | 📋 计划中 | -->

---

## 仓库结构

```
kyber-CS/
├── book/
│   ├── en/                   # 英文章节（待构建）
│   ├── zh/                   # 中文章节
│   └── draft/                # 开发中的内容
├── tools/
│   └── wordcount.py          # 章节字数统计工具
├── about.md                  # 关于本书与作者
├── contact.md                # 联系方式
├── privacy.md                # 隐私政策
├── terms.md                  # 服务条款
├── myst.yml                  # MyST 配置
├── pyproject.toml            # 项目元数据和依赖
└── README.md
```

---

## Connect · 关于作者

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
