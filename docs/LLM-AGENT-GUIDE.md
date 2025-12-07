# LLM Agent Guide for llm-fux

This guide helps LLM agents (like GitHub Copilot) run API calls on behalf of users.

## Quick Start

**The only command you need:**
```bash
poetry run run
```

That's it. This reads `config.yaml` and executes the configured test.

## How It Works

1. **User describes what they want** ("test Claude with MusicXML")
2. **You edit `config.yaml`** to match their request
3. **You run `poetry run run`**
4. **Results appear in `outputs/`**

## config.yaml Structure

The config has two modes. **Enable only ONE at a time** (set `enabled: true`).

### Single Run Mode
For testing one specific combination:

```yaml
single_run:
  enabled: true                          # Enable this mode
  file: Fux_CantusFirmus_C               # Which file to test
  model: claude                          # chatgpt, claude, or gemini
  datatype: musicxml                     # musicxml, mei, abc, or humdrum
  guide_path: data/guides/Pierre-Guide.md  # Context guide, or null for none
  temperature: 0.0                       # 0.0 to 1.0
  max_tokens: 16000                      # Max response length

batch_run:
  enabled: false                         # Disable batch mode
```

### Batch Run Mode
For testing multiple combinations at once:

```yaml
single_run:
  enabled: false                         # Disable single mode

batch_run:
  enabled: true                          # Enable this mode
  models:                                # Which models to test
    - claude
    - chatgpt
    - gemini
  datatypes:                             # Which formats to test
    - musicxml
    - mei
  files:                                 # Which files to test
    - Fux_CantusFirmus_C
  contexts:                              # with, without, or both
    - with
    - without
  guide_path: data/guides/Pierre-Guide.md  # Guide for "with" context runs
  temperature: 0.0
  max_tokens: 16000
  delay: 2                               # Seconds between API calls
```

## Translating User Requests

| User Says | Edit config.yaml to... |
|-----------|------------------------|
| "Run Claude on MusicXML" | single_run: model: claude, datatype: musicxml |
| "Test all models" | batch_run: models: [chatgpt, claude, gemini] |
| "Compare with and without context" | batch_run: contexts: [with, without] |
| "Test all formats" | batch_run: datatypes: [musicxml, mei, abc, humdrum] |
| "Use the Pierre guide" | guide_path: data/guides/Pierre-Guide.md |
| "No context, raw only" | guide_path: null (single) or contexts: [without] (batch) |

## Available Resources

**Models:** `chatgpt`, `claude`, `gemini`

**Formats:** `musicxml`, `mei`, `abc`, `humdrum`

**Files:**
- `Fux_CantusFirmus_A`
- `Fux_CantusFirmus_C`
- `Fux_CantusFirmus_D`
- `Fux_CantusFirmus_E`
- `Fux_CantusFirmus_F`
- `Fux_CantusFirmus_G`

**Guides:**
- `data/guides/Pierre-Guide.md` - Detailed counterpoint rules
- `data/guides/LLM-Guide.md` - Alternative guide

## Output Location

Results are saved to:
```
outputs/
├── response/{model}/{context}/{format}/    # LLM responses
├── prompt/{model}/{context}/{format}/      # Prompts sent
└── input/{model}/{context}/{format}/       # Input metadata
```

Where:
- `{model}` = Claude, ChatGPT, or Gemini
- `{context}` = context-Pierre, context-LLM, or no-context
- `{format}` = musicxml, mei, abc, or humdrum

Files are numbered automatically (_1, _2, _3, etc.) to prevent overwrites.

## Workflow Examples

### Example 1: Single Model Test
**User:** "Run Claude on file C in MusicXML"

**Agent:** Edit config.yaml:
```yaml
single_run:
  enabled: true
  file: Fux_CantusFirmus_C
  model: claude
  datatype: musicxml
  guide_path: null

batch_run:
  enabled: false
```

Then run: `poetry run run`

### Example 2: Compare All Models
**User:** "Compare all three models on ABC format"

**Agent:** Edit config.yaml:
```yaml
single_run:
  enabled: false

batch_run:
  enabled: true
  models: [chatgpt, claude, gemini]
  datatypes: [abc]
  files: [Fux_CantusFirmus_C]
  contexts: [without]
  guide_path: null
```

Then run: `poetry run run`

### Example 3: Context Comparison
**User:** "Does the Pierre guide help Claude?"

**Agent:** Edit config.yaml:
```yaml
single_run:
  enabled: false

batch_run:
  enabled: true
  models: [claude]
  datatypes: [musicxml]
  files: [Fux_CantusFirmus_C]
  contexts: [with, without]
  guide_path: data/guides/Pierre-Guide.md
```

Then run: `poetry run run`

This runs Claude twice (with and without guide) for comparison.

## Prerequisites

**API keys must be set in `.env`:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

**Working directory:** Always run from the repository root:
```bash
cd /path/to/llm-fux
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Required key missing" | Check `.env` has valid API keys |
| "Encoded source file not found" | Verify file exists in `data/encoded/{format}/` |
| "Guide file not found" | Use full path: `data/guides/Pierre-Guide.md` |
| Truncated responses | Increase `max_tokens` in config.yaml |
| Timeout | Increase `timeout` in config.yaml (default: 600) |

## Testing Code Changes

```bash
pytest -v              # Run all tests
pytest -v -k "test_"   # Run specific tests
```

## Summary

1. **Edit `config.yaml`** - Set model, format, file, and context
2. **Run `poetry run run`** - Execute the test
3. **Check `outputs/`** - Find the results

That's the entire workflow. Keep it simple.
