# Description: src/observability/stats/storage_engine.py

Module overview:
- Provides backup and snapshot management utilities (`StatsBackupManager`, `StatsSnapshotManager`) and a `StatsCompressor` helper.
- Attempts to use `rust_core` for JSON serialization and compression when available.

Primary classes:
- `StatsBackup` (dataclass)
- `StatsBackupManager`
- `StatsSnapshotManager`
- `StatsCompressor`

Behavioral notes:
- Supports in-memory and on-disk backups and snapshots; writes JSON files when `backup_dir` or `snapshot_dir` is specified.
