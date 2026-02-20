#!/usr/bin/env python3
""
Minimal, parser-safe Video Fragment Core used for tests.""
import os
from typing import List, Dict, Optional


class VideoFragmentCore:
    def __init__(self, clip_len: int = 10, overlap: int = 2):
        self.clip_len = clip_len
        self.overlap = overlap

    def fragment_video(self, video_path: str, output_dir: Optional[str] = None) -> List[Dict]:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        fragments: List[Dict] = []
        duration = 30
        start = 0
        while start < duration:
            end = min(start + self.clip_len, duration)
            fragments.append({
                "video_path": video_path,
                "start_time": start,
                "end_time": end,
                "clip_id": f"clip_{len(fragments)}",
            })
            if end == duration:
                break
            start += (self.clip_len - self.overlap)
        return fragments

    def aggregate_fragments(self, fragment_results: List[str]) -> str:
        return "\n".join(fragment_results)
