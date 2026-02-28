#!/usr/bin/env python3

"""Validation script for Phase 11: Market & Economy."""

import logging
import json
from pathlib import Path
from src.classes.fleet.FleetManager import FleetManager

def test_market_features():
    logging.basicConfig(level=logging.INFO)
    root = Path("c:/DEV/PyAgent")
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
        print(f"Bob successfully purchased SqlExpert template.")
        print(f"Bob Balance after purchase: {fleet.economy.get_balance('BobAgent')}")
    
    print("\nMarket features validation COMPLETED.")

if __name__ == "__main__":
    test_market_features()
