#!/usr/bin/env python3
"""Word count tool for Jupyter Book / MyST markdown chapters.

Counts plain-text words (strips markdown syntax, code blocks, frontmatter, directives)
for all chapters under book/en/ and book/zh/, excluding book/draft/.

Usage:
    python tools/wordcount.py           # list all chapters with word counts
    python tools/wordcount.py intro     # show word count for a specific chapter (fuzzy match)
    python tools/wordcount.py --json    # machine-readable output
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book"
EXCLUDE_DIRS = {"draft", "_build", ".ipynb_checkpoints"}


def strip_markdown(text: str) -> str:
    """Strip markdown syntax and return plain text for word counting."""

    # --- Remove YAML frontmatter (between --- fences at start) ---
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)

    # --- Remove MyST directives and roles ---
    # Block directives: ```{directive} ... ```
    text = re.sub(r"```\{[^}]*\}.*?```", "", text, flags=re.DOTALL)
    # Inline roles: {role}`content` → keep content
    text = re.sub(r"\{[a-zA-Z_]+?\}`([^`]*)`", r"\1", text)
    # Inline directives without content
    text = re.sub(r"\{[a-zA-Z_]+\}", "", text)

    # --- Remove code blocks (indented or fenced) ---
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)

    # --- Remove HTML comments ---
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # --- Remove HTML tags ---
    text = re.sub(r"<[^>]+>", "", text)

    # --- Remove images ---
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    # --- Remove links, keep link text ---
    text = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", text)
    # Reference-style links
    text = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", text)

    # --- Remove markdown formatting characters ---
    # Headers: keep text, remove # symbols
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Bold/italic markers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    # Strikethrough
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    # Inline code
    text = re.sub(r"`([^`]*)`", r"\1", text)
    # Blockquotes
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    # Horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # List markers
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    # --- Remove table formatting ---
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"^[-| :]+$", "", text, flags=re.MULTILINE)

    # --- Remove remaining MyST/admonition markers ---
    text = re.sub(r":::\{.*?\}", "", text)
    text = re.sub(r":::", "", text)
    # Admonition titles
    text = re.sub(r"^\.\. .*::", "", text, flags=re.MULTILINE)

    # --- Remove LaTeX math blocks ---
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\$.*?\$", "", text)

    # --- Collapse whitespace ---
    text = re.sub(r"\s+", " ", text).strip()

    return text


def count_words(filepath: Path) -> int:
    """Return plain-text word count for a markdown file."""
    raw = filepath.read_text(encoding="utf-8")
    plain = strip_markdown(raw)
    return len(plain.split())


def count_cjk(filepath: Path) -> int:
    """Return CJK (Chinese/Japanese/Korean) character count for a markdown file."""
    raw = filepath.read_text(encoding="utf-8")
    plain = strip_markdown(raw)
    cjk = 0
    for ch in plain:
        if '一' <= ch <= '鿿' or '㐀' <= ch <= '䶿' or '豈' <= ch <= '﫿':
            cjk += 1
    return cjk


def count_english_words(filepath: Path) -> int:
    """Return English word count (whitespace-delimited tokens after stripping CJK)."""
    raw = filepath.read_text(encoding="utf-8")
    plain = strip_markdown(raw)
    # Remove CJK characters
    en_only = ''.join(ch for ch in plain if not (
        '一' <= ch <= '鿿' or '㐀' <= ch <= '䶿' or '豈' <= ch <= '﫿'
    ))
    return len(en_only.split())


def detect_language(filepath: Path) -> str:
    """Detect primary language: 'zh' if CJK chars dominate, else 'en'."""
    raw = filepath.read_text(encoding="utf-8")
    plain = strip_markdown(raw)
    cjk = sum(1 for ch in plain if '一' <= ch <= '鿿')
    total = len(plain.replace(' ', '').replace('\n', ''))
    return 'zh' if (cjk > 0 and cjk / max(total, 1) > 0.15) else 'en'


def collect_chapters(lang: str | None = None) -> list[Path]:
    """Collect all .md chapter files, excluding draft and non-content dirs."""
    chapters: list[Path] = []
    if not BOOK_DIR.exists():
        return chapters

    langs = [lang] if lang else ["en", "zh"]
    for lg in langs:
        lang_dir = BOOK_DIR / lg
        if not lang_dir.is_dir():
            continue
        for md_file in sorted(lang_dir.rglob("*.md")):
            # Skip files inside excluded directories
            if any(excl in md_file.parts for excl in EXCLUDE_DIRS):
                continue
            chapters.append(md_file)
    return chapters


def fuzzy_match(chapters: list[Path], query: str) -> list[Path]:
    """Return chapters whose stem or path contains the query (case-insensitive)."""
    q = query.lower()
    return [c for c in chapters if q in c.stem.lower() or q in str(c).lower()]


def print_table(rows: list[tuple[str, int, int, str]], total_en: int, total_cjk: int) -> None:
    """Pretty-print a word-count table. rows = (path, en_words, cjk_chars, lang)."""
    if not rows:
        print("No chapters found.")
        return

    header = f"{'Chapter':<32} {'Lang':>4} {'EN words':>9} {'CJK chars':>10}  {'Status':>10}"
    print(header)
    print("-" * len(header))

    for name, en_wc, cjk_wc, lang in rows:
        if lang == 'zh':
            status = "✓" if cjk_wc >= 800 else f"need {800 - cjk_wc}"
        else:
            status = "✓" if en_wc >= 800 else f"need {800 - en_wc}"
        print(f"{name:<32} {lang:>4} {en_wc:>9,d} {cjk_wc:>10,d}  {status:>10}")

    print("-" * len(header))
    print(f"{'TOTAL':<32}      {total_en:>9,d} {total_cjk:>10,d}")
    print()
    print(f"AdSense target: 15+ chapters × 800+ words/chars = 12,000+ total")
    bar_total = min(total_en + total_cjk, 15000)
    bar = "█" * (bar_total // 500) + "░" * ((15000 - bar_total) // 500)
    print(f"[{bar}] {total_en + total_cjk:,d} / 15,000")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Word count tool for Jupyter Book chapters (excludes book/draft/)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Fuzzy-match chapter name (e.g. 'intro' matches '01_introduction.md')",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON for scripting",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "zh"],
        default=None,
        help="Filter by language (en or zh)",
    )
    args = parser.parse_args()

    chapters = collect_chapters(args.lang)

    if args.query:
        chapters = fuzzy_match(chapters, args.query)
        if not chapters:
            print(f"No chapter matching '{args.query}' found.", file=sys.stderr)
            sys.exit(1)

    if not chapters:
        print("No chapters found under book/en/ or book/zh/ (excluding draft/).")
        print("Create .md files in book/en/ or book/zh/ to get started.")
        sys.exit(0)

    rows: list[tuple[str, int, int, str]] = []  # (path, en_words, cjk_chars, lang)
    for ch in chapters:
        en_wc = count_english_words(ch)
        cjk_wc = count_cjk(ch)
        lang = detect_language(ch)
        rel = ch.relative_to(ROOT)
        rows.append((str(rel), en_wc, cjk_wc, lang))

    total_en = sum(en for _, en, _, _ in rows)
    total_cjk = sum(cjk for _, _, cjk, _ in rows)

    if args.json:
        output = {
            "chapters": [
                {"path": p, "en_words": en, "cjk_chars": cjk, "lang": lang}
                for p, en, cjk, lang in rows
            ],
            "total_en_words": total_en,
            "total_cjk_chars": total_cjk,
        }
        print(json.dumps(output, indent=2))
    else:
        print_table(rows, total_en, total_cjk)


if __name__ == "__main__":
    main()
