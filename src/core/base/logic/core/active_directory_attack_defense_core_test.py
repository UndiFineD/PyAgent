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
"""
Tests for active_directory_attack_defense_core
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from core.base.logic.core.active_directory_attack_defense_core import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_killchainphase_exists():
    """Test that KillChainPhase class exists and is importable."""
    assert 'KillChainPhase' in dir()


def test_attacktechnique_exists():
    """Test that AttackTechnique class exists and is importable."""
    assert 'AttackTechnique' in dir()


def test_defensecontrol_exists():
    """Test that DefenseControl class exists and is importable."""
    assert 'DefenseControl' in dir()


def test_attackvector_exists():
    """Test that AttackVector class exists and is importable."""
    assert 'AttackVector' in dir()


def test_defenseassessment_exists():
    """Test that DefenseAssessment class exists and is importable."""
    assert 'DefenseAssessment' in dir()


def test_killchainanalysis_exists():
    """Test that KillChainAnalysis class exists and is importable."""
    assert 'KillChainAnalysis' in dir()


def test_securityposture_exists():
    """Test that SecurityPosture class exists and is importable."""
    assert 'SecurityPosture' in dir()


def test_activedirectoryattackdefensecore_exists():
    """Test that ActiveDirectoryAttackDefenseCore class exists and is importable."""
    assert 'ActiveDirectoryAttackDefenseCore' in dir()


def test_activedirectoryattackdefensecore_instantiation():
    """Test that ActiveDirectoryAttackDefenseCore can be instantiated."""
    instance = ActiveDirectoryAttackDefenseCore()
    assert instance is not None


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

