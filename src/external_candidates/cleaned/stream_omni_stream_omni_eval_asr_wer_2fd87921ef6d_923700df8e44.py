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

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\eval\asr\wer.py
import argparse
import json
import re

from jiwer import wer


def normalize_text(text):
    """Remove punctuation and convert to uppercase."""
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)  # 移除所有标点符号
    return text.upper()


def compute_wer(file_path):
    """Compute WER for a JSONL file."""
    references, hypotheses = [], []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            references.append(normalize_text(data["transcription"]))
            hypotheses.append(normalize_text(data["outputs"]))

    error_rate = wer(references, hypotheses)
    print(f"WER: {error_rate:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to JSONL file")
    args = parser.parse_args()

    compute_wer(args.file)
