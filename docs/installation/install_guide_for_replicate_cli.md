# Installation Guide: Replicate CLI

This guide describes how to install and use the Replicate Command Line Interface to run and manage cloud-based machine learning models.

## Prerequisites

- A [Replicate account](https://replicate.com/signin)
- A [Replicate API Token](https://replicate.com/account/api-tokens)

## Installation

### macOS
```bash
brew install replicate/tap/replicate
```

### Linux
```bash
curl -sSL https://replicate.sh/install | sh
```

### Windows
Download the latest executable from the [Replicate GitHub Releases](https://github.com/replicate/cli/releases) and add it to your PATH.

## Configuration

Set your API token as an environment variable:

### Windows (PowerShell)
```powershell
$env:REPLICATE_API_TOKEN = "your-api-token-here"
```

### macOS / Linux
```bash
export REPLICATE_API_TOKEN=your-api-token-here
```

## Basic Usage

### Run a Model
```bash
replicate run stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7afe27d5300e84b726c79aee58482 \
  --prompt "a futuristic city in the style of cyberpunk"
```

### Check Current Jobs
```bash
replicate predictions list
```

## Documentation
For more details, visit the [official GitHub repository](https://github.com/replicate/cli).
