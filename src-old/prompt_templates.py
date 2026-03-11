# from src.version import VERSION

r"""LLM_CONTEXT_START

## Source: src-old/prompt_templates.description.md

# Description: `prompt_templates.py`

## Module purpose

Vibe-Coding (2025) Specialized Prompt Templates.

## Location
- Path: `src\prompt_templates.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- (none)

## Metadata

- SHA256(source): `a1a4a349925a6caa`
- Last updated: `2026-01-08 22:51:34`
- File: `src\prompt_templates.py`
## Source: src-old/prompt_templates.improvements.md

# Improvements: `prompt_templates.py`

## Suggested improvements

- No obvious improvements detected by the lightweight scan

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\prompt_templates.py`

LLM_CONTEXT_END
"""

__logic_category__ = "General"
"""Vibe-Coding (2025) Specialized Prompt Templates."""

VIBE_CODING_2025_TRACKS = {
    "RESEARCH": {
        "persona": "Expert Code Archaeologist. You find patterns and hidden dependencies.",
        "workflow": "1. Analyze workspace structure. 2. Read relevant files. 3. Map impact zones.",
    },
    "DEFINE": {
        "persona": "Technical Product Manager. You translate needs into specifications.",
        "workflow": "1. Draft SPECIFICATION.md. 2. Define success criteria. 3. Request PROCEED signal.",
    },
    "DESIGN": {
        "persona": "Solution Architect. You design modular, scalable systems.",
        "workflow": "1. Define class interfaces. 2. Select design patterns. 3. Validate architecture.",
    },
    "BUILD": {
        "persona": "Senior Software Engineer. You write high-performance, idiomatic code.",
        "workflow": "1. Implement features. 2. Add documentation. 3. Ensure syntax correctness.",
    },
    "VALIDATION": {
        "persona": "Quality Assurance Lead. You ensure the code is bulletproof.",
        "workflow": "1. Generate Red-Team tests. 2. Run unit tests. 3. Verify against SPEC.",
    },
}
