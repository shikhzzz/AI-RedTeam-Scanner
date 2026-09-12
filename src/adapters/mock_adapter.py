"""Mock adapter for offline testing (roadmap Part 14).

Returns canned responses keyed by attack_id (or a default), so the full
pipeline — executor, evaluator, metrics, reporter — can be tested end to end
with no API key and no network. This is how we validate the system's logic
before spending any real API calls.
"""
from __future__ import annotations

from .base import ModelAdapter, ModelResponse, GenParams


class MockAdapter(ModelAdapter):
    provider = "mock"

    def __init__(self, model_id: str = "mock-model", responses: dict | None = None,
                 default: str = "I can only help with questions about our product."):
        self.model_id = model_id
        self.responses = responses or {}
        self.default = default
        self._last_key = None

    def set_key(self, key: str):
        """Executor can set the current attack_id so the mock can vary output."""
        self._last_key = key

    def generate(self, system_prompt: str, user_prompt: str,
                 params: GenParams) -> ModelResponse:
        text = self.responses.get(self._last_key, self.default)
        return ModelResponse(text=text, model_id=self.model_id,
                             provider=self.provider, latency_s=0.0)
