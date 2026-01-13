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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Utility functions used by the Agent classes."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import importlib.util
import sys
from pathlib import Path
from typing import Set, Optional, Any, cast
from collections.abc import Callable

__version__ = VERSION

# Global cache for .codeignore patterns to avoid re-parsing
_CODEIGNORE_CACHE: dict[str, set[str]] = {}
_CODEIGNORE_CACHE_TIME: dict[str, float] = {}

def load_codeignore(root: Path) -> set[str]:
    """Load and parse ignore patterns from .codeignore file.

    Reads the .codeignore file from the repository root and extracts all
    ignore patterns (lines that are not empty or comments).

    Caches patterns to avoid re-parsing on subsequent calls. Cache is invalidated
    if the file is modified (checked by file mtime).

    Args:
        root: Path to the repository root directory.

    Returns:
        Set of ignore patterns (strings) from the .codeignore file.
        Returns empty set if file doesn't exist.

    Raises:
        None. Logs warnings if file cannot be read but doesn't raise.

    Example:
        patterns=load_codeignore(Path('/repo'))
        # patterns might be: {'*.log', '__pycache__/', 'venv/**'}

    Note:
        - Lines starting with '#' are treated as comments and ignored
        - Empty lines are skipped
        - File encoding is assumed to be UTF-8
        - Patterns are cached with mtime checking for efficiency
    """
    codeignore_path = root / ".codeignore"
    cache_key = str(codeignore_path)

    # Check cache validity
    if cache_key in _CODEIGNORE_CACHE and codeignore_path.exists():
        try:
            file_mtime = codeignore_path.stat().st_mtime
            cache_time = _CODEIGNORE_CACHE_TIME.get(cache_key, 0)
            if file_mtime == cache_time:
                logging.debug(f"Using cached .codeignore patterns for {cache_key}")
                return _CODEIGNORE_CACHE[cache_key]
        except OSError:
            pass

    if codeignore_path.exists():
        try:
            logging.debug(f"Loading .codeignore patterns from {codeignore_path}")
            content = codeignore_path.read_text(encoding='utf-8')
            patterns = {
                line.strip() for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            }
            logging.info(f"Loaded {len(patterns)} ignore patterns from .codeignore")

            # Cache the patterns
            _CODEIGNORE_CACHE[cache_key] = patterns
            try:
                _CODEIGNORE_CACHE_TIME[cache_key] = codeignore_path.stat().st_mtime
            except OSError:
                pass

            return patterns
        except Exception as e:
            logging.warning(f"Could not read .codeignore file: {e}")
    else:
        logging.debug(f"No .codeignore file found at {codeignore_path}")
    return set()

def setup_logging(verbosity: str | None = None) -> None:
    """Configure logging based on verbosity level.
    
    Defaults to WARNING to capture only errors and failures as requested.
    """
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    
    # Determine level from environment or argument
    level = levels.get(str(verbosity).lower(), logging.WARNING) if verbosity else logging.WARNING
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    if level <= logging.DEBUG:
        logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")

def _multiprocessing_worker(agent_instance: Any, file_path: Path) -> Path | None:
    """Worker function for multiprocessing file processing.

    This function must be at module level to be pickleable for multiprocessing.
    """
    try:
        logging.debug(f"[worker] Processing {file_path.name}")
        agent_instance.process_file(file_path)
        logging.info(f"[worker] Completed {file_path.name}")
        return file_path
    except Exception as e:
        logging.error(f"[worker] Failed: {e}")
        return None

def _load_fix_markdown_content() -> Callable[[str], str]:
    """Load the markdown fixer module dynamically."""
    # Calculate path from this file's location: src/classes/agent/utils.py
    # We need to go: utils.py -> agent -> classes -> src -> ../fix
    this_file = Path(__file__)
    fix_dir = this_file.parent.parent.parent.parent / 'fix'
    target_file = fix_dir / "fix_markdown_lint.py"
    
    if not target_file.exists():
        logging.debug(f"Markdown fixer not found at {target_file}. Using fallback.")
        def _fallback(text: str) -> str:
            return text
        return _fallback

    spec = importlib.util.spec_from_file_location(
        "fix_markdown_lint", str(target_file))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["fix_markdown_lint"] = module
        spec.loader.exec_module(module)
        return cast(Callable[[str], str], module.fix_markdown_content)

    def _fallback(text: str) -> str:
        return text

    return _fallback

fix_markdown_content: Callable[[str], str] = _load_fix_markdown_content()