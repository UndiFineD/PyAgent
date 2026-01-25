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
Test Phase92 module.
"""

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