#!/usr/bin/env python3
"""Read Markdown heading structure and sections as JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SUPPORTED_SUFFIXES = (
    ".md",
    ".markdown",
    ".md.j2",
    ".markdown.j2",
    ".j2",
)

HEADING_RE = re.compile(r"^(?P<indent> {0,3})(?P<marks>#{1,6})(?:[ \t]+|$)(?P<title>.*)$")
FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")


@dataclass
class Heading:
    level: int
    title: str
    line: int
    content_start_line: int
    end_line: int
    path: str
    children: list["Heading"] = field(default_factory=list)

    def to_dict(self, include_children: bool = True) -> dict[str, Any]:
        data: dict[str, Any] = {
            "level": self.level,
            "title": self.title,
            "line": self.line,
            "content_start_line": self.content_start_line,
            "end_line": self.end_line,
            "path": self.path,
        }
        if include_children:
            data["children"] = [child.to_dict(include_children=True) for child in self.children]
        return data


def fail(message: str, *, code: int = 2, payload: dict[str, Any] | None = None) -> None:
    if payload is not None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"mdreader: {message}", file=sys.stderr)
    raise SystemExit(code)


def validate_file(path: Path) -> None:
    if not path.exists():
        fail(f"file not found: {path}")
    if not path.is_file():
        fail(f"not a file: {path}")
    if not any(str(path).endswith(suffix) for suffix in SUPPORTED_SUFFIXES):
        supported = ", ".join(SUPPORTED_SUFFIXES)
        fail(f"unsupported file extension for {path}; supported: {supported}")


def read_lines(path: Path) -> list[str]:
    validate_file(path)
    try:
        return path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError as exc:
        fail(f"could not read {path} as UTF-8: {exc}")
    except OSError as exc:
        fail(f"could not read {path}: {exc}")


def strip_closing_hashes(title: str) -> str:
    stripped = title.strip()
    return re.sub(r"[ \t]+#{1,}[ \t]*$", "", stripped).strip()


def parse_headings(lines: list[str]) -> list[Heading]:
    roots: list[Heading] = []
    stack: list[Heading] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    total_lines = len(lines)

    for index, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r\n")
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group("fence")
            marker_char = marker[0]
            marker_len = len(marker)
            if not in_fence:
                in_fence = True
                fence_char = marker_char
                fence_len = marker_len
            elif marker_char == fence_char and marker_len >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
            continue

        if in_fence:
            continue

        heading_match = HEADING_RE.match(line)
        if not heading_match:
            continue

        level = len(heading_match.group("marks"))
        title = strip_closing_hashes(heading_match.group("title"))

        while stack and stack[-1].level >= level:
            stack[-1].end_line = index - 1
            stack.pop()

        parent_path = stack[-1].path if stack else ""
        path = f"{parent_path}/{title}" if parent_path else title
        heading = Heading(
            level=level,
            title=title,
            line=index,
            content_start_line=index + 1,
            end_line=total_lines,
            path=path,
        )

        if stack:
            stack[-1].children.append(heading)
        else:
            roots.append(heading)
        stack.append(heading)

    for heading in stack:
        heading.end_line = total_lines

    return roots


def flatten(headings: list[Heading]) -> list[Heading]:
    result: list[Heading] = []
    for heading in headings:
        result.append(heading)
        result.extend(flatten(heading.children))
    return result


def outline_payload(path: Path, headings: list[Heading]) -> dict[str, Any]:
    flat = flatten(headings)
    return {
        "file": str(path),
        "heading_count": len(flat),
        "headings": [heading.to_dict(include_children=True) for heading in headings],
        "flat": [heading.to_dict(include_children=False) for heading in flat],
    }


def section_text(lines: list[str], heading: Heading) -> str:
    return "".join(lines[heading.line - 1 : heading.end_line])


def section_payload(path: Path, lines: list[str], heading: Heading) -> dict[str, Any]:
    return {
        "file": str(path),
        "heading": heading.to_dict(include_children=False),
        "text": section_text(lines, heading),
    }


def select_heading(args: argparse.Namespace, headings: list[Heading]) -> Heading:
    flat = flatten(headings)
    selectors = [args.line is not None, args.path is not None, args.title is not None]
    if sum(selectors) != 1:
        fail("section requires exactly one selector: --line, --path, or --title")

    if args.line is not None:
        matches = [heading for heading in flat if heading.line == args.line]
        if not matches:
            fail(f"no heading found at line {args.line}")
        return matches[0]

    if args.path is not None:
        matches = [heading for heading in flat if heading.path == args.path]
        if not matches:
            fail(f"no heading found with path {args.path!r}")
        if len(matches) > 1:
            fail(
                f"path {args.path!r} is ambiguous",
                payload={
                    "error": "ambiguous_path",
                    "candidates": [heading.to_dict(include_children=False) for heading in matches],
                },
            )
        return matches[0]

    matches = [heading for heading in flat if heading.title == args.title]
    if not matches:
        fail(f"no heading found with title {args.title!r}")
    if len(matches) > 1:
        fail(
            f"title {args.title!r} is ambiguous; use --line or --path",
            payload={
                "error": "ambiguous_title",
                "candidates": [heading.to_dict(include_children=False) for heading in matches],
            },
        )
    return matches[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mdreader",
        description="Extract Markdown outlines and sections as JSON.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    outline = subparsers.add_parser("outline", help="print Markdown heading outline JSON")
    outline.add_argument("file", type=Path)

    section = subparsers.add_parser("section", help="print one Markdown section JSON")
    section.add_argument("file", type=Path)
    section.add_argument("--line", type=int, help="heading line number to read")
    section.add_argument("--path", help='heading path such as "A/B/C"')
    section.add_argument("--title", help="unique heading title to read")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = args.file
    lines = read_lines(path)
    headings = parse_headings(lines)

    if args.command == "outline":
        payload = outline_payload(path, headings)
    elif args.command == "section":
        heading = select_heading(args, headings)
        payload = section_payload(path, lines, heading)
    else:
        parser.error(f"unknown command: {args.command}")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
