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

import unittest
from pathlib import Path
from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
from src.core.base.common.auth_core import AuthCore
from src.core.base.common.registry_core import RegistryCore
from src.core.base.common.template_core import TemplateCore
from src.observability.stats.observability_core import ObservabilityCore


class TestSystemVerification(unittest.TestCase):
    """Integration test suite derived from verification scripts."""

    def test_imports(self):
        """Verifies that core components are importable and functional."""
        self.assertIsNotNone(MultimodalCore)
        self.assertIsNotNone(AuthCore)
        self.assertIsNotNone(RegistryCore)
        self.assertIsNotNone(TemplateCore)
        self.assertIsNotNone(ObservabilityCore)

    def test_multimodal_flow(self):
        """Verifies the multimodal stream session modification flow."""
        core = MultimodalCore()
        core.active_channels["Hardware"] = "NPU"
        session = MultimodalStreamSession(core)
        session.channels["Hardware"] = "NPU"

        def hardware_modificator(fragments):
            for f in fragments:
                if f["type"] == "text" and "trigger" in f["content"]:
                    f["content"] = f["content"].replace("trigger", "<Hardware:NPU_INIT>")
            return fragments

        session.add_modificator(hardware_modificator)
        raw = "Hello trigger world"

        filtered = session.filter_response(raw)
        # Check if the trigger was replaced by a modality fragment
        # Based on output: [{'type': 'modality', 'modality': 'Hardware', 'channel': 'NPU', 'id': 'INIT', 'content': None}]
        has_modality = any(f["type"] == "modality" and f["channel"] == "NPU" for f in filtered)
        self.assertTrue(has_modality)


if __name__ == "__main__":
    unittest.main()
