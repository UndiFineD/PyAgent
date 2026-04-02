# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# GitHub Import System Architecture

## Overview
A GitHub import system that processes lines from `user/import/github.md` to
download repositories into `.external/github/<user>/<repository>/` and generate
architecture documents with detailed file descriptions.  This infrastructure
is intended to bootstrap automated codebase analysis for onboarding,
compliance audits, and research projects.

The following sections capture motivation, candidate approaches, evaluation
criteria, and risks for each major subsystem.  Once a direction is chosen, a
separate implementation plan can be written using the TDD framework.

## System Components

### 1. Import Configuration Parser

**Motivation:** Provide a human‑editible manifest of repositories to import
so that engineers or automated processes can control the scope without writing
code.

**Candidate approaches:**

1. Simple line‑based parser (current design).
2. YAML or TOML manifest with metadata (version, tags, include/exclude).
3. Web UI backed by a service that stores the list and issues imports via API.

**Success criteria:**

* Parser tolerates blank lines and comments.
* Can reload the configuration without restarting the service.
* Emits structured events (`RepoAdded`, `RepoRemoved`) for downstream
  subscribers.

**Dependencies/Mapping:**

- `src/importer/config.py` (new module).
- Uses standard library `pathlib` & `re` or `toml` if YAML option chosen.
- Hooked into a watcher (watchdog) when file changes.

**Risks & Questions:**

* Should the parser validate that the repository exists on GitHub?
* How to handle authentication tokens for private repos?

---

### 2. Repository Downloader

**Motivation:** Retrieve a local copy of each repository to enable offline
analysis and avoid rate‑limit issues when repeatedly querying GitHub.

**Candidate approaches:**

1. `git clone` with depth=1 for minimal history.
2. Use the GitHub ZIP download API and unpack locally.
3. Leverage `gh` CLI for cloning and authentication.

**Success criteria:**

* Cloning finishes within 30 s for repositories <100 MB.
* Downloads are resumable and idempotent (re‑running does not redownload
  unchanged commits).
* Handles both public and private repos via token.

**Dependencies/Mapping:**

- `src/importer/downloader.py`.
- Needs Git executable or HTTP client (requests) if using ZIP API.
- Should report progress events for UI/monitoring.

**Risks & Questions:**

* Handling large monorepos that exceed disk quotas.
* Dealing with submodules or LFS objects.

---

### 3. File Descriptor Generator

**Motivation:** Produce machine‑readable summaries of every file to accelerate
search, auditing, and architecture extraction without reading the entire
source code each time.

**Candidate approaches:**

1. Walk the filesystem and compute metadata (size, mtime) plus first/last
   lines for context.
2. Use a language parser (tree‑sitter) to capture top‑level declarations.
3. Generate metadata in JSON instead of Markdown for easier consumption by
   other tools (the `.desc.md` format is human‑friendly but verbose).

**Success criteria:**

* Descriptor generation completes within 5 s for a 500‑file repo.
* Contains enough information that a later architecture compiler can operate
  purely on descriptors.

**Dependencies/Mapping:**

- `src/importer/describe.py`.
- Optional dependency on `tree_sitter` or `pygments` for language heuristics.

**Risks & Questions:**

* Descriptor explosion if binary files are included (should be skipped).
* Keeping descriptors in sync when the repo is updated.

---

### 4. Architecture Document Compiler

**Motivation:** Aggregate individual file descriptions into a single
navigable document for humans and tools to quickly understand a codebase’s
structure.

**Candidate approaches:**

1. Concatenate `*.desc.md` files with a generated table of contents.
2. Produce a separate `architecture.json` that includes the same information
   but structured; render Markdown from it when needed.
3. Build a small static site generator that creates browsable HTML docs.

**Success criteria:**

* The compiled `architecture.md` clearly mirrors the repository hierarchy.
* Compilation is incremental: only changed descriptors are reprocessed.

**Dependencies/Mapping:**

- `src/importer/compile.py`.
- May reuse the same Markdown template engine used by docs elsewhere.

**Risks & Questions:**

* Dealing with paths that contain characters invalid in Markdown titles.
* Size of the final document for very large repos (could exceed editors’ limits).

## Workflow

1. **Configuration Loading** - The system loads the `user/import/github.md` file 
   to get the list of repositories to import.

2. **Repository Parsing** - Each line in the file is parsed 
   to extract the user and repository name in the format `user/repository`.

3. **Repository Download** - For each repository, the system downloads it 
   to the directory structure: `.external/github/<user>/<repository>/`.

4. **File Description Generation** - The system creates a `*.desc.md` file 
   for every file in every directory of the downloaded repository.

5. **Architecture Compilation** - All the content from the `*.desc.md` files 
   is combined into a single `architecture.md` file in the repository's directory.

## Detailed File Description Format

Each `*.desc.md` file follows this format:

```markdown
# File Description: <filename>

## Path
<full_path_to_file>

## Size
<size_in_bytes>

## Last Modified
<timestamp>

## Content Summary
<brief_summary_of_file_content>

## Purpose
<description_of_file_purpose_and_function>

## Dependencies
<list_of_dependencies_or_other_files>

## Usage Context
<description_of_when_and_where_the_file_is_used>

## Version Information
<version_information_if_available>

## Notes
<additional_notes_or_information>
```

## Architecture Document Structure

The final `architecture.md` file contains a comprehensive overview 
of the entire repository, organized by component and functionality.

### 1. Repository Overview
A high-level summary of the repository including its purpose, scope, and key components.

### 2. Component Breakdown
A detailed breakdown of each major component in the repository, 
including its purpose, structure, and key files.

### 3. File System Hierarchy
A complete map of the file system hierarchy showing all directories and files.

### 4. Key Files and Functions
A list of the most important files and their key functions within the system.

### 5. Interactions and Dependencies
A description of how different components and files interact with each other.

### 6. Design Patterns and Principles
An overview of any design patterns or architectural principles used in the repository.

### 7. Future Enhancements
A list of potential future enhancements or features that could be added to the system.

## Error Handling and Failure Modes

- **File Not Found** - If the `user/import/github.md` file is missing, 
  the system will log an error and halt execution.
- **Parsing Errors** - If a line in the file cannot be parsed into 
  a valid `user/repository` format, the system will log the error and skip that line.
- **Download Failures** - If a repository download fails, the system will log the error 
  and continue with the next repository.
- **File Generation Failures** - If a file description cannot be generated, 
  the system will log the error and continue with the next file.
- **Compilation Failures** - If the architecture document compilation fails, 
  the system will log the error and halt execution.

## Security Considerations

- **Authentication** - The system requires authentication to access GitHub repositories.
- **Authorization** - The system must have proper authorization to download 
  and access repository files.
- **Data Privacy** - The system ensures that no sensitive data is exposed 
  during the download or processing process.
- **Secure Storage** - Downloaded files are stored in a secure, 
  isolated directory structure to prevent unauthorized access.

## Performance Optimization

- **Batch Processing** - The system processes multiple repositories 
  in a batch to minimize network overhead.
- **Parallel Downloads** - Repository downloads are performed 
  in parallel to reduce total download time.
- **Caching** - Frequently accessed files are cached to reduce redundant downloads.
- **Efficient File Reading** - The system reads files in chunks to minimize memory usage.

## Integration Points

- **User Interface** - The system can be integrated into a user interface 
  for easy configuration and monitoring.
- **Automation Scripts** - The system can be used in automation scripts 
  to import repositories as part of a larger workflow.
- **CI/CD Pipelines** - The system can be integrated into CI/CD pipelines 
  to automatically import repositories during deployment.

## Implementation Status

A minimal version of the import system is already live in the codebase:

* `src/importer/config.py`, `downloader.py`, `describe.py`, and
  `compile.py` modules are present with stub implementations.
* Corresponding unit tests (`tests/test_import_config.py`,
  `tests/test_downloader.py`, `tests/test_describe.py`,
  `tests/test_compile.py`, and the end-to-end `tests/test_importer_flow.py`)
  have been written and currently pass.
* Basic Makefile or script hooks are not yet defined, but the skeleton
  demonstrates the envisioned workflow.

This means the coursework described earlier under “System Components” has
been bootstrapped; further work can now iterate on more realistic
parsing, network downloads, and descriptor logic.

## Future Enhancements

- **Repository Analysis** - Enhanced analysis of repository content 
  to identify code quality issues, security vulnerabilities, and technical debt.
- **AI-Powered Suggestions** - Integration of AI models to provide suggestions 
  for code improvements, refactoring, and optimization.
- **Version Comparison** - Ability to compare different versions 
  of a repository to track changes over time.
- **Dependency Graph** - Generation of a detailed dependency graph 
  showing how files and components relate to each other.
- **Multi-Repository Support** - Expansion to support importing 
  multiple repositories simultaneously.
- **Blockchain Integration** - Potential integration 
  with blockchain technology for immutable repository records.

This architecture provides a complete, scalable, and secure system 
for importing and analyzing GitHub repositories 
with detailed file descriptions and a comprehensive architecture document.
