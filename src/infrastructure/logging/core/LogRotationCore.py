from __future__ import annotations
import os
import gzip
import shutil
from typing import List, Optional
from datetime import datetime

class LogRotationCore:
    """
    LogRotationCore handles rolling log file strategies with compression.
    It isolates the logic from the logging framework itself for future Rust migration.
    """

    def __init__(self, log_dir: str, max_size_bytes: int = 10 * 1024 * 1024):
        self.log_dir = log_dir
        self.max_size_bytes = max_size_bytes

    def should_rotate(self, file_path: str) -> bool:
        """Checks if a log file exceeds the size limit."""
        if not os.path.exists(file_path):
            return False
        return os.path.getsize(file_path) > self.max_size_bytes

    def rotate_and_compress(self, file_path: str) -> Optional[str]:
        """
        Rotates the file by renaming it with a timestamp and compressing it via gzip.
        Returns the path to the compressed file.
        """
        if not os.path.exists(file_path):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rotated_path = f"{file_path}.{timestamp}"
        compressed_path = f"{rotated_path}.gz"

        try:
            # Rename for rotation
            shutil.move(file_path, rotated_path)
            
            # Compress
            with open(rotated_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed rotated file
            os.remove(rotated_path)
            return compressed_path
        except Exception:
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
