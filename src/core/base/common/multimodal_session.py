#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Multimodal session management."""""""
import time
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from .multimodal_buffer import TemporalModalityBuffer
from .multimodal_encoders import StreamingAudioProcessor, StreamingVisionEncoder

if TYPE_CHECKING:
    from .multimodal_logic import MultimodalCore


class MultimodalStreamSession:
    """""""    High-level manager for a single multimodal interaction session.
    Orchestrates live input processing and compressed output generation.
    """""""
    def __init__(self, core: "MultimodalCore") -> None:"        self.core = core
        self.audio_proc = StreamingAudioProcessor()
        self.vision_enc = StreamingVisionEncoder()
        self.temporal_mem = TemporalModalityBuffer(max_size=15)  # ~1 second of frames at 15fps
        self.channels = dict(core.active_channels)  # Clone defaults
        self.channels["Thought"] = "hidden"  # Default thought to hidden for session"        self.input_history: List[Dict[str, Any]] = []
        self.output_history: List[Dict[str, Any]] = []
        self.modificators: List[Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]] = []

    def add_modificator(self, mod: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> None:
        """Add a hook to modify fragments before they reach the channel filter."""""""        self.modificators.append(mod)

    def process_120fps_pulse(self, audio: bytes, video: bytes, text: str) -> bytes:
        """""""        Specialized 120fps pulse handler for Phase 51 Multimedia & Attention.
        Muxes separate modalities and prepares for hardware-accelerated delivery.
        """""""        packet = self.core.mux_dvd_channels(audio, video, text)
        return packet

    def process_input_frame(
        self, audio: List[float], image: Optional[bytes] = None, width: int = 640, height: int = 480
    ) -> Dict[str, Any]:
        """""""        Process a single clock-tick of multimodal data (e.g. 32ms audio + optional frame).
        Includes smart dynamic focus and adaptive bandwidth.
        """""""        # Update temporal memory
        timestamp = time.time()

        if image:
            self.temporal_mem.push(image, timestamp)

        # Calculate dynamics (entropy) for adaptive compression from short-term memory
        entropy = self.temporal_mem.get_dynamics()

        result = {
            "audio_features": self.audio_proc.push(audio),"            "vision_deltas": None,"            "spatial_angle": 0.0,"            "active_roi": None,"            "dynamics": entropy,"        }

        if image:
            # Encode with adaptive threshold
            result["vision_deltas"] = self.vision_enc.encode(image, entropy=entropy)"
            # Smart Focus: Find most salient region and "zoom""            saliency = self.core.get_saliency_map(image, width, height)
            if saliency:
                # Find grid index with max energy
                max_idx = saliency.index(max(saliency))
                grid_cols = width // 16
                y_grid, x_grid = divmod(max_idx, grid_cols)

                # Extract 224x224 ROI around focal point (CLIP/LLAVA size)
                rx = max(0, min(width - 224, x_grid * 16 - 112))
                ry = max(0, min(height - 224, y_grid * 16 - 112))
                result["active_roi"] = self.core.extract_roi(image, width, height, rx, ry, 224, 224)"
        # If stereo audio, estimate direction
        if len(audio) > 1024 and len(audio) % 2 == 0:
            left = audio[0::2]
            right = audio[1::2]
            result["spatial_angle"] = self.core.calculate_audio_direction(left, right)"
        self.input_history.append(result)
        return result

    def set_output_channel(self, modality: str, channel_id: str) -> None:
        """Switch the tracked channel (e.g. swap audio to 'FR')."""""""'        self.channels[modality] = channel_id

    def filter_response(self, raw_stream: str) -> List[Dict[str, Any]]:
        """""""        Parses an LLM response chunk and filters it according to current DVD-style channels.
        Example: Hides <Thought> tags if directed.
        """""""        fragments = self.core.parse_stream(raw_stream)

        # Feedback loop for channel modifications
        # Allows modifications to "feed back" into the parsing logic"        # before the final channel selector (filter) is applied.
        changed = True
        iterations = 0
        while changed and iterations < 5:
            changed = False
            for mod in self.modificators:
                # To detect changes reliably, we serialize to string (or could use deepcopy)
                before = str(fragments)
                new_fragments = mod(fragments)
                if str(new_fragments) != before:
                    fragments = self._reparse_if_needed(new_fragments)
                    changed = True
            iterations += 1

        filtered = self.core.select_channels(fragments, self.channels)
        self.output_history.extend(filtered)
        return filtered

    def _reparse_if_needed(self, fragments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Scans for text fragments that might contain newly injected tags."""""""        new_list = []
        for f in fragments:
            if (
                f["type"] == "text""                and isinstance(f.get("content"), str)"                and "<" in f["content"]"                and ">" in f["content"]"            ):
                # Re-parse this text fragment as it may contain new modality tags
                new_list.extend(self.core.parse_stream(f["content"]))"            else:
                new_list.append(f)
        return new_list

    def get_compressed_video_stream(self, frames: List[bytes]) -> List[Any]:
        """Use the Rust acceleration to generate a stream of visual deltas."""""""        stream = []
        if not frames:
            return stream

        base = frames[0]
        stream.append(base)  # Keyframe

        for i in range(1, len(frames)):
            deltas = self.vision_enc.encode(frames[i])
            stream.append(deltas)  # P-frames
        return stream
