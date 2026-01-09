# PyAgent: AI-Powered Code Improvement Orchestration

An intelligent orchestration system that coordinates specialized AI agents to automatically improve code quality, documentation, testing, and code artifacts across Python projects.

## Overview

**PyAgent** is a comprehensive framework for multi-agent code improvement. It coordinates various specialized agents that work together to enhance code quality, generate documentation, improve tests, and maintain code artifacts. The system acts as an intelligent project manager, delegating specific improvement tasks to domain-expert agents while tracking progress and managing dependencies.

## Key Features

### 🛠 Evolution Phase 108: Autonomous Self-Improvement

The project has entered an autonomous maintenance phase where the system refactors and optimizes its own source code:
- **Relational Metadata Mapping**: Sharded interaction data (Zlib-compressed) is indexed into a relational SQL layer for meta-analysis at trillion-parameter scales.
- **AI-Driven Self-Healing**: The system identifies and fixes security vulnerabilities, performance bottlenecks, and robustness issues automatically.
- **Rust-Readiness Pipeline**: Automated type hint injection (Local-first AI assisted) is preparing the core logic for high-performance Rust FFI porting.
- **Gatekeeping**: `version.py` enforces maturity requirements to ensure stability during deep refactoring cycles.

### 🎯 Multi-Agent Coordination

- **Agent Orchestration**: Central `Agent` coordinates work among specialized sub-agents.
- **Task Distribution**: Intelligently assigns improvement tasks to appropriate agents.
- **Progress Tracking**: Monitors and reports on improvement metrics.
- **Smart Memory**: Agents retain "useful facts" across sessions and can "forget" bad choices to optimize context window.

### � Extensions & Community Plugins (SDK v2.1.0)

- **Manifest-Based Loading**: Community members can drop plugins into `plugins/` with a `manifest.json`.
- **SDK Version Guard**: Automatic gatekeeping (Major match, Minor >=) to ensure compatibility.
- **Fault-Tolerant Registry**: Broken plugins (syntax/import errors) are automatically isolated into `ResilientStubs`, preventing system crashes.
- **Core/Shell Architecture**: Most system logic has been extracted into "Cores" for streamlined performance and future cross-language porting.

### �🔧 Specialized Agent Modules

- All agents (Coder, Tests, Context, Changes, Errors, Stats) are now modular classes found in `src/classes/`.
- **Legacy Compatibility**: Original entry points in `src/*.py` are now wrappers around the modular framework.

### 📊 Advanced Capabilities

- **Hybrid Caching**: High-performance in-memory cache coupled with persistent disk-based caching for all AI responses.
- **Configurable Backends**: Support for Codex, Copilot CLI, gh copilot, and GitHub Models.
- **Configuration Management**: New global settings for GitHub tokens, model defaults, and caching behavior.
- **Smart Memory & History**: Agents now retain conversation history during GUI sessions, allowing for multi-turn iterative improvements.
- **BMAD V6 Methodology**: Native support for the "Build More, Architect Dreams" method, featuring dynamic tracks (Quick, BMad, Enterprise) and phased workflows.

### 🌐 Interfaces

PyAgent now supports a unified multi-interface architecture connected via a central **Fleet Load Balancer**:
- **GUI**: Comprehensive desktop control center ([MainApp.py](src/classes/gui/MainApp.py)).
- **Mobile**: Flutter-based mobile companion.
- **Web**: FastAPI-powered web interface.
- **CLI**: A new high-performance Command Line Interface ([pyagent_cli.py](src/pyagent_cli.py)) for terminal-based automation.

### 🚀 Architecture

```text
src/
├── classes/          → Modular, class-based core logic
│   ├── base_agent/   → Foundation, Memory, and CLI utilities
│   ├── backend/      → Multi-backend runner with disk caching
│   └── [agent_name]/ → Specialized agent implementations
├── agent.py          → Orchestrator wrapper
└── agent_gui.py      → New interactive multi-agent dashboard
```

## Installation

```bash
git clone https://github.com/PyAgent/pyagent
cd pyagent
python -m pip install -r requirements.txt
```

### GUI Dashboard (Experimental)

Launch the new interactive control center:

```bash
python src/agent_gui.py
```

## Usage

### Command Line Interface

```bash
# Improve a file using specific strategy and JSON output for automation
python src/agent.py --context src/module.py --prompt "Refactor for speed" --strategy cot --json
```

### Advanced Usage

```bash
# Run with specific reasoning strategy
python src/agent.py --dir . --strategy cot  # Chain-of-Thought
python src/agent.py --dir . --strategy reflexion  # Self-correction loop

# Run specific agents only
python src/agent.py --dir . --only-agents coder,tests

# Parallel execution
python src/agent.py --dir . --multiprocessing --workers 4

# Async I/O
python src/agent.py --dir . --async
```

### Programmatic Usage

```python
from src.agent import Agent

# Create agent for code improvement
agent = Agent("path/to/file.py")

# Read and analyze content
agent.read_previous_content()

# Request improvements
agent.improve_content("Add comprehensive docstrings and type hints")

# Apply and save changes
agent.update_file()

# Review changes
diff = agent.get_diff()
print(diff)
```

## Core Components

### Agent System

- **BaseAgent**: Foundation class with common functionality for all agents
- **Agent**: Main orchestrator coordinating all sub-agents
- **AgentBackend**: Interface to AI backends (OpenAI Codex, GitHub Copilot, Claude, etc.)

### Report Generation

- **ReportGenerator**: Creates detailed improvement reports
- **ReportComparison**: Compares before/after code states
- **ReportValidator**: Ensures report quality and completeness
- **ReportAccessControl**: Manages access permissions for reports
- **ReportAnnotationManager**: Adds and manages report annotations

### Advanced Features

- **ContextWindow**: Manages token budgets for LLM interactions
- **ResponseCache**: Caches AI responses for performance
- **TokenBudget**: Tracks and allocates token usage
- **EventManager**: Implements event-driven architecture
- **HealthChecker**: Monitors system health and performance
- **ConfigProfile**: Manages configuration profiles

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

## Features in Detail

### Multi-Agent Orchestration

The `DirectorAgent` (coordinated via `agent.py`) manages work by:

1. Analyzing the codebase structure
2. Identifying improvement opportunities
3. Delegating tasks to specialized agents
4. Collecting and merging improvements
5. Generating reports on changes

### Report Generation System

Generate comprehensive reports including:

- **HTML Reports**: Interactive, styled reports with side-by-side comparisons
- **CSV Exports**: Structured data for analysis and spreadsheets
- **JSON Format**: Machine-readable reports for integration
- **Annotated Reports**: Add custom notes and metadata

### Token Budget Management

- Tracks LLM token usage across all agents
- Prevents budget overruns with allocation limits
- Provides metrics on token consumption per task
- Supports dynamic token reallocation

### Health Monitoring

- System health checks and diagnostics
- Performance metrics collection
- Error rate tracking and reporting
- Request latency monitoring

## API Reference

### Main Agent

```python
class Agent:
    def read_previous_content() -> None
    def improve_content(prompt: str) -> None
    def update_file() -> None
    def get_diff() -> str
```

### Report Generation API

```python
class ReportGenerator:
    def generate(improvements: List[str]) -> Report
    def to_html() -> str
    def to_csv() -> str
    def to_json() -> Dict
```

### Utilities

```python
class ContextWindow:
    def add(message: str, token_count: int) -> None
    def clear() -> None

class TokenBudget:
    def allocate(name: str, tokens: int) -> None
    def release(name: str) -> None
```

## Performance Metrics

- **Token Efficiency**: ~95% utilization of allocated token budget
- **Success Rate**: Typical 87%+ test pass rate on improvements
- **Processing Speed**: Batch processing multiple files in parallel
- **Cache Hit Rate**: 60%+ reduction in API calls with response caching

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.

## Acknowledgments

Built with ❤️ for the Python community. Powered by AI backends including OpenAI Codex, GitHub Copilot, Claude, and other LLM providers.

## Status

**Current Version**: 1.0.0  
**Test Coverage**: 87% (2,352 passing tests)  
**Last Updated**: January 2026

