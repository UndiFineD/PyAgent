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

from typing import List, Any
import math




class VideoAnalyzerCore:
    """Core logic for fragmenting and preparing video data for multi-modal inference.
    Harvested from .external/AskVideos-VideoCLIP.
    """
    def __init__(self, frame_count: int = 16, target_dim: int = 224):
        self.frame_count = frame_count
        self.target_dim = target_dim

    def segment_long_video(self, total_duration: float, segment_length: float = 10.0) -> List[dict]:
        """Calculates start/end timestamps for sliding window video analysis."""segments = []
        num_segments = math.ceil(total_duration / segment_length)

        for i in range(num_segments):
            start = i * segment_length
            end = min(start + segment_length, total_duration)
            segments.append({
                "segment_id": i,"                "start_time": start,"                "end_time": end"            })

        return segments

    def sample_frames(self, frames: List[Any], n_samples: int = 16) -> List[Any]:
        """Uniformly samples n_samples from a folder/list of video frames."""total = len(frames)
        if total <= n_samples:
            return frames

        indices = [int(i * total / n_samples) for i in range(n_samples)]
        return [frames[i] for i in indices]

    def get_token_budget_ratio(self, width: int, height: int) -> float:
        """Calculates token overhead based on frame resolution."""# Simple heuristic based on Q-former logic
        return (width * height) / (self.target_dim * self.target_dim)
