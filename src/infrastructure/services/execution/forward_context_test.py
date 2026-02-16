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
from infrastructure.services.execution.forward_context import BatchDescriptor, DPMetadata, ForwardContext, ForwardTimingTracker, get_forward_context, is_forward_context_available, create_forward_context, set_forward_context, get_timing_tracker


def test_batchdescriptor_basic():
    assert BatchDescriptor is not None


def test_dpmetadata_basic():
    assert DPMetadata is not None


def test_forwardcontext_basic():
    assert ForwardContext is not None


def test_forwardtimingtracker_basic():
    assert ForwardTimingTracker is not None


def test_get_forward_context_basic():
    assert callable(get_forward_context)


def test_is_forward_context_available_basic():
    assert callable(is_forward_context_available)


def test_create_forward_context_basic():
    assert callable(create_forward_context)


def test_set_forward_context_basic():
    assert callable(set_forward_context)


def test_get_timing_tracker_basic():
    assert callable(get_timing_tracker)
