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
"""
Multimodal Logic Implementation

"""
This module provides the MultimodalCore class, which implements unified logic for aligning,
parsing, and synchronizing multiple data modalities (audio, video, text, etc.) in streaming
and batch settings. It supports both Python and Rust-accelerated backends for high-throughput,
low-latency processing, and is designed for use in autonomous agent swarms and advanced AI systems.

Key Features:
- Unified multimodal alignment and streaming core for "see-while-hear" experiences
- Efficient modality alignments (sequence-dimension concatenation)
- Simultaneous stream parsing and channel selection
- Rust-accelerated functions for performance-critical operations (via PyO3)
- Fallback to pure Python logic if Rust extensions are unavailable
- Modular design for easy extension and integration with agent mixins

Classes:
- MultimodalCore: Main class for multimodal alignment, streaming, and fusion

Dependencies:
- numpy, logging, typing, re
- src.infrastructure.engine.multimodal (Muxer, QuantizedMultimediaEngine)
- src.core.base.base_core (BaseCore)
- src.core.base.common.multimodal_state (StreamState)
"""
import logging
import math
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.infrastructure.engine.multimodal import (Muxer, QuantizedMultimediaEngine)

from .base_core import BaseCore
from .multimodal_state import StreamState

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.multimodal")


class MultimodalCore(BaseCore):
"""
Unified Multimodal Alignment and Streaming Core.
    Implements efficient modality alignments (sequence-dimension concatenation)
    and simultaneous stream parsing for "see-while-hear" experiences.""
def __init__(self, name: str = "MultimodalCore", root_path: Optional[str] = None) -> None:
"""
Initialize the MultimodalCore with optional name and root path for registry.""
super().__init__(name=name, repo_root=root_path)
        self.registry: Dict[str, str] = {}  # Tag -> URI/Path
        self._stream_states: Dict[str, StreamState] = {}
        self.muxer = Muxer()
        self.q_engine = QuantizedMultimediaEngine(mode="FP8")
        self.active_channels: Dict[str, str] = {
            "Audio": "default",
            "Video": "default",
            "Image": "default",
            "Thought": "default",
            "Time": "default",
            "Commandshell": "default",
            "Filter": "default",
            "Config": "default",
            "API": "default",
            "Hardware": "default",
            "Memory": "default",
            "Network": "default",
            "Draft": "default",
            "Tool": "default",
            "Registry": "default",
            "Security": "default",
            "Validation": "default",
            "Cascade": "default",
            "Transaction": "default",
            "Audit": "default",
            "Metrics": "default",
            "Swarm": "default",
            "Search": "default",
            "Kernel": "default",
            "Logic": "default",
            "Identity": "default",
            "Feedback": "default",
            "Synapse": "default",
            "Nexus": "default",
            "Hive": "default",
            "Flow": "default",
            "Spark": "default",
            "Pulse": "default",
            "Void": "default",
            "Core": "default",
            "Omni": "default",
            "Prime": "default",
            "Alpha": "default",
            "Omega": "default",
            "Sigma": "default",
            "Delta": "default",
            "Theta": "default",
            "Phi": "default",
            "Psi": "default",
            "Epsilon": "default",
            "Zeta": "default",
            "Lambda": "default",    
        }


    def set_active_channel(self, modality: str, channel_id: str) -> None:
"""
Switch the active channel for a specific modality (e.g. switch Audio to 'EN').""
self.active_channels[modality] = channel_id
        logger.info("Modality %s channel switched to: %s", modality, channel_id)


    def parse_and_filter_stream(self, stream_id: str, chunk: str) -> List[Dict[str, Any]]:
"""
Incrementally parse and automatically filter for active channels.
"""
fragments = self.parse_stream_incremental(stream_id, chunk)
        return self.select_channels(fragments, self.active_channels)


    def parse_stream_incremental(self, stream_id: str, chunk: str) -> List[Dict[str, Any]]:
"""
Incrementally parse a stream chunk, handling partial tags.
"""
if stream_id not in self._stream_states:
            self._stream_states[stream_id] = StreamState()

        state = self._stream_states[stream_id]
        full_content = state.buffer + chunk

        # We need to ensure we don't cut a tag in half
        # # If there's an open '<' without a '>', buffer it
        last_open_angle = full_content.rfind("<")
        last_close_angle = full_content.rfind(">")
        if last_open_angle > last_close_angle:
            # Tag is potentially split
            to_parse = full_content[:last_open_angle]
            state.buffer = full_content[last_open_angle:]
        else:
            to_parse = full_content
            state.buffer = ""
        return self.parse_stream(to_parse)


    def register_media(self, tag: str, uri: str) -> None:
"""
Associate a media tag with a resolved URI.""
self.registry[tag] = uri


    def mux_dvd_channels(self, audio: bytes, video: bytes, text: str) -> bytes:
"""
Packs separate modalities into a single sync-packet for 120fps DVD-like streaming.
        Uses 0xDEADBEEF binary muxer.
"""
return self.muxer.synchronize_tick(audio, video, text)


    def apply_scaling(self, activations: Any, scaling: Any) -> Any:
"""
Applies IA3 scaling via the QuantizedMultimediaEngine.""
return self.q_engine.apply_stream_ia3(activations, scaling)


    def resolve_tag(self, tag: str) -> Optional[str]:
"""
Get URI for a specific tag.""
return self.registry.get(tag)


    def calculate_audio_features(self, samples: List[float], num_bins: int = 80) -> List[float]:
"""
Extract Mel-frequency features for audio alignment.
"""
if rc and hasattr(rc, "calculate_mel_features_rust"):
            return rc.calculate_mel_features_rust(samples, num_bins, 16000)

        # Fallback: simple energy distribution
        chunks = np.array_split(samples, num_bins)
        return [float(np.log10(np.mean(c**2) + 1e-10)) for c in chunks]


    def synchronize_streams(
        self, transcriptions: List[Tuple[float, str]], responses: List[Tuple[float, str]]
    ) -> List[Tuple[float, str, str]]:
"""
Synchronize multiple modality streams (e.g. ASR + LLM) for "see-while-hear".""
if rc and hasattr(rc, "synchronize_modalities_rust"):
            return rc.synchronize_modalities_rust(transcriptions, responses)

        # Python fallback: Time-based matching
        synced = []
        for t_time, t_text in transcriptions:
            # Find closest response matching the time
            closest = min(responses, key=lambda x, t=t_time: abs(x[0] - t), default=(0, ""))
            synced.append((t_time, t_text, closest[1] if abs(closest[0] - t_time) < 2.0 else ""))
        return synced


    def project_alignment(
        self, embedding: List[float], weights: List[float], bias: Optional[List[float]] = None
    ) -> List[float]:
"""
Apply layer-dimension mapping (projection) for modality alignment.
"""
if rc and hasattr(rc, "project_modality_embeddings_rust"):
            in_dim = len(embedding)
            out_dim = len(weights) // in_dim
            return rc.project_modality_embeddings_rust(embedding, weights, bias, in_dim, out_dim)

        # Simple Python implementation
        emb_arr = np.array(embedding)
        in_dim = len(embedding)
        out_dim = len(weights) // in_dim
        w_arr = np.array(weights).reshape(out_dim, in_dim)
        res = w_arr @ emb_arr
        if bias:
            res += np.array(bias)
        return res.tolist()


    def quantize_audio(self, samples: List[float]) -> List[int]:
"""
Reduce audio bit-depth for low-latency streaming.
"""
if rc and hasattr(rc, "audio_quantize_int8_rust"):
            return rc.audio_quantize_int8_rust(samples)
        return [int(max(-1.0, min(1.0, s)) * 127) for s in samples]


    def split_image_grid(self, pixels: bytes, width: int, height: int, rows: int = 2, cols: int = 2) -> List[bytes]:
"""
Split high-resolution images into manageable tiles for multimodal tokens.
"""
if rc and hasattr(rc, "image_grid_split_rust"):
            tiles = rc.image_grid_split_rust(list(pixels), width, height, rows, cols)
            return [bytes(t) for t in tiles]

        # Basic Python chunking fallback
        tile_w, tile_h = width // cols, height // rows
        tiles = []
        for r in range(rows):
            for c in range(cols):
                tile = bytearray()
                for y in range(tile_h):
                    start = ((r * tile_h + y) * width + (c * tile_w)) * 3
                    tile.extend(pixels[start : start + tile_w * 3])
                tiles.append(bytes(tile))
        return tiles


    def get_modality_weights(self, audio_energy: float, text_density: float) -> Tuple[float, float]:
"""
Calculate importance weights for fusing modalities.
"""
if rc and hasattr(rc, "calculate_dynamic_modality_weights_rust"):
            return rc.calculate_dynamic_modality_weights_rust(audio_energy, text_density)

        ea, et = math.exp(audio_energy), math.exp(text_density)
        s = ea + et
        return ea / s, et / s


    def parse_stream(self, content: str) -> List[Dict[str, Any]]:
"""
Parse a streaming response for modality tags (e.g. <Audio:EN_123>).
        Supports multi-channel interleaved streams (DVD-style).
"""
if rc and hasattr(rc, "parse_modality_stream_rust"):
            fragments = rc.parse_modality_stream_rust(content)
            # Tuple: (type, m_type, channel, id/content)
            return [
                {
                    "type": f[0],
                    "modality": f[1],
                    "channel": f[2],
                    "id": f[3] if f[0] == "media" else None,
                    "content": f[3] if f[0] != "media" else None,
                }
                for f in fragments
            ]

        # Basic Python fallback with channel support
        parts = []
        last_idx = 0
        # Supports <Type:Channel_ID> or <Type_ID> (DVD-style) or <Thought>...</Thought>
        # Using DOTALL to allow thoughts to span lines
        # Expanded to support systemic tags like <Security:Isolation_DENY> or <Time_2026...>
        pattern = re.compile(r"<([A-Z][a-zA-Z0-9]+)(?::([^>_ ]+))?_([^>]+)>|<(Thought)>(.*?)</Thought>", re.DOTALL)
        for match in pattern.finditer(content):
            if match.start() > last_idx:
                parts.append(
                    {
                        "type": "text",
                        "modality": "text",
                        "channel": "default",
                        "id": None,
                        "content": content[last_idx : match.start()],
                    }
                )

            if match.group(4) and match.group(4).lower() == "thought":
                parts.append(
                    {
                        "type": "modality",
                        "modality": "Thought",
                        "channel": "default",
                        "id": None,
                        "content": match.group(5),
                    }
                )
            else:
                m_type = match.group(1)
                channel = match.group(2) or "default"
                m_id = match.group(3)

                parts.append(
                    {
                        "type": "media" if m_type in ["Audio", "Video", "Image"] else "modality",
                        "modality": m_type,
                        "channel": channel,
                        "id": m_id,
                        "content": None,
                    }
                )
            last_idx = match.end()

        if last_idx < len(content):
            parts.append(
                {"type": "text", "modality": "text", "channel": "default", "id": None, "content": content[last_idx:]}
            )

        return parts


    def select_channels(self, fragments: List[Dict[str, Any]], channels: Dict[str, str]) -> List[Dict[str, Any]]:
"""
Filter a multi-channel stream to show only active tracks (e.g. EN audio, Angle 1 video).
"""
if rc and hasattr(rc, "switch_modality_channel_rust"):
            # Convert dicts back to tuples for Rust processing
            rust_frags = [(f["type"], f["modality"], f["channel"], f["id"] or f["content"] or "") for f in fragments]
            result = rc.switch_modality_channel_rust(rust_frags, channels)
            return [
                {
                    "type": r[0],
                    "modality": r[1],
                    "channel": r[2],
                    "id": r[3] if r[0] == "media" else None,
                    "content": r[3] if r[0] == "text" else None,
                }
                for r in result
            ]

        # Python fallback
        output = []
        for f in fragments:
            if f["type"] == "text":
                output.append(f)
            else:
                m_type = f["modality"]
                current_ch = f["channel"]
                target_ch = channels.get(m_type)

                if not target_ch or current_ch == target_ch or current_ch == "default":
                    output.append(f)
        return output


    def create_mosaic(self, feeds: List[bytes], width: int, height: int, rows: int, cols: int) -> bytes:
"""
Combine multiple camera feeds into a single mosaic.
"""
if rc and hasattr(rc, "create_vision_mosaic_rust"):
            mosaic = rc.create_vision_mosaic_rust([list(f) for f in feeds], width, height, rows, cols)
            return bytes(mosaic)

        # Simple Python concatenation fallback
        feed_arrays = [np.frombuffer(f, dtype=np.uint8).reshape(height, width, 3) for f in feeds]
        row_images = []
        for r in range(rows):
            row = np.hstack(feed_arrays[r * cols : (r + 1) * cols])
            row_images.append(row)
        mosaic = np.vstack(row_images)
        return mosaic.tobytes()


    def detect_motion(self, prev: bytes, curr: bytes, threshold: float = 10.0) -> bool:
"""
Check for significant visual changes.""
if rc and hasattr(rc, "detect_motion_rust"):
            return rc.detect_motion_rust(list(prev), list(curr), threshold)
        return False  # Fallback to always process if Rust is missing


    def mix_audio(self, tracks: List[List[float]], weights: Optional[List[float]] = None) -> List[float]:
"""
Mix multiple audio streams (DVD-style).""
if not weights:
            weights = [1.0] * len(tracks)
        if rc and hasattr(rc, "audio_mix_tracks_rust"):
            return rc.audio_mix_tracks_rust(tracks, weights)

        # Simple Python mix
        max_len = max(len(t) for t in tracks) if tracks else 0
        output = [0.0] * max_len
        for i, track in enumerate(tracks):
            w = weights[i]
            for j, s in enumerate(track):
                output[j] += s * w
        return [max(-1.0, min(1.0, s)) for s in output]


    def get_av_sync_score(self, audio_energy: List[float], visual_motion: List[float]) -> float:
"""
Measure temporal alignment between audio and video frames.""
if rc and hasattr(rc, "calculate_av_alignment_score_rust"):
            return rc.calculate_av_alignment_score_rust(audio_energy, visual_motion)
        return 1.0  # Default to perfect sync if unable to measure


    def detect_scene_change(self, prev_hist: List[float], curr_hist: List[float], threshold: float = 0.5) -> bool:
"""
Detect when a video stream switches camera angles.""
if rc and hasattr(rc, "detect_visual_scene_change_rust"):
            return rc.detect_visual_scene_change_rust(prev_hist, curr_hist, threshold)
        return False


    def get_saliency_map(self, pixels: bytes, width: int, height: int, grid_size: int = 16) -> List[float]:
"""
Generate a heatmap of visual energy (focal points).""
if rc and hasattr(rc, "calculate_vision_saliency_rust"):
            return rc.calculate_vision_saliency_rust(list(pixels), width, height, grid_size)
        return []


    def extract_roi(self, pixels: bytes, width: int, height: int, x: int, y: int, rw: int, rh: int) -> bytes:
"""
Crop a sub-region (Region of Interest) from a frame.
        Useful for "zooming in" on active regions detected by saliency.
"""
if rc and hasattr(rc, "extract_vision_roi_rust"):
            roi = rc.extract_vision_roi_rust(list(pixels), width, height, x, y, rw, rh)
            return bytes(roi)

        # Simple Python crop
        row_size = width * 3
        roi = bytearray()
        for i in range(y, y + rh):
            start = i * row_size + x * 3
            roi.extend(pixels[start : start + rw * 3])
        return bytes(roi)


    def calculate_audio_direction(self, left: List[float], right: List[float], sample_rate: int = 16000) -> float:
"""
Estimate source angle (-90 to 90) using Interaural Time Difference (ITD).
"""
if rc and hasattr(rc, "calculate_audio_direction_rust"):
            return rc.calculate_audio_direction_rust(left, right, sample_rate)
        return 0.0  # Fallback: straight ahead


    def overlay_vision(
        self,
        base: bytes,
        overlay: bytes,
        base_size: Tuple[int, int],
        overlay_size: Tuple[int, int],
        position: Tuple[int, int] = (0, 0),
        alpha: float = 1.0,
    ) -> bytes:
"""
Overlay a camera feed (PiP) on a base video frame.""
if rc and hasattr(rc, "overlay_vision_feeds_rust"):
            res = rc.overlay_vision_feeds_rust(
                list(base),
                list(overlay),
                base_size[0],
                base_size[1],
                overlay_size[0],
                overlay_size[1],
                position[0],
                position[1],
                alpha,
            )
            return bytes(res)
        return base  # Fallback: return base if untransformable


    def transform_vision(
        self,
        pixels: bytes,
        src_size: Tuple[int, int],
        dst_size: Tuple[int, int],
        keep_aspect: bool = True,
        pad_color: Tuple[int, int, int] = (0, 0, 0),
    ) -> bytes:
"""
Resize or pad a camera feed to fit target dimensions.""
if rc and hasattr(rc, "transform_vision_feed_rust"):
            res = rc.transform_vision_feed_rust(
                list(pixels), src_size[0], src_size[1], dst_size[0], dst_size[1], keep_aspect, pad_color
            )
            return bytes(res)
        return pixels


    def apply_visual_filter(self, pixels: bytes, filter_type: str, intensity: float = 1.0) -> bytes:
"""
Apply a visual filter (e.g. grayscale, inverse) to a feed.""
if rc and hasattr(rc, "apply_vision_filter_rust"):
            res = rc.apply_vision_filter_rust(list(pixels), filter_type, intensity)
            return bytes(res)
        return pixels


    def synchronize_color_profiles(self, pixels: bytes, reference: bytes) -> bytes:
"""
Match the color/brightness of a feed to a reference feed (unify cameras).""
if rc and hasattr(rc, "match_vision_color_profiles_rust"):
            return bytes(rc.match_vision_color_profiles_rust(list(pixels), list(reference)))
        return pixels


    def apply_layout(
            self,
            feeds: List[bytes],
            sizes: List[Tuple[int, int]],
            target_size: Tuple[int, int],
            template: str = "grid"
        ) -> bytes:
"""
Apply a complex vision layout (e.g. sidebar, grid) to multiple feeds.""
if rc and hasattr(rc, "layout_vision_feeds_rust"):
            res = rc.layout_vision_feeds_rust(
                [list(f) for f in feeds], sizes, target_size[0], target_size[1], template
            )
            return bytes(res)

        # Fallback to simple mosaic if layout rust is missing
        if template == "grid":
            return self.create_mosaic(feeds, sizes[0][0], sizes[0][1], 2, 2)
        return feeds[0] if feeds else b""


    def fuse_modalities(self, vision_emb: List[float], audio_emb: List[float], dim: int = 4096) -> List[float]:
"""
Apply cross-modality gating (Logic: Audio weights Vision tokens).""
if rc and hasattr(rc, "calculate_multimodal_fusion_rust"):
            return rc.calculate_multimodal_fusion_rust(vision_emb, audio_emb, dim)

        # Python implementation: Gated Multimodal Fusion
        v = np.array(vision_emb).reshape(-1, dim)
        a = np.array(audio_emb).reshape(-1, dim).mean(axis=0)
        gate = 1.0 / (1.0 + np.exp(-a))
        return (v * gate).flatten().tolist()


    def align_modalities(
        self, text_embedding: List[float], vision_embedding: List[float], embedding_dim: int = 4096
    ) -> List[float]:
"""
Perform sequence-dimension concatenation for vision-text alignment.
        This follows the Stream-Omni architecture for efficient omni-modal integration.
"""
if rc and hasattr(rc, "align_modality_sequence_rust"):
            return rc.align_modality_sequence_rust(text_embedding, vision_embedding, embedding_dim)

        # Python fallback: concatenate vision sequence then text sequence
        return vision_embedding + text_embedding


    def process_multimodal_input(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
"""
Orchestrate multimodal inputs for model ingestion.
        Converts media references into aligned sequence embeddings (Stream-Omni style).
        Refactored for clarity and reduced complexity.
"""
processed = {
            "text": "",
            "media": [],
            "aligned_embeddings": [],
        }

        for item in inputs:
            if not self._validate_input_item(item):
                continue
            itype = item["type"]
            if itype == "text":
                processed["text"] += self._extract_text_content(item)
            elif itype == "media":
                self._process_media_item(item, processed)

        return processed


    def _validate_input_item(self, item: Dict[str, Any]) -> bool:
"""
Validate input item structure.""
return isinstance(item, dict) and "type" in item


    def _extract_text_content(self, item: Dict[str, Any]) -> str:
"""
Extract text content from item.""
return item.get("content", "")


    def _process_media_item(self, item: Dict[str, Any], processed: Dict[str, Any]) -> None:
        ""
Process a media item: append to media, align embedding, and update text.""
m_type = item.get("modality", "image")
        m_id = item.get("id")
        processed["media"].append(item)
        # Real embedding extraction and projection
        uri = self.registry.get(m_id) if m_id else None
        if m_type.lower() == "image" and uri:
        # Example: extract image embedding using QuantizedMultimediaEngine
            try:
                image_data = self.q_engine.load_image(uri)
                emb = self.q_engine.extract_image_embedding(image_data)
                weights = self.q_engine.get_projection_weights("image")
                aligned = self.project_alignment(emb, weights)
            except (IOError, ValueError, AttributeError) as e:
                logger.warning(f"Failed to process image media {m_id}: {e}")
                aligned = []
        elif m_type.lower() == "audio" and uri:
            try:
                audio_data = self.q_engine.load_audio(uri)
                emb = self.q_engine.extract_audio_embedding(audio_data)
                weights = self.q_engine.get_projection_weights("audio")
                aligned = self.project_alignment(emb, weights)
            except (IOError, ValueError, AttributeError) as e:
                logger.warning(f"Failed to process audio media {m_id}: {e}")
                aligned = []
        else:
            aligned = []

        processed["aligned_embeddings"].append(aligned)
        processed["text"] += f"<{m_type.capitalize()}_{m_id}>"
