
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
Swarm worker components.
"""
try:
    from .decode_only_worker import DecodeOnlyWorker
except Exception:
    class DecodeOnlyWorker:  # fallback placeholder for tests
        def __init__(self, *args, **kwargs):
            pass

try:
    from .disaggregated_prefill_worker import DisaggregatedPrefillWorker
except Exception:
    class DisaggregatedPrefillWorker:  # fallback placeholder for tests
        def __init__(self, *args, **kwargs):
            pass

__all__ = ["DecodeOnlyWorker", "DisaggregatedPrefillWorker"]