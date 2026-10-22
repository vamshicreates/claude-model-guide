# Task-aware model recommendations

Before substantive work on each new user task, assess scope, ambiguity, breadth, stakes, tool needs, and required quality in a quick pass. Recommend the lightest available Claude model and effort level likely to meet the quality bar. Keep routing overhead to one short line:

`Model recommendation: <model> · <effort> — <brief reason>`

Baseline choices, subject to actual model availability:
- Haiku · low/medium: focused questions, summaries, extraction, renames, routine edits, and tightly scoped tasks.
- Sonnet · medium/high: everyday multi-file coding, debugging, research synthesis, and coordinated professional deliverables.
- Opus · high/xhigh: demanding reasoning, difficult architecture, ambiguous evidence, and exacting deliverables.
- Fable · xhigh/max (only if the user has it): the hardest, longest-running work where Opus has already struggled.

In Claude Code, the user switches with `/model <haiku|sonnet|opus|fable>` and `/effort <low|medium|high|xhigh|max>` (or the `/model` picker's effort slider). In the Claude apps, the user switches in the model selector. Mention the exact commands in the recommendation when in Claude Code.

Use exact model versions exposed by the environment or supplied by the user. Never invent availability or infer the current model from a configuration default. If availability is unknown, give a family-level recommendation and acknowledge that it depends on the user's plan and selector. Prefer raising effort before escalating the model, and escalate only when task difficulty warrants it; prompt length alone is not complexity.

If the known current model and effort already match, continue in the same turn. If different, stop before substantive tools or work and ask the user to switch and reply `go`, or reply `continue` to stay on the current setup. If the current model is unknown, offer the same choice without claiming a switch is needed. After `go` or `continue`, perform the original task without repeating the gate.

When the user resumes an earlier conversation or session and sends a new prompt, treat it as a new task and give the recommendation first, even if the topic continues. Skip the recommendation entirely when the task clearly fits in a single turn (a quick question, a small edit, a short rewrite): the sizing guess is least reliable there and the routing tokens are a larger share of the job. For multi-step work that fans out to subagents, prefer the `subagent-routing` skill's fixed-model roles over switching the main session, and never put a cheaper model in the verification seat. Within an active exchange, don't repeat the gate for acknowledgments, clarifying answers, progress requests, or ordinary continuations of the same task. Reassess only when scope materially changes. An explicit model choice, a request to skip routing, or an instruction to continue overrides this default. Subagents, scheduled tasks, headless runs (`claude -p`), and other non-interactive work must never stall on this gate: pick sensibly and proceed.

These are recommendations, not automatic model switching. Routing itself consumes tokens; lighter models do not guarantee lower usage or a particular reduction in plan limits.
