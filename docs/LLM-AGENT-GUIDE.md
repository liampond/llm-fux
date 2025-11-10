# LLM Agent Guide for llm-fux

This document is designed for LLM agents (like GitHub Copilot) to understand how the llm-fux repository works and how to execute API calls on behalf of users.

## Repository Overview

**llm-fux** is a Python CLI tool that tests various LLM models (ChatGPT, Claude, Gemini) on Fux counterpoint generation tasks. It compares how different models handle music theory problems using various encoding formats.

### Core Functionality
- Send music notation files to LLMs with prompts
- Test with/without contextual guides
- Support multiple encoding formats (MusicXML, MEI, ABC, Humdrum)
- Organize outputs by model, context, and format
- Run single tests or batch experiments

## Project Structure

```
llm-fux/
├── config.yaml              # User-editable configuration
├── .env                     # API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY)
├── data/
│   ├── encoded/            # Music files in various formats
│   │   ├── musicxml/
│   │   ├── mei/
│   │   ├── abc/
│   │   └── humdrum/
│   ├── guides/             # Context guides for LLMs
│   │   ├── LLM-Guide.md
│   │   └── Pierre-Guide.md
│   └── prompts/            # Base prompts for each format
├── outputs/                # Organized by response/prompt/input > model > context > format
└── src/llm_fux/
    ├── cli/                # Command-line interfaces
    ├── config/             # Configuration management
    ├── core/               # Runner and dispatcher logic
    ├── models/             # LLM API wrappers
    └── prompts/            # Prompt building logic
```

## Configuration (config.yaml)

All default settings are in `config.yaml`:

```yaml
# Model Settings
model: claude                    # chatgpt, claude, or gemini
datatype: musicxml              # musicxml, mei, abc, or humdrum
temperature: 0.0                # 0.0-1.0

# Context Settings
guide: none                     # LLM-Guide, Pierre-Guide, or none
                               # If set to a guide name, context is automatically enabled

# API Settings
max_tokens: 16000              # Maximum response length (16000 prevents truncation)
timeout: 600                   # API timeout in seconds (0 = no timeout)
```

**Key Points:**
- Setting `guide: LLM-Guide` automatically enables context
- Setting `guide: none` means no context/guide
- Users can edit this file to change defaults
- CLI flags override config settings

## Running Commands

### Prerequisites
```bash
# Ensure you're in the project directory
cd /Users/liampond/Documents/GitHub/llm-fux

# API keys must be set in .env file
```

### Single Run Command

**Basic syntax:**
```bash
poetry run run-single --file <FILE_ID> [OPTIONS]
```

**Common patterns:**

1. **Use config.yaml defaults (simplest):**
   ```bash
   poetry run run-single --file Fux_CantusFirmus_C
   ```
   Uses model, datatype, guide from config.yaml

2. **Override specific settings:**
   ```bash
   poetry run run-single --file Fux_CantusFirmus_C --model chatgpt --datatype abc
   ```

3. **With context guide:**
   ```bash
   poetry run run-single --file Fux_CantusFirmus_C --context --guide LLM-Guide
   ```

4. **Without context (explicit):**
   ```bash
   poetry run run-single --file Fux_CantusFirmus_C --datatype musicxml
   ```
   (No --context or --guide flags)

5. **Custom temperature and tokens:**
   ```bash
   poetry run run-single --file Fux_CantusFirmus_C --temperature 0.7 --max-tokens 8000
   ```

**Available Options:**
- `--model`: chatgpt, claude, gemini
- `--model-name`: Specific model (e.g., gpt-4o, claude-3-sonnet-20240229)
- `--file`: File ID (e.g., Fux_CantusFirmus_C, Fux_CantusFirmus_A)
- `--datatype`: musicxml, mei, abc, humdrum
- `--context`: Include contextual guides (flag)
- `--guide`: Specific guide name (requires --context or sets it automatically)
- `--temperature`: 0.0-1.0
- `--max-tokens`: Maximum response length
- `--no-save`: Don't save outputs (by default, saves to outputs/)

**Listing commands:**
```bash
poetry run run-single --list-files      # Show available file IDs
poetry run run-single --list-datatypes  # Show available formats
poetry run run-single --list-guides     # Show available guides
```

### Batch Run Command

**Basic syntax:**
```bash
poetry run run-batch [OPTIONS]
```

**Common batch patterns:**

1. **All models, one format:**
   ```bash
   poetry run run-batch --models chatgpt claude gemini --datatypes abc --files Fux_CantusFirmus_C
   ```

2. **One model, all formats:**
   ```bash
   poetry run run-batch --models claude --datatypes musicxml mei abc humdrum --files Fux_CantusFirmus_C
   ```

3. **With and without context:**
   ```bash
   poetry run run-batch --models chatgpt claude --datatypes musicxml --contexts with without --files Fux_CantusFirmus_C
   ```

4. **Multiple files, one format:**
   ```bash
   poetry run run-batch --models claude --datatypes musicxml --files Fux_CantusFirmus_A Fux_CantusFirmus_C Fux_CantusFirmus_D
   ```

5. **Full comparison (all models, all formats, with/without context):**
   ```bash
   poetry run run-batch --models chatgpt claude gemini --datatypes musicxml mei abc humdrum --contexts with without --files Fux_CantusFirmus_C
   ```
   (This runs 24 API calls: 3 models × 4 formats × 2 contexts)

**Batch Options:**
- `--models`: Space-separated list (chatgpt, claude, gemini)
- `--datatypes`: Space-separated list (musicxml, mei, abc, humdrum)
- `--contexts`: with, without, or both (space-separated)
- `--files`: Space-separated file IDs
- `--guide`: Guide to use when contexts includes "with"
- `--temperature`: Temperature for all runs
- `--delay`: Seconds between API calls (default: 2)

## Output Organization

Outputs are automatically organized in this structure:

```
outputs/
├── response/           # LLM responses
│   └── claude/
│       ├── context/
│       │   └── musicxml/
│       │       └── Fux_CantusFirmus_C_001.musicxml
│       └── no-context/
│           └── musicxml/
│               └── Fux_CantusFirmus_C_001.musicxml
├── prompt/             # Full prompts sent to LLMs
│   └── claude/
│       ├── context/
│       │   └── musicxml/
│       │       └── Fux_CantusFirmus_C_001.txt
│       └── no-context/
│           └── musicxml/
│               └── Fux_CantusFirmus_C_001.txt
└── input/              # Input files bundled with metadata
    └── claude/
        ├── context/
        │   └── musicxml/
        │       └── Fux_CantusFirmus_C_001.json
        └── no-context/
            └── musicxml/
                └── Fux_CantusFirmus_C_001.json
```

**Benefits:**
- Easy comparison across models
- Clear separation of with/without context
- Format-specific organization
- Incremental numbering prevents overwrites

## Interpreting User Requests

### Common User Phrases → Commands

| User Says | Command to Run |
|-----------|----------------|
| "Run Claude on file C in MusicXML" | `poetry run run-single --file Fux_CantusFirmus_C --model claude --datatype musicxml` |
| "Test all models with ABC format" | `poetry run run-batch --models chatgpt claude gemini --datatypes abc --files Fux_CantusFirmus_C` |
| "Compare with and without context" | `poetry run run-batch --models claude --datatypes musicxml --contexts with without --files Fux_CantusFirmus_C` |
| "Run all formats for ChatGPT" | `poetry run run-batch --models chatgpt --datatypes musicxml mei abc humdrum --files Fux_CantusFirmus_C` |
| "Test everything" | `poetry run run-batch --models chatgpt claude gemini --datatypes musicxml mei abc humdrum --contexts with without --files Fux_CantusFirmus_C` |
| "Use the LLM guide" | `poetry run run-single --file Fux_CantusFirmus_C --context --guide LLM-Guide` |
| "No context, just raw" | `poetry run run-single --file Fux_CantusFirmus_C` (with guide: none in config) |

### Understanding Context
- **With context**: Includes guide documents (LLM-Guide.md or Pierre-Guide.md) in the prompt
- **Without context**: Only sends the music file and base prompt
- Context helps LLMs understand music theory rules better
- Research question: Do guides improve output quality?

### Available Files
Current data files (all in `data/encoded/`):
- `Fux_CantusFirmus_A`
- `Fux_CantusFirmus_C`
- `Fux_CantusFirmus_D`
- `Fux_CantusFirmus_E`
- `Fux_CantusFirmus_F`
- `Fux_CantusFirmus_G`

Each file represents a cantus firmus in a different key (A, C, D, E, F, G).

## Workflow Examples

### Example 1: Quick Single Test
**User**: "Run Claude on the C cantus firmus"

**Agent Actions**:
1. Check config.yaml for defaults
2. Run: `poetry run run-single --file Fux_CantusFirmus_C`
3. Report: "Running Claude with MusicXML format (from config). Output will be saved to outputs/response/claude/..."

### Example 2: Batch Comparison
**User**: "Compare all three models using ABC format"

**Agent Actions**:
1. Run: `poetry run run-batch --models chatgpt claude gemini --datatypes abc --files Fux_CantusFirmus_C`
2. Report: "Running 3 tests (ChatGPT, Claude, Gemini with ABC). This will take approximately 6-30 seconds..."
3. After completion: "Results saved to outputs/response/{model}/no-context/abc/"

### Example 3: Format Testing
**User**: "Test MusicXML and MEI with Gemini"

**Agent Actions**:
1. Run: `poetry run run-batch --models gemini --datatypes musicxml mei --files Fux_CantusFirmus_C`
2. Report: "Testing Gemini with 2 formats (MusicXML, MEI)..."

### Example 4: Context Comparison
**User**: "Does the LLM guide help Claude?"

**Agent Actions**:
1. Run: `poetry run run-batch --models claude --datatypes musicxml --contexts with without --guide LLM-Guide --files Fux_CantusFirmus_C`
2. Report: "Running Claude twice: once with LLM-Guide context, once without. Compare outputs in outputs/response/claude/context/ vs outputs/response/claude/no-context/"

## Troubleshooting Common Issues

### Exit Code 2: Missing Arguments
**Problem**: Command fails with "required: --model, --datatype"
**Solution**: Either set defaults in config.yaml or provide flags explicitly

### API Key Errors
**Problem**: "Required key missing or placeholder"
**Solution**: Check .env file has valid API keys:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### Truncated Responses
**Problem**: MusicXML output incomplete (e.g., only 80 lines)
**Solution**: Increase max_tokens in config.yaml (default: 16000)

### Timeout Errors
**Problem**: API call times out
**Solution**: Increase timeout in config.yaml (default: 600s) or set to 0 for no timeout

### File Not Found
**Problem**: "Encoded source file not found"
**Solution**: 
1. Check available files: `poetry run run-single --list-files`
2. Verify datatype exists: `poetry run run-single --list-datatypes`
3. Ensure file exists in data/encoded/{datatype}/

## Best Practices for Agents

1. **Always use absolute paths** when working with files
2. **Check config.yaml first** to understand current defaults
3. **Use --list-* commands** to verify available resources
4. **Estimate time for batch runs**: ~2-10 seconds per API call
5. **Monitor outputs/** directory for results
6. **For long batch runs**, set `isBackground: true` in run_in_terminal
7. **Verify .env exists** before running API calls
8. **Use poetry run** prefix for all CLI commands
9. **Check exit codes**: 0 = success, 2 = user error, 1 = unexpected error

## Testing Changes

After modifying code:
```bash
# Run single test
pytest tests/test_runner.py -v

# Run all tests
pytest -v

# Run specific test function
pytest tests/test_runner.py::test_runner_basic -v
```

## Git Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit with clear message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## API Rate Limits & Costs

**Be mindful when running batch tests:**
- Each API call costs money (varies by provider and model)
- Rate limits apply (especially for ChatGPT and Claude)
- Use `--delay` flag in batch runs to space out requests
- Default delay: 2 seconds between calls

**Estimated times:**
- Single run: 2-10 seconds
- Batch (3 models, 1 format): ~10-30 seconds
- Full comparison (3 models, 4 formats, 2 contexts): ~5-10 minutes

## Quick Reference Card

```bash
# List available resources
poetry run run-single --list-files
poetry run run-single --list-datatypes
poetry run run-single --list-guides

# Simple single run (uses config.yaml)
poetry run run-single --file Fux_CantusFirmus_C

# Single run with overrides
poetry run run-single --file Fux_CantusFirmus_C --model chatgpt --datatype abc

# Batch: All models, one format
poetry run run-batch --models chatgpt claude gemini --datatypes musicxml --files Fux_CantusFirmus_C

# Batch: Compare contexts
poetry run run-batch --models claude --datatypes musicxml --contexts with without --files Fux_CantusFirmus_C

# Batch: Full test matrix
poetry run run-batch --models chatgpt claude gemini --datatypes musicxml mei abc humdrum --contexts with without --files Fux_CantusFirmus_C
```

## Summary

This repository provides a clean, organized way to test LLM models on music theory tasks. As an LLM agent:
1. Parse user's natural language request
2. Map to appropriate CLI command(s)
3. Execute with `run_in_terminal` tool
4. Report results and output locations
5. Help user interpret results if needed

Focus on understanding the user's research question (comparing models, formats, or contexts) and translate that into the appropriate batch or single run command.
