"""
llm_client.py — luckyprompts starter kit

One function to call any model: local or cloud.
Swap providers in config, not code.

Tiers:
  local    — Ollama (free, runs on your machine)
  cheap    — Anthropic Haiku or AWS Bedrock Haiku
  capable  — Anthropic Sonnet or GPT-4o

Usage:
  from llm_client import get_client, log_usage

  llm = get_client(tier="local")
  response = llm.generate("Write a one-sentence summary of...")
  log_usage(response, label="summarize")
"""

import os
import csv
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int

    @property
    def cost_usd(self) -> float:
        """Approximate cost in USD."""
        rates = {
            "ollama":    (0.0, 0.0),
            "local":     (0.0, 0.0),
            "haiku":     (0.00080, 0.00400),   # per 1K tokens
            "sonnet":    (0.00330, 0.01500),
            "gpt-4o":    (0.00250, 0.01000),
        }
        provider_key = self.provider.lower()
        if "haiku" in self.model.lower():
            provider_key = "haiku"
        elif "sonnet" in self.model.lower():
            provider_key = "sonnet"
        elif "gpt-4o" in self.model.lower():
            provider_key = "gpt-4o"
        in_rate, out_rate = rates.get(provider_key, (0.0, 0.0))
        return (self.input_tokens / 1000 * in_rate) + (self.output_tokens / 1000 * out_rate)


class OllamaClient:
    """Local models via Ollama — free, runs on your machine."""

    def __init__(self, model: str = "mistral:7b", host: str = "http://localhost:11434"):
        try:
            from ollama import Client
        except ImportError:
            raise ImportError("Run: pip install ollama")
        self.model = model
        self._client = Client(host=host)

    def generate(self, prompt: str, system: str = "", max_tokens: int = 1200) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat(
            model=self.model,
            messages=messages,
            options={"num_predict": max_tokens, "temperature": 0.2},
        )
        text = response.message.content or getattr(response.message, "thinking", "") or ""
        return LLMResponse(
            text=text,
            model=self.model,
            provider="ollama",
            input_tokens=getattr(response, "prompt_eval_count", 0) or 0,
            output_tokens=getattr(response, "eval_count", 0) or 0,
        )


class LocalClient:
    """Any OpenAI-compatible local server — LM Studio, llama.cpp, Jan.ai."""

    def __init__(
        self,
        model: str = "local-model",
        host: str = "http://localhost:1234/v1",
        api_key: str = "local",
    ):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")
        self._client = OpenAI(base_url=host, api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system: str = "", max_tokens: int = 1200) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return LLMResponse(
            text=response.choices[0].message.content or "",
            model=self.model,
            provider="local",
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )


class AnthropicClient:
    """Anthropic Claude — Haiku (cheap) or Sonnet (capable)."""

    MODELS = {
        "cheap":   "claude-haiku-4-5-20251001",
        "capable": "claude-sonnet-4-6",
    }

    def __init__(self, tier: str = "cheap"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Run: pip install anthropic")
        api_key = os.getenv("ANTHROPIC_API_KEY") or _read_secrets("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Set ANTHROPIC_API_KEY in .env or ~/.secrets")
        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = self.MODELS.get(tier, self.MODELS["cheap"])

    def generate(self, prompt: str, system: str = "", max_tokens: int = 1200) -> LLMResponse:
        kwargs = {"model": self.model, "max_tokens": max_tokens,
                  "messages": [{"role": "user", "content": prompt}]}
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)
        return LLMResponse(
            text=response.content[0].text if response.content else "",
            model=self.model,
            provider="anthropic",
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )


def get_client(
    tier: str = "local",
    model: Optional[str] = None,
    host: Optional[str] = None,
) -> "OllamaClient | LocalClient | AnthropicClient":
    """
    Get an LLM client by tier.

    tier="local"    — Ollama local model (free, default: mistral:7b)
    tier="cheap"    — Anthropic Haiku (needs ANTHROPIC_API_KEY)
    tier="capable"  — Anthropic Sonnet (needs ANTHROPIC_API_KEY)
    tier="lmstudio" — LM Studio or any OpenAI-compatible local server

    Override model:  get_client(tier="local", model="gemma3:9b")
    Override host:   get_client(tier="local", host="http://localhost:11434")
    """
    if tier == "local":
        return OllamaClient(
            model=model or os.getenv("OLLAMA_MODEL", "mistral:7b"),
            host=host or os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        )
    elif tier == "lmstudio":
        return LocalClient(
            model=model or os.getenv("LM_STUDIO_MODEL", "local-model"),
            host=host or os.getenv("LM_STUDIO_HOST", "http://localhost:1234/v1"),
        )
    elif tier in ("cheap", "capable"):
        client = AnthropicClient(tier=tier)
        if model:
            client.model = model
        return client
    else:
        raise ValueError(f"Unknown tier: {tier}. Use: local, lmstudio, cheap, capable")


def log_usage(response: LLMResponse, label: str = "", log_file: str = "token_log.csv") -> None:
    """Append one row to token_log.csv."""
    log_path = Path(log_file)
    write_header = not log_path.exists()

    with open(log_path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "date", "label", "model", "provider",
                "input_tokens", "output_tokens", "total_tokens", "cost_usd"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            label,
            response.model,
            response.provider,
            response.input_tokens,
            response.output_tokens,
            response.input_tokens + response.output_tokens,
            f"{response.cost_usd:.6f}",
        ])


def _read_secrets(key: str) -> Optional[str]:
    """Fallback: read key from ~/.secrets (no export needed)."""
    secrets_path = Path.home() / ".secrets"
    if not secrets_path.exists():
        return None
    for line in secrets_path.read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return None
