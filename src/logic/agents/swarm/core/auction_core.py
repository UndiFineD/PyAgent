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

"""
Auction core.py module.
"""

# Facade for AuctionCore
from src.core.base.common.auction_core import \
    AuctionCore as StandardAuctionCore


class AuctionCore(StandardAuctionCore):
    """Facade for AuctionCore to maintain backward compatibility."""

    pass
=======
# Facade for AuctionCore
from src.core.base.common.auction_core import AuctionCore as StandardAuctionCore

class AuctionCore(StandardAuctionCore):
    """Facade for AuctionCore to maintain backward compatibility."""
    pass

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
