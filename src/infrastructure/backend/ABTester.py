#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .ABTestVariant import ABTestVariant

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class ABTester:
    """Conducts A / B tests across backends.

    Enables comparing performance between different backends or configurations.

    Example:
        tester=ABTester()
        tester.create_test("latency_test", "backend_a", "backend_b")

        # For each request:
        variant=tester.assign_variant("latency_test", user_id="user123")
        # Use variant.backend for request

        # Record result:
        tester.record_result("latency_test", variant.name, latency_ms=150)
    """

    def __init__(self) -> None:
        """Initialize A / B tester."""
        self._tests: Dict[str, Dict[str, ABTestVariant]] = {}
        self._assignments: Dict[str, Dict[str, str]] = {}  # test -> user -> variant
        self._lock = threading.Lock()

    def create_test(
        self,
        test_name: str,
        backend_a: str,
        backend_b: str,
        weight_a: float = 0.5,
    ) -> Tuple[ABTestVariant, ABTestVariant]:
        """Create an A / B test.

        Args:
            test_name: Test identifier.
            backend_a: First backend.
            backend_b: Second backend.
            weight_a: Weight for variant A (0 - 1).

        Returns:
            Tuple[ABTestVariant, ABTestVariant]: The two variants.
        """
        variant_a = ABTestVariant(
            name="A",
            backend=backend_a,
            weight=weight_a,
        )
        variant_b = ABTestVariant(
            name="B",
            backend=backend_b,
            weight=round(1.0 - weight_a, 10),
        )

        with self._lock:
            self._tests[test_name] = {
                "A": variant_a,
                "B": variant_b,
            }
            self._assignments[test_name] = {}

        return variant_a, variant_b

    def assign_variant(
        self,
        test_name: str,
        user_id: str,
    ) -> Optional[ABTestVariant]:
        """Assign user to a variant.

        Args:
            test_name: Test identifier.
            user_id: User identifier.

        Returns:
            Optional[ABTestVariant]: Assigned variant or None.
        """
        with self._lock:
            test = self._tests.get(test_name)
            if not test:
                return None

            # Check existing assignment
            if user_id in self._assignments.get(test_name, {}):
                variant_name = self._assignments[test_name][user_id]
                return test.get(variant_name)

            # Assign based on weights
            import random
            variant_a = test["A"]
            if random.random() < variant_a.weight:
                variant_name = "A"
            else:
                variant_name = "B"

            self._assignments[test_name][user_id] = variant_name
            return test[variant_name]

    def record_result(
        self,
        test_name: str,
        variant_name: str,
        **metrics: float,
    ) -> None:
        """Record test result for a variant.

        Args:
            test_name: Test identifier.
            variant_name: Variant name ("A" or "B").
            **metrics: Metric values to record.
        """
        with self._lock:
            test = self._tests.get(test_name)
            if not test or variant_name not in test:
                return

            variant = test[variant_name]
            variant.sample_count += 1

            for metric, value in metrics.items():
                # Running average
                if metric not in variant.metrics:
                    variant.metrics[metric] = value
                else:
                    n = variant.sample_count
                    variant.metrics[metric] = (
                        variant.metrics[metric] * (n - 1) + value
                    ) / n

    def get_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get test results.

        Args:
            test_name: Test identifier.

        Returns:
            Optional[Dict]: Test results or None.
        """
        with self._lock:
            test = self._tests.get(test_name)
            if not test:
                return None

            return {
                "test_name": test_name,
                "variants": {
                    name: {
                        "backend": v.backend,
                        "weight": v.weight,
                        "sample_count": v.sample_count,
                        "metrics": dict(v.metrics),
                    }
                    for name, v in test.items()
                },
            }

    def get_winner(
        self,
        test_name: str,
        metric: str,
        higher_is_better: bool = True,
    ) -> Optional[str]:
        """Determine winning variant.

        Args:
            test_name: Test identifier.
            metric: Metric to compare.
            higher_is_better: Whether higher metric values are better.

        Returns:
            Optional[str]: Winning variant name or None.
        """
        with self._lock:
            test = self._tests.get(test_name)
            if not test:
                return None

            best_name: Optional[str] = None
            best_value: Optional[float] = None

            for name, variant in test.items():
                value = variant.metrics.get(metric)
                if value is None:
                    continue

                if best_value is None:
                    best_name = name
                    best_value = value
                elif higher_is_better and value > best_value:
                    best_name = name
                    best_value = value
                elif not higher_is_better and value < best_value:
                    best_name = name
                    best_value = value

            return best_name
