"""
01_hello_local.py
-----------------
Your first local model call via Ollama.
Runs entirely on your machine. Free. No API key needed.

Prerequisites:
  1. Install Ollama: https://ollama.com
  2. Pull a model: ollama pull mistral:7b
  3. pip install -r requirements.txt

Blog post: "Local models first: my Ollama routing rule"
luckyprompts.ai
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_client, log_usage

def main():
    print("Connecting to local Ollama...")

    llm = get_client(tier="local")  # free, runs on your machine
    print(f"Using: {llm.model} (local, free)\n")

    prompt = "In two sentences, explain what a large language model is to someone who has never heard of one."

    print("Prompt:", prompt)
    print("\nGenerating...\n")

    response = llm.generate(prompt)

    print("Response:", response.text)
    print(f"\nTokens: {response.input_tokens} in, {response.output_tokens} out")
    print(f"Cost: ${response.cost_usd:.4f}")

    # Log this call to token_log.csv
    log_usage(response, label="hello_local")
    print("\nLogged to token_log.csv")

if __name__ == "__main__":
    main()
