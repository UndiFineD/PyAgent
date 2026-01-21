# Installation Guide: GPT4All

This guide describes how to install and use GPT4All, an ecosystem to run open-source LLMs locally on consumer-grade CPUs and GPUs.

## Prerequisites

- Modern CPU with AVX/AVX2 support
- At least 8GB of RAM (16GB recommended)

## Installation

### Desktop Application (Windows/macOS/Linux)
The easiest way is to download the installer from the [GPT4All website](https://gpt4all.io/).

### Python Client
If you want to use GPT4All programmatically via CLI or script:
```bash
pip install gpt4all
```

### CLI (Local Binary)
The standalone CLI is included in the build artifacts or can be compiled from source.

## Configuration

When using the Python client or CLI, you may need to specify the model path. By default, models are stored in:
- Windows: `%LOCALAPPDATA%\nomic.ai\GPT4All\`
- macOS: `~/Library/Application Support/nomic.ai/GPT4All/`
- Linux: `~/.local/share/nomic.ai/GPT4All/`

## Basic Usage (Python CLI Example)

```python
from gpt4all import GPT4All
model = GPT4All("orca-mini-3b-v2.q4_0.gguf")
output = model.generate("The capital of France is ", max_tokens=20)
print(output)
```

## Documentation
For more details, visit the [GPT4All Documentation](https://docs.gpt4all.io/).
