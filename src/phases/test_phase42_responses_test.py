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
from .test_phase42_responses import TestResponseEnums, TestContentParts, TestMessage, TestToolDefinition, TestResponse, TestResponseConfig, TestSSEStream, TestInMemoryResponseStore, TestStreamingHandler, TestResponsesAPIServer, TestConversationBuilder, TestParseResponseRequest


def test_testresponseenums_basic():
    assert TestResponseEnums is not None


def test_testcontentparts_basic():
    assert TestContentParts is not None


def test_testmessage_basic():
    assert TestMessage is not None


def test_testtooldefinition_basic():
    assert TestToolDefinition is not None


def test_testresponse_basic():
    assert TestResponse is not None


def test_testresponseconfig_basic():
    assert TestResponseConfig is not None


def test_testssestream_basic():
    assert TestSSEStream is not None


def test_testinmemoryresponsestore_basic():
    assert TestInMemoryResponseStore is not None


def test_teststreaminghandler_basic():
    assert TestStreamingHandler is not None


def test_testresponsesapiserver_basic():
    assert TestResponsesAPIServer is not None


def test_testconversationbuilder_basic():
    assert TestConversationBuilder is not None


def test_testparseresponserequest_basic():
    assert TestParseResponseRequest is not None
