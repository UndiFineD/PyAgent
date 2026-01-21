# Installation Guide: LocalAI

This guide describes how to install and use LocalAI, a self-hosted, community-driven, local OpenAI-compatible API.

## Prerequisites

- [Docker](https://www.docker.com/) (recommended)
- OR [Go](https://golang.org/) and C++ compiler (for manual builds)

## Installation

### Using Docker (Recommended)
You can run LocalAI using a single Docker command:

```bash
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-aio-cpu
```
*Note: Use `latest-aio-gpu-nvidia` if you have an NVIDIA GPU.*

### Using Binary (macOS/Linux)
```bash
curl -Lo local-ai https://github.com/mudler/LocalAI/releases/download/v2.19.4/local-ai-$(uname -s)-$(uname -m)
chmod +x local-ai
./local-ai
```

## Configuration

LocalAI looks for model configurations in the `models/` folder. You can add GGUF, Diffusers, or other supported model files there.

## Basic Usage

### Check Available Models
```bash
curl http://localhost:8080/v1/models
```

### Chat Completion (OpenAI Compatible)
```bash
curl http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "How are you?"}],
     "temperature": 0.7
   }'
```

## Documentation
For more details, visit the [LocalAI Documentation](https://localai.io/).
