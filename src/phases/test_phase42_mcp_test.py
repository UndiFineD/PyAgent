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
from .test_phase42_mcp import TestMCPServerType, TestSessionState, TestToolStatus, TestToolSchema, TestToolCall, TestToolResult, TestMCPSession, TestMCPServerConfig, TestSchemaAdapter, TestSessionManager, TestMCPServerRegistry, TestLocalMCPServer, TestSSEMCPServer, TestMCPToolServer, TestConvenienceFunctions


def test_testmcpservertype_basic():
    assert TestMCPServerType is not None


def test_testsessionstate_basic():
    assert TestSessionState is not None


def test_testtoolstatus_basic():
    assert TestToolStatus is not None


def test_testtoolschema_basic():
    assert TestToolSchema is not None


def test_testtoolcall_basic():
    assert TestToolCall is not None


def test_testtoolresult_basic():
    assert TestToolResult is not None


def test_testmcpsession_basic():
    assert TestMCPSession is not None


def test_testmcpserverconfig_basic():
    assert TestMCPServerConfig is not None


def test_testschemaadapter_basic():
    assert TestSchemaAdapter is not None


def test_testsessionmanager_basic():
    assert TestSessionManager is not None


def test_testmcpserverregistry_basic():
    assert TestMCPServerRegistry is not None


def test_testlocalmcpserver_basic():
    assert TestLocalMCPServer is not None


def test_testssemcpserver_basic():
    assert TestSSEMCPServer is not None


def test_testmcptoolserver_basic():
    assert TestMCPToolServer is not None


def test_testconveniencefunctions_basic():
    assert TestConvenienceFunctions is not None
