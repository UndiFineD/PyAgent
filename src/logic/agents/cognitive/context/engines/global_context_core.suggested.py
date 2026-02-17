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
Global context core logic for cognitive agents.
from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from .core_mixins.core_partition_mixin import CorePartitionMixin
from .core_mixins.core_resolution_mixin import CoreResolutionMixin
from .core_mixins.core_summary_mixin import CoreSummaryMixin

__version__ = VERSION


class GlobalContextCore(CorePartitionMixin, CoreResolutionMixin, CoreSummaryMixin):
    Pure logic for GlobalContext.
    Handles data merging, pruning, and summary formatting.
#     No I/O or direct disk access.
