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


"""Tests for DataProcessingMixin."""
import datetime
import json
import unittest

from src.core.base.mixins.data_processing_mixin import DataProcessingMixin


class TestDataProcessingMixin(unittest.TestCase):
    """Test cases for DataProcessingMixin."""
    def setUp(self):
        """Set up test fixtures."""self.mixin = DataProcessingMixin()

    def test_convert_user_account_control(self):
        """Test UAC flag conversion."""# Test normal account
        result = self.mixin.convert_user_account_control(0x200)  # NORMAL_ACCOUNT
        self.assertIn("NORMAL_ACCOUNT", result)"
        # Test multiple flags
        result = self.mixin.convert_user_account_control(0x202)  # NORMAL_ACCOUNT | ACCOUNTDISABLE
        self.assertIn("NORMAL_ACCOUNT", result)"        self.assertIn("ACCOUNTDISABLE", result)"
        # Test no flags
        result = self.mixin.convert_user_account_control(0)
        self.assertEqual(result, "NONE")"
    def test_convert_filetime_to_datetime(self):
        """Test FILETIME to datetime conversion."""# Windows FILETIME for 1970-01-01 00:00:00 UTC
        filetime_1970 = 116444736000000000  # Roughly
        result = self.mixin.convert_filetime_to_datetime(filetime_1970)

        # Should be around 1970
        expected = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        # Allow some tolerance due to rounding
        self.assertTrue(abs((result - expected).total_seconds()) < 10)

    def test_convert_account_expires_never(self):
        """Test account expires conversion for never expires."""result = self.mixin.convert_account_expires(0)
        self.assertEqual(result, "Never Expires")"
        result = self.mixin.convert_account_expires(str(2**63 - 1))  # Max int64
        self.assertEqual(result, "Never Expires")"
    def test_process_change_record_uac(self):
        """Test processing UAC change record."""record = {
            'attribute_name': 'userAccountControl','            'attribute_value': '512'  # NORMAL_ACCOUNT'        }
        result = self.mixin.process_change_record(record)

        self.assertIn('explanation', result)'        self.assertIn('NORMAL_ACCOUNT', result['explanation'])'
    def test_process_change_record_member(self):
        """Test processing member change record."""# Added to group (odd version)
        record = {
            'attribute_name': 'member','            'version': 1'        }
        result = self.mixin.process_change_record(record)
        self.assertEqual(result['explanation'], "Added to group")"'
        # Removed from group (even version)
        record['version'] = 2'        result = self.mixin.process_change_record(record)
        self.assertEqual(result['explanation'], "Removed from group")"'
    def test_format_change_output_table(self):
        """Test table output formatting."""changes = [
            {
                'object': 'CN=TestUser','                'attribute_name': 'userAccountControl','                'attribute_value': '512','                'last_orig_change_time': '2023-01-01 12:00:00','                'explanation': 'NORMAL_ACCOUNT''            }
        ]

        result = self.mixin.format_change_output(changes, 'table')'        self.assertIn('Object', result)'        self.assertIn('Attribute', result)'        self.assertIn('NORMAL_ACCOUNT', result)'
    def test_format_change_output_json(self):
        """Test JSON output formatting."""changes = [
            {
                'object': 'CN=TestUser','                'attribute_name': 'userAccountControl','                'attribute_value': '512''            }
        ]

        result = self.mixin.format_change_output(changes, 'json')'        # Should be valid JSON
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['object'], 'CN=TestUser')'