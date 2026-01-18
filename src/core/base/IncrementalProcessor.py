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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.models import IncrementalState
from pathlib import Path
from typing import Any
import logging
import time
import blake3
import orjson
import cbor2

__version__ = VERSION


class IncrementalProcessor:
    """Processes only files changed since last run.

    Tracks file modification times and content hashes to enable
    incremental processing, avoiding reprocessing unchanged files.
    Phases 233/271: Uses BLAKE3 and CBOR with buffered reads for performance.

    Attributes:
        state_file: Path to state persistence file.
        state: Current incremental processing state.
    """

    def __init__(self, repo_root: Path | str, state_file: str = ".agent_state.cbor") -> None:
        """Initialize the incremental processor.

        Args:
            repo_root: Repository root directory.
            state_file: Name of state file.
        """
        self.repo_root = Path(repo_root)
        # Support migration from .json to .cbor if needed, but default to .cbor
        self.state_file = self.repo_root / state_file
        self.state = IncrementalState()
        self._load_state()

    def _load_state(self) -> None:
        """Load state from disk using CBOR (Phase 271)."""
        if not self.state_file.exists():
            # Fallback to .json for migration
            json_state = self.state_file.with_suffix(".json")
            if json_state.exists():
                try:
                    data = orjson.loads(json_state.read_bytes())
                    self._apply_state_data(data)
                    logging.info(
                        f"Migrated incremental state from {json_state} to CBOR"
                    )
                    return
                except Exception as e:
                    logging.warning(f"Failed to migrate from JSON: {e}")
            return

        try:
            data = cbor2.loads(self.state_file.read_bytes())
            self._apply_state_data(data)
            logging.info(
                f"Loaded incremental state (CBOR/BLAKE3) from {self.state_file}"
            )
        except Exception as e:
            logging.warning(f"Failed to load state with CBOR: {e}")

    def _apply_state_data(self, data: dict[str, Any]) -> None:
        """Applies loaded data to the IncrementalState model."""
        self.state = IncrementalState(
            last_run_timestamp=data.get("last_run_timestamp", 0),
            processed_files=data.get("processed_files", {}),
            file_hashes=data.get("file_hashes", {}),
            pending_files=data.get("pending_files", []),
        )

    def _save_state(self) -> None:
        """Save state to disk using optimized CBOR (Phase 271)."""
        try:
            data: dict[str, Any] = {
                "last_run_timestamp": self.state.last_run_timestamp,
                "processed_files": self.state.processed_files,
                "file_hashes": self.state.file_hashes,
                "pending_files": self.state.pending_files,
            }
            # cbor2.dumps returns bytes
            self.state_file.write_bytes(cbor2.dumps(data))
            logging.debug(f"Saved incremental state using CBOR to {self.state_file}")
        except Exception as e:
            logging.warning(f"Failed to save state: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute BLAKE3 hash of file content using buffered reads (Phase 271)."""
        try:
            hasher = blake3.blake3()
            with open(file_path, "rb") as f:
                # Read in 64KB chunks to prevent memory spikes
                while chunk := f.read(65536):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logging.debug(f"Hash calculation failed for {file_path}: {e}")
            return ""

    def validate_hashes(self, files: list[Path]) -> list[Path]:
        """Validates existing hashes against current filesystem state.
        Phase 278: Detects silent mutations (e.g., external edits during agent run).
        """
        mutated = []
        for file_path in files:
            path_str = str(file_path.relative_to(self.repo_root))
            if path_str in self.state.file_hashes:
                current_hash = self._compute_file_hash(file_path)
                if current_hash != self.state.file_hashes[path_str]:
                    logging.warning(
                        f"IncrementalProcessor: DETECTED MUTATION in {path_str}"
                    )
                    mutated.append(file_path)
        return mutated

    # PHASE 263: TOKEN-AWARE BATCHING
    def batch_requests(
        self, files: list[Path], token_limit: int = 4096
    ) -> list[list[Path]]:
        """Groups small file requests into batches for efficient LLM processing."""
        batches: list[list[Path]] = []
        current_batch: list[Path] = []
        current_tokens = 0

        # Tight Pack algorithm (80% target)
        target_limit = int(token_limit * 0.8)

        for file in files:
            if not file.exists():
                continue

            # Simple approximation: 4 characters per token
            file_size = file.stat().st_size
            file_tokens = int(file_size / 4)

            if file_tokens > target_limit:
                # File too large for batching, give it its own "batch"
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                batches.append([file])
                current_tokens = 0
                continue

            if current_tokens + file_tokens > target_limit:
                # Close current batch and start new one
                batches.append(current_batch)
                current_batch = [file]
                current_tokens = file_tokens
            else:
                current_batch.append(file)
                current_tokens += file_tokens

        if current_batch:
            batches.append(current_batch)

        logging.info(
            f"Batched {len(files)} files into {len(batches)} efficient processing units."
        )
        return batches

    def get_changed_files(self, files: list[Path]) -> list[Path]:
        """Get list of files changed since last run.

        Args:
            files: List of all files to consider.

        Returns:
            List of files that have changed.
        """
        changed: list[Path] = []

        for file_path in files:
            path_str = str(file_path)

            # Check if file is new
            if path_str not in self.state.processed_files:
                changed.append(file_path)
                continue

            # Check if file was modified
            try:
                mtime = file_path.stat().st_mtime
                if mtime > self.state.processed_files.get(path_str, 0):
                    # Verify with hash comparison
                    new_hash = self._compute_file_hash(file_path)
                    if new_hash != self.state.file_hashes.get(path_str, ""):
                        changed.append(file_path)
            except Exception:
                changed.append(file_path)

        logging.info(f"Incremental: {len(changed)}/{len(files)} files changed")
        return changed

    def mark_processed(self, file_path: Path) -> None:
        """Mark a file as processed.

        Args:
            file_path: Path to the processed file.
        """
        path_str = str(file_path)
        self.state.processed_files[path_str] = time.time()
        self.state.file_hashes[path_str] = self._compute_file_hash(file_path)

        # Remove from pending if present
        if path_str in self.state.pending_files:
            self.state.pending_files.remove(path_str)

    def complete_run(self) -> None:
        """Mark the run as complete and save state."""
        self.state.last_run_timestamp = time.time()
        self.state.pending_files = []
        self._save_state()

    def reset_state(self) -> None:
        """Reset incremental state (force full reprocessing)."""
        self.state = IncrementalState()
        if self.state_file.exists():
            self.state_file.unlink()
        logging.info("Incremental state reset")
