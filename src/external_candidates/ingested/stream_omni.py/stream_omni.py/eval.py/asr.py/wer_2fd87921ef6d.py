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
