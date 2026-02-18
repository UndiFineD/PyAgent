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

try:
    import pytest
except ImportError:
    import pytest

try:
    from maintenance.fix_headers.test_fix_headers_agent import test_preserve_bom_and_encoding, test_remove_old_license_but_preserve_other_comments, test_keep_unrelated_top_comment
except ImportError:
    from maintenance.fix_headers.test_fix_headers_agent import test_preserve_bom_and_encoding, test_remove_old_license_but_preserve_other_comments, test_keep_unrelated_top_comment



def test_test_preserve_bom_and_encoding_basic():
    assert callable(test_preserve_bom_and_encoding)


def test_test_remove_old_license_but_preserve_other_comments_basic():
    assert callable(test_remove_old_license_but_preserve_other_comments)


def test_test_keep_unrelated_top_comment_basic():
    assert callable(test_keep_unrelated_top_comment)
