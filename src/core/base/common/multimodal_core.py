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
Core logic for multimodal stream parsing and modality alignment.
Inspired by Stream-Omni (ICTNLP).
"""

<<<<<<< HEAD
<<<<<<< HEAD
from .multimodal_buffer import TemporalModalityBuffer
from .multimodal_encoders import StreamingAudioProcessor, StreamingVisionEncoder
# Re-export modules to maintain backward compatibility
from .multimodal_logic import MultimodalCore
from .multimodal_session import MultimodalStreamSession
from .multimodal_state import StreamState

__all__ = [
    "StreamState",
    "TemporalModalityBuffer",
    "StreamingVisionEncoder",
    "StreamingAudioProcessor",
    "MultimodalCore",
    "MultimodalStreamSession",
]
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from .base_core import BaseCore
from .models.core_enums import InputType
from src.infrastructure.engine.multimodal import Muxer, ChannelType, QuantizedMultimediaEngine

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.multimodal")

class StreamState:
    """State management for incomplete modality tags in a stream."""
    def __init__(self) -> None:
        self.buffer = ""

class TemporalModalityBuffer:
    """
    Rolling buffer for multimodal sequences (Short-term memory).
    Stores recent frames/audio to allow temporal reasoning.
    """
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.frames: List[bytes] = []
        self.timestamps: List[float] = []

    def push(self, frame: bytes, timestamp: float):
        self.frames.append(frame)
        self.timestamps.append(timestamp)
        if len(self.frames) > self.max_size:
            self.frames.pop(0)
            self.timestamps.pop(0)

    def get_dynamics(self) -> float:
        """Calculate how much change is happening in this buffer."""
        if rc and hasattr(rc, "calculate_temporal_entropy_rust"):
            return rc.calculate_temporal_entropy_rust([list(f) for f in self.frames])
        return 0.0

class StreamingVisionEncoder:
    """
    Handles efficient vision streaming using adaptive delta compression.
    Only sends changed pixels between frames to conserve bandwidth.
    Adjusts sensitivity based on scene dynamics (entropy).
    """
    def __init__(self, base_threshold: int = 15):
        self.prev_frame: Optional[bytes] = None
        self.threshold = base_threshold
        self.base_threshold = base_threshold

    def adapt_threshold(self, entropy: float):
        """
        Adjust threshold based on motion complexity.
        Higher entropy (lots of motion) -> higher threshold to save bandwidth.
        """
        # Logic: If entropy is high, we can afford to skip subtle changes
        self.threshold = int(self.base_threshold * (1.0 + entropy))

    def encode(self, frame: bytes, entropy: float = 0.0) -> Union[bytes, List[Tuple[int, int, int, int]]]:
        """Encode frame: returns full bytes for keyframes, or deltas for P-frames."""
        if entropy > 0:
            self.adapt_threshold(entropy)
            
        if self.prev_frame is None:
            self.prev_frame = frame
            return frame # Keyframe
        
        if rc and hasattr(rc, "calculate_visual_deltas_rust"):
            deltas = rc.calculate_visual_deltas_rust(list(self.prev_frame), list(frame), self.threshold)
            self.prev_frame = frame
            return deltas
        
        self.prev_frame = frame
        return frame

    def decode(self, base_frame: bytes, deltas: List[Tuple[int, int, int, int]]) -> bytes:
        """Reconstruct a frame using a base and incoming deltas."""
        if rc and hasattr(rc, "apply_visual_deltas_rust"):
            return bytes(rc.apply_visual_deltas_rust(list(base_frame), deltas))
        return base_frame

class StreamingAudioProcessor:
    """
    Stateful processor for continuous audio streams.
    Handles rolling buffers, VAD, and feature extraction.
    """
    def __init__(self, sample_rate: int = 16000, frame_size: int = 512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.buffer: List[float] = []

    def push(self, chunk: List[float]) -> List[List[float]]:
        """
        Push new audio samples and return extracted Mel features for completed frames.
        """
        self.buffer.extend(chunk)
        frames = []
        
        while len(self.buffer) >= self.frame_size:
            frame = self.buffer[:self.frame_size]
            self.buffer = self.buffer[self.frame_size:]
            
            # Check for voice activity
            is_active = True
            if rc and hasattr(rc, "speech_vad_rust"):
                is_active = rc.speech_vad_rust(frame, 0.01)
            
            if is_active:
                if rc and hasattr(rc, "calculate_mel_features_rust"):
                    features = rc.calculate_mel_features_rust(frame, 80, self.sample_rate)
                    frames.append(features)
                else:
                    # Generic fallback
                    frames.append([sum(frame) / len(frame)] * 80)
                    
        return frames

class MultimodalCore(BaseCore):
    """
    Unified Multimodal Alignment and Streaming Core.
    Implements efficient modality alignments (sequence-dimension concatenation)
    and simultaneous stream parsing for "see-while-hear" experiences.
    """

    def __init__(self, name: str = "MultimodalCore", root_path: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=root_path)
        self.registry: Dict[str, str] = {} # Tag -> URI/Path
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
            "Psi": "default"
        }

    def set_active_channel(self, modality: str, channel_id: str) -> None:
        """
        Switch the active channel for a specific modality (e.g. switch Audio to 'EN').
        """
        self.active_channels[modality] = channel_id
        logger.info(f"Modality {modality} channel switched to: {channel_id}")

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
        # If there's an open '<' without a '>', buffer it
        last_open_angle = full_content.rfind('<')
        last_close_angle = full_content.rfind('>')
        
        if last_open_angle > last_close_angle:
            # Tag is potentially split
            to_parse = full_content[:last_open_angle]
            state.buffer = full_content[last_open_angle:]
        else:
            to_parse = full_content
            state.buffer = ""
            
        return self.parse_stream(to_parse)

    def register_media(self, tag: str, uri: str) -> None:
        """Associate a media tag with a resolved URI."""
        self.registry[tag] = uri

    def mux_dvd_channels(self, audio: bytes, video: bytes, text: str) -> bytes:
        """
        Packs separate modalities into a single sync-packet for 120fps DVD-like streaming.
        Uses 0xDEADBEEF binary muxer.
        """
        return self.muxer.synchronize_tick(audio, video, text)

    def apply_scaling(self, activations: Any, scaling: Any) -> Any:
        """Applies IA3 scaling via the QuantizedMultimediaEngine."""
        return self.q_engine.apply_stream_ia3(activations, scaling)

    def resolve_tag(self, tag: str) -> Optional[str]:
        """Get URI for a specific tag."""
        return self.registry.get(tag)

    def calculate_audio_features(self, samples: List[float], num_bins: int = 80) -> List[float]:
        """
        Extract Mel-frequency features for audio alignment.
        """
        if rc and hasattr(rc, "calculate_mel_features_rust"):
            return rc.calculate_mel_features_rust(samples, num_bins, 16000)
        
        # Fallback: simple energy distribution
        import numpy as np
        chunks = np.array_split(samples, num_bins)
        return [float(np.log10(np.mean(c**2) + 1e-10)) for c in chunks]

    def synchronize_streams(
        self, 
        transcriptions: List[Tuple[float, str]], 
        responses: List[Tuple[float, str]]
    ) -> List[Tuple[float, str, str]]:
        """
        Synchronize multiple modality streams (e.g. ASR + LLM) for "see-while-hear".
        """
        if rc and hasattr(rc, "synchronize_modalities_rust"):
            return rc.synchronize_modalities_rust(transcriptions, responses)
        
        # Python fallback: Time-based matching
        synced = []
        for t_time, t_text in transcriptions:
            # Find closest response matching the time
            closest = min(responses, key=lambda x: abs(x[0] - t_time), default=(0, ""))
            synced.append((t_time, t_text, closest[1] if abs(closest[0] - t_time) < 2.0 else ""))
        return synced

    def project_alignment(
        self, 
        embedding: List[float], 
        weights: List[float], 
        bias: Optional[List[float]] = None
    ) -> List[float]:
        """
        Apply layer-dimension mapping (projection) for modality alignment.
        """
        if rc and hasattr(rc, "project_modality_embeddings_rust"):
            in_dim = len(embedding)
            out_dim = len(weights) // in_dim
            return rc.project_modality_embeddings_rust(embedding, weights, bias, in_dim, out_dim)
        
        # Simple Python implementation
        import numpy as np
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
        
        import math
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
                    "content": f[3] if f[0] != "media" else None
                }
                for f in fragments
            ]

        # Basic Python fallback with channel support
        import re
        parts = []
        last_idx = 0
        # Supports <Type:Channel_ID> or <Type_ID> (DVD-style) or <Thought>...</Thought>
        # Using DOTALL to allow thoughts to span lines
        # Expanded to support systemic tags like <Security:Isolation_DENY> or <Time_2026...>
        pattern = re.compile(
            r"<([A-Z][a-zA-Z0-9]+)(?::([^>_ ]+))?_([^>]+)>|<(Thought)>(.*?)</Thought>", 
            re.DOTALL
        )
        for match in pattern.finditer(content):
            if match.start() > last_idx:
                parts.append({
                    "type": "text", 
                    "modality": "text", 
                    "channel": "default", 
                    "id": None, 
                    "content": content[last_idx:match.start()]
                })
            
            if match.group(4) and match.group(4).lower() == "thought":
                parts.append({
                    "type": "modality",
                    "modality": "Thought",
                    "channel": "default",
                    "id": None,
                    "content": match.group(5)
                })
            else:
                m_type = match.group(1)
                channel = match.group(2) or "default"
                m_id = match.group(3)
                
                parts.append({
                    "type": "media" if m_type in ["Audio", "Video", "Image"] else "modality", 
                    "modality": m_type, 
                    "channel": channel, 
                    "id": m_id, 
                    "content": None
                })
            last_idx = match.end()
            
        if last_idx < len(content):
            parts.append({
                "type": "text", 
                "modality": "text", 
                "channel": "default", 
                "id": None, 
                "content": content[last_idx:]
            })
            
        return parts

    def select_channels(self, fragments: List[Dict[str, Any]], channels: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Filter a multi-channel stream to show only active tracks (e.g. EN audio, Angle 1 video).
        """
        if rc and hasattr(rc, "switch_modality_channel_rust"):
            # Convert dicts back to tuples for Rust processing
            rust_frags = [
                (f["type"], f["modality"], f["channel"], f["id"] or f["content"] or "")
                for f in fragments
            ]
            result = rc.switch_modality_channel_rust(rust_frags, channels)
            return [
                {
                    "type": r[0],
                    "modality": r[1],
                    "channel": r[2],
                    "id": r[3] if r[0] == "media" else None,
                    "content": r[3] if r[0] == "text" else None
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
        import numpy as np
        feed_arrays = [np.frombuffer(f, dtype=np.uint8).reshape(height, width, 3) for f in feeds]
        row_images = []
        for r in range(rows):
            row = np.hstack(feed_arrays[r*cols : (r+1)*cols])
            row_images.append(row)
        mosaic = np.vstack(row_images)
        return mosaic.tobytes()

    def detect_motion(self, prev: bytes, curr: bytes, threshold: float = 10.0) -> bool:
        """Check for significant visual changes."""
        if rc and hasattr(rc, "detect_motion_rust"):
            return rc.detect_motion_rust(list(prev), list(curr), threshold)
        return False # Fallback to always process if Rust is missing

    def mix_audio(self, tracks: List[List[float]], weights: Optional[List[float]] = None) -> List[float]:
        """Mix multiple audio streams (DVD-style)."""
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
        """Measure temporal alignment between audio and video frames."""
        if rc and hasattr(rc, "calculate_av_alignment_score_rust"):
            return rc.calculate_av_alignment_score_rust(audio_energy, visual_motion)
        return 1.0 # Default to perfect sync if unable to measure

    def detect_scene_change(self, prev_hist: List[float], curr_hist: List[float], threshold: float = 0.5) -> bool:
        """Detect when a video stream switches camera angles."""
        if rc and hasattr(rc, "detect_visual_scene_change_rust"):
            return rc.detect_visual_scene_change_rust(prev_hist, curr_hist, threshold)
        return False

    def get_saliency_map(self, pixels: bytes, width: int, height: int, grid_size: int = 16) -> List[float]:
        """Generate a heatmap of visual energy (focal points)."""
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
        return 0.0 # Fallback: straight ahead

    def overlay_vision(
        self, 
        base: bytes, 
        overlay: bytes, 
        base_size: Tuple[int, int], 
        overlay_size: Tuple[int, int], 
        position: Tuple[int, int] = (0, 0),
        alpha: float = 1.0
    ) -> bytes:
        """Overlay a camera feed (PiP) on a base video frame."""
        if rc and hasattr(rc, "overlay_vision_feeds_rust"):
            res = rc.overlay_vision_feeds_rust(
                list(base), list(overlay), 
                base_size[0], base_size[1], 
                overlay_size[0], overlay_size[1], 
                position[0], position[1], 
                alpha
            )
            return bytes(res)
        return base # Fallback: return base if untransformable

    def transform_vision(
        self, 
        pixels: bytes, 
        src_size: Tuple[int, int], 
        dst_size: Tuple[int, int], 
        keep_aspect: bool = True,
        pad_color: Tuple[int, int, int] = (0, 0, 0)
    ) -> bytes:
        """Resize or pad a camera feed to fit target dimensions."""
        if rc and hasattr(rc, "transform_vision_feed_rust"):
            res = rc.transform_vision_feed_rust(
                list(pixels), src_size[0], src_size[1], 
                dst_size[0], dst_size[1], 
                keep_aspect, pad_color
            )
            return bytes(res)
        return pixels

    def apply_visual_filter(self, pixels: bytes, filter_type: str, intensity: float = 1.0) -> bytes:
        """Apply a visual filter (e.g. grayscale, inverse) to a feed."""
        if rc and hasattr(rc, "apply_vision_filter_rust"):
            res = rc.apply_vision_filter_rust(list(pixels), filter_type, intensity)
            return bytes(res)
        return pixels

    def synchronize_color_profiles(self, pixels: bytes, reference: bytes) -> bytes:
        """Match the color/brightness of a feed to a reference feed (unify cameras)."""
        if rc and hasattr(rc, "match_vision_color_profiles_rust"):
            res = rc.match_vision_color_profiles_rust(list(pixels), list(reference))
            return bytes(res)
        return pixels

    def get_saliency_map(self, pixels: bytes, size: Tuple[int, int], grid_size: int = 16) -> List[float]:
        """Identify regions of interest based on visual energy (Luminance)."""
        if rc and hasattr(rc, "calculate_vision_saliency_rust"):
            return rc.calculate_vision_saliency_rust(list(pixels), size[0], size[1], grid_size)
        return []

    def extract_roi(
        self, 
        pixels: bytes, 
        size: Tuple[int, int], 
        roi: Tuple[int, int, int, int]
    ) -> bytes:
        """Extract and zoom into a Region of Interest (ROI) (e.g. crop x,y,w,h)."""
        if rc and hasattr(rc, "extract_vision_roi_rust"):
            res = rc.extract_vision_roi_rust(
                list(pixels), size[0], size[1], 
                roi[0], roi[1], roi[2], roi[3]
            )
            return bytes(res)
        
        # Python fallback
        import numpy as np
        arr = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 3)
        crop = arr[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
        return crop.tobytes()

    def apply_layout(
        self, 
        feeds: List[bytes], 
        sizes: List[Tuple[int, int]], 
        target_size: Tuple[int, int], 
        template: str = "grid"
    ) -> bytes:
        """Apply a complex vision layout (e.g. sidebar, grid) to multiple feeds."""
        if rc and hasattr(rc, "layout_vision_feeds_rust"):
            res = rc.layout_vision_feeds_rust(
                [list(f) for f in feeds], 
                sizes, 
                target_size[0], target_size[1], 
                template
            )
            return bytes(res)
        
        # Fallback to simple mosaic if layout rust is missing
        if template == "grid":
            return self.create_mosaic(feeds, sizes[0][0], sizes[0][1], 2, 2)
        return feeds[0] if feeds else b""

    def fuse_modalities(
        self, 
        vision_emb: List[float], 
        audio_emb: List[float], 
        dim: int = 4096
    ) -> List[float]:
        """Apply cross-modality gating (Logic: Audio weights Vision tokens)."""
        if rc and hasattr(rc, "calculate_multimodal_fusion_rust"):
            return rc.calculate_multimodal_fusion_rust(vision_emb, audio_emb, dim)
        
        # Python implementation: Gated Multimodal Fusion
        import numpy as np
        v = np.array(vision_emb).reshape(-1, dim)
        a = np.array(audio_emb).reshape(-1, dim).mean(axis=0)
        gate = 1.0 / (1.0 + np.exp(-a))
        return (v * gate).flatten().tolist()

    def align_modalities(
        self, 
        text_embedding: List[float], 
        vision_embedding: List[float],
        embedding_dim: int = 4096
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
        """
        processed = {
            "text": "",
            "media": [],
            "aligned_embeddings": [] # List of (dim, sequence)
        }
        
        for item in inputs:
            itype = item.get("type")
            if itype == "text":
                processed["text"] += item.get("content", "")
            elif itype == "media":
                m_type = item.get("modality", "image")
                m_id = item.get("id")
                
                # Logic: Resolve embedding from storage and project it
                # For now, we simulate the alignment step
                processed["media"].append(item)
                
                # Mock embedding for demonstration of the alignment logic
                mock_emb = [0.1] * 4096 
                mock_weights = [0.01] * (4096 * 4096)
                
                # Apply Rust-accelerated projection
                aligned = self.project_alignment(mock_emb, mock_weights)
                processed["aligned_embeddings"].append(aligned)
                
                # Insert token placeholder in text
                processed["text"] += f"<{m_type.capitalize()}_{m_id}>"
                
        return processed


class MultimodalStreamSession:
    """
    High-level manager for a single multimodal interaction session.
    Orchestrates live input processing and compressed output generation.
    """
    def __init__(self, core: MultimodalCore):
        self.core = core
        self.audio_proc = StreamingAudioProcessor()
        self.vision_enc = StreamingVisionEncoder()
        self.temporal_mem = TemporalModalityBuffer(max_size=15) # ~1 second of frames at 15fps
        self.channels = dict(core.active_channels) # Clone defaults
        self.channels["Thought"] = "hidden" # Default thought to hidden for session
        self.input_history: List[Dict[str, Any]] = []
        self.output_history: List[Dict[str, Any]] = []
        self.modificators: List[Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]] = []

    def add_modificator(self, mod: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]):
        """Add a hook to modify fragments before they reach the channel filter."""
        self.modificators.append(mod)

    def process_120fps_pulse(self, audio: bytes, video: bytes, text: str) -> bytes:
        """
        Specialized 120fps pulse handler for Phase 51 Multimedia & Attention.
        Muxes separate modalities and prepares for hardware-accelerated delivery.
        """
        packet = self.core.mux_dvd_channels(audio, video, text)
        return packet

    def process_input_frame(self, audio: List[float], image: Optional[bytes] = None, width: int = 640, height: int = 480) -> Dict[str, Any]:
        """
        Process a single clock-tick of multimodal data (e.g. 32ms audio + optional frame).
        Includes smart dynamic focus and adaptive bandwidth.
        """
        # Update temporal memory
        import time
        timestamp = time.time()
        
        if image:
            self.temporal_mem.push(image, timestamp)
            
        # Calculate dynamics (entropy) for adaptive compression from short-term memory
        entropy = self.temporal_mem.get_dynamics()
            
        result = {
            "audio_features": self.audio_proc.push(audio),
            "vision_deltas": None,
            "spatial_angle": 0.0,
            "active_roi": None,
            "dynamics": entropy
        }
        
        if image:
            # Encode with adaptive threshold
            result["vision_deltas"] = self.vision_enc.encode(image, entropy=entropy)
            
            # Smart Focus: Find most salient region and "zoom"
            saliency = self.core.get_saliency_map(image, width, height)
            if saliency:
                # Find grid index with max energy
                max_idx = saliency.index(max(saliency))
                grid_cols = width // 16
                y_grid, x_grid = divmod(max_idx, grid_cols)
                
                # Extract 224x224 ROI around focal point (CLIP/LLAVA size)
                rx = max(0, min(width - 224, x_grid * 16 - 112))
                ry = max(0, min(height - 224, y_grid * 16 - 112))
                result["active_roi"] = self.core.extract_roi(image, width, height, rx, ry, 224, 224)
        
        # If stereo audio, estimate direction
        if len(audio) > 1024 and len(audio) % 2 == 0:
            left = audio[0::2]
            right = audio[1::2]
            result["spatial_angle"] = self.core.calculate_audio_direction(left, right)
            
        self.input_history.append(result)
        return result

    def set_output_channel(self, modality: str, channel_id: str):
        """Switch the tracked channel (e.g. swap audio to 'FR')."""
        self.channels[modality] = channel_id
        
    def filter_response(self, raw_stream: str) -> List[Dict[str, Any]]:
        """
        Parses an LLM response chunk and filters it according to current DVD-style channels.
        Example: Hides <Thought> tags if directed.
        """
        fragments = self.core.parse_stream(raw_stream)

        # Feedback loop for channel modifications
        # Allows modifications to "feed back" into the parsing logic
        # before the final channel selector (filter) is applied.
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
        """Scans for text fragments that might contain newly injected tags."""
        new_list = []
        for f in fragments:
            if f["type"] == "text" and isinstance(f.get("content"), str) and "<" in f["content"] and ">" in f["content"]:
                # Re-parse this text fragment as it may contain new modality tags
                new_list.extend(self.core.parse_stream(f["content"]))
            else:
                new_list.append(f)
        return new_list

    def get_compressed_video_stream(self, frames: List[bytes]) -> List[Any]:
        """Use the Rust acceleration to generate a stream of visual deltas."""
        stream = []
        if not frames:
            return stream
            
        base = frames[0]
        stream.append(base) # Keyframe
        
        for i in range(1, len(frames)):
            deltas = self.vision_enc.encode(frames[i])
            stream.append(deltas) # P-frames
        return stream
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
