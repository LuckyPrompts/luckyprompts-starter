"""
02_provider_routing.py
----------------------
Route tasks by cost tier: free local → cheap cloud → capable cloud.
Same prompt, three tiers. See the quality and cost difference.

The rule: start local. Only upgrade if local output isn't good enough.

Blog post: "A provider-routing abstraction for LLM apps (one factory, any model)"
luckyprompts.ai
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_client, log_usage

PROMPT = """
You are helping a solo founder write a cold outreach email.
Client context: Sarah runs a personal training business,
10 clients, wants to grow to 20 by end of year.

Write a 3-sentence follow-up email for a prospect who
attended a free trial session last week but hasn't signed up.
"""

TIERS = [
    ("local",   "Free — Ollama on your machine"),
    # ("cheap",   "~$0.001 — Anthropic Haiku"),    # uncomment if you have ANTHROPIC_API_KEY
    # ("capable", "~$0.005 — Anthropic Sonnet"),   # uncomment if you have ANTHROPIC_API_KEY
]

def main():
    print("Provider Routing Demo")
    print("=" * 50)
    print(f"Prompt: {PROMPT.strip()[:100]}...\n")

    for tier, description in TIERS:
        print(f"\n{'─' * 50}")
        print(f"Tier: {tier} ({description})")
        print("─" * 50)

        try:
            llm = get_client(tier=tier)
            response = llm.generate(PROMPT)

            print(response.text)
            print(f"\nCost: ${response.cost_usd:.6f} | Tokens: {response.input_tokens} in, {response.output_tokens} out")

            log_usage(response, label=f"routing_demo_{tier}")

        except Exception as e:
            print(f"Skipped ({e})")

    print("\n" + "=" * 50)
    print("Costs logged to token_log.csv")
    print("\nThe rule: local is free and good enough for most tasks.")
    print("Upgrade only when quality matters more than cost.")

if __name__ == "__main__":
    main()
