import unittest
import os
import json
from src.infrastructure.fleet.FleetManager import FleetManager

class TestPhases56_58(unittest.TestCase):
    def setUp(self):
        self.workspace = "c:/DEV/PyAgent"
        self.fleet = FleetManager(self.workspace)

    def test_cloud_infrastructure(self) -> None:
        print("\nTesting Phase 56: Multi-Cloud Infrastructure (IaC)...")
        # Configure AWS
        res = self.fleet.cloud_provider.configure_provider("aws", {"api_key": "mock_key"})
        print(res)
        self.assertIn("aws", self.fleet.cloud_provider.credentials)
        
        # Generate Terraform
        template = self.fleet.cloud_provider.generate_terraform_template("aws", 3, "us-west-2")
        print(f"Terraform Template:\n{template}")
        self.assertIn('region = "us-west-2"', template)
        self.assertIn('count         = 3', template)
        
        # Optimal region
        region = self.fleet.cloud_provider.select_optimal_region({"us-east-1": 150, "eu-west-1": 80, "ap-southeast-1": 250})
        print(f"Optimal Region: {region}")
        self.assertEqual(region, "eu-west-1")

    def test_data_compliance(self) -> None:
        print("\nTesting Phase 57: Data Privacy & Compliance...")
        sensitive_doc = "User email: john.doe@example.com, Phone: 123-456-7890. SSN: 123-45-6789."
        
        # Scan
        scan_res = self.fleet.compliance_agent.scan_shard(sensitive_doc)
        print(f"Scan Result: {scan_res}")
        self.assertTrue(scan_res["pii_detected"])
        self.assertEqual(len(scan_res["findings"]), 3)
        
        # Mask
        masked = self.fleet.compliance_agent.mask_pii(sensitive_doc)
        print(f"Masked Data: {masked}")
        self.assertIn("[MASKED_EMAIL]", masked)
        self.assertIn("[MASKED_PHONE]", masked)
        self.assertNotIn("john.doe@example.com", masked)
        
        # Audit ZK Fusion
        is_safe = self.fleet.compliance_agent.audit_zk_fusion([masked, "Clean data"])
        print(f"ZK Fusion Audit: {is_safe}")
        self.assertTrue(is_safe)

    def test_multimedia_grounding(self) -> None:
        print("\nTesting Phase 58: Multimedia Grounding (Audio/Video)...")
        
        # Audio
        transcription = self.fleet.audio_reasoning.transcribe_audio("engine_hum.mp3")
        analysis = self.fleet.audio_reasoning.analyze_audio_intent(transcription)
        print(f"Audio Analysis: {analysis}")
        self.assertEqual(analysis["intent"], "diagnostic_report")
        
        correlation = self.fleet.audio_reasoning.correlate_with_telemetry(analysis, {"vibration_level": 0.9})
        print(f"Telemetry Correlation: {correlation}")
        self.assertIn("confirmed", correlation)
        
        # Video (Visualizer expand)
        frames = [
            {"timestamp": 10.1, "detected_objects": ["hand", "tool_far"]},
            {"timestamp": 10.5, "detected_objects": ["hand", "tool_close"]},
            {"timestamp": 11.0, "detected_objects": ["hand", "holding_tool"]}
        ]
        video_res = self.fleet.visualizer.video_grounding(frames, "Pick up tool")
        print(f"Video Grounding: {video_res}")
        self.assertEqual(len(video_res["detected_sequence"]), 3)
        self.assertIn("Pick up tool", video_res["conclusion"])

if __name__ == "__main__":
    unittest.main()
