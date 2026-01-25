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
Verify System module.
"""

import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path.cwd()))

try:
    print("Attempting to import MultimodalCore...")
    from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
    print("Success!")

    print("Attempting to import AuthCore...")
    from src.core.base.common.auth_core import AuthCore
    print("Success!")

    print("Attempting to import RegistryCore...")
    from src.core.base.common.registry_core import RegistryCore
    print("Success!")

    print("Attempting to import TemplateCore...")
    from src.core.base.common.template_core import TemplateCore
    print("Success!")

    print("Attempting to import ObservabilityCore...")
    from src.observability.stats.observability_core import ObservabilityCore
    print("Success!")

    # Test MultimodalStreamSession with a dummy hook
    core = MultimodalCore()
    # Enable Hardware:NPU channel
    core.active_channels["Hardware"] = "NPU"
    session = MultimodalStreamSession(core)
    # The session clones active_channels, but we should make sure Hardware is copied
    session.channels["Hardware"] = "NPU"

    def my_mod(frags):
        for f in frags:
            if f["type"] == "text" and "trigger" in f["content"]:
                f["content"] = f["content"].replace("trigger", "<Hardware:NPU_INIT>")
        return frags

    session.add_modificator(my_mod)
    raw = "Hello trigger world"
    # We want to see the fragments before filtering too
    fragments = core.parse_stream(raw) # Initial
    fragments = session._reparse_if_needed(my_mod(fragments))
    print(f"Intermediate fragments: {fragments}")

    filtered = session.filter_response(raw)
    print(f"Final filtered result: {filtered}")

except Exception:  # pylint: disable=broad-exception-caught, unused-variable
    import traceback
    traceback.print_exc()
    sys.exit(1)
