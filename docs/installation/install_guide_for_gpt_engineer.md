# Installation Guide: gpt-engineer

This guide describes how to install and use gpt-engineer, a tool that builds entire projects from a single prompt.

## Prerequisites

- [Python](https://www.python.org/) (3.10 or later)
- [OpenAI API Key](https://platform.openai.com/account/api-keys)

## Installation

You can install gpt-engineer using `pip`:

```bash
pip install gpt-engineer
```

## Configuration

Set your OpenAI API key as an environment variable:

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

### macOS / Linux
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Basic Usage

### Create a New Project
1. Create an empty directory for your project:
   ```bash
   mkdir my-new-app
   cd my-new-app
   ```
2. Run gpt-engineer:
   ```bash
   gpt-engineer .
   ```
3. Follow the prompts in the `prompt` file created in your project folder.

## Documentation
For more details, visit the [gpt-engineer GitHub repository](https://github.com/gpt-engineer-org/gpt-engineer).
