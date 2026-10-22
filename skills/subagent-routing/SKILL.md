---
name: subagent-routing
description: Assign the right model to each step of a multi-step Claude Code workflow using fixed-model subagents (extractor, analyst, judge, synthesizer), with the judge seat never on a cheap model. Use when planning or running work that fans out to subagents, or to install, inspect, or remove the role agents.
---

# Subagent Routing

An extension to Model Guide. Model Guide recommends a model for the main conversation. This skill picks models per step, ahead of time, so nothing stops to ask.

## Roles

| Role | Model · effort | Use for |
|---|---|---|
| `extractor` | Haiku · low | Extraction and formatting |
| `analyst` | Sonnet · medium | Fan-out analysis, one self-contained piece each |
| `judge` | Opus · high | Verifying and grading other workers' output |
| `synthesizer` | Opus · high | Final combined answer from checked material |

## Rules

1. The main session stays on one model. Choose models by delegating to these agents, not by switching the session.
2. **The judge seat never gets a cheaper model.** A weak judge fails quietly and the output still reads fine. Verification and the final synthesis always use `judge` and `synthesizer`.
3. Savings come from the workers: send extraction and formatting to `extractor`, and parallel piece-by-piece analysis to `analyst` (one agent per piece, run in parallel).
4. Typical flow: `extractor` pulls and formats, several `analyst` agents run in parallel, `judge` checks every report against its sources, `synthesizer` writes the final answer from items the judge passed.
5. If the judge returns FAIL or UNVERIFIED on an item, fix or re-run that piece and re-judge it before synthesis.
6. Skip delegation when the whole task fits in one turn. Spawning agents costs tokens and only pays off on multi-step or parallel work.
7. If a role agent is not installed, say so and offer to run setup. Do not silently substitute a cheaper model for `judge` or `synthesizer`.
8. Never claim token savings without measurement.

## Setup

Run `python3 scripts/setup.py install` from this skill directory. It copies the four agents into `~/.claude/agents/` (honors `CLAUDE_CONFIG_DIR`, or `--claude-home PATH`). Use `--dry-run` to preview. It never overwrites an agent file you already have with the same name that it did not install; it skips that file and reports it. `status` shows what is installed. `uninstall` removes only the files it installed. Start a new Claude Code session afterward so the agents load.

To make rules 1 to 7 apply to every session, also copy this skill to `~/.claude/skills/`.
