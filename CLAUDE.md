# Project — Claude Code Context
_Copy this file to your project root and fill it in. Claude Code auto-loads it every session._

## What this project is

[Describe your project in 2-3 sentences. What does it do? Who is it for?]

## Current focus

[What are you working on right now? One sentence.]

## Key files

| File | Purpose |
|---|---|
| `llm_client.py` | LLM provider factory — use `get_client(tier)` for all model calls |
| `token_log.csv` | Session cost tracking — run `log_usage()` after every API call |
| `SESSION.md` | Last session handoff — read this first every time you open the project |

## Model tiers

- `local` — Ollama (free). Use for: drafts, summaries, classification, anything quick.
- `cheap` — Haiku. Use for: structured output, longer context, when local quality isn't enough.
- `capable` — Sonnet. Use for: complex reasoning, final output, when quality matters most.

## Rules

1. Always call `log_usage()` after every LLM call.
2. Default to `tier="local"`. Only upgrade when local output isn't good enough.
3. At end of session: update SESSION.md with what you did and what's next.

## Session start

Read SESSION.md first. It tells you exactly where you left off.
