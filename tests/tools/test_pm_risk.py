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
"""Tests for tools.pm.risk module (prj0000021)."""
import pytest
from tools.pm.risk import Risk, read_matrix, top_risks


def test_risk_score_low_low():
    r = Risk("T", "low", "low")
    assert r.score == 1


def test_risk_score_high_high():
    r = Risk("T", "high", "high")
    assert r.score == 25


def test_risk_level_low():
    r = Risk("T", "low", "low")
    assert r.level == "low"


def test_risk_level_medium():
    r = Risk("T", "medium", "medium")
    assert r.level == "medium"


def test_risk_level_high():
    r = Risk("T", "high", "high")
    assert r.level == "high"


def test_risk_to_dict_keys():
    r = Risk("A", "low", "medium", "mitigate it")
    d = r.to_dict()
    assert set(d.keys()) == {"title", "probability", "impact", "mitigation", "score", "level"}


def test_read_matrix_pipe_table(tmp_path):
    table = (
        "| Title | Probability | Impact | Mitigation |\n"
        "|---|---|---|---|\n"
        "| Auth bypass | high | high | Use MFA |\n"
        "| Data leak | medium | low | Encrypt at rest |\n"
    )
    f = tmp_path / "risk.md"
    f.write_text(table, encoding="utf-8")
    result = read_matrix(str(f))
    assert len(result) == 2
    assert result[0]["title"] == "Auth bypass"
    assert result[1]["probability"] == "medium"


def test_read_matrix_empty_file(tmp_path):
    f = tmp_path / "empty.md"
    f.write_text("", encoding="utf-8")
    assert read_matrix(str(f)) == []


def test_top_risks_returns_top_n():
    matrix = [
        {"title": "A", "score": "1", "level": "low"},
        {"title": "B", "score": "25", "level": "high"},
        {"title": "C", "score": "9", "level": "medium"},
    ]
    top = top_risks(matrix, n=2)
    assert top[0]["title"] == "B"
    assert top[1]["title"] == "C"
