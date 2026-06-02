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

## Agent Installation

`mdreader` can be used either as a native Codex skill or as a checked-out helper repo referenced by other coding agents. The script only needs Python 3 and does not require third-party packages.

### Shared Checkout

Use one local checkout when an agent does not support Codex-style skills directly:

```sh
mkdir -p ~/.local/share
git clone https://github.com/ptlzc/mdreader.git ~/.local/share/mdreader
```

If the directory already exists, update it with:

```sh
git -C ~/.local/share/mdreader pull --ff-only
```

### Codex

Install as a Codex skill:

```sh
mkdir -p ~/.codex/skills
git clone https://github.com/ptlzc/mdreader.git ~/.codex/skills/mdreader
```

Restart Codex after installing or updating the skill so the `mdreader` skill metadata is loaded.

For source-managed Codex homes, keep the source in the repository that owns `~/.codex/skills` and sync it into the runtime home instead of editing runtime files directly.

### Cursor

Cursor can use `mdreader` through project instructions. For a simple project-wide setup, add an `AGENTS.md` file at the repository root:

````md
# Agent Instructions

When inspecting or editing Markdown, Markdown Jinja2, or Markdown-oriented `.j2` source, use mdreader before reading or writing section content.

Run outline first:

```sh
python3 ~/.local/share/mdreader/scripts/mdreader.py outline <file>
```

Then read the exact target section:

```sh
python3 ~/.local/share/mdreader/scripts/mdreader.py section <file> --line <line>
python3 ~/.local/share/mdreader/scripts/mdreader.py section <file> --path "A/B/C"
```

Do not append unrelated Markdown to the end of a file unless the outline shows that the file end is the correct section boundary.
````

For a Cursor Project Rule, create a rule from `Cursor Settings > Rules` or the `New Cursor Rule` command and paste the same instruction. Keep the rule scoped to Markdown files if you only want it to activate for documentation work.

### Claude Code

Claude Code can use `mdreader` through memory files or custom slash commands.

For shared project memory, add this to `CLAUDE.md` in the project root:

````md
## Markdown Structure

Before reading or editing Markdown, Markdown Jinja2, or Markdown-oriented `.j2` files, run:

```sh
python3 ~/.local/share/mdreader/scripts/mdreader.py outline <file>
```

Use `section` with `--line`, `--path`, or a unique `--title` before making targeted edits. Avoid unstructured end-of-file accumulation unless the outline shows the file end is the correct section boundary.
````

For a reusable slash command, create `.claude/commands/mdreader.md`:

````md
---
allowed-tools: Bash(python3:*), Read, Grep, Glob
description: Inspect Markdown structure with mdreader before reading or editing
argument-hint: <markdown-file>
---

Run mdreader outline on `$ARGUMENTS`, inspect the heading tree, and then use mdreader section by line, path, or unique title before reading or editing content.

```sh
python3 ~/.local/share/mdreader/scripts/mdreader.py outline "$ARGUMENTS"
```
````

Then invoke it in Claude Code with:

```text
/mdreader path/to/file.md
```

### Other Agents

For agents that read repository instruction files, add the same structure-first instruction to the tool's project guidance file and reference the shared checkout path:

```text
Use python3 ~/.local/share/mdreader/scripts/mdreader.py outline <file> before reading or editing Markdown source. Use section selection by line, path, or unique title before targeted edits.
```

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
