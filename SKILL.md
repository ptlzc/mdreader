---
name: mdreader
description: Use when inspecting Markdown or Markdown Jinja2 heading structure, line numbers, section boundaries, or section content; prefer the bundled script over ad hoc parsing for `.md`, `.markdown`, `.md.j2`, `.markdown.j2`, and `.j2` files.
---

# Markdown Structure Reader

## Purpose

Use this skill when you need a stable outline or a precise section slice from Markdown or Markdown Jinja2 source. It is meant for reading source structure, not rendering Markdown or evaluating Jinja templates.

## Workflow

1. Run the bundled script to inspect the heading tree:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py outline <file>
   ```

2. Use the JSON output to choose a precise section by heading line or path:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py section <file> --line <line>
   python3 skills/mdreader/scripts/mdreader.py section <file> --path "A/B/C"
   ```

3. Use title lookup only when the title is unique:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py section <file> --title "C"
   ```

   If multiple headings share the same title, the script reports ambiguity with candidate metadata. Use `--line` or `--path` to disambiguate.

## Behavior

- Parses ATX headings (`#` through `######`) only.
- Ignores heading-like lines inside fenced code blocks.
- Preserves Jinja expressions and statements as raw source text.
- Outputs machine-readable JSON with heading level, title, heading line, content start line, section end line, path, and children.
- Reads `.md`, `.markdown`, `.md.j2`, `.markdown.j2`, and `.j2` files.
- Uses Python 3 standard library modules only.

## Boundaries

- Do not render Jinja templates.
- Do not execute template logic or load template variables.
- Do not treat setext headings as supported heading structure.
- Do not replace the script with one-off `grep`, `sed`, or regex parsing when exact section boundaries matter.
