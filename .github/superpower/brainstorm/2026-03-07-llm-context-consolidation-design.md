# Tiered LLM Context Doc Structure - Design

## 1. Context Structure

**The Root Context (`llms.txt`)**
- A high-level entry point placed in the repository root.
- Contains the core project purpose, the "VOYAGER STABILITY" architecture brief, and links/pointers to the secondary context files.
- Provides just enough context for an LLM to understand what `PyAgent` is and where to find more details.

**Architecture & Code Base Context (`llms-architecture.txt`)**
- Consolidates `docs/architecture/` files.
- Explains the `src/core/base/state.py` transactional integrity, mixins, Rust core bridging, etc.
- Explicitly documents the project's layout rules (e.g., `*.py` files next to `*_test.py`).

**Improvements & Rules Context (`llms-improvements.txt`)**
- Consolidates all scattered `*.description.md` and `*.improvements.md` files.
- Summarizes past improvements, lessons learned, and future ideas.

**Code Rewrites**
- Component-specific markdown files will have their content migrated to module-level docstrings in the Python files themselves.

## 2. Execution & Automation Plan

**The Migration Script (`scripts/consolidate_llm_context.py`)**
- A Python script to scan the repository for target files.
- Parses the contents and injects them into their respective `llms*.txt` tier or Python module docstrings.

**File Cleanup**
- After successful parsing and injection, the script will automatically delete the old scattered markdown files.
- It will output a summary report (`consolidation_report.txt`) showing which files were merged and which were deleted.

**CI / Dev Workflow Integration**
- Add guidelines to `.github/copilot-instructions.md` instructing future AI agents to append new architectural decisions to the `llms-*.txt` files rather than creating new stray `.md` files.

## 3. Superpower Copilot Agent Updates
- Update the custom agents located at `C:\Users\keimpe\.superpower-copilot\agents` to reference this new tiered `llms.txt` structure, optimizing how they consume context going forward.
