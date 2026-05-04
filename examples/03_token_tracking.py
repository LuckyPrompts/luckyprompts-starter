"""
03_token_tracking.py
--------------------
Track every AI session: model, tokens, cost, task type.
Know exactly where your money goes.

Replaces: Helicone, LangFuse, and every other paid LLM observability tool.
Cost: $0.

Blog post: "Track AI spend like cloud spend: a per-session token log"
luckyprompts.ai
"""

import sys
import os
import csv
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_client, log_usage

# Simulate a few different tasks in one session
TASKS = [
    {
        "label": "summarize",
        "prompt": "Summarize this in one sentence: AI models work by predicting the next token in a sequence, trained on vast amounts of text data to develop general language capabilities.",
    },
    {
        "label": "classify",
        "prompt": "Classify this as positive, negative, or neutral: 'The product works fine but setup took longer than expected.'",
    },
    {
        "label": "draft",
        "prompt": "Write a 2-sentence bio for a personal trainer named Alex who specializes in strength training for people over 40.",
    },
]

def show_log_summary(log_file: str = "token_log.csv") -> None:
    """Print a summary of the current token log."""
    log_path = Path(log_file)
    if not log_path.exists():
        return

    rows = []
    with open(log_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return

    total_tokens = sum(int(r["total_tokens"]) for r in rows)
    total_cost = sum(float(r["cost_usd"]) for r in rows)

    print(f"\n{'─' * 50}")
    print(f"token_log.csv — {len(rows)} total calls logged")
    print(f"{'─' * 50}")
    print(f"{'Label':<20} {'Model':<20} {'Tokens':>8} {'Cost':>10}")
    print(f"{'─' * 20} {'─' * 20} {'─' * 8} {'─' * 10}")
    for row in rows[-5:]:  # show last 5
        print(f"{row['label']:<20} {row['model']:<20} {row['total_tokens']:>8} ${float(row['cost_usd']):>9.6f}")
    print(f"{'─' * 50}")
    print(f"{'TOTAL':<20} {'':<20} {total_tokens:>8} ${total_cost:>9.6f}")

def main():
    print("Token Tracking Demo")
    print("=" * 50)

    llm = get_client(tier="local")
    print(f"Model: {llm.model}\n")

    for task in TASKS:
        print(f"Task: {task['label']}")
        response = llm.generate(task["prompt"])
        log_usage(response, label=task["label"])
        print(f"  → {response.text[:80].strip()}...")
        print(f"  Tokens: {response.input_tokens} in, {response.output_tokens} out | Cost: ${response.cost_usd:.6f}\n")

    show_log_summary()
    print("\nThe principle: measure everything. You can't optimize what you don't track.")

if __name__ == "__main__":
    main()
