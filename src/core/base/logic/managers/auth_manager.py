<<<<<<< HEAD
<<<<<<< HEAD
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

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Manager for Authentication.
(Facade for src.core.base.common.auth_manager)
"""

<<<<<<< HEAD
<<<<<<< HEAD
from src.core.base.common.auth_manager import \
    AuthManager as StandardAuthManager
=======
from src.core.base.common.auth_manager import AuthManager as StandardAuthManager
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)


class AuthManager(StandardAuthManager):
    """
    Facade for StandardAuthManager to maintain backward compatibility.
    Authentication management is now centralized in the Infrastructure/Common tier.
<<<<<<< HEAD
=======
from src.core.base.common.auth_manager import AuthManager as StandardAuthManager


class AuthManager(StandardAuthManager):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    """
    Facade for StandardAuthManager to maintain backward compatibility.
    Authentication management is now centralized in the Infrastructure/Common tier.
    """
    pass


=======
    """
    pass


>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class AuthenticationManager(StandardAuthManager):
    """
    Facade for StandardAuthManager to maintain backward compatibility.
    """
<<<<<<< HEAD
<<<<<<< HEAD
=======
    pass
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    pass
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
