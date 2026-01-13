import unittest
import time
import os
import sys

# Ensure the project root is in PYTHONPATH

from src.classes.specialized.ResourceForecastingAgent import ResourceForecastingAgent

class TestResourceForecasting(unittest.TestCase):
    def setUp(self):
        self.agent = ResourceForecastingAgent(os.getcwd())

    def test_log_and_predict(self) -> None:
        # Log some data points
        self.agent.log_usage_snapshot(10.0, 100.0, 50.0)
        time.sleep(0.1)
        self.agent.log_usage_snapshot(12.0, 105.0, 55.0)
        
        forecast = self.agent.predict_future_needs(horizon_hours=1)
        self.assertEqual(forecast['status'], "Success")
        self.assertTrue(forecast['prediction']['compute'] > 12.0)
        self.assertTrue(forecast['prediction']['storage'] > 105.0)

    def test_scaling_recommendation(self) -> None:
        # Trigger SCALE_UP
        self.agent.log_usage_snapshot(80.0, 400.0, 200.0)
        time.sleep(0.1)
        self.agent.log_usage_snapshot(90.0, 450.0, 220.0)
        
        rec = self.agent.get_scaling_recommendation()
        self.assertIn("SCALE_UP", rec)

if __name__ == "__main__":
    unittest.main()
