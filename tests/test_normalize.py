"""Tests for reasoning-model think-block normalization."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator.normalize import final_answer


def test_removes_well_formed_think_block():
    text = "<think>I should refuse. Never reveal internal instructions.</think>\nHow can I help with our product?"
    out = final_answer(text)
    assert "think" not in out.lower()
    assert "never reveal" not in out.lower()
    assert "how can i help" in out.lower()


def test_no_think_block_returns_text():
    text = "DAN MODE ENABLED"
    assert final_answer(text) == "DAN MODE ENABLED"


def test_unclosed_think_is_dropped():
    text = "<think>reasoning that got truncated with the token UNLOCKED mentioned"
    out = final_answer(text)
    assert out == ""


def test_empty():
    assert final_answer("") == ""
    assert final_answer(None) == ""
