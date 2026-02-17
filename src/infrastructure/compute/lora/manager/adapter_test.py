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

import pytest
from infrastructure.compute.lora.manager.adapter import LoRAAdapter, load_lora_adapter, get_lora_info


def test_loraadapter_basic():
    assert LoRAAdapter is not None


def test_load_lora_adapter_basic():
    assert callable(load_lora_adapter)


def test_get_lora_info_basic():
    assert callable(get_lora_info)
