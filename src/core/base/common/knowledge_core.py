<<<<<<< HEAD
<<<<<<< HEAD
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Core logic for Sharded Knowledge Management.
Handles trillion-parameter scale entity distribution.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

import hashlib
from pathlib import Path
from typing import Any, Dict, Optional

from .base_core import BaseCore
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.core.base.common.base_core import BaseCore
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class KnowledgeCore(BaseCore):
    """
    Standardized sharded knowledge management.
    Uses Adler-32 or MD5 based sharding.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, shard_count: int = 1024, base_path: Optional[Path] = None) -> None:
=======
    
    def __init__(self, shard_count: int = 1024, base_path: Optional[Path] = None):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self, shard_count: int = 1024, base_path: Optional[Path] = None):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        super().__init__()
        self.shard_count = shard_count
        self.base_path = base_path

    def get_shard_id(self, entity_key: str) -> int:
        """Determines the shard index for a given entity key."""
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "get_adler32_shard"):  # pylint: disable=no-member
            return rc.get_adler32_shard(entity_key, self.shard_count)  # pylint: disable=no-member

=======
        if rc and hasattr(rc, "get_adler32_shard"):
            return rc.get_adler32_shard(entity_key, self.shard_count)
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        if rc and hasattr(rc, "get_adler32_shard"):
            return rc.get_adler32_shard(entity_key, self.shard_count)
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        hash_val = int(hashlib.md5(entity_key.encode()).hexdigest(), 16)
        return hash_val % self.shard_count

    def index_entity(self, entity: Dict[str, Any]) -> bool:
        """Maintains the global knowledge index footprint."""
        key = entity.get("id") or entity.get("name", "unknown")
<<<<<<< HEAD
<<<<<<< HEAD
        # Determine shard placement but don't store yet
        self.get_shard_id(key)
=======
        shard = self.get_shard_id(key)
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        shard = self.get_shard_id(key)
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Logic for writing to shard storage
        return True
