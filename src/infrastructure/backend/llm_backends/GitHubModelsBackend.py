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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import os
from pathlib import Path
from .LLMBackend import LLMBackend

__version__ = VERSION


class GitHubModelsBackend(LLMBackend):
    """GitHub Models LLM Backend."""

    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs,
    ) -> str:
        if not self._is_working("github_models"):
            logging.debug("GitHub Models skipped due to connection cache.")
            return ""

        token = kwargs.get("token") or os.environ.get("GITHUB_TOKEN")
        logging.debug(f"DEBUG: token from kwargs/env: {token is not None}")
        if not token:
            search_paths = [os.environ.get("DV_GITHUB_TOKEN_FILE"), "github-token.txt"]
            for path_str in search_paths:
                if not path_str:
                    continue
                path = Path(path_str)
                if path.exists():
                    try:
                        token = path.read_text(encoding="utf-8").strip()
                        if token:
                            logging.debug(f"DEBUG: token found in file: {path}")
                            break
                    except Exception:
                        continue

        # Phase 120: Fallback to GitHub CLI token if possible
        if not token:
            try:
                import subprocess

                res = subprocess.run(
                    ["gh", "auth", "token"], capture_output=True, text=True, check=False
                )
                if res.returncode == 0:
                    token = res.stdout.strip()
                    if token:
                        logging.debug(
                            "GitHub Models: Using token from 'gh auth token'."
                        )
            except Exception:
                pass

        if not token:
            logging.warning("GitHub Models: Missing token. Skipping.")
            return (
                ""  # Return empty instead of raising to allow fallback logic to proceed
            )

        logging.debug(f"DEBUG: using token: {token[:3]}...")

        base_url = (
            kwargs.get("base_url")
            or os.environ.get("GITHUB_MODELS_BASE_URL")
            or "https://models.inference.ai.azure.com"
        ).strip()
        url = base_url.rstrip("/") + "/v1/chat/completions"

        # Multi-modal support logic
        import re

        image_match = re.search(r"\[IMAGE_DATA:(.*?)\]", prompt, re.DOTALL)
        if image_match:
            b64_data = image_match.group(1).strip()
            clean_prompt = prompt.replace(image_match.group(0), "").strip()
            user_content = [
                {"type": "text", "text": clean_prompt or "Describe this image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"},
                },
            ]
        else:
            user_content = prompt

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "stream": kwargs.get("stream", False),
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        max_retries = kwargs.get("max_retries", 2)
        timeout_s = kwargs.get("timeout_s", 60)
        import json

        for attempt in range(max_retries + 1):
            try:
                # Use current token (might have been updated in previous attempt)
                headers["Authorization"] = f"Bearer {token}"

                response = self.session.post(
                    url, headers=headers, data=json.dumps(payload), timeout=timeout_s
                )

                if response.status_code == 401:
                    logging.warning(
                        f"GitHub Models: Unauthorized (401) on attempt {attempt + 1}. Refreshing token..."
                    )
                    try:
                        import subprocess

                        # Phase 149: Hardened self-healing. Try to refresh via GH CLI.
                        res = subprocess.run(
                            ["gh", "auth", "token"],
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        new_token = res.stdout.strip() if res.returncode == 0 else ""

                        if new_token and new_token != token:
                            logging.info(
                                "GitHub Models: New token obtained via GitHub CLI. Retrying..."
                            )
                            token = new_token
                            # Sticky token for session (Phase 141)
                            os.environ["GITHUB_TOKEN"] = token
                            headers["Authorization"] = f"Bearer {token}"
                            # Retry immediately with new token
                            response = self.session.post(
                                url,
                                headers=headers,
                                data=json.dumps(payload),
                                timeout=timeout_s,
                            )
                        elif res.returncode != 0:
                            logging.error(
                                "GitHub Models: 'gh auth token' failed. Manual 'gh auth login' may be required."
                            )
                        else:
                            logging.warning(
                                "GitHub Models: Token refresh returned identical token. Authorization likely revoked."
                            )
                    except Exception as e:
                        logging.debug(f"GitHub Models token refresh error: {e}")

                if response.status_code == 401:
                    logging.warning(
                        "GitHub Models: Unauthorized even after token refresh."
                    )
                    self._update_status("github_models", False)
                    return ""

                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                self._record(
                    "github_models", model, prompt, content, system_prompt=system_prompt
                )
                self._update_status("github_models", True)
                return content
            except Exception as e:
                if attempt < max_retries:
                    import threading

                    threading.Event().wait(timeout=min(2**attempt, 10))
                else:
                    # Lowered logging level for fallback-friendly behavior (Phase 123)
                    logging.debug(
                        f"GitHub Models call failed after {max_retries} retries: {e}"
                    )
                    self._update_status("github_models", False)
                    self._record(
                        "github_models",
                        model,
                        prompt,
                        f"ERROR: {str(e)}",
                        system_prompt=system_prompt,
                    )
        return ""
