# PyAgent: AI-Powered Code Improvement Orchestration (v3.6.0-PHASE-317)

An intelligent orchestration system that coordinates specialized AI agents to automatically improve code quality, documentation, testing, and code artifacts across Python projects.

## Overview

**PyAgent** is a comprehensive framework for multi-agent code improvement. It coordinates various specialized agents that work together to enhance code quality, generate documentation, improve tests, and maintain code artifacts. The system acts as an intelligent project manager, delegating specific improvement tasks to domain-expert agents while tracking progress and managing dependencies.

## Key Features

### 🎯 Roadmap Targets set

### 🚀 Latest developments 

### 🏆 Goals reached 

### 🛠 Core development

### 🛠 Project development

### � Extensions & Community Plugins

### �🔧 Specialized Agent Modules

### 📊 Statistics

### 🌐 Interfaces

PyAgent now supports a unified multi-interface architecture 
connected via a central **Fleet Load Balancer**:
- **Mobile**: Flutter-based mobile companion.
- **Web**: FastAPI-powered web interface.
- **CLI**: A high-performance Command Line Interface ([pyagent_cli.py](src/interface/ui/cli/pyagent_cli.py)) for terminal-based automation.

### 🚀 Architecture 

## 🧠 Research and Knowledge gained


## Installation

```bash
git clone https://github.com/UndiFineD/PyAgent
cd PyAgent
# Configure your virtual environment
python -m venv .venv
. .venv/bin/activate  # Or your platform equivalent
pip install -r requirements.txt
```

## Configuration

Create a `.agent.yml` file in your project root:

```yaml
# Agent Configuration
agent:
  backend: "codex"  # Options: "codex" (default), "copilot", "gh", "github-models", "auto"
  timeout: 30
  retries: 3

# Model Selection
models:
  code_review:
    model_id: "gpt-4"
    temperature: 0.7
    max_tokens: 2000

# Feature Flags
features:
  async_execution: true
  report_generation: true
  annotation_support: true
  html_export: true
  csv_export: true
```


## Usage

### Command Line Interface

```bash
# High-performance CLI entrypoint
python -m src.interface.ui.cli.pyagent_cli --task "Analyze codebase" --strategy cot
```


## Project Structure

```text
pyagent/
├── src/
│   ├── classes/                      # Modular class-based logic
│   │   ├── base_agent/               # Foundation & utilities
│   │   ├── agent/                    # Orchestration logic
│   │   ├── coder/                    # Coder, MarkdownAgent, etc.
│   │   ├── context/                  # KnowledgeAgent, ContextAgent
│   │   └── ...                       # Other specialist agents
│   ├── agent.py                      # Main orchestrator wrapper
│   ├── agent_gui.py                  # Interactive dashboard
│   ├── agent_coder.py                # Specialized CLI wrappers
│   ├── agent_knowledge.py            # Workspace knowledge manager
│   └── ...                           # Legacy/wrapper entry points
├── tests/                            # Unit and integration tests
├── docs/                             # Project documentation
├── .codeignore                       # Patterns to skip during scan
└── README.md                         # This file
```

### Programmatic Usage

```python
from src.core.base.BaseAgent import BaseAgent

# Create agent for code improvement
agent = BaseAgent("path/to/file.py")

# Read and analyze content
agent.read_previous_content()

# Request improvements
agent.improve_content("Add comprehensive docstrings and type hints")

# Apply and save changes
agent.update_file()
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_cli_wrappers.py -v
```
