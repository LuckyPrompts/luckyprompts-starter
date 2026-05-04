# luckyprompts-starter — Claude Code Context

## What this project is

luckyprompts.ai starter kit for solo founders and SMBs learning local-first AI.
Every blog post at luckyprompts.ai has a matching example file here.
Philosophy: Local-first. Self-hostable. Free. Software is Eph'd.

## Current focus

Read SESSION.md first — it tells you exactly where you left off.

## Key files

| File | Purpose |
|---|---|
| `llm_client.py` | LLM provider factory — use `get_client(tier)` for all model calls |
| `token_log.csv` | Session cost tracking — every call logged here, even $0 local calls |
| `SESSION.md` | Last session handoff — read before doing anything else |
| `ROADMAP.md` | Active post backlog, in-progress items, and done list — the local task board |
| `examples/` | One file per blog post. Numbered sequentially. |

## Model tiers

| Tier | Provider | Cost | Use when |
|---|---|---|---|
| `local` | Ollama (mistral, gemma, qwen) | $0 | Drafts, summaries, classification, anything quick |
| `cheap` | Claude Haiku / GPT-4o-mini | ~$0.001 | Structured output, longer context, local quality not enough |
| `capable` | Claude Sonnet | ~$0.01 | Complex reasoning, final output, quality matters |

Default is always `local`. Upgrade only when output quality fails.

## Rules

1. Call `log_usage()` after every LLM call — local calls too (cost_usd will be 0.0).
2. Default to `tier="local"`. Only upgrade when local isn't good enough.
3. New example file = next number in sequence. Check `ls examples/` before creating.
4. Every example must run from a clean clone with no global deps.

## "update the mds" command

When the user says **"update the mds"**, do all of the following:

1. **token_log.csv** — append any new calls from this session that aren't logged yet.
   Schema: `date,label,model,provider,input_tokens,output_tokens,total_tokens,cost_usd`
   Local Ollama calls: cost_usd = 0.000000. Still log them.

2. **SESSION.md** — overwrite with current state:
   - What was worked on this session
   - Exact file(s) changed
   - Where things stand right now
   - First thing to do next session
   - Anything blocked

3. **ROADMAP.md** — move any completed items from `## In Progress` to `## Done`.
   Add any new items discovered this session to `## Backlog`.

4. Report back: "MDs updated. Session cost: $X.XXXXXX. Next: [first item in ROADMAP In Progress]."

## Session start checklist

1. Read SESSION.md
2. Read ROADMAP.md — know what's in progress before starting
3. Check `token_log.csv` tail — see what last session cost
