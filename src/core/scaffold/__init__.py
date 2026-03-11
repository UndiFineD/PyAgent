#!/usr/bin/env python3
# module scaffold for creating new Core modules
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

"""Scaffold package for creating new Core modules.
Use this as a copy/paste starting point for new cores.
"""

from dataclasses import dataclass
from typing import Protocol


class CoreAPI(Protocol):
    """Protocol describing a simple Core API contract."""

    def validate(self) -> None: ...


@dataclass
class ExampleCore:
    """Example core implementation scaffold."""

    name: str = "example"

    def do_work(self, payload: dict[str, object]) -> dict[str, object]:
        """Perform core work; implementers must use typed inputs/outputs.

        Args:
            payload: input payload
        Returns:
            result dict

        """
        # minimal example
        return {"status": "ok", "input_keys": list(payload.keys())}


def validate() -> None:
    """Lightweight self-check for the core module.

    This function should be import-safe and avoid heavy runtime behaviour.
    """
    # Basic smoke checks
    assert isinstance(ExampleCore().do_work({}), dict)
