# luckyprompts-starter

> Local-first AI starter kit for solo founders and builders.
> Free. Self-hostable. Yours forever.

**Software is Eph'd.** Tools come and go. This kit teaches you the workflow layer that lasts — how to route tasks to the right model, track what AI costs you, and build pipelines that run without a monthly subscription.

Every post on [luckyprompts.ai](https://luckyprompts.ai) starts here.

---

## What's in the kit

| File | What it does |
|---|---|
| `llm_client.py` | One function to call any model — local or cloud. Swap providers in config, not code. |
| `token_log.csv` | Track every AI session: model, tokens, cost, task type. Know where your money goes. |
| `CLAUDE.md` | Project context file — tells your AI assistant about your project once, auto-loads every session. |
| `SESSION.md` | End-of-session handoff note. Pick up exactly where you left off next time. |
| `examples/01_hello_local.py` | Your first local model call via Ollama. |
| `examples/02_provider_routing.py` | Route tasks by cost tier: free local → cheap cloud → capable cloud. |
| `examples/03_token_tracking.py` | Log a session to `token_log.csv`. |
| `examples/04_session_handoff.py` | Write `SESSION.md` at the end of a session. |
| `examples/05_first_pipeline.py` | Chain two model calls: summarize → extract key points. |

---

## Prerequisites

1. **Install Ollama** — [ollama.com](https://ollama.com) — runs local models on your machine
2. **Pull a model** — open your terminal and run:
   ```bash
   ollama pull mistral:7b
   ```
3. **Verify Ollama is running:**
   ```bash
   ollama list
   ```
   You should see `mistral:7b` in the list.

That's it for local-only usage. For cloud models (optional), see `.env.example`.

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/LuckyPrompts/luckyprompts-starter.git
cd luckyprompts-starter

# Install dependencies
pip install -r requirements.txt

# Copy env template (optional — only needed for cloud models)
cp .env.example .env

# Run your first local model call
python examples/01_hello_local.py
```

Expected output:
```
Using: mistral:7b (local, free)
Response: Hello! I'm running entirely on your machine...
Tokens: 12 in, 38 out | Cost: $0.00
```

---

## The three-tier routing rule

Every task gets routed to the cheapest model that can do it:

```
Tier 1 — Local (free)     Ollama: mistral:7b, gemma3:9b, qwen2.5:7b
Tier 2 — Cheap cloud      Anthropic Haiku, AWS Bedrock Haiku
Tier 3 — Capable cloud    Anthropic Sonnet, GPT-4o
```

Use `llm_client.py` and it handles this automatically:

```python
from llm_client import get_client

# Uses local model by default — free
llm = get_client(tier="local")
response = llm.generate("Summarize this in one sentence: ...")

# Upgrade tier when you need more capability
llm = get_client(tier="capable")
```

---

## Blog series

Each `examples/` file pairs with a post on [luckyprompts.ai](https://luckyprompts.ai):

| Example | Blog post |
|---|---|
| `01_hello_local.py` | Local models first: my Ollama routing rule |
| `02_provider_routing.py` | A provider-routing abstraction for LLM apps |
| `03_token_tracking.py` | Track AI spend like cloud spend |
| `04_session_handoff.py` | The SESSION.md handoff |
| `05_first_pipeline.py` | Output tokens cost 5x what input costs |

---

## Philosophy

**Local-first.** Runs on your machine. Your data stays with you.
**Self-hostable.** No vendor lock-in. Pull the repo, run it, own it.
**Free.** The models, the tools, the infrastructure. $0/month.

The specific models and tools in this kit will be replaced by better ones. That's the point. The workflow patterns — routing, tracking, session management, pipelines — those transfer to whatever comes next.

**Software is Eph'd. Your workflows aren't.**

---

## License

MIT — use it, fork it, build on it.
