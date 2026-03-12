#!/usr/bin/env python3
"""Run Claude on all 5 species, both above and below.

Usage:
    poetry run python run_claude_all_species.py
    poetry run python run_claude_all_species.py --dry-run   # preview without calling API
"""

import subprocess
import sys
import yaml
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration: one entry per species
# --------------------------------------------------------------------------- #
SPECIES_RUNS = [
    {
        "name": "1st species",
        "guide": "data/guides/1_first_species/Fux Rules- 1vs1 note - v1.6.txt",
    },
    {
        "name": "2nd species",
        "guide": "data/guides/2_second_species/Cantus 2notes vs 1 - version 1.7.txt",
    },
    {
        "name": "3rd species",
        "guide": "data/guides/3_third_species/Fux Rules- 3rd species - 4vs1 - v1.4.txt",
    },
    {
        "name": "4th species",
        "guide": "data/guides/4_fourth_species/Fux Rules- 4th species - Syncopatio - v1.2.txt",
    },
    {
        "name": "5th species",
        "guide": "data/guides/5_fifth_species/Fux Rules- 5th species - Florish - v1.7.txt",
    },
]

# Use E as the cantus firmus.
# (The Fux reference examples in D are loaded automatically by the runner
# whenever a species guide is detected — they serve as style references.)
FILES = ["Above_E", "Below_E"]

MODEL = "claude-opus-4-5"
TEMPERATURE = 0.0
MAX_TOKENS = 16000
DELAY = 2
RETRY = 2


def main():
    dry_run = "--dry-run" in sys.argv

    project_root = Path(__file__).resolve().parent
    config_path = project_root / "config.yaml"

    # Back up original config
    original_config = config_path.read_text()

    total = len(SPECIES_RUNS) * len(FILES)
    completed = 0
    failed = []

    print(f"\n{'='*60}")
    print(f"  Claude batch: {len(SPECIES_RUNS)} species × {len(FILES)} positions = {total} runs")
    print(f"{'='*60}\n")

    try:
        for species in SPECIES_RUNS:
            for file_id in FILES:
                completed += 1
                label = f"[{completed}/{total}] {species['name']} — {file_id}"
                print(f"\n{'─'*60}")
                print(f"  {label}")
                print(f"  Guide: {species['guide']}")
                print(f"{'─'*60}")

                if dry_run:
                    print("  (dry run — skipping API call)")
                    continue

                # Build config for this run
                config = {
                    "timeout": 600,
                    "default_models": {
                        "openai": "gpt-5.1-2025-11-13",
                        "anthropic": "claude-opus-4-5",
                        "google": "gemini-3-pro-preview",
                    },
                    "model_temperatures": {
                        "chatgpt": 0.0,
                        "claude": 0.0,
                        "gemini": 1.0,
                    },
                    "data_dir": "./data",
                    "dataset": "",
                    "outputs_dir": "./outputs",
                    "single_run": {"enabled": False},
                    "batch_run": {
                        "enabled": True,
                        "models": [MODEL],
                        "datatypes": ["musicxml"],
                        "files": [file_id],
                        "contexts": ["with"],
                        "guide_path": species["guide"],
                        "temperature": TEMPERATURE,
                        "max_tokens": MAX_TOKENS,
                        "delay": DELAY,
                        "retry": RETRY,
                    },
                }

                # Write temporary config
                config_path.write_text(yaml.dump(config, default_flow_style=False, allow_unicode=True))

                # Run
                result = subprocess.run(
                    ["poetry", "run", "run"],
                    cwd=str(project_root),
                    capture_output=False,
                )

                if result.returncode != 0:
                    failed.append(label)
                    print(f"  ⚠ FAILED (exit code {result.returncode})")
                else:
                    print(f"  ✓ Done")

    finally:
        # Always restore original config
        config_path.write_text(original_config)
        print(f"\n  ↻ Restored original config.yaml")

    # Summary
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {completed - len(failed)}/{total} succeeded")
    if failed:
        print(f"  FAILED ({len(failed)}):")
        for f in failed:
            print(f"    • {f}")
    print(f"{'='*60}\n")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
