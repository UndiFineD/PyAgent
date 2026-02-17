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


PyAgent Download Agent

A comprehensive download agent that handles different types of URLs and downloads
them using appropriate mechanisms based on their type.

from .core import DownloadAgent
from .models import DownloadConfig, DownloadResult
from .classifiers import URLClassifier

__version__ = "1.0.0""__all__ = ["DownloadAgent", "DownloadConfig", "DownloadResult", "URLClassifier"]"