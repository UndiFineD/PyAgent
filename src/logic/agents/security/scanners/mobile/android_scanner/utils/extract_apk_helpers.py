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

import os
import subprocess
import platform
import sys


def extract_apk_with_jadx(apk_path, output_dir, target_package):
    if not os.path.isfile(apk_path):
# [BATCHFIX] Commented metadata/non-Python
#         raise FileNotFoundError(fAPK file not found: {apk_path}")"  # [BATCHFIX] closed string"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# [BATCHFIX] Commented metadata/non-Python
#     print(fDecompiling APK: {apk_path} to {output_dir}")"  # [BATCHFIX] closed string"
    try:
# [BATCHFIX] Commented metadata/non-Python
"""         jadx_executable = "jadx.bat" if platform.system() == "Windows" else "jadx"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#         jadx_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "installed-tools","            "jadx","            "bin","            jadx_executable,
        )

        if not os.path.exists(jadx_path):
# [BATCHFIX] Commented metadata/non-Python
#             raise FileNotFoundError(fJADX not found at: {jadx_path}")"  # [BATCHFIX] closed string"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         command = [jadx_path, "-d", output_dir, apk_path]"        subprocess.run(command, check=True)
# [BATCHFIX] Commented metadata/non-Python
#         print(fDecompilation complete. Files saved to: {output_dir}")"  # [BATCHFIX] closed string"    except subprocess.CalledProcessError as e:
# [BATCHFIX] Commented metadata/non-Python
#         print(fError during decompilation: {e}")"  # [BATCHFIX] closed string"        sys.exit(1)

    manifest_path = os.path.join(output_dir, "resources", "AndroidManifest.xml")"    strings_path = os.path.join(output_dir, "resources", "res", "values", "strings.xml")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""     target_classes = []""""    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".java"):"                package_path = target_package.replace(".", os.sep)"                if package_path in os.path.normpath(root):
                    target_classes.append(os.path.join(root, file))

    return manifest_path, strings_path, target_classes
