# Installation Guide: OpenAI CLI

This guide describes how to install and use the official OpenAI Command Line Interface.

## Prerequisites

- [Python](https://www.python.org/) (3.7.1 or later)
- An [OpenAI API account](https://platform.openai.com/signup)
- An [OpenAI API Key](https://platform.openai.com/account/api-keys)

## Installation

You can install the OpenAI CLI using `pip`:

```bash
pip install --upgrade openai
```

## Configuration

To use the CLI, you need to set your API key as an environment variable:

### Windows (Command Prompt)
```cmd
setx OPENAI_API_KEY "your-api-key-here"
```

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

### macOS / Linux
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Basic Usage

### List Models
```bash
openai models list
```

### Chat Completion
```bash
openai api chat.completions.create -m gpt-4 -g user "Hello, how can you help me today?"
```

## Documentation

For more detailed information, visit the [official OpenAI Python Library documentation](https://github.com/openai/openai-python).
