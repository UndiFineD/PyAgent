# PyAgent Download Agent

A comprehensive download agent that automatically detects URL types and uses appropriate download mechanisms for different content types.

## Overview

The Download Agent reads URLs from `docs/download/urls.txt` and intelligently handles different types of content:

- **GitHub Repositories** → Git clone to `.external/`
- **GitHub Gists** → Git clone to `.external/gists/`
- **ArXiv Papers** → PDF download to `data/research/`
- **Research Papers** → PDF download to `data/research/`
- **Datasets** → Download to `data/datasets/`
- **Documentation** → Download to `docs/external/`
- **Web Pages** → HTML download to `data/webpages/`

## Installation & Usage

### Basic Usage

```bash
# Process all URLs in docs/download/urls.txt
python download_agent_cli.py

# Dry run to see what would be downloaded
python download_agent_cli.py --dry-run

# Verbose output with detailed logging
python download_agent_cli.py --verbose

# Save results to JSON file
python download_agent_cli.py --output download_results.json
```

### Advanced Options

```bash
# Custom URLs file
python download_agent_cli.py --urls-file my_urls.txt

# Custom base directory
python download_agent_cli.py --base-dir /path/to/project

# Adjust timeouts and retries
python download_agent_cli.py --timeout 60 --max-retries 5

# Control download delays
python download_agent_cli.py --delay 2.0

# Force re-download existing files
python download_agent_cli.py --no-skip-existing
```

### Programmatic Usage

```python
from src.tools.download_agent import DownloadAgent, DownloadConfig

config = DownloadConfig(
    urls_file="docs/download/urls.txt",
    base_dir=".",
    dry_run=True,
    verbose=True
)

agent = DownloadAgent(config)
results = agent.process_urls_file()

# Save results
agent.save_results(results, "download_results.json")
```

## URL Format

URLs in `docs/download/urls.txt` should be one per line:

```
# PyAgent Download URLs
# Format: URL [# optional comment]

# GitHub Repositories
https://github.com/microsoft/vscode # Popular code editor
https://github.com/0xSojalSec/automem-ai-memory # AI memory system

# ArXiv Papers
https://arxiv.org/abs/2305.10601 # Chain-of-Thought paper
https://arxiv.org/pdf/2310.06825.pdf # Direct PDF link

# Research Papers
https://proceedings.neurips.cc/paper_files/paper/2023/file/example.pdf

# Datasets
https://huggingface.co/datasets/imdb/resolve/main/data.parquet

# Documentation
https://raw.githubusercontent.com/project/docs/main/README.md

# Web Pages
https://en.wikipedia.org/wiki/Artificial_intelligence
```

## URL Type Classification

### GitHub Repositories
- **Pattern**: `https://github.com/owner/repo`
- **Action**: `git clone --depth 1` to `.external/owner-repo`
- **Example**: `https://github.com/microsoft/vscode`

### GitHub Gists
- **Pattern**: `https://gist.github.com/owner/id`
- **Action**: `git clone` to `.external/gists/gist-owner-id`
- **Example**: `https://gist.github.com/jwa91/b0fa41d90ceb27f905aa4fd1fdd3dd68`

### ArXiv Papers
- **Pattern**: `https://arxiv.org/abs/id` or `https://arxiv.org/pdf/id.pdf`
- **Action**: Download PDF to `data/research/arxiv_id.pdf`
- **Example**: `https://arxiv.org/abs/2305.10601`

### Research Papers
- **Pattern**: URLs ending in `.pdf` with research-related keywords
- **Action**: Download to `data/research/`
- **Example**: `https://proceedings.neurips.cc/paper/2023/file/paper.pdf`

### Datasets
- **Pattern**: URLs containing dataset-related keywords
- **Action**: Download to `data/datasets/`
- **Example**: `https://huggingface.co/datasets/imdb/resolve/main/data.parquet`

### Documentation
- **Pattern**: URLs with docs/documentation keywords or raw GitHub content
- **Action**: Download to `docs/external/`
- **Example**: `https://raw.githubusercontent.com/project/docs/main/README.md`

### Web Pages
- **Pattern**: General web URLs (Wikipedia, etc.)
- **Action**: Download HTML to `data/webpages/`
- **Example**: `https://en.wikipedia.org/wiki/Artificial_intelligence`

## Output and Results

The agent provides detailed output including:

- **Progress Tracking**: Real-time status for each URL
- **Success/Failure Summary**: Overall statistics
- **File Type Breakdown**: Content type distribution
- **Size Information**: Total downloaded bytes
- **Error Details**: Specific failure reasons

### JSON Output Format

When using `--output results.json`, the agent saves:

```json
{
  "timestamp": "2026-02-03T10:30:00",
  "config": {
    "urls_file": "docs/download/urls.txt",
    "max_retries": 3,
    "timeout_seconds": 30,
    "dry_run": false
  },
  "results": [
    {
      "url": "https://github.com/microsoft/vscode",
      "success": true,
      "destination": ".external\\microsoft-vscode",
      "file_type": "git_repo",
      "size_bytes": 123456,
      "metadata": {
        "owner": "microsoft",
        "repo": "vscode"
      }
    }
  ],
  "summary": {
    "total": 10,
    "successful": 8,
    "failed": 2,
    "skipped": 0,
    "dry_run": 0,
    "total_size_bytes": 987654
  }
}
```

## Configuration

### Default Settings

- **URLs File**: `docs/download/urls.txt`
- **Base Directory**: Current directory (`.`)
- **Max Retries**: 3 attempts per download
- **Timeout**: 30 seconds per request
- **Delay**: 1 second between downloads
- **Skip Existing**: `true` (don't re-download existing content)

### Environment Variables

```bash
# Custom user agent
export PYAGENT_USER_AGENT="MyCustomAgent/1.0"

# Disable SSL verification (not recommended)
export PYAGENT_VERIFY_SSL=false
```

## Integration

### CI/CD Pipeline

```yaml
# .github/workflows/download.yml
name: Download Resources
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday

jobs:
  download:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Download Agent
        run: python download_agent_cli.py --output download-results.json
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: download-results
          path: download-results.json
```

### Fleet Usage

The Download Agent is designed to be reusable across the PyAgent fleet:

```python
from src.tools.download_agent import DownloadAgent, DownloadConfig

# Custom configuration for different projects
config = DownloadConfig(
    urls_file="research/urls.txt",
    base_dir="/path/to/research/project",
    max_retries=5,
    timeout_seconds=60
)

agent = DownloadAgent(config)
results = agent.process_urls_file()
```

## Error Handling

The agent handles various error conditions:

- **Network Timeouts**: Automatic retries with exponential backoff
- **HTTP Errors**: Detailed error messages with status codes
- **Git Clone Failures**: Repository-specific error reporting
- **Permission Issues**: Clear indication of access problems
- **Disk Space**: Size validation before download

## Security Considerations

- **Safe Git Operations**: Uses `--depth 1` for shallow clones
- **URL Validation**: Only processes known URL patterns
- **Rate Limiting**: Built-in delays to be respectful to servers
- **Content Type Checking**: Validates downloaded content types

## Troubleshooting

### Common Issues

1. **Git Not Found**: Ensure git is installed and in PATH
2. **Permission Denied**: Check write permissions for destination directories
3. **Network Timeouts**: Increase timeout with `--timeout 60`
4. **Large Downloads**: Monitor disk space for big repositories

### Debug Mode

```bash
# Enable verbose logging
python download_agent_cli.py --verbose

# Dry run to check URL classification
python download_agent_cli.py --dry-run --verbose
```

## Contributing

When adding new URL types:

1. Update `URLClassifier.classify_url()` with new patterns
2. Add corresponding download method in `DownloadAgent`
3. Update this documentation
4. Add test cases for new URL types

## License

Copyright 2026 PyAgent Authors. Licensed under Apache 2.0.