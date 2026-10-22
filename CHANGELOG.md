# Changelog

## 0.2.0 — Subagent Routing extension

Based on community feedback to pick models per subagent instead of per session, and to skip the nudge on one-turn tasks.

- **New skill: `subagent-routing`.** 14 fixed-model role subagents installed into `~/.claude/agents/`:
  - Haiku · low: `scout`, `extractor`, `triager`, `summarizer`
  - Sonnet · medium: `analyst`, `researcher`, `implementer`, `test-writer`, `drafter` (`debugger` at high)
  - Opus · high: `planner`, `reviewer`, `judge`, `synthesizer`
- **Rule:** match the model to the cost of a quiet failure. Planning and checking seats never get a cheaper model, and tests enforce it. Cheap workers are read-only.
- **Safe installer:** never overwrites an agent you already have under the same name; `uninstall` removes only what it installed.
- **Model Guide change:** the recommendation is skipped for tasks that clearly fit in one turn.

## 0.1.0 — Initial release

Task-aware model and effort recommendations for Claude Code and the Claude apps, with a one-time global setup and uninstall. Ported from Codex Model Guide.
