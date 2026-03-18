# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# PyAgent Core Project Structure Design

## Overview

This document outlines the proposed core project structure for the PyAgent system, defining the directory hierarchy, file organization, and component placement.

## Directory Structure

### Root Project Directory

The repository root is `C:\dev\PyAgent` (not `project/`).  The `project/` subdirectory is a **metadata area** containing documentation, templates and configuration related to managing the PyAgent project; it does *not* house the application source.  The bulk of runnable code remains under `src/`.

```
project/
```

### Core Project Structure

```
project/
├── llms-architecture.txt              # Detailed architecture documentation
├── llms-improvements.txt              # Proposed improvements and enhancements
├── PyAgent.md                           # Project README and overview
├── list.md                          # Comprehensive list for project tasks
├── scripts/                             # Project scripts and utilities
│   ├── setup.py                       # Project setup and initialization
│   └── deploy.py                     # Deployment scripts
├── docs/                                # Project documentation
│   ├── architecture.md               # Project architecture overview
│   ├── api-reference.md             # API documentation
│   ├── getting-started.md           # Getting started guide
│   └── contributing.md              # Contribution guidelines
├── tests/                               # Test suite and test files
│   ├── unit/                          # Unit tests
│   ├── integration/                 # Integration tests
│   └── e2e/                          # End-to-end tests
├── src/                                 # Source code directory
│   ├── logic/                         # Core logic and reasoning
│   │   ├── agents/                  # Specialized agents
│   │   │   ├── coder.py            # Code generation agent
│   │   │   ├── analyst.py          # Analysis agent
│   │   │   └── quantum_scaler.py # Quantum scaling agent
│   │   ├── core/                     # Core reasoning and logic
│   │   └── inference/               # Inference and reasoning
│   ├── core/                          # Core components and mixins
│   │   ├── base/                     # Base mixins and state managers
│   │   ├── providers/               # Provider adapters and configurations
│   │   │   ├── FlmProviderConfig.py
│   │   │   └── FlmChatAdapter.py
│   │   └── transactional_fs/      # Transactional file system
│   └── utils/                         # Utility functions and helpers
├── config/                             # Configuration files
│   ├── pyproject.toml               # Project configuration
│   ├── .gitignore                    # Git ignore configuration
│   └── environment.yaml              # Environment configuration
├── release/                           # Release management
│   ├── notes.md                       # Release notes template
│   └── version.py                    # Version management
├── scripts-old/                      # Legacy scripts (for migration)
└── temp_output/                      # Temporary output files
```

## Directory Purpose and Content

### project/
- Central project directory containing all project documentation and configuration files

### scripts/
- Project scripts for setup, deployment, and automation tasks

### docs/
- Comprehensive project documentation including architecture, API references, and getting started guides

### tests/
- Complete test suite including unit, integration, and end-to-end tests

### src/
- Source code directory with organized subdirectories for different components

### config/
- Project configuration files including pyproject.toml, gitignore, and environment settings

### release/
- Release management files including release notes template and version management

### scripts-old/
- Legacy scripts that may be migrated or deprecated

### temp_output/
- Directory for temporary output files generated during processing

## Design Principles

### 1. Modularity
- Clear separation of concerns with well-defined boundaries between components
- Each directory and file has a single, well-defined purpose

### 2. Scalability
- Directory structure designed to accommodate future growth and expansion
- Clear hierarchy allows for easy addition of new components and features

### 3. Maintainability
- Logical organization makes code and documentation easy to navigate
- Clear naming conventions and consistent structure

### 4. Version Control
- Directory structure supports clear version control and branching strategies
- Configuration files are versioned and tracked

## Implementation Status

The repository already follows the structure laid out above:

* The `project/` directory contains metadata files such as
  `llms-architecture.txt`, `PyAgent.md`, and various templates; many of the
  listed subfolders (scripts, docs, tests) already exist and are populated.
* `src/` holds packages like `core`, `tools`, `roadmap`, and others matching
  the described hierarchy.  Utility modules and agent code have been added in
  their respective subdirectories.
* The `tests/` tree mirrors source packages with unit and integration tests
  present under `tests/structure`, `tests/tools`, and other locations.
* Configuration files (`pyproject.toml`, `.gitignore`) are already under
  `config/` and at the repo root, and the `release/` folder contains version
  helpers.
* Legacy scripts remain in `scripts-old/` and temporary output goes into
  `temp_output/` as described.

Thus Phase 1 of the roadmap—establishing the directory layout and populating
it with initial content—has been largely completed.  Subsequent work will
focus on filling in the placeholder files and ensuring comprehensive test
coverage before proceeding to Phase 2.
## Implementation Roadmap

Phase 1 (0-3 months): 
- Complete foundational structure design and specifications
- Develop initial directory structure and file organization

Phase 2 (3-6 months): 
- Implement core directory structure with initial content
- Develop project configuration files and scripts
- Create initial documentation and test suite

Phase 3 (6-12 months): 
- Populate all directories with appropriate content
- Implement full test coverage and validation
- Optimize directory structure for performance and scalability

This core project structure design provides a comprehensive and scalable foundation for the PyAgent system, ensuring clear organization, maintainability, and future growth potential.