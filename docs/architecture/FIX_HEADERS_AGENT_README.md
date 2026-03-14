# PyAgent Fix Headers Tool

A maintenance tool that ensures all Python files have proper Apache 2.0 license headers and copyright notices.

## Overview

The Fix Headers Tool automatically adds or corrects Apache 2.0 license headers in Python files across the PyAgent codebase. It ensures consistency and proper licensing across all Python files in the project.

## Location

The tool is organized in `src/maintenance/fix_headers/`:
```
src/maintenance/fix_headers/
├── __init__.py              # Package initialization
├── fix_headers_agent.py     # Main FixHeadersAgent class
└── cli.py                   # CLI interface
```

## Usage

### Basic Usage

```bash
# Fix headers in a single file
python fix_headers_cli.py path/to/file.py

# Fix headers in an entire directory
python fix_headers_cli.py src/logic/agents/

# Dry run to see what would be changed
python fix_headers_cli.py --dry-run src/

# Verbose output with detailed progress
python fix_headers_cli.py --verbose src/maintenance/
```

### Module Usage

```bash
# Run as a module
python -m src.maintenance.fix_headers.cli --help
python -m src.maintenance.fix_headers.cli --dry-run src/
```

### Advanced Options

```bash
# Exclude additional directories
python fix_headers_cli.py --exclude .git --exclude build src/

# Combine options for comprehensive processing
python fix_headers_cli.py --dry-run --verbose --exclude __pycache__ --exclude .pytest_cache src/
```

### Programmatic Usage

```python
from src.maintenance.fix_headers import FixHeadersAgent

# Create agent instance
agent = FixHeadersAgent(dry_run=True, verbose=True)

# Process a directory
agent.run("src/logic/agents/")

# Get processing summary
print(agent.get_summary())
```

## Header Format

The agent adds the standard PyAgent Apache 2.0 header:

```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

## Processing Logic

1. **Header Detection**: Checks if files already have proper PyAgent headers
2. **Content Cleaning**: Removes existing shebangs and copyright headers
3. **Header Addition**: Prepends the standard Apache 2.0 header
4. **Content Preservation**: Maintains all original code unchanged

## Default Exclusions

The agent automatically excludes common directories that shouldn't be processed:

- `__pycache__` - Python bytecode cache
- `.git` - Git repository data
- `.venv` - Virtual environments
- `node_modules` - Node.js dependencies
- `.pytest_cache` - Pytest cache

## Examples

### Process Logic Agents Directory

```bash
python fix_headers_cli.py --verbose src/logic/agents/
```

### Dry Run on Entire Source Tree

```bash
python fix_headers_cli.py --dry-run --verbose src/
```

### Fix Single File

```bash
python fix_headers_cli.py src/core/base/mixins/config_mixin.py
```

### Custom Exclusions

```bash
python fix_headers_cli.py --exclude docs --exclude tests --exclude scratch src/
```

## Output Examples

### Verbose Mode Output
```
✓ src/maintenance/agents.py - already has proper header
✏️  src/maintenance/new_file.py - header updated
🔍 src/maintenance/temp_file.py - would be updated (dry run)

Header Fix Summary:
==================
Files processed: 3
Files updated:    1
Files skipped:    1
Mode:             LIVE
```

## Integration

### CI/CD Pipeline

Add to your CI/CD pipeline to ensure all new files have proper headers:

```yaml
# .github/workflows/check-headers.yml
name: Check License Headers
on: [pull_request]

jobs:
  check-headers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Headers
        run: python fix_headers_cli.py --dry-run src/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check that all Python files have proper headers
python fix_headers_cli.py --dry-run src/
if [ $? -ne 0 ]; then
    echo "Some files are missing proper headers. Run 'python fix_headers_cli.py src/' to fix."
    exit 1
fi
```

## Safety Features

- **Dry Run Mode**: Always test with `--dry-run` first
- **Backup Preservation**: Original files are overwritten safely
- **Error Handling**: Continues processing even if individual files fail
- **UTF-8 Encoding**: Proper handling of international characters

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure write permissions on target files
2. **Encoding Errors**: Files must be readable as UTF-8
3. **Large Directories**: Use exclusions to skip unnecessary directories

### Debug Mode

```bash
# Enable verbose logging
python fix_headers_cli.py --verbose --dry-run src/

# Process single problematic file
python fix_headers_cli.py --verbose single_file.py
```

## Contributing

When adding new features:

1. Update the `FixHeadersAgent` class with new functionality
2. Add corresponding CLI options if needed
3. Update this documentation
4. Add tests for new features

## License

Copyright 2026 PyAgent Authors. Licensed under Apache 2.0.
