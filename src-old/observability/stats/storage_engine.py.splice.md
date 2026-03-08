# Splice: src/observability/stats/storage_engine.py

This module contains multiple classes and responsibilities:

- `StatsBackup` dataclass and `StatsBackupManager` for persistent backups.
- `StatsSnapshotManager` for snapshot creation and restore.
- `StatsCompressor` for compression helper, with rust acceleration fallback.

Suggested splices:
- `backup.py`: backup manager and dataclass.
- `snapshot.py`: snapshot manager logic.
- `compressor.py`: compression utilities and rust adapter.
