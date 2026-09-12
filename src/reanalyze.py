from __future__ import annotations

import sys
import glob
import json
from collections import defaultdict

from .dataset import load_attacks
from .evaluator import keyword, expected_behavior, objective
from .evaluator.normalize import final_answer

EVALS = {
    "keyword_v1": keyword.evaluate,
    "expected_behavior_v1": expected_behavior.evaluate,
    "objective_v2": objective.evaluate,
}


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        sys.exit("Usage: python -m src.reanalyze <result_glob> [more...]")

    _, attacks = load_attacks()
    by_id = {a.attack_id: a for a in attacks}

    # group records by model
    by_model = defaultdict(list)
    for pattern in argv:
        for path in glob.glob(pattern):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    r = json.loads(line)
                    by_model[r["target_model"]].append(r)

    if not by_model:
        sys.exit("No records found for the given path(s). Check the glob and quoting.")

    for model, recs in sorted(by_model.items()):
        print(f"\n=== {model} ===  ({len(recs)} records)")
        # count reasoning blocks
        n_think = sum(1 for r in recs
                      if final_answer(r["response"]) != (r["response"] or "").strip())
        print(f"  responses containing <think> reasoning blocks: {n_think}/{len(recs)}")

        # per-evaluator ASR on normalized final answers
        print(f"  {'evaluator':22s}{'ASR (normalized final answer)':>32s}")
        for name, fn in EVALS.items():
            succ = 0
            for r in recs:
                a = by_id[r["attack_id"]]
                ans = final_answer(r["response"])
                if fn(a, ans).success:
                    succ += 1
            print(f"  {name:22s}{succ}/{len(recs)} = {succ/len(recs):.3f}".rjust(54))

        # also show what the STORED verdict said, for contrast
        stored_true = sum(1 for r in recs if r.get("verdict") is True)
        print(f"  [stored verdict in file: {stored_true}/{len(recs)} = "
              f"{stored_true/len(recs):.3f}]")


if __name__ == "__main__":
    main()