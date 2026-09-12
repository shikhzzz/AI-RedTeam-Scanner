"""Command-line interface for the AI Red Team Scanner.

Usage:
  python -m src.cli list-models
  python -m src.cli run experiments/exp1_baseline.yaml

The API key is read from GROQ_API_KEY (loaded from .env). It is never printed,
logged, or written to any output file.
"""
from __future__ import annotations

import os
import sys
import json

import yaml
from dotenv import load_dotenv

from .dataset import load_attacks
from .adapters.base import GenParams
from .adapters.groq_adapter import GroqAdapter
from .executor import run_experiment


def _load_env():
    load_dotenv()  # reads .env in CWD
    if not os.getenv("GROQ_API_KEY"):
        sys.exit("ERROR: GROQ_API_KEY not set. Put it in a .env file (never commit it).")


def cmd_list_models():
    """Print the model IDs this key can access (helps pick a valid target)."""
    _load_env()
    import requests
    key = os.getenv("GROQ_API_KEY")
    resp = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json().get("data", [])
    print(f"{len(data)} models accessible with your key:\n")
    for m in sorted(data, key=lambda x: x.get("id", "")):
        print("  ", m.get("id"))
    # NOTE: we print only model IDs from the API, never the key.


def _run_one_model(model_id, attacks, version, cfg, repeats, out_dir):
    adapter = GroqAdapter(model_id=model_id)
    params = GenParams(temperature=cfg.get("temperature", 0.0),
                       max_tokens=cfg.get("max_tokens", 512))
    all_records = []
    safe_model = model_id.replace("/", "_")
    for r in range(1, repeats + 1):
        exp_id = f"{cfg['experiment_id']}__{safe_model}__run{r}"
        out_path = os.path.join(out_dir, f"{exp_id}.jsonl")
        records = run_experiment(
            adapter, attacks, version,
            experiment_id=exp_id,
            evaluator_name=cfg.get("evaluator", "expected_behavior_v1"),
            params=params,
            out_path=out_path,
        )
        n_err = sum(1 for x in records if x["error"])
        n_succ = sum(1 for x in records if x["verdict"] is True)
        print(f"  [{model_id}] run {r}/{repeats}: "
              f"{len(records)} tests, {n_succ} success, {n_err} errors -> {out_path}")
        all_records.extend(records)
    return all_records


def cmd_run(config_path):
    _load_env()
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    version, attacks = load_attacks(cfg.get("dataset", "attacks/payloads.yaml"))
    out_dir = cfg.get("out_dir", "results")
    os.makedirs(out_dir, exist_ok=True)
    repeats = int(cfg.get("repeats", 1))

    models = cfg.get("models") or [cfg["model_id"]]
    print(f"Running '{cfg['experiment_id']}' | dataset v{version} "
          f"| {len(attacks)} attacks | {len(models)} model(s) | {repeats} repeat(s)\n")

    for model_id in models:
        _run_one_model(model_id, attacks, version, cfg, repeats, out_dir)

    print("\nDone. JSONL result files are in:", out_dir)
    print("Send those .jsonl files back for analysis. They contain NO secrets.")


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print(__doc__)
        return
    cmd = argv[0]
    if cmd == "list-models":
        cmd_list_models()
    elif cmd == "run":
        if len(argv) < 2:
            sys.exit("Usage: python -m src.cli run <config.yaml>")
        cmd_run(argv[1])
    else:
        print(__doc__)
        sys.exit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
