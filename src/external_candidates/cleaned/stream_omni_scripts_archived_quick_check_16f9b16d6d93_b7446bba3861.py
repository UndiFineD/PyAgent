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

# Extracted from: C:\DEV\PyAgent\.external\Stream-Omni\scripts\archived\quick_check.py
import argparse
import json
import os

import yaml
from tqdm import tqdm


def check_missing_images(json_path, images_folder):
    data = json.load(open(json_path, "r"))
    missing_data = []

    for i, d in enumerate(tqdm(data)):
        image = d["image"] if "image" in d else ""
        if image != "":
            path = os.path.join(images_folder, image)
            if not os.path.exists(path):
                print(f"Missing image: {path}")
                missing_data.append(d)

    return missing_data


def read_yaml_to_llava_data(yaml_path, images_folder):
    print(f"Reading YAML file: {yaml_path}")
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    llava_json_paths = data["datasets"]
    for item in llava_json_paths:
        json_path = item["json_path"]
        missing_data = check_missing_images(json_path, images_folder)
        if len(missing_data) > 0:
            print(f"Missing images in {json_path}:")
            for d in missing_data:
                print(d)


def direct_check_llava_data(json_path, images_folder):
    missing_data = check_missing_images(json_path, images_folder)
    if len(missing_data) > 0:
        print(f"Missing images in {json_path}:")
        for d in missing_data:
            print(d)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for missing images in dataset.")
    parser.add_argument(
        "--yaml_path",
        type=str,
        default="",
        help="Path to the YAML file containing the dataset.",
    )
    parser.add_argument(
        "--json_path",
        type=str,
        default="",
        help="Path to the JSON file containing the dataset.",
    )
    parser.add_argument(
        "--images_folder",
        type=str,
        default="/mnt/bn/vl-research/data/llava_data",
        help="Path to the folder containing the images.",
    )

    args = parser.parse_args()

    if args.json_path != "":
        direct_check_llava_data(args.json_path, args.images_folder)
    elif args.yaml_path != "":
        read_yaml_to_llava_data(args.yaml_path, args.images_folder)
