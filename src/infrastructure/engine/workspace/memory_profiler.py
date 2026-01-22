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
Real-time memory profiling for Phase 52.
Tracks DBO allocation patterns and fragmentation in the synchronized workspace.
"""

import logging
import time
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Any, Dict, List
=======
from typing import Dict, List, Any, Optional
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import Dict, List, Any, Optional
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class MemoryProfiler:
    """
    Profiles workspace memory usage with sub-millisecond precision.
    Integrates with Rust for high-throughput allocation tracking.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self) -> None:
=======
    
    def __init__(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.snapshots: List[Dict[str, Any]] = []
        self.peak_memory = 0
        self.start_time = time.time()

<<<<<<< HEAD
<<<<<<< HEAD
    def take_snapshot(self, label: str = "auto") -> Dict[str, Any]:
        """Captures current memory state and fragmentation metrics."""
        usage = 0
        frag = 0.0

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def take_snapshot(self, label: str = "auto"):
        """Captures current memory state and fragmentation metrics."""
        usage = 0
        frag = 0.0
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if rc and hasattr(rc, "memory_profile_rust"):
            try:
                stats = rc.memory_profile_rust()
                usage = stats.get("current_usage", 0)
                frag = stats.get("fragmentation", 0.0)
<<<<<<< HEAD
<<<<<<< HEAD
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug(f"Rust profiling failed: {e}")

        self.peak_memory = max(self.peak_memory, usage)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            except Exception as e:
                logger.debug(f"Rust profiling failed: {e}")

        if usage > self.peak_memory:
            self.peak_memory = usage
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        snapshot = {
            "timestamp": time.time() - self.start_time,
            "label": label,
            "usage_bytes": usage,
<<<<<<< HEAD
<<<<<<< HEAD
            "fragmentation": frag,
=======
            "fragmentation": frag
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            "fragmentation": frag
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        }
        self.snapshots.append(snapshot)
        return snapshot

    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyzes allocation patterns to detect leaks or inefficiencies."""
        if not self.snapshots:
            return {}
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return {
            "duration": time.time() - self.start_time,
            "peak_mb": self.peak_memory / (1024 * 1024),
            "avg_fragmentation": sum(s["fragmentation"] for s in self.snapshots) / len(self.snapshots),
<<<<<<< HEAD
<<<<<<< HEAD
            "snapshot_count": len(self.snapshots),
        }

    def reset(self) -> None:
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            "snapshot_count": len(self.snapshots)
        }

    def reset(self):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Clears profiler history."""
        self.snapshots.clear()
        self.peak_memory = 0
        self.start_time = time.time()
