# Agent installation guidance

## Summary

- Added installation guidance for Codex, Cursor, Claude Code, and other coding agents.
- Documented `~/.codex/skills/mdreader` as the native Codex skill installation path.
- Documented `~/.local/share/mdreader` as a shared helper checkout for agents that consume project instructions rather than Codex skills.

## Agent Behavior

Agents should install or reference `mdreader` once, then use its `outline` command before reading or editing Markdown, Markdown Jinja2, or Markdown-oriented `.j2` source.

## Validation

- README outline was inspected with `scripts/mdreader.py outline`.
