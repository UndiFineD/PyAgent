import unittest
import os
import json
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhases59_61(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_legal_and_smart_contract_audit(self) -> None:
        print("\nTesting Phase 59: Legal & Smart Contract Auditing...")
        # Licensing scan
        content = "This project uses the GPL v3 license."
        lic_res = self.fleet.legal_audit.scan_licensing(content)
        print(f"Licensing Result: {lic_res}")
        self.assertEqual(lic_res["risk_level"], "high")
        
        # Smart Contract verify
        contract = """
        function withdraw() public {
            (bool success, ) = msg.sender.call{value: 1 ether}("");
            require(success);
        }
        """
        audit_res = self.fleet.legal_audit.verify_smart_contract(contract)
        print(f"Audit Result: {audit_res}")
        self.assertEqual(audit_res["status"], "fail")
        self.assertIn("Reentrancy", audit_res["vulnerabilities"][0])
        
        # Liability
        report = self.fleet.legal_audit.generate_liability_report("I guarantee this code is 100% safe.")
        print(f"Liability Report: {report}")
        self.assertIn("WARNING", report)

    def test_quantum_resistant_crypto(self) -> None:
        print("\nTesting Phase 60: Quantum-Resistant Cryptographic Layer...")
        fleet_b = "RemoteFleet_Alpha"
        
        # PQC Keygen
        pub_key = self.fleet.entropy_guard.generate_pqc_keypair(fleet_b)
        print(f"PQC Public Key (simulated): {pub_key}")
        self.assertEqual(len(pub_key), 128) # SHA3-512 hex length
        
        # Encryption
        msg = "Top secret quantum message"
        encrypted = self.fleet.entropy_guard.simulate_quantum_safe_encrypt(msg, fleet_b)
        print(f"Encrypted Data: {encrypted.hex()}")
        self.assertNotEqual(msg, encrypted.decode(errors='ignore'))
        
        # Entropy rotation
        old_pool = self.fleet.entropy_guard.entropy_pool
        self.fleet.entropy_guard.rotate_entropy_pool()
        self.assertNotEqual(old_pool, self.fleet.entropy_guard.entropy_pool)

    def test_empathy_and_sentiment(self) -> None:
        print("\nTesting Phase 61: Emotional Intelligence...")
        
        # Sentiment
        analysis = self.fleet.empathy_engine.analyze_user_sentiment("This is wrong, fix it now!")
        print(f"Sentiment Analysis: {analysis}")
        self.assertEqual(analysis["sentiment"], "frustrated")
        self.assertEqual(analysis["linguistic_adjustment"], "concise_and_apologetic")
        
        # Conflict Mediation
        mediation = self.fleet.empathy_engine.mediate_conflict("CoderAgent", "I don't like this refactoring.")
        print(f"Mediation: {mediation}")
        self.assertIn("understand", mediation)

if __name__ == "__main__":
    unittest.main()
