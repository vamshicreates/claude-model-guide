---
name: subagent-routing
description: Assign the right model to each step of a multi-step Claude Code workflow using fixed-model role subagents (scout, extractor, analyst, implementer, planner, reviewer, judge, synthesizer and more), with checking and planning seats never on a cheap model. Use when planning or running work that fans out to subagents, or to install, inspect, or remove the role agents.
---

# Subagent Routing

An extension to Model Guide. Model Guide recommends a model for the main conversation. This skill picks models per step, ahead of time, so nothing stops to ask.

## The principle

Match the model to the cost of a quiet failure. If a mistake is loud or easy to spot (a missing file, a failing test), a cheaper model is fine. If a mistake stays quiet and the output still reads fine (a plan, a review, a verdict, a final answer), that seat gets the strongest model.

## Roles

**Cheap workers: Haiku · low.** Output is mechanical or easy to check.

| Role | Use for |
|---|---|
| `scout` | Finding files, symbols, usages, and where things are mentioned (read-only) |
| `extractor` | Pulling fields, quotes, and lists out of text, and reformatting |
| `triager` | Labeling, sorting, bucketing, and deduplicating long lists by given criteria |
| `summarizer` | Shortening long text or logs for orientation, never as the basis for a decision |

**Builders and analysts: Sonnet · medium (debugger: high).** Real work, but its output gets checked.

| Role | Use for |
|---|---|
| `analyst` | Fan-out analysis, one self-contained piece each |
| `researcher` | Web and docs research on one question, with sources |
| `implementer` | Building a well-specified change |
| `test-writer` | Writing and running tests from the spec |
| `drafter` | First drafts and variants of posts, emails, docs, scripts |
| `debugger` | Reproducing a failure and finding the root cause |

**Planners and checkers: Opus · high.** A quiet failure here is expensive.

| Role | Use for |
|---|---|
| `planner` | Design, decomposition, acceptance criteria, and assigning steps to roles |
| `reviewer` | Reviewing code changes for bugs, security, regressions, and spec drift |
| `judge` | Verifying research and analysis claims against their sources |
| `synthesizer` | The final combined answer from checked material |

## Rules

1. The main session stays on one model. Choose models by delegating to these agents, not by switching the session.
2. **Planner, reviewer, judge, and synthesizer never get a cheaper model.** A weak checker fails quietly and the output still reads fine.
3. Savings come from the workers and builders. Run independent pieces in parallel, one agent per piece.
4. Typical flows:
   - Code: `scout` finds, `planner` plans, `implementer` and `test-writer` build, `reviewer` checks, `debugger` takes failures.
   - Research or analysis: `researcher` and `analyst` run in parallel, `judge` checks every report against its sources, `synthesizer` writes the answer.
   - Writing: `drafter` writes variants, `judge` checks the facts, `synthesizer` finishes the one that matters.
   - Bulk data: `extractor` and `triager` clean and sort, `analyst` examines, `judge` verifies.
5. Builders' output is never final. `implementer` goes to `reviewer`; `analyst`, `researcher`, and `drafter` go to `judge`.
6. If a checker returns FAIL, FIX FIRST, or UNVERIFIED, fix or re-run that piece and check it again before synthesis. If `debugger` cannot find a cause, send it to `planner` instead of letting it guess.
7. Skip delegation when the whole task fits in one turn. Spawning agents costs tokens and only pays off on multi-step or parallel work.
8. If a role agent is not installed, say so and offer to run setup. Do not silently substitute a cheaper model for a planner or checker seat.
9. Never claim token savings without measurement.

## Setup

Run `python3 scripts/setup.py install` from this skill directory. It copies the role agents into `~/.claude/agents/` (honors `CLAUDE_CONFIG_DIR`, or `--claude-home PATH`). Use `--dry-run` to preview. It never overwrites an agent file you already have with the same name that it did not install; it skips that file and reports it. `status` shows what is installed. `uninstall` removes only the files it installed. Start a new Claude Code session afterward so the agents load.

To make these rules apply to every session, also copy this skill to `~/.claude/skills/`. To change a role's model, edit its `model:` and `effort:` lines in `~/.claude/agents/<role>.md`; a later install keeps a timestamped backup of edited files before refreshing them.
