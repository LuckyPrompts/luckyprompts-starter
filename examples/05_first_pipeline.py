"""
05_first_pipeline.py
--------------------
Chain two model calls: summarize → extract key points.
This is the foundation of every AI pipeline.

The pattern: each step does one job.
Output of step 1 becomes input of step 2.
Track cost at every step.

Blog post: "Output tokens cost 5x what input costs. Here's what I did about it."
luckyprompts.ai
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_client, log_usage, LLMResponse
from typing import List

# Sample document — replace with your own content
SAMPLE_DOCUMENT = """
Meeting notes — May 3, 2026

Attendees: Sarah (founder), Marcus (dev), Priya (design)

We discussed the Q2 roadmap. Main priorities are:
1. Launch the new onboarding flow by May 15. Marcus estimates 3 days of work.
   Priya has the mockups ready. Waiting on final copy from Sarah.
2. Fix the billing bug affecting ~12% of users on the Pro plan.
   Marcus identified the root cause — timezone handling in the subscription renewal logic.
   Fix is ready, needs QA sign-off before deploy.
3. Consider adding a mobile app. Tabled until Q3 — not enough bandwidth.

Action items:
- Sarah: send final onboarding copy to Marcus by May 5
- Marcus: deploy billing fix after QA approval
- Priya: share onboarding mockups in Figma by EOD
- All: Q3 planning meeting scheduled for June 1

Budget note: We're $2,400 under Q2 budget. Sarah wants to put $1,000 toward
paid acquisition test in late May if onboarding launches on time.
"""

def step1_summarize(document: str, llm) -> LLMResponse:
    """Step 1: Condense the document."""
    prompt = f"""Summarize the following in 3 sentences.
Be specific — keep names, dates, and numbers.
No fluff.

Document:
{document}"""

    response = llm.generate(prompt, max_tokens=300)
    log_usage(response, label="pipeline_step1_summarize")
    return response

def step2_extract_actions(summary: str, llm) -> LLMResponse:
    """Step 2: Pull out action items from the summary."""
    prompt = f"""From the following summary, extract all action items.
Return as a numbered list. Each item: [Owner]: [Action] (by [Date if known]).

Summary:
{summary}"""

    response = llm.generate(prompt, max_tokens=200)
    log_usage(response, label="pipeline_step2_extract")
    return response

def main():
    print("Two-Step Pipeline Demo")
    print("=" * 50)
    print(f"Document: {len(SAMPLE_DOCUMENT)} characters\n")

    llm = get_client(tier="local")
    print(f"Model: {llm.model} (local, free)\n")

    # Step 1
    print("Step 1: Summarize")
    print("─" * 30)
    r1 = step1_summarize(SAMPLE_DOCUMENT, llm)
    print(r1.text)
    print(f"Cost: ${r1.cost_usd:.6f} | {r1.input_tokens} → {r1.output_tokens} tokens\n")

    # Step 2 — input is the OUTPUT of step 1, not the full document
    # This is the key: step 2 pays for a short summary, not 400 lines
    print("Step 2: Extract action items")
    print("─" * 30)
    r2 = step2_extract_actions(r1.text, llm)
    print(r2.text)
    print(f"Cost: ${r2.cost_usd:.6f} | {r2.input_tokens} → {r2.output_tokens} tokens\n")

    # Total
    total_cost = r1.cost_usd + r2.cost_usd
    total_tokens = (r1.input_tokens + r1.output_tokens + r2.input_tokens + r2.output_tokens)
    print("─" * 50)
    print(f"Total tokens: {total_tokens} | Total cost: ${total_cost:.6f}")
    print("\nThe principle: chain outputs, not documents.")
    print("Step 2 processed a 3-sentence summary, not a 400-character document.")
    print("That's the token savings — and it compounds across every step you add.")

if __name__ == "__main__":
    main()
