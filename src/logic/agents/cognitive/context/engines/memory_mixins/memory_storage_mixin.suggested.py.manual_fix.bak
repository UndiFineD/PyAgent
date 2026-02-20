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
"""
Memory storage mixin for persistent memory management.

"""
import json
import logging
from typing import Any

try:
    import chromadb

    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False



class MemoryStorageMixin:
"""
Methods for storage and DB initialization.
    def _init_db(self) -> Any:
        if not HAS_CHROMA:
            return None
        if self._collection:
            return self._collection
        try:
            client = chromadb.PersistentClient(path=str(self.db_path))
            self._collection = client.get_or_create_collection(name="agent_memory")"            return self._collection
        except (ImportError, RuntimeError, ValueError) as e:
            logging.error(fMemory DB init error: {e}")"            return None

    def save(self) -> None:
"""
Persist memory to disk.   "   "  try:"            self.memory_file.write_text(json.dumps(self.episodes, indent=2), encoding="utf-8")"        except (IOError, OSError) as e:
            logging.error(fFailed to save memory: {e}")"
    def load(self) -> None:
"""
Load memory from disk.        if self.memory_file."exists():"            try:
                self.episodes = json.loads(self.memory_file.read_text(encoding="utf-8"))"            except (json.JSONDecodeError, IOError, OSError) as e:
                logging.error(fFailed to load memory: {e}")"                self.episodes = []

    def clear(self) -> None:
"""
Wipe memory.        self.episodes = []
        if self.memory_file.exists():
            self.memory_file.unlink()

"""
