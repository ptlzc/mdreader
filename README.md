# mdreader

`mdreader` is a dependency-free Markdown structure reader for agents and maintainers who need reliable heading outlines, line numbers, section boundaries, and section text before changing Markdown source.

This repository is the canonical source of truth for standalone `mdreader` files. The `skills/mdreader` directory in `ptlzc/skills` is the shared skills distribution copy and should be synchronized from this repository.

## Supported Files

- `.md`
- `.markdown`
- `.md.j2`
- `.markdown.j2`
- Markdown-oriented `.j2` files

Jinja templates are preserved as raw source. `mdreader` does not render templates, execute template logic, or load template variables.

## Outline Workflow

Run `outline` before reading or writing supported Markdown source:

```sh
python3 scripts/mdreader.py outline <file>
```

The JSON output includes heading level, title, heading line, content start line, section end line, path, and children. Use it to understand the document tree and to identify the exact target section.

## Section Workflow

Read a precise section by heading line or path:

```sh
python3 scripts/mdreader.py section <file> --line <line>
python3 scripts/mdreader.py section <file> --path "A/B/C"
```

Use title lookup only when the title is unique:

```sh
python3 scripts/mdreader.py section <file> --title "C"
```

If a title is ambiguous, the script returns candidate metadata. Use `--line` or `--path` to disambiguate.

## Structure-first Principle

Agents should understand Markdown structure before reading or writing. The expected workflow is:

1. Run `outline`.
2. Identify heading tree, line numbers, section boundaries, and candidate target sections.
3. Read or edit within a selected section boundary.
4. If no matching section exists, infer the appropriate heading level and insertion location from the existing outline.

Avoid unstructured end-of-file accumulation unless the outline shows that the end of the file is the correct section boundary.

## Distribution

Canonical source:

```text
ptlzc/mdreader
```

Distribution copy:

```text
ptlzc/skills:skills/mdreader
```

Release order:

1. Push or release `ptlzc/mdreader`.
2. Synchronize `SKILL.md`, `scripts/mdreader.py`, and `agents/openai.yaml` into `ptlzc/skills:skills/mdreader`.
3. Push or release `ptlzc/skills`.
4. Update the parent `.codex-src` `skills` submodule pointer.

## License

MIT. See [LICENSE](LICENSE).
