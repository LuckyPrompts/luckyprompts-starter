"""
04_session_handoff.py
---------------------
Write SESSION.md at the end of every session.
Pick up exactly where you left off next time — in 30 seconds.

Replaces: trying to remember what you were doing, reading through chat history,
          re-explaining your project to your AI assistant from scratch.

Blog post: "The SESSION.md handoff: how I start every AI conversation in 30 seconds"
luckyprompts.ai
"""

import sys
import os
from datetime import datetime
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_client, log_usage

SESSION_TEMPLATE = """# SESSION.md
_Last updated: {date}_

## What I was working on
{what}

## Where I left off
{where}

## Next action (first thing to do next session)
{next_action}

## Blocked on anything?
{blocked}

## Don't forget
{notes}
"""

def write_session(
    what: str,
    where: str,
    next_action: str,
    blocked: str = "No.",
    notes: str = "",
    session_file: str = "SESSION.md",
) -> None:
    """Write a SESSION.md handoff file."""
    content = SESSION_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        what=what,
        where=where,
        next_action=next_action,
        blocked=blocked,
        notes=notes or "Nothing critical.",
    )
    Path(session_file).write_text(content)
    print(f"Written: {session_file}")
    print(content)

def summarize_session_with_ai(work_done: str) -> str:
    """Use a local model to generate a concise 'where I left off' summary."""
    llm = get_client(tier="local")
    prompt = f"""You are writing a handoff note for a solo developer.
Summarize the following work done in 2-3 specific sentences.
Be concrete — mention what works, what doesn't, and exact state.
No fluff.

Work done this session:
{work_done}"""

    response = llm.generate(prompt, max_tokens=200)
    log_usage(response, label="session_summary")
    return response.text.strip()

def main():
    print("Session Handoff Demo")
    print("=" * 50)

    # Example: describe your session in plain text, AI condenses it
    work_done = """
    Added token tracking to my AI pipeline. Wired log_usage() after every
    Bedrock call. Tested with 3 different prompts. Costs are now visible in
    token_log.csv. Still need to add a weekly summary view and wire it to
    the dashboard. The CSV schema has 8 columns: date, label, model, provider,
    input_tokens, output_tokens, total_tokens, cost_usd.
    """

    print("Generating AI summary of your session...\n")
    summary = summarize_session_with_ai(work_done)

    write_session(
        what="Token tracking for AI pipeline — wiring log_usage() to all Bedrock calls",
        where=summary,
        next_action="Add weekly cost summary view to dashboard",
        blocked="No.",
        notes="token_log.csv schema is finalized — don't change column order or existing analysis scripts break.",
    )

    print("\nThe principle: write the handoff while context is fresh.")
    print("Future-you will thank present-you.")

if __name__ == "__main__":
    main()
