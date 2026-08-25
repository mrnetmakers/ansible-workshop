#!/usr/bin/env python3
"""
Split a long Ansible workshop README.md into one Markdown file per numbered chapter.

Input chapter headings must use this form:

    # 0. Get the workshop repository
    # 1. Ansible basics: localhost and ping
    # 2. Learn YAML Syntax – Build Your First Playbook

Subsections such as "# 2.3 ..." are NOT treated as chapter boundaries.

Generated structure:

    README.md
    docs/
      0/README.md
      1/README.md
      2/README.md
      ...

The original README is backed up before it is replaced.

Usage:
    python3 split_workshop_readme.py
    python3 split_workshop_readme.py README.md
    python3 split_workshop_readme.py README.md --docs docs
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


CHAPTER_RE = re.compile(r"^#\s+(\d+)\.\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass
class Chapter:
    number: int
    title: str
    start: int
    end: int = 0


def find_chapters(lines: list[str]) -> list[Chapter]:
    """Find top-level numbered chapters, ignoring headings inside fenced code blocks."""
    chapters: list[Chapter] = []
    fence_marker: str | None = None

    for index, line in enumerate(lines):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_marker is None:
                fence_marker = marker
            elif marker == fence_marker:
                fence_marker = None
            continue

        if fence_marker is not None:
            continue

        match = CHAPTER_RE.match(line)
        if match:
            chapters.append(
                Chapter(
                    number=int(match.group(1)),
                    title=match.group(2).strip(),
                    start=index,
                )
            )

    for i, chapter in enumerate(chapters):
        chapter.end = chapters[i + 1].start if i + 1 < len(chapters) else len(lines)

    return chapters


def build_navigation(chapters: list[Chapter], index: int) -> str:
    """Create previous/index/next links for a chapter page."""
    parts: list[str] = []

    if index > 0:
        prev = chapters[index - 1]
        parts.append(f"[← Chapter {prev.number}](../{prev.number}/)")

    parts.append("[↑ Workshop index](../../)")

    if index + 1 < len(chapters):
        nxt = chapters[index + 1]
        parts.append(f"[Chapter {nxt.number} →](../{nxt.number}/)")

    return " | ".join(parts)


def root_readme(chapters: list[Chapter]) -> str:
    """Generate the short repository README shown on GitHub."""
    toc = "\n".join(
        f"- [{chapter.number}. {chapter.title}](docs/{chapter.number}/)"
        for chapter in chapters
    )

    return f"""# Ansible Deep-Dive Hands-On Workshop

A full-day, hands-on Ansible workshop for RHEL 9.

The workshop is organized into separate chapters under [`docs/`](docs/). Work through the chapters in order. The repository also contains the inventories, playbooks, roles, templates, and other files used by the exercises.

## Workshop environment

- one RHEL 9 Ansible control node (`rhelmain`);
- three RHEL 9 managed nodes (`rhel1`, `rhel2`, `rhel3`);
- one individual `studXX` account per student on all systems;
- `ansible-core` installed on the control node.

> **Important:** Several students use the same managed systems. Follow the exercises in order and use the student-specific resource names described in the workshop.

## Contents

{toc}

## Start here

Begin with [Chapter 0 – {chapters[0].title}](docs/{chapters[0].number}/).

## Repository structure

```text
.
├── README.md
├── ansible.cfg
├── requirements.yml
├── inventory/
├── playbooks/
├── roles/
└── docs/
    ├── 0/
    ├── 1/
    ├── 2/
    └── ...
```

Each chapter directory contains its own `README.md`, so GitHub automatically renders the chapter when you open the directory.
"""


def choose_backup_path(source: Path) -> Path:
    candidate = source.with_name(f"{source.stem}.full{source.suffix}")
    if not candidate.exists():
        return candidate

    counter = 1
    while True:
        candidate = source.with_name(f"{source.stem}.full.{counter}{source.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split a numbered workshop README into docs/<chapter>/README.md files."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="README.md",
        help="Source Markdown file (default: README.md)",
    )
    parser.add_argument(
        "--docs",
        default="docs",
        help="Output documentation directory (default: docs)",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    docs_dir = Path(args.docs)
    if not docs_dir.is_absolute():
        docs_dir = (source.parent / docs_dir).resolve()

    if not source.is_file():
        print(f"ERROR: Source file not found: {source}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    chapters = find_chapters([line.rstrip("\r\n") for line in lines])

    if not chapters:
        print(
            "ERROR: No numbered top-level chapters found.\n"
            "Expected headings such as '# 1. Chapter title'.",
            file=sys.stderr,
        )
        return 2

    numbers = [chapter.number for chapter in chapters]
    if len(numbers) != len(set(numbers)):
        print("ERROR: Duplicate chapter numbers detected.", file=sys.stderr)
        return 3

    # Back up the complete source before replacing README.md.
    backup = choose_backup_path(source)
    shutil.copy2(source, backup)

    docs_dir.mkdir(parents=True, exist_ok=True)

    # Write one README.md per chapter.
    for index, chapter in enumerate(chapters):
        chapter_dir = docs_dir / str(chapter.number)
        chapter_dir.mkdir(parents=True, exist_ok=True)

        content = "".join(lines[chapter.start:chapter.end]).rstrip() + "\n"
        nav = build_navigation(chapters, index)

        chapter_readme = (
            f"{nav}\n\n---\n\n"
            f"{content}\n"
            f"---\n\n{nav}\n"
        )

        (chapter_dir / "README.md").write_text(chapter_readme, encoding="utf-8")

    # Replace the repository README with a concise generated index.
    source.write_text(root_readme(chapters), encoding="utf-8")

    print(f"Split {len(chapters)} chapters.")
    print(f"Root README: {source}")
    print(f"Chapter docs: {docs_dir}")
    print(f"Original README backup: {backup}")
    print()
    print("Generated chapters:")
    for chapter in chapters:
        print(f"  docs/{chapter.number}/  {chapter.number}. {chapter.title}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
