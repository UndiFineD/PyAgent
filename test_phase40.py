#!/usr/bin/env python3

"""Test script for Phase 40 improvements: Recursive Self-Debugging & Neural Pruning."""

import os
import sys
import unittest
import logging
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.classes.orchestration.AutoDebuggerOrchestrator import AutoDebuggerOrchestrator
from src.classes.orchestration.SwarmPruningOrchestrator import SwarmPruningOrchestrator
from src.classes.specialized.NeuralPruningEngine import NeuralPruningEngine

class TestPhase40(unittest.TestCase):

    def setUp(self):
        self.workspace_root = os.getcwd()
        logging.basicConfig(level=logging.DEBUG)

    def test_auto_debugger_syntax_check(self) -> None:
        """Tests that the AutoDebugger can identify syntax errors."""
        orchestrator = AutoDebuggerOrchestrator(self.workspace_root)
        
        # Test with a valid file (this file)
        result = orchestrator.validate_and_repair(__file__)
        self.assertEqual(result["status"], "success")

    def test_neural_pruning_performance(self) -> None:
        """Tests the Neural Pruning logic with performance tracking."""
        mock_fleet = MagicMock()
        engine = NeuralPruningEngine(mock_fleet)
        orchestrator = SwarmPruningOrchestrator(mock_fleet)
        orchestrator.pruning_engine = engine # Ensure they use the same engine

        # High performance, low cost node
        orchestrator.record_node_performance("EfficientAgent", True, 100)
        orchestrator.record_node_performance("EfficientAgent", True, 100)
        
        # Low performance, high cost node
        orchestrator.record_node_performance("WastefulAgent", False, 5000)
        orchestrator.record_node_performance("WastefulAgent", False, 5000)

        # Check synaptic weights
        efficient_weight = engine.active_synapses.get("EfficientAgent")
        wasteful_weight = engine.active_synapses.get("WastefulAgent")
        
        print(f"Efficient Weight: {efficient_weight}")
        print(f"Wasteful Weight: {wasteful_weight}")
        
        self.assertGreater(efficient_weight, wasteful_weight)
        
        # Run pruning cycle with a threshold that should prune WastefulAgent
        result = orchestrator.run_pruning_cycle(threshold=1.0)
        self.assertIn("WastefulAgent", result["pruned_nodes"])
        self.assertNotIn("EfficientAgent", result["pruned_nodes"])

    @patch('subprocess.run')
    def test_auto_debugger_repair_trigger(self, mock_run) -> None:
        """Tests that repair is triggered on syntax error."""
        from subprocess import CalledProcessError
        
        # Simulate a syntax error
        mock_run.side_effect = CalledProcessError(1, "python -m py_compile", stderr="SyntaxError: invalid syntax")
        
        orchestrator = AutoDebuggerOrchestrator(self.workspace_root)
        
        # Mock CoderAgent.improve_content
        orchestrator.coder.improve_content = MagicMock(return_value="fixed code")
        
        # Create a dummy broken file
        dummy_file = "dummy_broken.py"
        with open(dummy_file, "w") as f:
            f.write("invalid python code")
            
        try:
            result = orchestrator.validate_and_repair(dummy_file)
            self.assertEqual(result["status"], "repaired")
            orchestrator.coder.improve_content.assert_called()
        finally:
            if os.path.exists(dummy_file):
                os.remove(dummy_file)

if __name__ == "__main__":
    unittest.main()
