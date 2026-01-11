import unittest
from src.classes.fleet.FleetManager import FleetManager

class TestPhase51(unittest.TestCase):
    def setUp(self):
        self.fleet = FleetManager("c:/DEV/PyAgent")

    def test_tenant_isolation(self) -> None:
        print("\nTesting Phase 51: Multi-Tenant Fleet Isolation & Privacy...")
        tenant_a = "Client_A"
        tenant_b = "Client_B"
        
        # Resource limits
        self.fleet.tenant_isolation.set_resource_limits(tenant_a, 10000, 5)
        self.assertIn(tenant_a, self.fleet.tenant_isolation.resource_limits)
        
        # ZK-Knowledge Sharding
        shard_id = self.fleet.tenant_isolation.encrypt_knowledge_shard(tenant_a, "Top secret project alpha")
        print(f"Encrypted Shard ID: {shard_id}")
        self.assertIsNotNone(shard_id)
        
        # Access validation
        self.assertTrue(self.fleet.tenant_isolation.validate_access(tenant_a, "Client_A_Resource_01"))
        self.assertFalse(self.fleet.tenant_isolation.validate_access(tenant_a, "Client_B_Resource_01"))
        
        # ZK-Fusion
        shard_id_2 = self.fleet.tenant_isolation.encrypt_knowledge_shard(tenant_b, "Project beta highlights")
        fusion_res = self.fleet.tenant_isolation.fuse_knowledge_zk([shard_id, shard_id_2])
        print(f"Fused Insights: {fusion_res}")
        self.assertIn("Insight from", fusion_res)

if __name__ == "__main__":
    unittest.main()
