# ROADMAP.md
_Last updated: 2026-05-04_
_This is the local task board. Update it every session via "update the mds"._

---

## In Progress

- [ ] **luckyprompts.ai live site** — manifesto post + "coming soon" for blog series. Needed before any sharing.
- [ ] **Post template** — `blog/templates/post-template.md` with all 10 sections pre-filled with placeholder text.
- [ ] **Week 1 Monday post** — "I replaced Siri with a free local voice assistant" (Voicebox origin story)
- [ ] **Week 1 Thursday post** — "How I built push-to-talk: whisper.cpp + Ollama + macOS TTS" (Voicebox deep-dive)

---

## Backlog

### Blog infrastructure
- [ ] Add GitHub Topics to luckyprompts-starter: ollama, local-ai, llm, solo-founder
- [ ] `examples/06_voicebox_intro.py` — starter kit companion for Voicebox Week 1 post
- [ ] `examples/07_ledger_tagging.py` — starter kit companion for Learning Ledger Week 2 post
- [ ] Post template file — `blog/templates/post-template.md`
- [ ] ELI5 block component — reusable copy-paste prompt section for every post

### Content calendar — Weeks 1–4
- [ ] Week 1 Mon: Voicebox — "I replaced Siri with a free local voice assistant"
- [ ] Week 1 Thu: Voicebox deep-dive — whisper.cpp + Ollama + macOS TTS
- [ ] Week 2 Mon: Learning Ledger — "I replaced Notion AI with a local knowledge journal"
- [ ] Week 2 Thu: Learning Ledger deep-dive — vocabulary-controlled tagging + BM25 index
- [ ] Week 3 Mon: CLAUDE.md — "I replaced my AI assistant setup cost with a $0 local stack"
- [ ] Week 3 Thu: CLAUDE.md deep-dive — brief your AI like a remote contractor
- [ ] Week 4 Mon: SESSION.md — "I stopped paying for project management software"
- [ ] Week 4 Thu: SESSION.md deep-dive — 30-second session handoff pattern

### Content calendar — Weeks 5–8
- [ ] Week 5 Mon: token_log.csv — "I built my own AI cost dashboard for free"
- [ ] Week 5 Thu: token_log.csv deep-dive — track AI spend like cloud spend
- [ ] Week 6 Mon: Local models — "Why I never pay for GPT-4 on simple tasks"
- [ ] Week 6 Thu: Model routing — Ollama / LM Studio / llama.cpp routing rule
- [ ] Week 7 Mon: SEO audit — "A 10-page audit used to cost $200. Now it costs $0.04."
- [ ] Week 7 Thu: Context engineering — output tokens cost 5x what input costs
- [ ] Week 8 Mon: Plan mode — "I stopped debugging blindly. I made my AI plan first."
- [ ] Week 8 Thu: Plan mode vs freeform — the $0.24 debugging receipt

### Compliance gates (non-negotiable)
- [ ] Prior-inventions disclosure to Abstract before 2026-05-11
- [ ] Written consent from Abstract CEO under PIIA §4(c)(iv) before Meijin Company Page launches
- [ ] Operational firewall: separate device for Meijin/luckyprompts.ai work

### Starter kit
- [ ] docker-compose service for AI-Core-Local (when it goes public, Week 21+)
- [ ] Obsidian integration example (Phase 2)
- [ ] n8n self-hosted workflow example

### CCA-F exam prep (ties into Thursday posts)
- [ ] Agent SDK hooks (domain 1.5) — map to a Thursday post
- [ ] Message Batches API (domain 4.5) — map to a Thursday post
- [ ] tool_choice mechanics (domain 2.3) — already covered in Week 7 deep-dive material
- [ ] @import / .claude/rules/ (domains 3.1, 3.3) — map to CLAUDE.md post
- [ ] fork_session (domain 1.7) — map to a Thursday post

---

## Done

- [x] Manifesto — "Software is Eph'd" published to `docs/2026-05-04-software-is-ephd-manifesto.md`
- [x] Starter kit scaffolded — `llm_client.py`, 5 example files, README, CLAUDE.md, SESSION.md, token_log.csv
- [x] GitHub repo created — `LuckyPrompts/luckyprompts-starter` (public)
- [x] devcontainer added — `.devcontainer/devcontainer.json`, `Dockerfile`, `docker-compose.yml`
- [x] Content calendar — 21-week plan mapped across 3 source repos
- [x] Blog drafts copied — 40 source docs to `luckyprompts/blog/drafts/`
- [x] tool_choice forced selection — implemented in Meijin scanner audit.js
- [x] Cost finding documented — +67% cost increase when tool_choice breaks prompt caching on Bedrock

---

## Metrics (updated each week)

| Metric | Target (Week 8) | Current |
|---|---|---|
| luckyprompts-starter GitHub stars | 50 | 0 |
| Qualified inbound conversations | 3/month | 0 |
| Reddit/LinkedIn comment quality ratio | >1:3 technical | — |
