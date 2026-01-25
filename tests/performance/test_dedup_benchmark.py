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
Test Dedup Benchmark module.
"""

import time
import random
import string
from src.observability.reports.core.deduplication_core import DeduplicationCore


def generate_sentence(words=10):
    return " ".join(
        "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
        for _ in range(words)
    )


def test_dedup_benchmark():
    # Setup
    size = 1000
    base_sentences = [generate_sentence() for _ in range(size // 10)]

    dataset = []

    # Generate dataset with mix of duplicates (high similarity) and unique

    for _ in range(size):
        if random.random() < 0.3:
            # Create a duplicate (near match)
            base = random.choice(base_sentences)
            # perturbations

            words = base.split()
            if len(words) > 2:
                words[random.randint(0, len(words) - 1)] = "changed"
            text = " ".join(words)
        else:
            text = generate_sentence()

        dataset.append({"message": text, "id": _})

    # Benchmark Python

    start = time.perf_counter()
    unique_py = DeduplicationCore.deduplicate_items(dataset, threshold=0.8)
    duration_py = (time.perf_counter() - start) * 1000

    print(f"Deduplication (Python) N={size}: {duration_py:.4f} ms")

    # Validate result count
    assert len(unique_py) > 0
    assert len(unique_py) <= size


if __name__ == "__main__":
    test_dedup_benchmark()