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
Test Auth Benchmark module.
"""

import timeit
from src.core.base.logic.core.auth_core import AuthCore


def benchmark_auth():
    core = AuthCore()
    agent_id = "agent_007"
    secret = "super_secret_key_value_12345"

    # Measure generate_challenge
    def run_gen_challenge():
        core.generate_challenge(agent_id)

    t_challenge = timeit.timeit(run_gen_challenge, number=100000)
    print(f"generate_challenge: {t_challenge / 100000 * 1_000_000:.4f} μs per call")

    # Measure generate_proof

    challenge = core.generate_challenge(agent_id)

    def run_gen_proof():
        core.generate_proof(challenge, secret)

    t_proof = timeit.timeit(run_gen_proof, number=100000)

    print(f"generate_proof: {t_proof / 100000 * 1_000_000:.4f} μs per call")

    # Measure verify_proof
    proof = core.generate_proof(challenge, secret)

    def run_verify():
        core.verify_proof(challenge, proof, secret)

    t_verify = timeit.timeit(run_verify, number=100000)
    print(f"verify_proof: {t_verify / 100000 * 1_000_000:.4f} μs per call")


if __name__ == "__main__":
    benchmark_auth()