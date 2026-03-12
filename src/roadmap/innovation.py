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

import json
from pathlib import Path
from typing import Any


def record_experiment(name: str, db_path: str = "experiments.json") -> Path:
    """Record an experiment name in a JSON file, creating it if it doesn't exist.

    Args:
        name: The name of the experiment to record.
        db_path: The path to the experiments JSON file to create or update.

    Returns:
        Path: The path to the updated experiments JSON file.
    """
    db: list[Any] = []
    p: Path = Path(db_path)
    if p.exists():
        db = json.loads(p.read_text())
    db.append({"name": name})
    p.write_text(json.dumps(db))
    return p
