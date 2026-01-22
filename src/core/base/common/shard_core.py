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
Core logic for fleet sharding and partitioning.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=import-error
except ImportError:
    rc = None

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
=======
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
=======
>>>>>>> 2a6f2626e (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
from typing import Any, List, Dict, Optional
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
<<<<<<< HEAD
logger = logging.getLogger("pyagent.sharding")
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

=======
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
=======
>>>>>>> 2a6f2626e (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
class ShardCore(BaseCore):
    """
    Authoritative engine for agent and data partitioning.
    Handles shard assignment, rebalancing, and cross-shard routing.
    """
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def calculate_shard_id(self, key: str, shard_count: int) -> int:
        """
        Determines the shard ID for a given key.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "calculate_shard_id_rust"):  # pylint: disable=no-member
            try:
                return rc.calculate_shard_id_rust(  # pylint: disable=no-member
                    key, shard_count
                )  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        # Fallback to simple hash-based sharding
        import hashlib  # pylint: disable=import-outside-toplevel

        h = hashlib.md5(key.encode()).digest()
        seed = int.from_bytes(h[:8], "big")
        return seed % shard_count

    def verify_integrity(self) -> bool:
        """
        Verifies that shard calculation is deterministic and functional.
        Acts as a circuit breaker for shard-dependent operations.
        """
        try:
            # Test Vector: "test_key" with 10 shards should reliably map to 5
            # (MD5 of test_key -> ... % 10) - value depends on implementation but must be consistent
            test_key = "test_key"
            shard_count = 10
            
            id1 = self.calculate_shard_id(test_key, shard_count)
            id2 = self.calculate_shard_id(test_key, shard_count)
            
            if id1 != id2:
                return False
                
            if not isinstance(id1, int) or id1 < 0 or id1 >= shard_count:
                return False
                
            return True
        except Exception:  # pylint: disable=broad-exception-caught
            return False
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if rc and hasattr(rc, "calculate_shard_id_rust"):
=======
        if rc and hasattr(rc, "calculate_shard_id_rust"): # pylint: disable=no-member
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
            try:
=======
        if rc and hasattr(rc, "calculate_shard_id_rust"): # pylint: disable=no-member
            try:
>>>>>>> 2a6f2626e (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
                return rc.calculate_shard_id_rust(key, shard_count) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass
        
        # Fallback to simple hash-based sharding
        import hashlib
        h = hashlib.md5(key.encode()).digest()
        seed = int.from_bytes(h[:8], "big")
        return seed % shard_count
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
