#!/usr/bin/env python3
"""Test the watch_file utility for monitoring file changes."""
import asyncio
from pathlib import Path

import pytest

import src.runtime_py


@pytest.mark.asyncio
async def test_watch_file(tmp_path: Path) -> None:
    """Test that watch_file detects changes to a file."""
    file = tmp_path / "foo.txt"
    file.write_text("initial")

    event = asyncio.Event()

    async def cb(_event_str: str) -> None:
        """Callback for file change event."""
        # any notification from the watcher is sufficient for the test
        event.set()

    src.runtime_py.watch_file(str(file), cb)

    # give the background watcher a moment to start up
    await asyncio.sleep(0.1)

    # modify the file and wait for callback
    file.write_text("changed")
    await asyncio.wait_for(event.wait(), timeout=1.0)
    # ensure watcher triggered
    assert event.is_set()
