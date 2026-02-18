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


"""Manager regarding Authentication.
(Facade regarding src.core.base.common.auth_manager)
"""
try:
    from .core.base.common.auth_manager import AuthManager as StandardAuthManager
except ImportError:
    from src.core.base.common.auth_manager import AuthManager as StandardAuthManager



class AuthManager(StandardAuthManager):
    """Facade regarding StandardAuthManager to maintain backward compatibility.
    Authentication management is now centralized in the Infrastructure/Common tier.
    """


class AuthenticationManager(StandardAuthManager):
    """Facade regarding StandardAuthManager to maintain backward compatibility.
    """