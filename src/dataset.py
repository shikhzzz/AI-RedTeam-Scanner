from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import yaml

VALID_CATEGORIES = {
    "system_prompt_extraction",
    "role_manipulation",
    "instruction_override",
    "authority_social_engineering",
    "obfuscation_encoding",
}

VALID_SUCCESS_TYPES = {"disclosure", "persona_adoption", "action", "compliance"}


@dataclass
class Attack:
    attack_id: str
    category: str
    description: str
    payload: str
    objective: str
    expected_safe_behavior: str
    success_criteria: dict[str, Any]
    source: str = "unknown"


def _validate(entry: dict, idx: int) -> Attack:
    required = ["attack_id", "category", "description", "payload",
                "objective", "expected_safe_behavior", "success_criteria"]
    for key in required:
        if key not in entry:
            raise ValueError(f"attack #{idx}: missing required field '{key}'")

    if entry["category"] not in VALID_CATEGORIES:
        raise ValueError(
            f"attack {entry['attack_id']}: unknown category '{entry['category']}'"
        )

    sc = entry["success_criteria"]
    if not isinstance(sc, dict) or "type" not in sc:
        raise ValueError(
            f"attack {entry['attack_id']}: success_criteria must have a 'type'"
        )
    if sc["type"] not in VALID_SUCCESS_TYPES:
        raise ValueError(
            f"attack {entry['attack_id']}: unknown success type '{sc['type']}'"
        )

    return Attack(
        attack_id=entry["attack_id"],
        category=entry["category"],
        description=entry["description"],
        payload=entry["payload"],
        objective=entry["objective"],
        expected_safe_behavior=entry["expected_safe_behavior"],
        success_criteria=sc,
        source=entry.get("source", "unknown"),
    )


def load_attacks(path: str = "attacks/payloads.yaml") -> tuple[str, list[Attack]]:
    """Return (dataset_version, [Attack, ...])."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "attacks" not in data or not isinstance(data["attacks"], list):
        raise ValueError("dataset must contain a top-level 'attacks' list")

    version = str(data.get("version", "0.0.0"))
    attacks = [_validate(e, i) for i, e in enumerate(data["attacks"])]

    ids = [a.attack_id for a in attacks]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate attack_id found in dataset")

    return version, attacks