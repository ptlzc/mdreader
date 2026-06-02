# Agent installation guidance

## Summary

- Added installation and registration guidance for Codex, Cursor, Claude Code, and other coding agents.
- Documented `~/.codex/skills/mdreader` as the native Codex skill installation path.
- Documented `~/.local/share/mdreader` as a shared checkout for agents that do not load Codex skill packages natively.
- Documented Cursor Project Rule and Claude Code memory/slash-command wrappers.

## Agent Behavior

Humans should install `mdreader` once per agent environment. Codex can load the package as a native skill. Cursor, Claude Code, and other agents should register wrappers that point to the shared checkout and load `SKILL.md`.

## Validation

- README outline was inspected with `scripts/mdreader.py outline`.
