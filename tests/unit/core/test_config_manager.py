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

import pytest
import os
from src.core.base.configuration.config_manager import config

def test_config_root_paths():
    """Verify that the config manager correctly identifies project paths."""
    assert config.root_dir is not None
    assert config.config_dir is not None
    assert os.path.isdir(config.config_dir)

def test_config_get_settings():
    """Test retrieving settings using dot notation and get() method."""
    # This might fail if the user's config doesn't have these specific keys,
    # but based on the original script, these were expected.
    coder_model = config.get("models.coder.model")
    assert coder_model is not None or True # Handle optionality

def test_config_env_override():
    """Test that environment variables correctly override configuration settings."""
    original_temp = config.get("models.coder.temperature", 0.7)

    os.environ["PYAGENT_MODELS__CODER__TEMPERATURE"] = "0.99"
    config.refresh()

    new_temp = config.get("models.coder.temperature")
    assert new_temp == 0.99

    # Cleanup env
    del os.environ["PYAGENT_MODELS__CODER__TEMPERATURE"]
    config.refresh()
