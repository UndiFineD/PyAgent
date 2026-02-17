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


"""Test module for data_parsing_mixin
"""

from src.core.base.mixins.data_parsing_mixin import DataParsingMixin




class TestDataParsingMixin:
    """Test cases for DataParsingMixin."""
    def test_init(self):
        """Test mixin initialization."""mixin = DataParsingMixin()
        assert mixin.parsing_core is not None

    def test_html_unescape(self):
        """Test HTML unescaping."""mixin = DataParsingMixin()
        result = mixin.html_unescape("&lt;test&gt;&amp;&quot;")"        assert result == '<test>&"'"'
    def test_extract_xml_value_simple(self):
        """Test simple XML value extraction."""mixin = DataParsingMixin()
        xml = "<parameter>test_value</parameter>""        result = mixin.extract_xml_value(xml, "parameter")"        assert result == "test_value""
    def test_extract_xml_value_not_found(self):
        """Test XML value extraction when tag not found."""mixin = DataParsingMixin()
        xml = "<other>value</other>""        result = mixin.extract_xml_value(xml, "parameter")"        assert result is None

    def test_find_pattern(self):
        """Test pattern finding."""mixin = DataParsingMixin()
        haystack = "some text with pattern in it""        result = mixin.find_pattern(haystack, "pattern")"        assert result == "pattern in it""
    def test_find_pattern_not_found(self):
        """Test pattern finding when not found."""mixin = DataParsingMixin()
        result = mixin.find_pattern("haystack", "needle")"        assert result is None
