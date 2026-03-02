# Copilot Instructions for llm-fux

## Protected Configuration

**DO NOT modify model identifiers.** The default model names in `config.yaml`
(under `default_models:`) and any references to them in the codebase are locked
for experimental reproducibility. Changing model names (e.g., updating
`gpt-5.1-2025-11-13` to a different version) invalidates prior results and
requires explicit human approval.

Specifically, do not:
- Change the `default_models` section in `config.yaml`
- Change the `_FALLBACK_MODELS` dictionary in `src/llm_fux/config/config.py`
- Change model name strings in `src/llm_fux/models/chatgpt.py`, `claude.py`, or `gemini.py`

## Project Context

This is a research project for a master's thesis studying LLM-generated species
counterpoint (music theory). The codebase sends prompts to LLM APIs (OpenAI,
Anthropic, Google) and saves the responses as MusicXML encoded music files.

## Code Style

- Python 3.11+, managed with Poetry
- Tests use pytest (run with `poetry run pytest tests/`)
- Logging via the `logging` module (not `print()`)
- Type hints preferred
