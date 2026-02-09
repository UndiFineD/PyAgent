# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\stream_omni\eval\asr\cer.py
import argparse
import json
import re

from jiwer import cer  # You can use pycer or implement your own CER function if needed


def normalize_text(text):
    """Remove all non-Chinese characters."""
    text = re.sub(r"[^\u4e00-\u9fff]", "", text)  # 只保留中文字符
    return text


def compute_cer(file_path):
    """Compute CER for a JSONL file."""
    references, hypotheses = [], []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if (
                normalize_text(str(data["transcription"])) == ""
                or normalize_text(str(data["outputs"])) == ""
            ):
                continue
            references.append(normalize_text(str(data["transcription"])))
            hypotheses.append(normalize_text(str(data["outputs"])))
    error_rate = cer(references, hypotheses)  # Use the CER function from jiwer
    print(f"CER: {error_rate:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to JSONL file")
    args = parser.parse_args()

    compute_cer(args.file)
