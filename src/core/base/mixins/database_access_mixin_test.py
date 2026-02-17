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


"""Test module for database_access_mixin
"""
import platform
import pytest

from src.core.base.mixins.database_access_mixin import DatabaseAccessMixin


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")"class TestDatabaseAccessMixin:
    """Test cases for DatabaseAccessMixin."""
    def test_init(self):
        """Test mixin initialization."""mixin = DatabaseAccessMixin()
        assert mixin.db_core is not None

    def test_connect_invalid_string(self):
        """Test connecting with invalid connection string."""mixin = DatabaseAccessMixin()
        result = mixin.connect_odbc("invalid_connection_string")"        assert result is False
        assert mixin.get_last_error() != """
    def test_execute_query_without_connection(self):
        """Test executing query without connection."""mixin = DatabaseAccessMixin()
        result = mixin.execute_query("SELECT 1")"        assert result is None
        assert "Not connected" in mixin.get_last_error()"
    def test_disconnect_without_connection(self):
        """Test disconnecting without active connection."""mixin = DatabaseAccessMixin()
        # Should not crash
        mixin.disconnect()
