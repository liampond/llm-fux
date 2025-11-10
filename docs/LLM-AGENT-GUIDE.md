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

All default settings are in `config.yaml`. This file now supports three modes of operation:

### 1. Default Settings (Always Used)
```yaml
model: claude                    # chatgpt, claude, or gemini
datatype: musicxml              # musicxml, mei, abc, or humdrum
temperature: 0.0                # 0.0-1.0
guide: none                     # LLM-Guide, Pierre-Guide, or none
max_tokens: 16000              # Maximum response length
timeout: 600                   # API timeout in seconds (0 = no timeout)
```

### 2. Single Run Configuration
Configure a specific single run for repeated testing:

```yaml
single_run:
  enabled: true                # Set to true to enable
  file: Fux_CantusFirmus_C    # File to test
  model: claude                # Override default if desired
  datatype: musicxml          # Override default if desired
  guide: LLM-Guide            # Use guide (or 'none')
```

Then run with: `poetry run run-config`

### 3. Batch Run Configuration
Configure batch runs to test multiple combinations:

```yaml
batch_run:
  enabled: true                # Set to true to enable
  models:
    - claude
    - chatgpt
    - gemini
  datatypes:
    - musicxml
    - mei
  files:
    - Fux_CantusFirmus_C
  contexts:
    - with                     # Options: with, without (can list both)
    - without
  guide: LLM-Guide            # Guide for 'with' context runs
  delay: 2                    # Seconds between API calls
```

Then run with: `poetry run run-config`

**Key Points:**
- Only enable ONE of `single_run` or `batch_run` at a time
- Setting `guide: LLM-Guide` automatically enables context
- Setting `guide: none` means no context/guide
- Batch runs with both `with` and `without` contexts will run twice
- Users can edit config.yaml to set up their test scenario, then run `poetry run run-config`
- CLI flags always override config settings

## Running Commands

### Prerequisites
```bash
# Ensure you're in the project directory
cd /Users/liampond/Documents/GitHub/llm-fux

# API keys must be set in .env file
```

### Config-Based Run (NEW - Easiest Method)

**Run using config.yaml settings:**
```bash
poetry run run-config
```

This reads your configured single_run or batch_run from config.yaml and executes it automatically. 

**Examples:**

1. **Quick single test setup:**
   Edit config.yaml:
   ```yaml
   single_run:
     enabled: true
     file: Fux_CantusFirmus_C
     model: claude
     datatype: musicxml
   ```
   Then run: `poetry run run-config`

2. **Batch test all models with MusicXML:**
   Edit config.yaml:
   ```yaml
   batch_run:
     enabled: true
     models: [claude, chatgpt, gemini]
     datatypes: [musicxml]
     files: [Fux_CantusFirmus_C]
     contexts: [without]
   ```
   Then run: `poetry run run-config`

3. **Compare all formats with Claude:**
   Edit config.yaml:
   ```yaml
   batch_run:
     enabled: true
     models: [claude]
     datatypes: [musicxml, mei, abc, humdrum]
     files: [Fux_CantusFirmus_C]
     contexts: [without]
   ```
   Then run: `poetry run run-config`

**Force specific mode:**
```bash
poetry run run-config single   # Force single run
poetry run run-config batch    # Force batch run
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
poetry run run-batch --models <model1,model2> [OPTIONS]
```

**Common batch patterns:**

1. **All models, one format:**
   ```bash
   poetry run run-batch --models chatgpt,claude,gemini --datatypes abc --files Fux_CantusFirmus_C
   ```

2. **One model, all formats:**
   ```bash
   poetry run run-batch --models claude --datatypes musicxml mei abc humdrum --files Fux_CantusFirmus_C
   ```

3. **With context:**
   ```bash
   poetry run run-batch --models chatgpt,claude --datatypes musicxml --context --guide LLM-Guide --files Fux_CantusFirmus_C
   ```

4. **Multiple files, one format:**
   ```bash
   poetry run run-batch --models claude --datatypes musicxml --files Fux_CantusFirmus_A Fux_CantusFirmus_C Fux_CantusFirmus_D
   ```

5. **Full comparison (all models, all formats):**
   ```bash
   poetry run run-batch --models chatgpt,claude,gemini --datatypes musicxml mei abc humdrum --files Fux_CantusFirmus_C
   ```
   (This runs 12 API calls: 3 models × 4 formats)
   
   For with/without context comparison, run the command twice (once with --context, once without)

**Batch Options:**
- `--models`: Comma-separated list (chatgpt,claude,gemini) or 'all'
- `--datatypes`: Space-separated list (musicxml mei abc humdrum)
- `--context`: Include context guide (flag)
- `--files`: Space-separated file IDs
- `--guide`: Guide to use when --context is specified
- `--temperature`: Temperature for all runs
- `--jobs`: Number of parallel jobs (default: 1)
- `--delay`: Seconds between API calls (default: 2)
- `--retry`: Number of retries for failed runs (default: 0)

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
| "Test all models with ABC format" | Configure batch_run in config.yaml with models: [chatgpt, claude, gemini], datatypes: [abc], then `poetry run run-config` |
| "Compare with and without context" | Configure batch_run with contexts: [with, without], then `poetry run run-config` |
| "Run all formats for ChatGPT" | Configure batch_run with models: [chatgpt], datatypes: [musicxml, mei, abc, humdrum], then `poetry run run-config` |
| "Test everything" | Configure batch_run with all models, all datatypes, both contexts, then `poetry run run-config` |
| "Use the LLM guide" | Set guide: LLM-Guide in config.yaml |
| "No context, just raw" | Set guide: none in config.yaml |

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

### Example 2: Batch Comparison Using Config
**User**: "Compare all three models using ABC format"

**Agent Actions**:
1. Update config.yaml:
   ```yaml
   batch_run:
     enabled: true
     models: [chatgpt, claude, gemini]
     datatypes: [abc]
     files: [Fux_CantusFirmus_C]
     contexts: [without]
   ```
2. Run: `poetry run run-config`
3. Report: "Running 3 tests (ChatGPT, Claude, Gemini with ABC). Results saved to outputs/response/{model}/no-context/abc/"

### Example 3: Format Testing
**User**: "Test MusicXML and MEI with Gemini"

**Agent Actions**:
1. Update config.yaml:
   ```yaml
   batch_run:
     enabled: true
     models: [gemini]
     datatypes: [musicxml, mei]
     files: [Fux_CantusFirmus_C]
     contexts: [without]
   ```
2. Run: `poetry run run-config`
3. Report: "Testing Gemini with 2 formats (MusicXML, MEI)..."

### Example 4: Context Comparison
**User**: "Does the LLM guide help Claude?"

**Agent Actions**:
1. Update config.yaml:
   ```yaml
   batch_run:
     enabled: true
     models: [claude]
     datatypes: [musicxml]
     files: [Fux_CantusFirmus_C]
     contexts: [with, without]
     guide: LLM-Guide
   ```
2. Run: `poetry run run-config`
3. Report: "Running Claude twice: once with LLM-Guide context, once without. Compare outputs in outputs/response/claude/context/ vs outputs/response/claude/no-context/"

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

# === CONFIG-BASED RUNS (Recommended) ===
# Edit config.yaml first, then:
poetry run run-config              # Auto-detect single or batch
poetry run run-config single       # Force single run
poetry run run-config batch        # Force batch run

# === DIRECT CLI RUNS ===
# Simple single run (uses config.yaml defaults)
poetry run run-single --file Fux_CantusFirmus_C

# Single run with overrides
poetry run run-single --file Fux_CantusFirmus_C --model chatgpt --datatype abc

# Batch: All models, one format
poetry run run-batch --models chatgpt,claude,gemini --datatypes musicxml --files Fux_CantusFirmus_C

# Batch: One model, all formats
poetry run run-batch --models claude --datatypes musicxml mei abc humdrum --files Fux_CantusFirmus_C

# Batch: With context
poetry run run-batch --models claude --datatypes musicxml --context --guide LLM-Guide --files Fux_CantusFirmus_C
```

## Summary

This repository provides a clean, organized way to test LLM models on music theory tasks. As an LLM agent:

### Recommended Workflow:
1. **Parse user's natural language request**
2. **Edit config.yaml** to set up single_run or batch_run configuration
3. **Execute with** `poetry run run-config`
4. **Report results** and output locations
5. **Help user interpret** results if needed

### Key Commands:
- **`poetry run run-config`** - Run tests based on config.yaml (easiest)
- **`poetry run run-single --file <FILE>`** - Ad-hoc single test
- **`poetry run run-batch --models <MODELS> ...`** - Ad-hoc batch test

### Config-Based Approach Benefits:
- No long CLI commands to construct
- User can easily tweak settings in YAML
- Repeatable test configurations
- Clear documentation of test parameters
- Easy to version control test scenarios

Focus on understanding the user's research question (comparing models, formats, or contexts) and translate that into the appropriate config.yaml settings or CLI command.
