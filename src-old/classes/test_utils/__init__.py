#!/usr/bin/env python3
"""Compatibility shim exposing test utilities under `src.classes.test_utils`."""

try:
    from src.infrastructure.services.dev.test_utils.file_system_isolator import (
        FileSystemIsolator,
    )
    from src.infrastructure.services.dev.test_utils.log_capturer import LogCapturer
    from src.infrastructure.services.dev.test_utils.mock_ai_backend import MockAIBackend
    from src.infrastructure.services.dev.test_utils.module_loader import ModuleLoader
    from src.infrastructure.services.dev.test_utils.snapshot_manager import (
        SnapshotManager,
    )
except Exception:
    # Minimal fallbacks if infrastructure implementations aren't importable
    class ModuleLoader:  # pragma: no cover - fallback stub
        def __init__(self, *a, **k):
            self.agent_dir = None

        def load_module_from_path(self, *a, **k):
            raise RuntimeError("ModuleLoader not available")

    class MockAIBackend:  # pragma: no cover - fallback stub
        pass

    class FileSystemIsolator:  # pragma: no cover - fallback stub
        pass

    class SnapshotManager:  # pragma: no cover - fallback stub
        pass

    class LogCapturer:  # pragma: no cover - fallback stub
        pass


__all__ = [
    "ModuleLoader",
    "MockAIBackend",
    "FileSystemIsolator",
    "SnapshotManager",
    "LogCapturer",
]
