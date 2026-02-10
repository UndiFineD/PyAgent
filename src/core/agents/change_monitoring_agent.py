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
Change Monitoring Agent for PyAgent.

Monitors changes in various data sources using incremental update patterns
inspired by ADSpider's USN-based change detection.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.mixins.data_processing_mixin import DataProcessingMixin

__version__ = VERSION


class ChangeDataSource(ABC):
    """Abstract base class for data sources that support change monitoring."""

    @abstractmethod
    async def get_current_usn(self) -> Union[int, str]:
        """Get the current update sequence number."""
        pass

    @abstractmethod
    async def get_changes_since(self, usn: Union[int, str]) -> List[Dict[str, Any]]:
        """Get changes since the given USN."""
        pass

    @abstractmethod
    async def get_initial_dump(self) -> List[Dict[str, Any]]:
        """Get initial full dump of data (expensive operation)."""
        pass


class FileSystemDataSource(ChangeDataSource):
    """Example data source for file system monitoring."""

    def __init__(self, watch_path: str):
        self.watch_path = Path(watch_path)
        self._last_mtime = 0

    async def get_current_usn(self) -> float:
        """Use modification time as USN."""
        if self.watch_path.exists():
            return self.watch_path.stat().st_mtime
        return 0

    async def get_changes_since(self, usn: Union[int, str]) -> List[Dict[str, Any]]:
        """Get files changed since last USN."""
        changes = []
        current_mtime = await self.get_current_usn()

        if current_mtime > float(usn):
            # Simple example: just report the directory change
            changes.append({
                'object': str(self.watch_path),
                'attribute_name': 'mtime',
                'attribute_value': current_mtime,
                'last_orig_change_time': time.time(),
                'usn': current_mtime
            })

        return changes

    async def get_initial_dump(self) -> List[Dict[str, Any]]:
        """Get initial file listing."""
        files = []
        if self.watch_path.exists() and self.watch_path.is_dir():
            for file_path in self.watch_path.rglob('*'):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        'object': str(file_path),
                        'attribute_name': 'size',
                        'attribute_value': stat.st_size,
                        'last_orig_change_time': stat.st_mtime,
                        'usn': stat.st_mtime
                    })
        return files


class HistoryManager:
    """Manages change history for comparison and analysis."""

    def __init__(self, max_history: int = 1000):
        self.history: List[Dict[str, Any]] = []
        self.max_history = max_history

    def add_change(self, change: Dict[str, Any]) -> None:
        """Add a change to history."""
        self.history.append(change)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_previous_value(self, object_id: str, attribute: str) -> Optional[Any]:
        """Get the most recent previous value for an object/attribute."""
        matches = []
        for change in reversed(self.history):
            if (
                    change.get('object') == object_id
                    and change.get('attribute_name') == attribute
            ):
                matches.append(change.get('attribute_value'))
                if len(matches) >= 2:
                    return matches[1]
        return None

    def save_to_file(self, filepath: str) -> None:
        """Save history to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)

    def load_from_file(self, filepath: str) -> None:
        """Load history from JSON file."""
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                self.history = json.load(f)


class ChangeMonitoringAgent(BaseAgent, DataProcessingMixin):
    """
    Agent for monitoring changes in data sources using incremental patterns.

    Inspired by ADSpider's real-time change detection using USN and replication metadata.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.data_sources: Dict[str, ChangeDataSource] = {}
        self.history_managers: Dict[str, HistoryManager] = {}
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        self.output_file: Optional[str] = None
        self.poll_interval = 30  # seconds

        self._system_prompt = (
            "You are the Change Monitoring Agent. "
            "Your role is to monitor changes in various data sources in real-time. "
            "You use incremental update patterns to detect changes efficiently without "
            "performing expensive full scans. You process raw change data into "
            "human-readable formats and maintain change history for analysis."
        )

    def add_data_source(self, name: str, data_source: ChangeDataSource) -> None:
        """Add a data source to monitor."""
        self.data_sources[name] = data_source
        self.history_managers[name] = HistoryManager()

    def set_output_file(self, filepath: str) -> None:
        """Set file to save change data."""
        self.output_file = filepath

    def set_poll_interval(self, interval: int) -> None:
        """Set polling interval in seconds."""
        self.poll_interval = interval

    async def start_monitoring(self, data_source_name: str) -> None:
        """Start monitoring a specific data source."""
        if data_source_name not in self.data_sources:
            raise ValueError(f"Data source {data_source_name} not found")

        # Cancel existing task if running
        if data_source_name in self.monitoring_tasks:
            self.monitoring_tasks[data_source_name].cancel()

        # Start new monitoring task
        task = asyncio.create_task(self._monitor_loop(data_source_name))
        self.monitoring_tasks[data_source_name] = task

    async def stop_monitoring(self, data_source_name: str) -> None:
        """Stop monitoring a data source."""
        if data_source_name in self.monitoring_tasks:
            self.monitoring_tasks[data_source_name].cancel()
            del self.monitoring_tasks[data_source_name]

    async def _monitor_loop(self, data_source_name: str) -> None:
        """Main monitoring loop for a data source."""
        data_source = self.data_sources[data_source_name]
        history_manager = self.history_managers[data_source_name]

        # Get initial USN
        try:
            current_usn = await data_source.get_current_usn()
            last_usn = current_usn
        except Exception as e:
            logging.error(f"Failed to get initial USN for {data_source_name}: {e}")
            return

        while True:
            try:
                await asyncio.sleep(self.poll_interval)

                # Check for changes
                changes = await data_source.get_changes_since(last_usn)

                if changes:
                    # Process changes
                    processed_changes = []
                    for change in changes:
                        # Add to history
                        history_manager.add_change(change)

                        # Process with data processing mixin
                        processed_change = self.process_change_record(change)
                        processed_changes.append(processed_change)

                        # Update last USN
                        if 'usn' in change:
                            last_usn = change['usn']

                    # Output changes
                    await self._output_changes(processed_changes)

                    # Log changes
                    logging.info(f"Detected {len(changes)} changes in {data_source_name}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in monitoring loop for {data_source_name}: {e}")
                await asyncio.sleep(self.poll_interval)

    async def _output_changes(self, changes: List[Dict[str, Any]]) -> None:
        """Output changes in configured format."""
        if self.output_file:
            # Append to file
            with open(self.output_file, 'a') as f:
                for change in changes:
                    f.write(json.dumps(change, default=str) + '\n')

        # Also print to console in table format
        if changes:
            output = self.format_change_output(changes, 'table')
            print(f"\n--- Changes Detected ---\n{output}\n")

    async def get_initial_dump(self, data_source_name: str) -> List[Dict[str, Any]]:
        """Get initial full dump from a data source."""
        if data_source_name not in self.data_sources:
            raise ValueError(f"Data source {data_source_name} not found")

        data_source = self.data_sources[data_source_name]
        dump = await data_source.get_initial_dump()

        # Process the dump
        processed_dump = [self.process_change_record(item) for item in dump]

        return processed_dump

    async def save_history(self, data_source_name: str, filepath: str) -> None:
        """Save change history to file."""
        if data_source_name in self.history_managers:
            self.history_managers[data_source_name].save_to_file(filepath)

    async def load_history(self, data_source_name: str, filepath: str) -> None:
        """Load change history from file."""
        if data_source_name in self.history_managers:
            self.history_managers[data_source_name].load_from_file(filepath)

    async def get_change_summary(self, data_source_name: str) -> Dict[str, Any]:
        """Get summary of changes for a data source."""
        if data_source_name not in self.history_managers:
            return {}

        history = self.history_managers[data_source_name].history
        summary = {
            'total_changes': len(history),
            'attributes_changed': set(),
            'objects_affected': set(),
            'time_range': {}
        }

        if history:
            summary['time_range'] = {
                'start': min(h.get('last_orig_change_time', 0) for h in history),
                'end': max(h.get('last_orig_change_time', 0) for h in history)
            }

        for change in history:
            summary['attributes_changed'].add(change.get('attribute_name', ''))
            summary['objects_affected'].add(change.get('object', ''))

        # Convert sets to lists for JSON serialization
        summary['attributes_changed'] = list(summary['attributes_changed'])
        summary['objects_affected'] = list(summary['objects_affected'])

        return summary
