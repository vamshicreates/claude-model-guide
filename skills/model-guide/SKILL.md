---
name: model-guide
description: Set up, inspect, or remove global task-aware model recommendations (Haiku, Sonnet, Opus, Fable + effort) in Claude Code, or recommend a model and effort level for a supplied task.
---

# Model Guide

For setup, explain that this installs persistent instructions in the user's global Claude Code memory file (`~/.claude/CLAUDE.md`). It recommends a model and effort level; the user switches with `/model` and `/effort`. Installing the skill alone does not activate global routing.

Run `python3 scripts/setup.py install` from this skill directory when the user requests global activation. The script preserves existing instructions and backs up changed files. Respect the environment's permission prompts. Use `--dry-run` to preview and `--claude-home PATH` for a custom location. The default honors `CLAUDE_CONFIG_DIR`, falling back to `~/.claude`.

For status, run `python3 scripts/setup.py status`. To disable global routing, run `python3 scripts/setup.py uninstall`; this removes only this package's marked instruction block. Removing the skill alone does not remove the global rule. Tell the user to start a new Claude Code session (or `/clear`) so changed instructions load.

For a task-specific recommendation, read `policy.md` and apply its decision criteria. Don't execute the supplied task unless requested. Never claim to have changed a model, verified the current model, or measured token savings without evidence.
