"""Shared evaluator types (roadmap Part 7)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Verdict:
    success: bool          # did the attack achieve its objective?
    rationale: str         # human-readable reason (logged for auditability)
    evaluator: str         # which evaluator produced this verdict
