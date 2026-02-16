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
from core.testing.framework import ScenarioResult, TestType, TestStatus, TestResult, TestScenario, TestSuite, AgentTestingPyramidCore, ScenarioTestingEngine, PromptVersioningSystem, EvaluationNotebookSystem, assert_equal, run_scenario


def test_scenarioresult_basic():
    assert ScenarioResult is not None


def test_testtype_basic():
    assert TestType is not None


def test_teststatus_basic():
    assert TestStatus is not None


def test_testresult_basic():
    assert TestResult is not None


def test_testscenario_basic():
    assert TestScenario is not None


def test_testsuite_basic():
    assert TestSuite is not None


def test_agenttestingpyramidcore_basic():
    assert AgentTestingPyramidCore is not None


def test_scenariotestingengine_basic():
    assert ScenarioTestingEngine is not None


def test_promptversioningsystem_basic():
    assert PromptVersioningSystem is not None


def test_evaluationnotebooksystem_basic():
    assert EvaluationNotebookSystem is not None


def test_assert_equal_basic():
    assert callable(assert_equal)


def test_run_scenario_basic():
    assert callable(run_scenario)
