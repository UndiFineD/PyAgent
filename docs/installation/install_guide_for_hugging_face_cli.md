# Installation Guide: Hugging Face CLI

This guide describes how to install and use the Hugging Face Hub CLI to interact with models, datasets, and spaces.

## Prerequisites

- [Python](https://www.python.org/) (3.8 or later)
- [pip](https://pip.pypa.io/en/stable/installation/)
- A [Hugging Face account](https://huggingface.co/join) (optional but recommended for authentication)

## Installation

The CLI is part of the `huggingface_hub` library. You can install it using `pip`:

```bash
pip install -U "huggingface_hub[cli]"
```

## Configuration

To access private or gated models, you need to log in to your account:

```bash
huggingface-cli login
```

This will prompt you for a User Access Token, which you can generate in your [Hugging Face settings](https://huggingface.co/settings/tokens).

## Basic Usage

### Download a Model
```bash
huggingface-cli download gpt2
```

### Download a specific file
```bash
huggingface-cli download gpt2 config.json
```

### List Models
```bash
huggingface-cli scan-cache
```

## Documentation
For more details, visit the [official documentation](https://huggingface.co/docs/huggingface_hub/guides/cli).
