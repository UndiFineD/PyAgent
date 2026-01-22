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

"""
Core logic for object serialization and format conversion.
"""

from __future__ import annotations
<<<<<<< HEAD

import base64
import json
import pickle
from typing import Any

from .base_core import BaseCore


=======
import json
import pickle
import base64
from typing import Any
from .base_core import BaseCore

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class SerializationCore(BaseCore):
    """
    Authoritative engine for object serialization.
    Supports JSON, Pickle, and Base64 encoding.
    """
<<<<<<< HEAD

    def to_json(self, data: Any) -> str:
        """Convert object to JSON string."""
        return json.dumps(data, default=str)

    def from_json(self, data: str) -> Any:
        """Parse JSON string to object."""
        return json.loads(data)

    def to_base64_pickle(self, obj: Any) -> str:
        """Pickle object and encode as Base64 string."""
        pickled = pickle.dumps(obj)
        return base64.b64encode(pickled).decode("utf-8")

    def from_base64_pickle(self, data: str) -> Any:
        """Decode Base64 string and unpickle to object."""
        decoded = base64.b64decode(data.encode("utf-8"))
=======
    def to_json(self, data: Any) -> str:
        return json.dumps(data, default=str)

    def from_json(self, data: str) -> Any:
        return json.loads(data)

    def to_base64_pickle(self, obj: Any) -> str:
        pickled = pickle.dumps(obj)
        return base64.b64encode(pickled).decode('utf-8')

    def from_base64_pickle(self, data: str) -> Any:
        decoded = base64.b64decode(data.encode('utf-8'))
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return pickle.loads(decoded)
