# mdreader canonical repository

## Summary

- Created `ptlzc/mdreader` as the public canonical source of truth for `mdreader`.
- Documented the shared skills distribution copy at `ptlzc/skills:skills/mdreader`.
- Documented the structure-first read/write workflow for Markdown and Markdown Jinja2 files.

## Agent Behavior

Agents must run `outline` before reading or writing supported Markdown source files, then use heading line, heading path, or unique title metadata to target a precise section.

Agents must avoid unstructured end-of-file accumulation unless the outline shows that the file end is the correct section boundary.

## Jinja Boundary

Markdown Jinja templates are preserved as raw source. `mdreader` does not render templates, execute template logic, or load template variables.

## Release Order

1. Push or release `ptlzc/mdreader`.
2. Sync `SKILL.md`, `scripts/mdreader.py`, and `agents/openai.yaml` into `ptlzc/skills:skills/mdreader`.
3. Push or release `ptlzc/skills`.
4. Update `.codex-src` to the pushed `skills` submodule commit.
