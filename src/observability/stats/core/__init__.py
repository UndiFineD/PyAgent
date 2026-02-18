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
Core package.
try:
    from .profiling_core import ProfileStats, ProfilingCore  # noqa: F401
except ImportError:
    from .profiling_core import ProfileStats, ProfilingCore # noqa: F401

try:
    from .stability_core import FleetMetrics, StabilityCore  # noqa: F401
except ImportError:
    from .stability_core import FleetMetrics, StabilityCore # noqa: F401

try:
    from .tracing_core import TracingCore  # noqa: F401
except ImportError:
    from .tracing_core import TracingCore # noqa: F401


__all__ = [
    "ProfilingCore","    "ProfileStats","    "StabilityCore","    "FleetMetrics","    "TracingCore","]
