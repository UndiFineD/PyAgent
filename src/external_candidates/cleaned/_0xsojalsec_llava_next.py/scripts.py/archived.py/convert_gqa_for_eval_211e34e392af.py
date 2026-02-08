# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LLaVA-NeXT\scripts\archived\convert_gqa_for_eval.py
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--src", type=str)
parser.add_argument("--dst", type=str)
args = parser.parse_args()

all_answers = []
for line_idx, line in enumerate(open(args.src)):
    res = json.loads(line)
    question_id = res["question_id"]
    text = res["text"].rstrip(".").lower()
    all_answers.append({"questionId": question_id, "prediction": text})

with open(args.dst, "w") as f:
    json.dump(all_answers, f)
