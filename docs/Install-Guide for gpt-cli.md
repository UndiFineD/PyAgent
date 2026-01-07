# Installation Guide: gpt-cli

This guide describes how to install and use gpt-cli, a command-line interface for interacting with ChatGPT and other LLMs.

## Prerequisites

- [Python](https://www.python.org/) (3.8 or later)
- API key for OpenAI, Anthropic, or other supported provider

## Installation

Install via `pip`:

```bash
pip install gpt-cli
```

## Configuration

You can configure gpt-cli using environment variables or a YAML configuration file.

### Environment Variable
```bash
export OPENAI_API_KEY=your-api-key-here
```

### Configuration File
Create a file at `~/.config/gpt-cli/config.yaml` (Linux/macOS) or `%USERPROFILE%\.config\gpt-cli\config.yaml` (Windows):

```yaml
openai_api_key: "your-api-key-here"
default_model: "gpt-4"
```

## Basic Usage

### Standard Chat
```bash
gpt chat "What is the best way to learn Python?"
```

### Interactive Session
```bash
gpt interactive
```

### Pipe Input
```bash
cat code.py | gpt chat "Refactor this code for better performance"
```

## Documentation
For more details, visit the [gpt-cli GitHub repository](https://github.com/kharvd/gpt-cli).
