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

`mdreader` is packaged as a Codex skill: `SKILL.md` plus `scripts/` and optional agent metadata. Codex can load that package directly. Other coding agents usually do not load Codex skill packages natively, so install `mdreader` as a shared checkout and register a small wrapper in that agent's own skill, rule, memory, or command system.

### Install Target Matrix

| Agent | Native `mdreader` install | Recommended target |
| --- | --- | --- |
| Codex | Yes, as a skill directory | `~/.codex/skills/mdreader` |
| Cursor | No native Codex skill loader | Shared checkout plus `.cursor/rules/mdreader.mdc` or `AGENTS.md` |
| Claude Code | No native Codex skill loader | Shared checkout plus `~/.claude/CLAUDE.md` import or `.claude/commands/mdreader.md` |
| Other agents | Depends on agent | Shared checkout plus that agent's instruction or skill registry |

### Codex Native Skill

Install directly into the Codex skills directory:

```sh
mkdir -p ~/.codex/skills
git clone https://github.com/ptlzc/mdreader.git ~/.codex/skills/mdreader
```

Update:

```sh
git -C ~/.codex/skills/mdreader pull --ff-only
```

Restart Codex, or start a new Codex session, after installing or updating the skill.

If your Codex home is generated from a source repository, install `mdreader` in that source repository and run your normal sync/installer instead of editing `~/.codex` directly.

### Shared Checkout for Non-Codex Agents

Create one shared source checkout:

```sh
mkdir -p ~/.local/share
git clone https://github.com/ptlzc/mdreader.git ~/.local/share/mdreader
```

Update:

```sh
git -C ~/.local/share/mdreader pull --ff-only
```

Use this checkout when registering `mdreader` with Cursor, Claude Code, or any other agent that does not read Codex skill directories directly.

### Cursor Skill Wrapper

Cursor can register `mdreader` as a Project Rule. Add this file to a project:

```sh
mkdir -p .cursor/rules
cat > .cursor/rules/mdreader.mdc <<'EOF'
---
description: Load the mdreader Markdown structure skill
globs: **/*.{md,markdown,md.j2,markdown.j2,j2}
alwaysApply: false
---

Use the mdreader skill installed at `~/.local/share/mdreader`.

Skill package:
- Instructions: `~/.local/share/mdreader/SKILL.md`
- CLI: `python3 ~/.local/share/mdreader/scripts/mdreader.py`
EOF
```

For agents or Cursor setups that prefer shared repository instructions, add an `AGENTS.md` file:

```sh
cat > AGENTS.md <<'EOF'
# Agent Skills

mdreader is installed at `~/.local/share/mdreader`.
Load `~/.local/share/mdreader/SKILL.md` when working with Markdown or Markdown Jinja2 structure.
EOF
```

### Claude Code Skill Wrapper

Claude Code can load persistent instructions from `CLAUDE.md`. Register the skill globally:

```sh
mkdir -p ~/.claude
cat >> ~/.claude/CLAUDE.md <<'EOF'

## mdreader Skill

Import and follow the mdreader skill instructions:
@~/.local/share/mdreader/SKILL.md

The mdreader CLI is:
python3 ~/.local/share/mdreader/scripts/mdreader.py
EOF
```

For a project-only install, add the same block to `./CLAUDE.md` in that repository instead.

Optionally add a reusable slash command:

```sh
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/mdreader.md <<'EOF'
---
allowed-tools: Bash(python3:*), Read, Grep, Glob
description: Load and run the mdreader Markdown structure skill
argument-hint: <markdown-file>
---

Use the skill instructions at `~/.local/share/mdreader/SKILL.md`.

Run:
!`python3 ~/.local/share/mdreader/scripts/mdreader.py outline "$ARGUMENTS"`
EOF
```

Then the command is available as:

```text
/mdreader path/to/file.md
```

### Other Agents

For any agent with a skill registry, register this package path:

```text
~/.local/share/mdreader
```

For any agent with only project instructions, add a short entry that points to:

```text
~/.local/share/mdreader/SKILL.md
python3 ~/.local/share/mdreader/scripts/mdreader.py
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
