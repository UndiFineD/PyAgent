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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Plugin demonstrating handling of broken imports during agent initialization."""



from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.plugins.core.ImportHealerCore import ImportHealerCore
import logging
import json
import os

class BrokenImportAgent(BaseAgent):
    """
    Agent designed to catch and heal broken imports in the fleet (Phase 186).
    """
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
        self.core = ImportHealerCore()
        self.import_map_file = "data/system/import_map.json"
        os.makedirs(os.path.dirname(self.import_map_file), exist_ok=True)

    def heal_import_error(self, error_msg: str):
        fix = self.core.suggest_fix(error_msg)
        print(f"[HEALER] Detected broken import. {fix}")
        return fix

    def update_global_import_map(self):
        print("[HEALER] Updating global import map...")
        imap = self.core.build_internal_import_map(os.path.join(self._workspace_root, "src"))
        with open(self.import_map_file, "w") as f:
            json.dump(imap, f, indent=2)
        print(f"[HEALER] Map saved to {self.import_map_file}")
