# Claude Model Guide 🎛️

Get a one-line model recommendation before Claude starts a new task — **Haiku, Sonnet, Opus, or Fable + effort level** — based on the work. Switch with `/model` and `/effort` and reply `go`, or reply `continue` to stay on your current setup.

One-time global setup. You control the switch.

The Claude port of [Codex Model Guide](https://github.com/vamshicreates/codex-model-guide). It combines a reusable skill with a one-time installer that adds a marked block to your global Claude Code memory file, `~/.claude/CLAUDE.md`, which Claude Code loads into every session.

## Install for Claude Code

```
git clone https://github.com/vamshicreates/claude-model-guide.git
cd claude-model-guide
python3 skills/model-guide/scripts/setup.py install --dry-run
python3 skills/model-guide/scripts/setup.py install
```

Requires Python 3 and Git. Start a new Claude Code session (or run `/clear`) after setup. On Windows, use `py -3` if `python3` isn't available. The installer honors `CLAUDE_CONFIG_DIR` and also supports `--claude-home PATH`.

Optional: also install the skill so you can ask for a recommendation on demand with `/model-guide`:

```
mkdir -p ~/.claude/skills && cp -r skills/model-guide ~/.claude/skills/
```

Or just give Claude Code the link:

> Read https://github.com/vamshicreates/claude-model-guide, run its setup command to enable global model recommendations, and preserve my existing CLAUDE.md. After setup, tell me how to uninstall it.

## Install for the Claude apps (claude.ai, desktop, mobile)

The apps have no `CLAUDE.md`, so paste the contents of [`claude-app-preferences.md`](claude-app-preferences.md) into your profile preferences in Settings (or a Project's instructions to scope it to one project). Switch models in the model selector.

## Behavior

| Task | Starting recommendation | Claude Code switch |
|---|---|---|
| Focused questions, extraction, small edits | Haiku · low/medium | `/model haiku` · `/effort low` |
| Multi-file coding, debugging, research synthesis | Sonnet · medium/high | `/model sonnet` · `/effort medium` |
| Hard reasoning, architecture, exacting deliverables | Opus · high/xhigh | `/model opus` · `/effort high` |
| Hardest long-running work (if available on your plan) | Fable · xhigh/max | `/model fable` · `/effort xhigh` |

Example:

```
Model recommendation: Sonnet · medium — multi-file bug fix with tests to run.
Switch with /model sonnet and /effort medium, then reply go — or reply continue.
```

Exact versions depend on the models your plan exposes. These choices are heuristics, not benchmarks. Claude can't always see your current model or effort; when it can't, it gives the recommendation and waits for `go` or `continue`. Tasks that clearly fit in one turn skip the recommendation entirely (the sizing guess is shakiest there and the routing tokens are a bigger share of the job). Follow-ups, acknowledgments, and continuations of the same task don't repeat the gate. Subagents, headless (`claude -p`) runs, and scheduled tasks never stall on it.

Model switching stays manual. Routing costs a few tokens, and savings depend on your workload, model, effort, and plan's usage accounting — no fixed savings are promised. This is an instruction convention, not an enforced runtime interceptor; project `CLAUDE.md` files and explicit instructions can override it.

## Extension: Subagent Routing (Claude Code)

Model Guide picks the model for the *main conversation*. The `subagent-routing` skill picks models *per step*, ahead of time, so nothing stops to ask. The main session stays on one model and hands work to four fixed-model subagents:

| Role | Model · effort | Use for |
|---|---|---|
| `extractor` | Haiku · low | Extraction and formatting |
| `analyst` | Sonnet · medium | Fan-out analysis, one piece each, in parallel |
| `judge` | Opus · high | Verifying other workers' output |
| `synthesizer` | Opus · high | Final answer from checked material |

The rule that matters: **the judge seat never gets the cheap model.** A weak judge fails quietly, and the output still reads fine. Save money on the workers, not on the checker.

```
python3 skills/subagent-routing/scripts/setup.py install --dry-run
python3 skills/subagent-routing/scripts/setup.py install
```

This copies the four agents into `~/.claude/agents/` (honors `CLAUDE_CONFIG_DIR` and `--claude-home PATH`). It never overwrites an agent you already have under the same name, and `uninstall` removes only the files it installed. To have Claude follow the routing rules in every session, also copy the skill: `cp -r skills/subagent-routing ~/.claude/skills/`. Start a new session afterward. Subagent roles need Claude Code; the Claude apps don't support custom subagents.

Idea credit: a Reddit reply that suggested choosing models per subagent and skipping the recommendation for one-turn tasks.

## Disable or inspect

```
python3 skills/model-guide/scripts/setup.py status
python3 skills/model-guide/scripts/setup.py uninstall
```

Uninstall removes only the marked Model Guide block and restores the file byte-for-byte. Changes create timestamped backups next to `CLAUDE.md`. Deleting the skill or this repository alone does not disable the global rule. Start a new session after uninstalling. In the Claude apps, delete the pasted text from your preferences.

## Contribute

Test one simple task and one complex task, including manual switching and uninstalling. Run `python3 -m unittest discover -s tests -v` to check the installer.

## References

- [Claude Code model configuration (aliases, `/model`, `/effort`)](https://code.claude.com/docs/en/model-config)
- [Choosing a Claude model and effort level in Claude Code](https://www.claude.com/blog/claude-model-and-effort-level-in-claude-code)

Community project; not affiliated with Anthropic. Made by [Vamshi Creates](https://instagram.com/vamshicreatess).
