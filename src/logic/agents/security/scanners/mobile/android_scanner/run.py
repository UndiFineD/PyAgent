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

import os
import sys
import argparse
import markdown
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import api_keys, Models, instruction
from models.genai_model import scan_code
from utils.html_helpers import generate_index_html
from utils.extract_apk_helpers import extract_apk_with_jadx


def get_available_models():
    return ", ".join(api_keys.keys())


def process_file(file_path, code_content, model_key, model_variant, input_dir, output_dir):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     print(colored(f"[+] Scanning {file_path} with model {model_key}...", "cyan"))

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     result = scan_code(api_keys[model_key], model_variant, instruction, code_content)

    html_result = markdown.markdown(result)

    relative_path = os.path.relpath(file_path, input_dir)
    output_file_dir = os.path.join(output_dir, os.path.dirname(relative_path))

    os.makedirs(output_file_dir, exist_ok=True)

# [BATCHFIX] Commented metadata/non-Python
# #     markdown_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.md"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #     html_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.html"  # [BATCHFIX] closed string

    markdown_path = os.path.join(output_file_dir, markdown_filename)
    html_path = os.path.join(output_file_dir, html_filename)

    with open(markdown_path, "w", encoding="utf-8") as markdown_file:
        markdown_file.write(result)

    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_result)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     print(colored(f"[✓] Report saved to {markdown_path} and {html_path}", "green"))
    return file_path, markdown_path, html_path


def process_and_generate_reports(all_pathes, model_key, model_variant, input_dir, output_dir, num_threads):
    pass  # [BATCHFIX] inserted for empty block
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     files_to_process = []
    for path in all_pathes:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                files_to_process.append((path, f.read()))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         futures = []
        for file_path, code_content in files_to_process:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             futures.append(
                executor.submit(process_file, file_path, code_content, model_key, model_variant, input_dir, output_dir)
            )

        for future in as_completed(futures):
            future.result()

    generate_index_html(output_dir)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     print(colored(f"[✓] Index file created at {os.path.join(output_dir, 'index.html')}", "green"))


def main():
    parser = argparse.ArgumentParser(description="AI Code Scanner")
    parser.add_argument("--apk-path", required=True, help="Path to the APK file")
    parser.add_argument("--out-dir", required=True, help="Directory to save the decompiled files")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     parser.add_argument(
# [BATCHFIX] Commented metadata/non-Python
# #         "--target-package", required=True, help="Target package name to find classes (e.g., 'jakhar.aseem.diva')"  # [BATCHFIX] closed string
    )
    parser.add_argument("--model-name", required=True, help="Model key (e.g., GENEAI, OPENAI).")
    parser.add_argument("--report", required=True, help="Directory to save the reports.")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     parser.add_argument(
        "--threads",
        type=int,
        default=1,
        choices=range(1, 11),
        help="Number of threads to use for scanning files (default: 1, max: 10).",
    )

    args = parser.parse_args()

    input_dir = args.out_dir
    output_dir = args.report
    model_key = args.model_name.upper()
    num_threads = args.threads

    if model_key not in api_keys or model_key not in Models:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         print(colored(f"[!] Invalid model key: {model_key}", "red"))
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         print(colored(f"[!] Available model keys are: {get_available_models()}", "yellow"))
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     model_variant = list(Models[model_key].values())[0]

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     manifest_path, strings_path, target_classes = extract_apk_with_jadx(
        args.apk_path, args.out_dir, args.target_package
    )
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     all_pathes = []
    all_pathes.append(manifest_path)
    all_pathes.append(strings_path)
    for target_class in target_classes:
        all_pathes.append(target_class)
    process_and_generate_reports(all_pathes, model_key, model_variant, input_dir, output_dir, num_threads)


if __name__ == "__main__":
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
#     main()
