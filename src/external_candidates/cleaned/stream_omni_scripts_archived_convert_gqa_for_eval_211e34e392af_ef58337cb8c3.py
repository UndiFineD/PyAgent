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

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\scripts\archived\convert_gqa_for_eval.py
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
