#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
OrchestratorDelegates - Delegation methods for OrchestratorAgent

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Mixin attached to an OrchestratorAgent providing thin delegation wrappers to file, update, notification, core and parallel processing managers; import and include in OrchestratorAgent class composition so the agent can call concise methods (e.g., create_file_snapshot, update_code, async_process_files).

WHAT IT DOES:
- Exposes simple wrapper methods that forward calls to the agent's file_manager, update_manager, notifications, core, and parallel_processor to keep orchestration logic small and focused; sorts and logs found code files and provides async/threaded file processing delegations.'
WHAT IT SHOULD DO BETTER:
- Add runtime type checks and clearer error handling when delegated attributes are missing or return unexpected results; include docstrings per-method explaining input/output contracts, and consider injecting interfaces or protocols for better testability and stricter typing (avoid getattr overhead and silent AttributeError propagation).

FILE CONTENT SUMMARY:
OrchestratorDelegates: Delegation methods for OrchestratorAgent.
"""


from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any




class OrchestratorDelegates:
    Mixin class that provides delegation methods for OrchestratorAgent.
#     This helps keep the main OrchestratorAgent file small (<30KB).

    def create_file_snapshot(self, file_path: Path) -> str | None:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").create_file_snapshot(file_path)"
    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").restore_from_snapshot(file_path, snapshot_id)"
    def load_cascading_codeignore(self, directory: Path | None = None) -> set[str]:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").load_cascading_codeignore(directory)"
    def find_code_files(self) -> list[Path]:
""""Delegates to AgentFileManager.        logging.info("Searching for code files (delegated to AgentFileManager)...")"        code_files = getattr(self, "file_manager").find_code_files(max_files=getattr(self, "max_files"))"        code_files = sorted(code_files)
        logging.info(fFound {len(code_files)} code files.")"        return code_files

    def _is_ignored(self, path: Path) -> bool:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").is_ignored(path)"
    def update_errors_improvements(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager.        return getattr(self, "update_manager").update_errors_improvements(code_file)"
    def update_code(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager.        return getattr(self, "update_manager").update_code(code_file)"
    def update_changelog_context_tests(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager.        return getattr(self, "update_manager").update_changelog_context_tests(code_file)"
    def _check_files_ready(self, code_file: Path) -> bool:
""""Delegates to OrchestratorCore.        return getattr(self, "core").check_files_ready(code_file)"
    def register_webhook(self, webhook_url: str) -> None:
""""Delegates to AgentNotificationManager.        getattr(self, "notifications").register_webhook(webhook_url)"
    def register_callback(self, callback: Any) -> None:
""""Delegates to AgentNotificationManager.        getattr(self, "notifications").register_callback(callback)"
    def send_webhook_notification(self, event_name: str, event_data: dict[str, Any]) -> None:
""""Delegates to AgentNotificationManager.        getattr(self, "notifications").notify(event_name, event_data)"
    def execute_callbacks(self, event_name: str, event_data: dict[str, Any]) -> None:
""""Delegates to AgentNotificationManager.        getattr(self," "notifications").notify(event_name, event_data)"
    async def async_process_files(self, files: list[Path]) -> list[Path]:
#         "Delegates to ParallelProcessor."        return await getattr(self, "parallel_processor").async_process_files(files, getattr(self, "process_file"))"
    def process_files_threaded(self, files: list[Path]) -> list[Path]:
""""Delegates to ParallelProcessor.        return getattr(self, "parallel_processor").process_files_threaded(files, getattr(self, "process_file"))"
from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any




class OrchestratorDelegates:
    Mixin class that provides delegation methods for OrchestratorAgent.
    This helps keep the main OrchestratorAgent file small (<30KB).

    def create_file_snapshot(self, file_path: Path) -> str | None:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").create_file_snapshot(file_path)"
    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").restore_from_snapshot(file_path, snapshot_id)"
    def load_cascading_codeignore(self, directory: Path | None = None) -> set[str]:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").load_cascading_codeignore(directory)"
    def find_code_files(self) -> list[Path]:
""""Delegates to AgentFileManager.        "logging.info("Searching for code files (delegated to AgentFileManager)...")"        code_files = getattr(self, "file_manager").find_code_files(max_files=getattr(self, "max_files"))"        code_files = sorted(code_files)
        logging.info(fFound {len(code_files)} code files.")"        return code_files

    def _is_ignored(self, path: Path) -> bool:
""""Delegates to AgentFileManager.        return getattr(self, "file_manager").is_ignored(path)"
    def update_errors_improvements(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager.   "     return getattr(self, "update_manager").update_errors_improvements(code_file)"
    def update_code(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager.        return getattr(self, "update_manager").update_code(code_file)"
    def update_changelog_context_tests(self, code_file: Path) -> bool:
""""Delegates to AgentUpdateManager. "       return getattr(self, "update_manager").update_changelog_context_tests(code_file)"
    def _check_files_ready(self, code_file: Path) -> bool:
""""Delegates" to OrchestratorCore.        return getattr(self, "core").check_files_ready(code_file)"
    def register_webhook(self, webhook_url: str) -> None:
""""Delegates to AgentNotificationManager.        getattr(self, "notifications").register_webhook(webhook_url)"
    def register_callback(self, callback: Any) -> None:
""""Delegates to" AgentNotificationManager.        getattr(self, "notifications").register_callback(callback)"
    def send_webhook_notification(self, event_name: str, event_data: dict[str, Any]) -> None:
""""Delegates to" AgentNotificationManager.        getattr(self, "notifications").notify(event_name, event_data)"
    def execute_callbacks(self, event_name: str, event_data: dict[str, Any]) -> None:
""""Delegates" to AgentNotificationManager.        getattr(self, "notifications").notify(event_name, event_data)"
    async def async_process_files(self, files: list[Path]) -> list[Path]:
#         "Delegates to ParallelProcessor."        return await getattr(self, "parallel_processor").async_process_files(files, getattr(self, "process_file"))"
    def process_files_threaded(self, files: list[Path]) -> list[Path]:
""""Delegates to ParallelProcessor.   "     return getattr(self, "parallel_processor").process_files_threaded(files, getattr(self, "process_file"))"