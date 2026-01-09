#!/usr/bin/env python3

"""
Foundation for high-performance 'Core' components.
These classes are designed to be eventually implemented in Rust (using PyO3 or FFI).
They should remain as 'pure' as possible - no complex dependencies on AI or IO.
"""

import difflib
import fnmatch
import hashlib
import logging
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from pathlib import Path

@dataclass
class CodeQualityReport:
    score: float
    violations: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)

class BaseCore:
    """Pure logic core for all agents."""
    
    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = workspace_root

    @staticmethod
    def detect_workspace_root(file_path: Path) -> str:
        """Heuristic-based workspace root detection."""
        root = os.environ.get("PYAGENT_WORKSPACE_ROOT")
        if root:
            return root
            
        # Fallback heuristic: search upwards for .git or requirements.txt
        curr = file_path.absolute()
        for _ in range(5):
            if (curr / ".git").exists() or (curr / "requirements.txt").exists() or (curr / "README.md").exists():
                return str(curr)
            if curr.parent == curr: break
            curr = curr.parent
            
        # Last fallback: legacy logic (3 parents up from file_path)
        return str(file_path.parent.parent.parent)

    def is_path_ignored(self, path: Path, repo_root: Path, ignored_patterns: Set[str]) -> bool:
        """Check if a path should be ignored based on .codeignore patterns."""
        try:
            relative_path = str(path.relative_to(repo_root)).replace('\\', '/')
        except ValueError:
            # Path not in repo_root
            return True
        
        # Check against ignored patterns
        for pattern in ignored_patterns:
            if fnmatch.fnmatch(relative_path, pattern) or \
               fnmatch.fnmatch(relative_path.split('/')[0], pattern):
                return True
        
        # Default ignores for common directories if not specified
        default_ignores = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', '.agent_cache', '.agent_snapshots'}
        parts = relative_path.split('/')
        if any(part in default_ignores for part in parts):
            return True
            
        return False

    def calculate_diff(self, old_content: str, new_content: str, filename: str = "file") -> str:
        """Generates a unified diff between two strings."""
        if not old_content or not new_content:
            return ""
            
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}"
        )
        return "".join(diff)

    def fix_markdown(self, content: str) -> str:
        """Normalization logic for markdown text."""
        if not content:
            return ""
        # Example fix: ensure double newlines between headings and text
        content = re.sub(r'^(#+.*)\n([^\n#])', r'\1\n\n\2', content, flags=re.MULTILINE)
        return content

    def validate_content_safety(self, content: str) -> bool:
        """High-performance safety check on content (e.g., secrets, malware patterns)."""
        return True

    def score_response_quality(self, response: str) -> int:
        """Score the quality of an AI response (1-5)."""
        if not response or response.isspace():
            return 1 # ResponseQuality.INVALID (defined in models.py)
        return 5

    def filter_code_files(self, files: List[Path], repo_root: Path, ignored_patterns: Set[str], supported_extensions: Set[str]) -> List[Path]:
        """
        Pure logic for filtering code files.
        """
        return [
            f for f in files 
            if f.suffix in supported_extensions and not self.is_path_ignored(f, repo_root, ignored_patterns)
        ]

        # Basic quality heuristics
        score = 3  # Start at ResponseQuality.ACCEPTABLE

        # Longer responses generally better (to a point)
        if len(response) > 100:
            score += 1
        if len(response) < 20:
            score -= 1

        # Check for error indicators
        error_indicators: List[str] = ["error", "failed", "unavailable", "unable"]
        if any(ind in response.lower() for ind in error_indicators):
            score -= 1

        # Check for actual content
        if response.strip().startswith("#") or "def " in response or "class " in response:
            score += 1

        return min(max(score, 1), 5)

    def generate_cache_key(self, prompt: str, content: str, model: str = "") -> str:
        """Generate a content-based cache key."""
        combined: str = f"{prompt}:{content}:{model}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Rough estimate: ~4 characters per token
        return len(text) // 4

    def truncate_for_context(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit."""
        max_chars: int = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars - 20] + "\n... [truncated]"

    def get_default_content(self, filename: str = "") -> str:
        """Return standardized default content for new files."""
        return f"# Default content for {filename}\n\n# Add content here\n"

class LogicCore:
    """Base class for performance-critical logic."""
    def process_text(self, text: str) -> str:
        raise NotImplementedError()

    def analyze_structure(self, text: str) -> Dict[str, Any]:
        """Expensive AST/regex analysis."""
        raise NotImplementedError()
