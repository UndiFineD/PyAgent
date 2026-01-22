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

"""
Log rotation core.py module.
"""

from __future__ import annotations

import contextlib
import gzip
import os
import shutil
from datetime import datetime
from src.core.base.common.file_system_core import FileSystemCore

from src.core.base.common.file_system_core import FileSystemCore


class LogRotationCore:
    """
    LogRotationCore handles rolling log file strategies with compression.
    It isolates the logic from the logging framework itself for future Rust migration.
    """

    def __init__(self, log_dir: str, max_size_bytes: int = 10 * 1024 * 1024) -> None:
        self.log_dir = log_dir
        self.max_size_bytes = max_size_bytes
        self._fs = FileSystemCore()

    def should_rotate(self, file_path: str) -> bool:
        """Checks if a log file exceeds the size limit."""
        if not os.path.exists(file_path):
            return False
        return os.path.getsize(file_path) > self.max_size_bytes

    def rotate_and_compress(self, file_path: str) -> str | None:
        """
        Rotates the file by renaming it with a timestamp and compressing it via gzip.
        Returns the path to the compressed file.
        """
        if not os.path.exists(file_path):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_path = f"{file_path}.{timestamp}"
        compressed_path = f"{rotated_path}.gz"

        with contextlib.suppress(Exception):
            # Rename for rotation
            self._fs.move(file_path, rotated_path)

            # Compress
            with open(rotated_path, 'rb', encoding='utf-8') as f_in:
                with gzip.open(compressed_path, 'wb', encoding='utf-8') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove uncompressed rotated file
            self._fs.delete(rotated_path)
            return compressed_path

        # If compression fails, try to restore or at least leave the rotated file
        return None

    def calculate_log_level(self, fleet_health_score: float) -> str:
        """
        Dynamically adjusts logging levels based on health score (0.0 to 1.0).
        Lower health = higher logging verbosity.
        """
        if fleet_health_score < 0.3:
            return "DEBUG"
        elif fleet_health_score < 0.6:
            return "INFO"
        elif fleet_health_score < 0.8:
            return "WARNING"
        else:
            return "ERROR"
