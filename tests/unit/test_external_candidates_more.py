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

from src.external_candidates.h2o_exceptions import LLMDataException
from src.external_candidates.voicecraft_utils import get_span
from src.external_candidates.webnavigator_utils import read_markdown_file
from src.external_candidates.homoglyph import CharacterManager
from src.external_candidates.made_with_ml import validate_dataset


def test_h2o_exception_exists():
    assert issubclass(LLMDataException, Exception)


def test_get_span_substitution():
    orig = "the quick brown fox"
    new = "the quick red fox"
    orig_span, new_span = get_span(orig, new, "substitution")
    assert orig_span and new_span


def test_read_markdown(tmp_path):
    p = tmp_path / "t.md"
    p.write_text("# hello\nworld")
    content = read_markdown_file(str(p))
    assert "hello" in content


def test_character_manager():
    cm = CharacterManager()
    cm.add_pair('a', 'а')  # Latin a vs Cyrillic a
    s = cm.get_set_for_char('a')
    assert s is not None


def test_made_with_ml_placeholder():
    class DummyDF:
        columns = ['id', 'created_on', 'title', 'description', 'tag']

    assert validate_dataset(DummyDF()) is True
