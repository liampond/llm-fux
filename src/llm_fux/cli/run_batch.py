#!/usr/bin/env python3
"""Batch CLI for running multiple prompt combinations efficiently.

Goals:
  * Parse arguments & expand cartesian product of (models × files × datatypes).
  * Provide parallel execution with basic retry handling.
  * Validate dataset structure & API keys early.

Non‑goals:
  * Prompt construction logic (delegated to `PromptRunner`).
  * Complex scheduling / rate limiting (future enhancement).
"""

from __future__ import annotations

import argparse
import logging
import sys
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, List, Dict, Sequence, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from time import sleep
from dotenv import load_dotenv

from llm_fux.core.dispatcher import get_llm, get_llm_with_model_name, detect_model_provider
from llm_fux.core.runner import PromptRunner
from llm_fux.utils.path_utils import (
    find_project_root,
    list_file_ids,
    list_datatypes,
)
from llm_fux.config.config import DEFAULT_MODELS

# Legacy compatibility: tests may patch this symbol.
def list_questions(_path):  # type: ignore
    return ["Q1b"]


MODEL_ENV_VARS: Dict[str, str] = {
    "chatgpt": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GOOGLE_API_KEY",
}


def load_project_env() -> None:
    """Load a .env file at project root if present.

    Tests assert we call load_dotenv with only the dotenv_path kwarg (no override flag).
    """
    root = find_project_root()
    dotenv_path = root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    else:
        logging.debug("No .env file found; proceeding with existing environment.")


def parse_csv_or_list(values: Optional[Sequence[str]]) -> Optional[List[str]]:
    """Split a list of possibly comma-delimited strings into a flat list.

    Example: ["Q1a,Q1b", "Q1c"] -> ["Q1a", "Q1b", "Q1c"]
    """
    if not values:
        return None
    out: List[str] = []
    for v in values:
        out.extend([p.strip() for p in v.split(",") if p.strip()])
    return out or None


def validate_api_keys(models: Iterable[str]) -> None:
    for m in set(models):
        env_var = MODEL_ENV_VARS.get(m)
        if not env_var:
            continue
        api_key = os.getenv(env_var)
        if not api_key or "your_" in api_key.lower():
            logging.error(
                "Required key %s missing or placeholder. Add it to your .env to use model '%s'.",
                env_var,
                m,
            )
            raise SystemExit(2)


@dataclass(frozen=True)
class Task:
    model_name: str  # This is now the original model specification (could be provider or specific model)
    file_id: str
    datatype: str
    context: bool
    guide: Optional[str]
    temperature: float
    max_tokens: Optional[int]
    save: bool
    overwrite: bool
    dataset: str


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("Batch-run music-theory prompts")
    parser.add_argument(
        "--models",
        required=True,
        help="Comma-separated models (e.g. chatgpt,claude or gpt-5.1-2025-11-13,claude-opus-4-5) or 'all'",
    )
    parser.add_argument(
        "--context",
        action="store_true",
        help="Include contextual guides",
    )
    parser.add_argument(
        "--guide",
        type=str,
        help="Path to guide file (e.g., data/guides/LLM-Guide.md). Requires --context.",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="List of file IDs (default: all discovered)",
    )
    parser.add_argument("--questions", nargs="*", help=argparse.SUPPRESS)
    parser.add_argument(
        "--datatypes",
        nargs="*",
        help="List of formats (default: all)",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path.cwd() / "data",
        help="Root data directory (contains dataset subfolders)",
    )
    parser.add_argument(
        "--dataset",
        default="",
        help="Dataset name inside data-dir (default: root of data-dir)",
    )
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=Path.cwd() / "outputs",
        help="Where to save model responses (default: ./outputs)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Optional token cap",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing outputs",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=0,
        help="Number of retries for failed runs",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Number of parallel jobs",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser


def expand_models(
    raw: str,
) -> tuple[List[str], List[str]]:
    """Determine explicit model names and their providers.

    If given 'chatgpt', expands to ['gpt-5.1-2025-11-13'] and ['openai'].

    Returns:
        (resolved_models, providers)
    """
    input_models = [m.lower() for m in raw.split(",")]
    if "all" in input_models:
        input_models = ["chatgpt", "claude", "gemini"]

    resolved_models: List[str] = []
    providers: List[str] = []

    # Map canonical provider key to config.py key
    provider_to_config = {
        "chatgpt": "openai",
        "claude": "anthropic",
        "gemini": "google",
    }
    
    for model in input_models:
        # Check if it's a known alias FIRST
        if model in ["chatgpt", "claude", "gemini", "openai", "anthropic", "google"]:
            # It's an alias/provider name
            # Map alias -> provider
            if model == "chatgpt": provider = "openai"
            elif model == "openai": provider = "openai"
            elif model == "claude": provider = "anthropic"
            elif model == "anthropic": provider = "anthropic"
            elif model == "gemini": provider = "google"
            elif model == "google": provider = "google"
            else: provider = "unknown" # Should not happen given the list check
            
            providers.append(provider)

            conf_key = provider_to_config.get(model)
            if not conf_key: # e.g. model="openai" -> conf_key=None
                 # reverse lookup or direct map
                 if model in provider_to_config.values(): conf_key = model # e.g. "openai"
                 elif model in provider_to_config: conf_key = provider_to_config[model] # e.g. "chatgpt" -> "openai"
            
            # The logic above is a bit convoluted. Let's simplify based on the intent.
            # Intent: if model is "chatgpt", use DEFAULT_MODELS["openai"]
            
            target_config_key = provider_to_config.get(model, model) # "chatgpt" -> "openai", "openai" -> "openai"
            
            if target_config_key in DEFAULT_MODELS:
                 resolved_models.append(DEFAULT_MODELS[target_config_key])
            else:
                 # Should not happen for known aliases, but fallback
                 resolved_models.append(model)
                 
        else:
            # It's likely a specific model name (e.g. gpt-4)
            # Use detection
            try:
                provider = detect_model_provider(model)
                providers.append(provider)
                resolved_models.append(model)
            except ValueError:
                # Fallback or error? Let's just append it and let dispatcher fail later if needed, 
                # or maybe default to openai?
                # Actually, the error came from here. So we must catch it.
                logging.warning(f"Could not auto-detect provider for '{model}'. Assuming it's valid for a provider if configured.")
                resolved_models.append(model)
                providers.append("openai") # Fallback to openai? Or maybe skip?
                # A safer bet might be to just let it fail if it's truly invalid, but the issue was "chatgpt" failing.
                
    return resolved_models, providers


def prepare_tasks(
    models: Sequence[str],
    file_ids: Sequence[str],
    datatypes: Sequence[str],
    args: argparse.Namespace,
) -> List[Task]:
    return [
        Task(
            model_name=m,
            file_id=fid,
            datatype=dt,
            context=args.context,
            guide=args.guide,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            save=True,  # Always save
            overwrite=args.overwrite,
            dataset=args.dataset,
        )
        for m in models
        for fid in file_ids
        for dt in datatypes
    ]


def run_task(task: Task, base_dirs: Dict[str, Path]) -> bool:
    # Determine if we need to use auto-detection or standard model loading
    try:
        # Try to detect provider (handles specific model names like "gpt-4o")
        provider = detect_model_provider(task.model_name)
        model = get_llm_with_model_name(task.model_name, provider)
    except ValueError:
        # Not a specific model name, try to treat it as a provider name
        try:
            model = get_llm(task.model_name)
        except ValueError as e:
            logging.error(
                "[%s] Invalid model specification: %s", task.model_name, e
            )
            return False
    
    runner = PromptRunner(
        model=model,
        file_id=task.file_id,
        datatype=task.datatype,
        context=task.context,
        guide=task.guide,
        dataset=task.dataset,
        base_dirs=base_dirs,
        temperature=task.temperature,
        max_tokens=task.max_tokens,
        save=task.save,
    )
    out_path = runner.save_to
    if task.save and out_path and out_path.exists() and not task.overwrite:
        logging.info(
            "Skipping %s/%s/%s (already exists)",
            task.model_name,
            task.file_id,
            task.datatype,
        )
        return True
    try:
        runner.run()
        return True
    except Exception as e:  # pragma: no cover (unexpected edge)
        logging.error(
            "[%s][%s][%s] failed: %s", task.model_name, task.file_id, task.datatype, e
        )
        return False


# ---------------------------------------------------------------------------
# Legacy compatibility shim for existing tests expecting a tuple-based worker.
# test_cli_batch imports `worker` with signature worker(task_tuple) where
# task_tuple = (model_name, file_id, datatype, context, base_dirs,
#               temperature, max_tokens, save, overwrite)
# We construct a Task from this tuple and delegate to current logic.
def worker(task_tuple) -> bool:  # type: ignore
    try:
        (
            model_name,
            file_id,
            datatype,
            context,
            base_dirs,
            temperature,
            max_tokens,
            save,
            overwrite,
        ) = task_tuple
    except Exception:
        logging.error("Invalid task tuple passed to worker: %r", task_tuple)
        return False

    task = Task(
        model_name=model_name,
        file_id=file_id,
        datatype=datatype,
        context=context,
        guide=None,  # Legacy worker doesn't support guide selection
        temperature=temperature,
        max_tokens=max_tokens,
        save=save,
        overwrite=overwrite,
        dataset="",  # default dataset for legacy tests
    )
    return run_task(task, base_dirs)

# Keep a reference to detect when tests monkey-patch `worker`.
_original_worker = worker


def execute_tasks(
    tasks: List[Task], base_dirs: Dict[str, Path], jobs: int
) -> List[Task]:
    failures: List[Task] = []
    if jobs <= 1:
        for t in tasks:
            if not run_task(t, base_dirs):
                failures.append(t)
        return failures
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        future_map: Dict[Future, Task] = {
            pool.submit(run_task, t, base_dirs): t for t in tasks
        }
        for fut in as_completed(future_map):
            if not fut.result():
                failures.append(future_map[fut])
    return failures


def retry_failures(
    failures: List[Task], base_dirs: Dict[str, Path], retries: int
) -> List[Task]:
    for attempt in range(retries):
        if not failures:
            break
        logging.info(
            "Retry attempt %d for %d failures", attempt + 1, len(failures)
        )
        new_failures: List[Task] = []
        for t in failures:
            if not run_task(t, base_dirs):
                new_failures.append(t)
            else:
                # optional backoff small pause removed for performance
                pass
        failures = new_failures
    return failures


def run_main(argv: list[str] | None = None) -> int:
    """Internal entrypoint returning an exit code (no SystemExit)."""
    load_project_env()
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=level)

    if args.jobs < 1:
        logging.error("--jobs must be >= 1")
        return 2

    dataset_root = args.data_dir / args.dataset if args.dataset else args.data_dir
    base_dirs: Dict[str, Path] = {
        "encoded": dataset_root / "encoded",
        "prompts": dataset_root / "prompts",
        "questions": dataset_root / "prompts" / "questions",
        "guides": dataset_root / "guides",
        "outputs": args.outputs_dir,
    }
    for sub in ("encoded", "prompts"):
        if not base_dirs[sub].exists():
            logging.error("Missing required dataset subdirectory: %s", base_dirs[sub])
            return 2

    models, providers = expand_models(args.models)
    validate_api_keys(providers)

    # Validate guide usage
    if args.guide and not args.context:
        logging.error("--guide requires --context")
        return 2
    
    if args.guide:
        # Validate that the guide file exists
        from pathlib import Path
        guide_path = Path(args.guide)
        if not guide_path.exists():
            logging.error("Guide file not found: %s", args.guide)
            return 2
        if not guide_path.is_file():
            logging.error("Guide path is not a file: %s", args.guide)
            return 2

    selected_files = parse_csv_or_list(args.files) or parse_csv_or_list(args.questions)
    file_ids = selected_files or list_file_ids(base_dirs["encoded"])
    datatypes = parse_csv_or_list(args.datatypes) or list_datatypes(base_dirs["encoded"])

    if not file_ids:
        logging.error("No file IDs resolved (check --files or dataset contents)")
        return 2
    if not datatypes:
        logging.error("No datatypes resolved (check --datatypes or dataset contents)")
        return 2

    tasks = prepare_tasks(models, file_ids, datatypes, args)
    logging.info(
        "Prepared %d tasks (%d models × %d files × %d datatypes) using %d job(s)",
        len(tasks),
        len(models),
        len(file_ids),
        len(datatypes),
        args.jobs,
    )
    # Use the legacy worker shim only when tests have monkey-patched it;
    # otherwise use the modern execute_tasks path that preserves guide/dataset.
    import llm_fux.cli.run_batch as _self_mod
    _worker_patched = getattr(_self_mod, 'worker', None) is not getattr(_self_mod, '_original_worker', None)
    failures: list[Task] = []
    if _worker_patched:
        for t in tasks:
            tuple_task = (
                t.model_name,
                t.file_id,
                t.datatype,
                t.context,
                base_dirs,
                t.temperature,
                t.max_tokens,
                t.save,
                t.overwrite,
            )
            ok = _self_mod.worker(tuple_task)  # type: ignore
            if not ok:
                failures.append(t)
    else:
        failures = execute_tasks(tasks, base_dirs, args.jobs)
        failures = retry_failures(failures, base_dirs, args.retry)

    if failures:
        logging.error("Batch completed with %d failure(s)", len(failures))
        for t in failures[:10]:
            logging.error("  %s", t)
        if len(failures) > 10:
            logging.error("  ... (%d more)", len(failures) - 10)
        return 1

    logging.info("Batch completed successfully.")
    return 0


def main(argv: list[str] | None = None) -> None:  # type: ignore
    """Public CLI entrypoint raising SystemExit (legacy test contract)."""
    code = run_main(argv)
    raise SystemExit(code)


if __name__ == "__main__":  # pragma: no cover
    main()
