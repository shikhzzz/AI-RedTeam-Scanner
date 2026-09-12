# How to Run the Experiments Locally

These are the exact steps to run Experiment 1 (baseline) and Experiment 3
(two-model comparison) and produce the real result files to send back.

**Your API key stays in `.env` only. It is never printed, logged, or written
to any result file. Never commit `.env`.**

---

## 1. One-time setup

```bash
# from the project folder
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Create your `.env` from the template and paste your fresh Groq key into it:

```bash
# Windows (PowerShell):
Copy-Item .env.example .env
# macOS/Linux:
cp .env.example .env
```

Then open `.env` in a text editor and set:

```
GROQ_API_KEY=<your_fresh_key>
```

Confirm `.env` is ignored by git (it should already be in `.gitignore`):

```bash
git status        # .env must NOT appear in the list
```

---

## 2. Verify which models your key can access (IMPORTANT)

The original model (`llama-3.3-70b-versatile`) was retired by Groq in 2026.
Run this first and note the IDs that print:

```bash
python -m src.cli list-models
```

Look for the models named in the experiment configs:
- `openai/gpt-oss-120b`
- `qwen/qwen3-32b`  (or a `qwen/qwen3.6-27b` if that is what shows)

**If a model in the config is NOT in the printed list**, edit the config file
(`experiments/exp1_baseline.yaml` / `exp3_model_compare.yaml`) and replace the
`model_id` / `models:` entries with IDs that DID print. Pick two *different
families* for Experiment 3 (e.g. one `openai/...` and one `qwen/...`) so the
comparison is meaningful.

---

## 3. Run Experiment 1 (baseline, single model, 3 repeats)

```bash
python -m src.cli run experiments/exp1_baseline.yaml
```

This writes files like `results/exp1-baseline__<model>__run1.jsonl` (3 of them).

Quick look at your own results:

```bash
python -m src.analyze "results/exp1-baseline__*.jsonl"
```

---

## 4. Run Experiment 3 (two models, same suite, 3 repeats each)

```bash
python -m src.cli run experiments/exp3_model_compare.yaml
```

This writes `results/exp3-model-compare__<modelA>__run*.jsonl` and
`...<modelB>__run*.jsonl`.

```bash
python -m src.analyze "results/exp3-model-compare__*.jsonl"
```

---

## 5. Send the results back

Send the whole `results/` folder (all `.jsonl` files). They contain the model
responses, verdicts, categories, timestamps, and config hashes — **no secrets**.

If you want to be certain before sending, check:

```bash
# should print nothing:
# Windows PowerShell:
Select-String -Path results\*.jsonl -Pattern "gsk_"
# macOS/Linux:
grep -r "gsk_" results/    # should return nothing
```

---

## What each experiment answers

- **Experiment 1:** overall Attack Success Rate and ASR-by-category against one
  model, plus how stable verdicts are across 3 repeats (nondeterminism).
- **Experiment 3:** whether two different model families differ in robustness to
  the identical attack suite under identical settings.

## Important honesty note (for your presentation)

The human gold labels in `gold/labeled_responses.jsonl` were written for the
**original** run's specific responses. When you run against a *different* model,
that model produces *different* responses, so the old gold labels do **not**
transfer. To report evaluator reliability (FPR/FNR) on a NEW model, those new
responses must be human-labelled first. Until then, evaluator-reliability
numbers are valid only for the original run. `analyze.py` prints this caveat.
