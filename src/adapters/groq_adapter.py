"""Groq-hosted model adapter (roadmap Part 6).

Reuses the API call pattern from the original scanner.py, but adds:
- retries with exponential backoff (Part 14: rate limits / transient errors)
- error capture instead of crashing (Part 1.8 weakness fixed)
- latency measurement (useful context in records)

The groq client is imported lazily so the module can be imported (and unit
tested with a mock) without the groq package or an API key present.
"""
from __future__ import annotations

import os
import time

from .base import ModelAdapter, ModelResponse, GenParams


class GroqAdapter(ModelAdapter):
    provider = "groq"

    def __init__(self, model_id: str, api_key_env: str = "GROQ_API_KEY",
                 max_retries: int = 3, backoff_base: float = 1.5):
        self.model_id = model_id
        self.api_key_env = api_key_env
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._client = None  # created on first use

    def _client_or_create(self):
        if self._client is None:
            from groq import Groq  # lazy import
            api_key = os.getenv(self.api_key_env)
            if not api_key:
                raise RuntimeError(
                    f"Environment variable {self.api_key_env} is not set. "
                    f"Never hardcode the key; put it in .env (gitignored)."
                )
            self._client = Groq(api_key=api_key)
        return self._client

    def generate(self, system_prompt: str, user_prompt: str,
                 params: GenParams) -> ModelResponse:
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                client = self._client_or_create()
                start = time.time()
                resp = client.chat.completions.create(
                    model=self.model_id,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=params.temperature,
                    max_tokens=params.max_tokens,
                )
                latency = time.time() - start
                text = resp.choices[0].message.content or ""
                return ModelResponse(
                    text=text, model_id=self.model_id, provider=self.provider,
                    latency_s=round(latency, 3),
                )
            except Exception as e:  # noqa: BLE001 - deliberately broad
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(self.backoff_base ** attempt)
        return ModelResponse(
            text="", model_id=self.model_id, provider=self.provider,
            error=last_error or "unknown error",
        )
