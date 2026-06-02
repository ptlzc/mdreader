---
name: mdreader
description: Use when inspecting Markdown or Markdown Jinja2 heading structure, line numbers, section boundaries, or section content; run outline before reading or writing `.md`, `.markdown`, `.md.j2`, `.markdown.j2`, and Markdown-oriented `.j2` files.
---

# Markdown Structure Reader

## Purpose

Use this skill when you need a stable outline or a precise section slice from Markdown or Markdown Jinja2 source. It is meant for reading and editing source structure, not rendering Markdown or evaluating Jinja templates.

## Workflow

1. Before reading or writing a supported Markdown source file, run the bundled script to inspect the heading tree:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py outline <file>
   ```

2. Use the JSON output to identify heading levels, heading lines, content start lines, section end lines, paths, and candidate target sections.

3. When reading content, choose a precise section by heading line or path:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py section <file> --line <line>
   python3 skills/mdreader/scripts/mdreader.py section <file> --path "A/B/C"
   ```

4. Use title lookup only when the title is unique:

   ```sh
   python3 skills/mdreader/scripts/mdreader.py section <file> --title "C"
   ```

   If multiple headings share the same title, the script reports ambiguity with candidate metadata. Use `--line` or `--path` to disambiguate.

5. When writing content, first choose the exact section boundary or insertion point from the outline. Write within or around that boundary instead of appending unrelated content to the end of the file.

6. If the outline does not contain a suitable target section, infer the appropriate heading level and insertion location from nearby headings before adding content under a coherent heading.

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
- Do not create unstructured end-of-file accumulation unless the outline shows that the file end is the correct section boundary.
