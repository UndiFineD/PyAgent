# Description: `agent-context.py`

## Module purpose

Improves and maintains `*.description.md` “context” files for source code.

The agent can optionally derive and read the matching source file (same stem) to
provide better context to the LLM prompt.

## Location

- Path: `src/agent-context.py`

## Public surface (high level)

- CLI:

  - `main` (created via `create_main_function(...)`)
- Primary class:

  - `ContextAgent(BaseAgent)`
- Key supporting types (selected):

  - Enums: `ContextPriority`, `FileCategory`, `SearchAlgorithm` (and others)
  - Dataclasses: `ContextTemplate`, `ContextTag`, `ContextVersion`,
    `ValidationRule`, `ContextAnnotation` (and others)
  - Helper classes: `SemanticSearchEngine`, `CrossRepoAnalyzer` (and others)

## Behavior summary

- Input is typically a file named `something.description.md`.
- Derives a source path by checking common extensions (e.g. `.py`, `.js`, `.ts`,

  `.go`, `.rs`, `.java`, `.sh`) next to the context file.
- When a source file is available, reads up to ~8000 characters and appends it

  to the prompt before delegating to `BaseAgent.improve_content()`.
- Provides local helpers for templates/tags/versioning/validation/annotations/

  metadata export that can be used by callers or tests.

## How to run

```bash
python src/agent-context.py path/to/file.description.md
```

## Key dependencies

- `base_agent.BaseAgent`
- `base_agent.create_main_function`

## File fingerprint

- SHA256(source): `61b976a17c5402d83b2c6f9e259afffd7621b9f3dcda3e0c072aab7cd387cf40`
