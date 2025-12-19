# PyAgent Runner Setup Guide

This guide explains how to configure and run the PyAgent orchestration system.

## Prerequisites

- Python 3.10+
- Git
- Access to an AI Backend (OpenAI Codex, GitHub Copilot CLI, or GitHub Models)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/debvisor/pyagent
   cd pyagent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

PyAgent can be configured via command-line arguments or environment variables.

### Environment Variables

- `DV_AGENT_BACKEND`: Selects the AI backend (`codex`, `copilot`, `gh`, `github-models`, `auto`).
- `DV_AGENT_MODEL`: Specifies the model to use (backend-dependent).
- `DV_AGENT_MAX_TOKENS`: Max tokens for generation (default: 4096).
- `DV_AGENT_TEMPERATURE`: Sampling temperature (default: 0.7).

## Running the Agent

### Basic Execution

Run the agent on the current directory:

```bash
python src/agent.py --dir .
```

### Reasoning Strategies

You can choose how the agent "thinks" using the `--strategy` flag:

- **Direct** (`--strategy direct`): Fast, zero-shot prompting. Good for simple tasks.
- **Chain-of-Thought** (`--strategy cot`): The agent plans its steps before executing. Good for complex logic.
- **Reflexion** (`--strategy reflexion`): The agent critiques and revises its own work. Best for high-quality output.

```bash
python src/agent.py --dir . --strategy cot
```

### Parallel Execution

For large repositories, you can run agents in parallel:

```bash
# Use 4 worker processes
python src/agent.py --dir . --multiprocessing --workers 4
```

### Selective Execution

Run only specific sub-agents:

```bash
python src/agent.py --dir . --only-agents coder,tests
```

### Async I/O

Enable asynchronous file processing for better I/O performance:

```bash
python src/agent.py --dir . --async
```

## Troubleshooting

- **Backend Errors**: Ensure you have the necessary CLI tools installed (e.g., `gh` for GitHub Copilot) and are authenticated.
- **Path Issues**: Run the agent from the repository root.
