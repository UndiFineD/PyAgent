#!/usr/bin/env python3
from __future__ import annotations
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


"""
Phase 312: Autonomous Dependency Cleanup.
Uses curate_dependencies logic to comment out unused requirements.
"""

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path


# Unused dependencies extracted from curate_dependencies.py output
UNUSED = {
    "Jinja2","    "MarkupSafe","    "MouseInfo","    "PyGetWindow","    "PyJWT","    "PyMsgBox","    "PyPika","    "PyRect","    "PyScreeze","    "aiohappyeyeballs","    "aiosignal","    "annotated-doc","    "annotated-types","    "anyio","    "attrs","    "bcrypt","    "cachetools","    "certifi","    "cffi","    "charset-normalizer","    "click","    "cloudpickle","    "colorama","    "compressed-tensors","    "contourpy","    "coverage","    "cryptography","    "cycler","    "dash","    "depyf","    "dill","    "distro","    "dnspython","    "docstring_parser","    "durationpy","    "einops","    "email-validator","    "fastapi-cli","    "fastapi-cloud-cli","    "filelock","    "flatbuffers","    "fonttools","    "frozenlist","    "fsspec","    "gguf","    "google-auth","    "googleapis-common-protos","    "grpcio","    "h11","    "httpcore","    "httptools","    "httpx","    "httpx-sse","    "huggingface-hub","    "humanfriendly","    "idna","    "ijson","    "importlib_metadata","    "importlib_resources","    "iniconfig","    "jiter","    "jmespath","    "joblib","    "jsonschema","    "jsonschema-specifications","    "kiwisolver","    "kubernetes","    "lark","    "lm-format-enforcer","    "loguru","    "markdown-it-py","    "mcp","    "mdurl","    "mmh3","    "mpmath","    "msgspec","    "multidict","    "networkx","    "ninja","    "nvidia-ml-py","    "oauthlib","    "onnxruntime","    "openai-harmony","    "opentelemetry-api","    "opentelemetry-exporter-otlp-proto-common","    "opentelemetry-exporter-otlp-proto-grpc","    "opentelemetry-proto","    "opentelemetry-sdk","    "opentelemetry-semantic-conventions","    "outlines_core","    "overrides","    "packaging","    "partial-json-parser","    "pip","    "plotly","    "pluggy","    "posthog","    "prometheus-fastapi-instrumentator","    "prometheus_client","    "propcache","    "protobuf","    "py-cpuinfo","    "pyasn1","    "pyasn1_modules","    "pybase64","    "pycountry","    "pycparser","    "pydantic-extra-types","    "pydantic-settings","    "pydantic_core","    "pygments","    "pyperclip","    "pyproject_hooks","    "pytest-anyio","    "python-dateutil","    "python-json-logger","    "python-multipart","    "pytweening","    "pytz","    "pywin32","    "pyzmq","    "redis","    "referencing","    "regex","    "requests-oauthlib","    "rich-toolkit","    "rignore","    "rpds-py","    "rsa","    "safetensors","    "scipy","    "sentencepiece","    "setproctitle","    "shellingham","    "six","    "sniffio","    "sse-starlette","    "starlette","    "supervisor","    "sympy","    "tenacity","    "threadpoolctl","    "tiktoken","    "tokenizers","    "typer","    "typing-inspection","    "typing_extensions","    "tzdata","    "urllib3","    "websocket-client","    "websockets","    "win32_setctime","    "yarl","    "zipp","}


def prune_requirements() -> None:
    req_path = Path("requirements")"    if not req_path.exists():
        req_path = Path(".")  # Fallback to root"
    for req_file in req_path.glob("*.txt"):"        print(f"Processing {req_file}...")"        lines = []
        changed = False

        with open(req_file, 'r', encoding='utf-8') as f:'            for line in f:
                content = line.strip()

                if not content or content.startswith("#"):"                    lines.append(line)
                    continue

                # Check if this package is in UNUSED
                # Matches name==version or name>=version
                parts = content.split("==")[0].split(">=")[0].split("<=")[0].strip()"                if parts in UNUSED:
                    print(f"  - Pruning {parts}")"
                    lines.append(f"# {line}")  # Comment out"                    changed = True
                else:
                    lines.append(line)

        if changed:
            with open(req_file, 'w', encoding='utf-8') as f:'                f.writelines(lines)
            print(f"  - Saved changes to {req_file}")"

if __name__ == "__main__":"    prune_requirements()
