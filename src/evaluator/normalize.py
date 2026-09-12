from __future__ import annotations

import re

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_OPEN_THINK_RE = re.compile(r"<think>.*", re.DOTALL | re.IGNORECASE)


def final_answer(text: str) -> str:
    """Return the model's final answer with any <think> reasoning removed.

    Handles: well-formed <think>...</think> pairs (removed), and a dangling
    <think> with no close tag (everything from the tag on is treated as
    reasoning and dropped). If no think block is present, returns the text
    unchanged (stripped)."""
    if not text:
        return ""
    cleaned = _THINK_RE.sub("", text)
    # If an unclosed <think> remains (truncated output), drop from it onward.
    cleaned = _OPEN_THINK_RE.sub("", cleaned)
    return cleaned.strip()