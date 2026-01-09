#!/usr/bin/env python3

import os
import logging
import fnmatch
import time
import hashlib
from pathlib import Path
from typing import Set, List, Optional, Dict
from .utils import load_codeignore

class AgentFileManager:
    """Manages file discovery, filtering, and snapshots for the Agent."""
    
    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self, repo_root: Path, agents_only: bool = False, ignored_patterns: Optional[Set[str]] = None) -> None:
        self.repo_root = repo_root
        self.agents_only = agents_only
        self.ignored_patterns = ignored_patterns or load_codeignore(repo_root)

    def is_ignored(self, path: Path) -> bool:
        """Check if a path should be ignored based on .codeignore patterns."""
        try:
            relative_path = str(path.relative_to(self.repo_root)).replace('\\', '/')
        except ValueError:
            # Path not in repo_root
            return True
        
        # Check against ignored patterns
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(relative_path, pattern) or \
               fnmatch.fnmatch(relative_path.split('/')[0], pattern):
                return True
        
        # Default ignores for common directories if not specified
        default_ignores = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', '.agent_cache', '.agent_snapshots'}
        parts = relative_path.split('/')
        if any(part in default_ignores for part in parts):
            return True
            
        return False

    def find_code_files(self, max_files: Optional[int] = None) -> List[Path]:
        """Find code files in the repository, respecting filters and ignore patterns."""
        code_files = []
        
        search_root = self.repo_root
        if self.agents_only:
            # Look for agent-specific directories
            for sub in ['scripts/agent', 'src/classes/agent', 'src/classes/specialized']:
                potential = self.repo_root / sub
                if potential.exists():
                    search_root = potential
                    break

        logging.info(f"Searching for code files in {search_root}")
        
        for root, _, files in os.walk(search_root):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    if not self.is_ignored(file_path):
                        code_files.append(file_path)
                        if max_files and len(code_files) >= max_files:
                            return code_files
                            
        return code_files

    def load_cascading_codeignore(self, directory: Optional[Path] = None) -> Set[str]:
        """Load .codeignore patterns with cascading support."""
        if directory is None:
            directory = self.repo_root

        all_patterns: set[str] = set()
        current_dir = directory.resolve()

        # Walk up to repo root, loading .codeignore files
        while current_dir >= self.repo_root:
            codeignore_file = current_dir / '.codeignore'
            if codeignore_file.exists():
                try:
                    patterns = load_codeignore(current_dir)
                    all_patterns.update(patterns)
                    logging.debug(f"Loaded {len(patterns)} patterns from {codeignore_file}")
                except Exception as e:
                    logging.warning(f"Failed to load {codeignore_file}: {e}")

            # Stop at repo root
            if current_dir == self.repo_root:
                break

            current_dir = current_dir.parent

        logging.debug(f"Total cascading patterns from {directory}: {len(all_patterns)}")
        return all_patterns

    def create_file_snapshot(self, file_path: Path) -> Optional[str]:
        """Create a snapshot of file content before modifications."""
        try:
            if not file_path.exists():
                logging.debug(f"Cannot snapshot non-existent file: {file_path}")
                return None

            # Create snapshots directory if needed
            snapshot_dir = self.repo_root / '.agent_snapshots'
            snapshot_dir.mkdir(exist_ok=True)

            # Generate snapshot ID based on timestamp
            content = file_path.read_text(encoding='utf-8', errors='replace')
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            snapshot_id = f"{time.time():.0f}_{content_hash}"

            # Save relative path and content
            rel_path = file_path.relative_to(self.repo_root)
            snapshot_file = snapshot_dir / f"{snapshot_id}_{rel_path.name}"
            snapshot_file.write_text(content, encoding='utf-8')

            logging.debug(f"Created snapshot {snapshot_id} for {rel_path}")
            return snapshot_id

        except Exception as e:
            logging.error(f"Failed to create snapshot for {file_path}: {e}")
            return None

    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
        """Restore a file from a previously created snapshot."""
        try:
            snapshot_dir = self.repo_root / '.agent_snapshots'
            if not snapshot_dir.exists():
                logging.warning(f"Snapshot directory not found: {snapshot_dir}")
                return False

            # Find snapshot file matching pattern
            rel_path = file_path.relative_to(self.repo_root)
            pattern = f"{snapshot_id}_{rel_path.name}"

            snapshot_file = snapshot_dir / pattern
            if not snapshot_file.exists():
                logging.warning(f"Snapshot not found: {pattern}")
                return False

            # Restore content
            content = snapshot_file.read_text(encoding='utf-8')
            file_path.write_text(content, encoding='utf-8')

            logging.info(f"Restored {rel_path} from snapshot {snapshot_id}")
            return True

        except Exception as e:
            logging.error(f"Failed to restore snapshot for {file_path}: {e}")
            return False

    def cleanup_old_snapshots(self, max_age_days: int = 7,
                              max_snapshots_per_file: int = 10) -> int:
        """Clean up old file snapshots according to retention policy."""
        snapshot_dir = self.repo_root / '.agent_snapshots'
        if not snapshot_dir.exists():
            logging.debug("No snapshot directory found, nothing to clean")
            return 0

        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            snapshots_deleted = 0

            # Group snapshots by file
            snapshots_by_file: Dict[str, List[Path]] = {}
            for snapshot_file in snapshot_dir.glob('*'):
                if snapshot_file.is_file():
                    # Extract filename from snapshot name (format: timestamp_hash_filename)
                    parts = snapshot_file.name.split('_', 2)
                    if len(parts) >= 3:
                        filename = parts[2]
                        if filename not in snapshots_by_file:
                            snapshots_by_file[filename] = []
                        snapshots_by_file[filename].append(snapshot_file)

            # Clean by age and count
            for filename, snapshots in snapshots_by_file.items():
                # Sort by modification time (newest first)
                snapshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)

                for i, snapshot in enumerate(snapshots):
                    # Delete if too old
                    mtime = snapshot.stat().st_mtime
                    age = current_time - mtime
                    if age > max_age_seconds:
                        snapshot.unlink()
                        snapshots_deleted += 1
                        logging.debug(f"Deleted old snapshot: {snapshot.name}")
                    # Or if exceeds max count
                    elif i >= max_snapshots_per_file:
                        snapshot.unlink()
                        snapshots_deleted += 1
                        logging.debug(f"Deleted excess snapshot: {snapshot.name}")

            logging.info(f"Cleaned up {snapshots_deleted} old snapshots")
            return snapshots_deleted

        except Exception as e:
            logging.error(f"Failed to cleanup snapshots: {e}")
            return 0
