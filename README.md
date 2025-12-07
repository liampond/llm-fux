# LLM-Fux

Framework for analyzing Fux counterpoint using Large Language Models (LLMs).

## Overview

This project provides tools for evaluating how well LLMs understand and apply the rules of species counterpoint as described in Johann Joseph Fux's *Gradus ad Parnassum*. The framework supports multiple music encoding formats (MusicXML, MEI, ABC, Humdrum) and multiple LLM providers (ChatGPT, Claude, Gemini).

## Quick Start

```bash
# 1. Install
poetry install --extras all

# 2. Set up API keys in .env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# 3. Edit config.yaml to set your test parameters

# 4. Run
poetry run run
```

That's it! Results appear in `outputs/`.

## Features

- **Multi-format support**: MusicXML, MEI, ABC, Humdrum
- **Multiple LLM providers**: OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini)
- **Context comparison**: Test with/without counterpoint guides
- **Simple workflow**: Edit `config.yaml`, run `poetry run run`

## Configuration

Edit `config.yaml` to configure your tests:

```yaml
# Single test
single_run:
  enabled: true
  file: Fux_CantusFirmus_C
  model: claude           # chatgpt, claude, or gemini
  datatype: musicxml      # musicxml, mei, abc, or humdrum
  guide_path: data/guides/Pierre-Guide.md  # or null for no guide

# Or batch test (set single_run.enabled: false)
batch_run:
  enabled: false
  models: [chatgpt, claude, gemini]
  datatypes: [musicxml, mei]
  files: [Fux_CantusFirmus_C]
  contexts: [with, without]
```

Then run: `poetry run run`

## Project Structure

```
llm-fux/
├── config.yaml          # Test configuration
├── data/
│   ├── encoded/         # Music files (musicxml/, mei/, abc/, humdrum/)
│   ├── guides/          # Context guides for LLMs
│   └── prompts/         # Prompt templates
├── outputs/             # Results organized by model/context/format
├── src/llm_fux/         # Main package code
└── tests/               # Test suite
```

## Documentation

See `docs/LLM-AGENT-GUIDE.md` for detailed usage instructions.

## License

See LICENSE file for details.
