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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Validation script for Phase 11: Market & Economy."""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager

__version__ = VERSION







def test_market_features() -> None:
    """Validate agent economy and blockchain features."""
    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[5]) + "")
    fleet = FleetManager(str(root))

    print("--- Phase 11: Agent Economy ---")
    alice_bal = fleet.economy.get_balance("AliceAgent")
    print(f"Alice Starting Balance: {alice_bal}")






    success = fleet.economy.transfer_credits("AliceAgent", "BobAgent", 50.0, "Subcontracting research")
    print(f"Transfer Alice -> Bob (50.0): {'Success' if success else 'Failed'}")
    print(f"Alice New Balance: {fleet.economy.get_balance('AliceAgent')}")



    print(f"Bob New Balance: {fleet.economy.get_balance('BobAgent')}")

    print("\n--- Phase 11: Blockchain Audit ---")
    print(f"Blockchain height: {len(fleet.economy.blockchain)}")





    last_block = fleet.economy.blockchain[-1]
    print(f"Last Block Hash: {last_block['hash']}")
    print(f"Block Transaction: {last_block['transactions'][0]['reason']}")

    print("\n--- Phase 11: Agent Store ---")

    templates = fleet.store.list_templates()
    print(f"Store Templates: {list(templates.keys())}")

    purchased = fleet.store.purchase_template("BobAgent", "SqlExpert", fleet.economy)
    if purchased:




        print("Bob successfully purchased SqlExpert template.")
        print(f"Bob Balance after purchase: {fleet.economy.get_balance('BobAgent')}")

    print("\nMarket features validation COMPLETED.")





if __name__ == "__main__":
    test_market_features()
