"""Model adapter interface (roadmap Part 6).

Every target model is accessed through a ModelAdapter so the rest of the
system never depends on a specific provider. This is what makes the
model-vs-model comparison (Experiment 3) possible without rewriting the
executor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenParams:
    """Generation parameters. temperature=0 by default for reproducibility
    (roadmap Part 8 — noted as best-effort, LLMs are not perfectly
    deterministic even at 0)."""
    temperature: float = 0.0
    max_tokens: int = 512


@dataclass
class ModelResponse:
    """Uniform response object returned by every adapter."""
    text: str
    model_id: str
    provider: str
    latency_s: Optional[float] = None
    raw: Optional[dict] = field(default=None, repr=False)
    error: Optional[str] = None


class ModelAdapter(ABC):
    """Abstract interface every provider adapter implements."""

    provider: str = "unknown"

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str,
                 params: GenParams) -> ModelResponse:
        """Send one (system, user) exchange and return a ModelResponse.

        Implementations MUST NOT raise on ordinary API failures; they should
        return a ModelResponse with `error` set so the executor can record the
        failure and continue (roadmap Part 14 — robustness)."""
        raise NotImplementedError
