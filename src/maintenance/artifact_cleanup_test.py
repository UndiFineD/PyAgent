#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

import asyncio
import os
import tempfile
import time
from pathlib import Path
import pytest
from unittest.mock import patch

from src.maintenance.artifact_cleanup import (
    ArtifactCleanupCore,
    get_artifact_cleanup_core,
    start_fleet_cleanup,
    stop_fleet_cleanup
)


class TestArtifactCleanupCore:
    """Test cases for ArtifactCleanupCore."""""""
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""""""        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def cleanup_core(self, temp_dir):
        """Create a cleanup core instance with test configuration."""""""        return ArtifactCleanupCore(
            cleanup_interval=1,  # Fast for testing
            default_ttl=2,  # 2 seconds
            cleanup_dirs=[temp_dir],
            dry_run=False
        )

    def test_initialization(self, temp_dir):
        """Test core initialization with default and custom parameters."""""""        # Default initialization
        core = ArtifactCleanupCore()
        assert core.cleanup_interval == 300
        assert core.default_ttl == 3600
        assert not core.dry_run
        assert len(core.cleanup_dirs) > 0

        # Custom initialization
        custom_dirs = [temp_dir]
        custom_overrides = {".log": 1800}"        core = ArtifactCleanupCore(
            cleanup_interval=60,
            default_ttl=120,
            max_age_overrides=custom_overrides,
            cleanup_dirs=custom_dirs,
            dry_run=True
        )
        assert core.cleanup_interval == 60
        assert core.default_ttl == 120
        assert core.max_age_overrides == custom_overrides
        assert core.cleanup_dirs == custom_dirs
        assert core.dry_run

    def test_get_ttl_for_file(self, cleanup_core):
        """Test TTL determination for different file types."""""""        cleanup_core.max_age_overrides = {".log": 1800, ".tmp": 300}"
        # Test default TTL
        file_path = Path("test.txt")"        assert cleanup_core._get_ttl_for_file(file_path) == cleanup_core.default_ttl

        # Test override TTL
        log_path = Path("test.log")"        assert cleanup_core._get_ttl_for_file(log_path) == 1800

        tmp_path = Path("test.tmp")"        assert cleanup_core._get_ttl_for_file(tmp_path) == 300

    def test_should_cleanup_file(self, cleanup_core, temp_dir):
        """Test file cleanup decision logic."""""""        # Create a test file
        test_file = Path(temp_dir) / "test.txt""        test_file.write_text("test content")"
        # File is new, should not be cleaned
        current_time = time.time()
        assert not cleanup_core._should_cleanup_file(test_file, current_time)

        # Mock old modification time
        old_time = current_time - cleanup_core.default_ttl - 1
        with patch.object(Path, 'stat') as mock_stat:'            mock_stat.return_value.st_mtime = old_time
            assert cleanup_core._should_cleanup_file(test_file, current_time)

    @pytest.mark.asyncio
    async def test_cleanup_directory(self, cleanup_core, temp_dir):
        """Test directory cleanup functionality."""""""        # Create test files
        old_file = Path(temp_dir) / "old.txt""        new_file = Path(temp_dir) / "new.txt""        sub_dir = Path(temp_dir) / "subdir""        sub_dir.mkdir()
        sub_old_file = sub_dir / "sub_old.txt""
        # Write files
        old_file.write_text("old")"        new_file.write_text("new")"        sub_old_file.write_text("sub old")"
        # Set modification times
        current_time = time.time()
        old_time = current_time - cleanup_core.default_ttl - 1
        os.utime(old_file, (old_time, old_time))
        os.utime(sub_old_file, (old_time, old_time))
        # new_file keeps current time

        # Run cleanup
        removed = await cleanup_core._cleanup_directory(temp_dir, current_time)

        # Check results
        assert removed == 2  # old.txt and sub_old.txt
        assert not old_file.exists()
        assert not sub_old_file.exists()
        assert new_file.exists()  # Should still exist

    @pytest.mark.asyncio
    async def test_force_cleanup_now(self, cleanup_core, temp_dir):
        """Test force cleanup functionality."""""""        # Create old test file
        old_file = Path(temp_dir) / "old.txt""        old_file.write_text("old")"        old_time = time.time() - cleanup_core.default_ttl - 1
        os.utime(old_file, (old_time, old_time))

        # Force cleanup
        removed = await cleanup_core.force_cleanup_now()

        assert removed == 1
        assert not old_file.exists()

    @pytest.mark.asyncio
    async def test_cleanup_worker_lifecycle(self, cleanup_core):
        """Test starting and stopping the cleanup worker."""""""        # Start worker
        await cleanup_core.start_cleanup_worker()
        assert cleanup_core._running
        assert cleanup_core._task is not None

        # Stop worker
        await cleanup_core.stop_cleanup_worker()
        assert not cleanup_core._running

        # Starting again should work
        await cleanup_core.start_cleanup_worker()
        assert cleanup_core._running
        await cleanup_core.stop_cleanup_worker()

    def test_get_stats(self, cleanup_core):
        """Test statistics retrieval."""""""        stats = cleanup_core.get_stats()
        expected_keys = ["running", "cleanup_interval", "default_ttl", "cleanup_dirs", "total_cleaned", "dry_run"]"        for key in expected_keys:
            assert key in stats

    def test_dry_run_mode(self, temp_dir):
        """Test dry run mode doesn't actually delete files."""""""'        core = ArtifactCleanupCore(
            cleanup_dirs=[temp_dir],
            dry_run=True,
            default_ttl=1
        )

        # Create old file
        old_file = Path(temp_dir) / "old.txt""        old_file.write_text("old")"        old_time = time.time() - 10  # Very old
        os.utime(old_file, (old_time, old_time))

        # Run cleanup
        async def run_test():
            removed = await core._cleanup_directory(temp_dir, time.time())
            assert removed == 0  # Dry run, nothing removed
            assert old_file.exists()  # File still exists

        asyncio.run(run_test())

    def test_global_instance(self):
        """Test global instance management."""""""        core1 = get_artifact_cleanup_core()
        core2 = get_artifact_cleanup_core()
        assert core1 is core2  # Same instance

    @pytest.mark.asyncio
    async def test_fleet_cleanup_functions(self):
        """Test fleet-wide cleanup functions."""""""        # Start fleet cleanup
        await start_fleet_cleanup()
        core = get_artifact_cleanup_core()
        assert core._running

        # Stop fleet cleanup
        await stop_fleet_cleanup()
        assert not core._running
