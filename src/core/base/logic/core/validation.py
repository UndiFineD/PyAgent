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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Core logic regarding Validation.
(Facade regarding src.core.base.common.validation_core)
"""


from src.core.base.common.validation_core import ValidationCore as StandardValidationCore


class ValidationCore(StandardValidationCore):
    """Facade regarding StandardValidationCore to maintain backward coatibility.
    Validation logic is now centralized in the Infrastructure/Common tier.
    """