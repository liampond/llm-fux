# LLM-Fux

Framework for analyzing Fux counterpoint using Large Language Models (LLMs).

## Overview

This project provides tools for evaluating how well LLMs understand and apply the rules of species counterpoint as described in Johann Joseph Fux's *Gradus ad Parnassum*. The framework supports multiple music encoding formats (ABC, HumDrum, MEI, MusicXML) and multiple LLM providers.

## Features

- **Multi-format support**: ABC, HumDrum, MEI, MusicXML
- **Multiple LLM providers**: OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini)
- **Systematic evaluation**: Test LLMs on counterpoint analysis and generation tasks
- **Flexible prompting**: Support for both context-rich and minimal prompts

## Installation

```bash
# Clone the repository
git clone https://github.com/liampond/llm-fux.git
cd llm-fux

# Install dependencies
poetry install

# Install optional providers
poetry install --extras all  # or --extras anthropic, --extras google
```

## Configuration

Set up your API keys in a `.env` file:

```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## Usage

```bash
# Run single experiment
poetry run run-single --model chatgpt --format mei --question Q1

# Run batch experiments
poetry run run-batch --models chatgpt claude gemini --formats mei musicxml
```

## Project Structure

```
llm-fux/
├── data/
│   ├── fux-counterpoint/    # Counterpoint exercises and guides
│   └── prompts/             # Prompt templates
├── src/llm_fux/             # Main package code
├── tests/                   # Test suite
└── docs/                    # Documentation
```

## Documentation

See the `docs/` directory for detailed documentation on:
- Installation and setup
- Configuration options
- Adding new questions
- API reference

## License

See LICENSE file for details.
