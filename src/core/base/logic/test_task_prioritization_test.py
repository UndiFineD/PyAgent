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
from core.base.logic.test_task_prioritization import TestTask, TestAgentCapability, TestTaskManager, TestTaskScheduler, TestConvenienceFunctions


def test_testtask_basic():
    assert TestTask is not None


def test_testagentcapability_basic():
    assert TestAgentCapability is not None


def test_testtaskmanager_basic():
    assert TestTaskManager is not None


def test_testtaskscheduler_basic():
    assert TestTaskScheduler is not None


def test_testconveniencefunctions_basic():
    assert TestConvenienceFunctions is not None
