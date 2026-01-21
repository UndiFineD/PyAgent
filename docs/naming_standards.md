# PyAgent Naming and Style Standards

## 1. Naming Conventions

### Modules/Files
- **Standard**: Strict `snake_case`.
- **Requirement**: Filenames must be lowercase with underscores separating words (e.g., `coder_agent.py`, `identity_mixin.py`).
- **Rationale**: Enforced workspace-wide to align with PEP 8 and ensure cross-platform import stability (especially on case-sensitive filesystems like Linux vs. Windows).

### Classes
- **Standard**: `PascalCase`.
- **Requirement**: Use capitalized words without separators (e.g., `CoderAgent`).

### Variables/Methods
- **Standard**: `snake_case`.
- **Requirement**: Lowercase with underscores (e.g., `calculate_metrics()`, `current_content`).

### Folders and Directories
- **Standard**: Strict `snake_case`.
- **Requirement**: All folders in `src`, `models`, `fixes`, `tests`, and `temp` must be lowercase. No hyphens or PascalCase folders (e.g., `sql_agent` instead of `SQLAgent`).
- **Rationale**: Ensures uniform path resolution across all tier levels and prevents Windows/Linux case-sensitivity mismatch.

## 2. Documentation Style

### Docstring Standards
- **Standard**: Strict **Google Style** or **NumPy Style**.
- **Requirement**: Use descriptive sections for `Args`, `Returns`, and `Raises`.
- **Format**: Obsidian-compatible Markdown. Ensure all internal links use the `[[file]]` or `[text](file.md)` format compatible with Obsidian vaults.

## 3. Error Handling

### Pattern
- **Standard**: **Exceptions + Tuple Results**.
- **Usage**: Prefer raising specific exceptions for critical failures and returning `tuple[bool, str]` (SuccessStatus, Message/Data) for high-level agent outcomes to ensure clear state communication in the swarm.

---
*Maintained under Voyager Stability Guidelines.*
