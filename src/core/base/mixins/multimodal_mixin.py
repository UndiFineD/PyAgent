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
Multimodal Mixin for BaseAgent.
Provides support for interleaved modality tags and streaming sessions.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

from typing import Any, Dict, List

from src.core.base.common.multimodal_core import (MultimodalCore,
                                                  MultimodalStreamSession)

=======
from typing import Any, Optional, Dict, List
from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import Any, Optional, Dict, List
from src.core.base.common.multimodal_core import MultimodalCore, MultimodalStreamSession
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

class MultimodalMixin:
    """
    Mixin to provide multimodal capabilities to agents.
    Enables handling of interleaved channel tracks and feedback loops.
    """

<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, **_kwargs: Any) -> None:
        self.multimodal_core = MultimodalCore()
        # Initialize a default stream session for the agent
        self.multimodal_session = MultimodalStreamSession(self.multimodal_core)

    def get_multimodal_instructions(self) -> str:
        """Returns the system instructions for the multimodal tag system."""
        channels: str = ", ".join(self.multimodal_core.active_channels.keys())
        return (
            "MODALITY PROTOCOL ENABLED.\n"
            "You can interleave modality tags in your output using the format <Type:Channel_ID>.\n"
            f"Available Modalities: {channels}\n"
            "Use <Thought_...> for internal reasoning and "
            "<Hardware:NPU_...> for acceleration hooks.\n"
            "Example: '<Audio:EN_01> Hello world <Thought_Greeting user>'."
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def __init__(self, **kwargs: Any) -> None:
        self.multimodal_core = MultimodalCore()
        # Initialize a default stream session for the agent
        self.multimodal_session = MultimodalStreamSession(self.multimodal_core)
        
    def get_multimodal_instructions(self) -> str:
        """Returns the system instructions for the multimodal tag system."""
        channels = ", ".join(self.multimodal_core.active_channels.keys())
        return (
            f"MODALITY PROTOCOL ENABLED.\n"
            f"You can interleave modality tags in your output using the format <Type:Channel_ID>.\n"
            f"Available Modalities: {channels}\n"
            f"Use <Thought_...> for internal reasoning and <Hardware:NPU_...> for acceleration hooks.\n"
            f"Example: '<Audio:EN_01> Hello world <Thought_Greeting user>'."
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        )

    def process_multimodal_output(self, raw_output: str) -> List[Dict[str, Any]]:
        """Processes agent output through the multimodal feedback loop and filter."""
        return self.multimodal_session.filter_response(raw_output)

    def set_output_track(self, modality: str, channel: str) -> None:
        """Switch the active output track for a modality."""
        self.multimodal_session.set_output_channel(modality, channel)
