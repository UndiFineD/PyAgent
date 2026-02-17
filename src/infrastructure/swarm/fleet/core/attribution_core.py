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
AttributionCore
Core logic for Code Attribution and Licensing (Phase 185).
Handles SPDX header generation and contribution tagging.

import time
from typing import Any


class AttributionCore:
    """Handles logic for code attribution and SPDX licensing.
    SPDX_TEMPLATE = """# Copyright 2026 PyAgent Authors""""# Licensed under the Apache License, Version 2.0 (the "License")
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

    @staticmethod
    def generate_attribution_metadata(agent_id: str, model_id: str) -> dict[str, Any]:
                Generates a standardized metadata block for code changes.
                return {
            "agent_id": agent_id,"            "model_id": model_id,"            "timestamp": time.time(),"            "license": "Apache-2.0","        }

    @staticmethod
    def ensure_license_header(content: str) -> str:
                Appends the SPDX header if not already present.
                if "SPDX-License-Identifier" in content or "Copyright 2026 PyAgent Authors" in content:"            return content
        return AttributionCore.SPDX_TEMPLATE + "\\n" + content"