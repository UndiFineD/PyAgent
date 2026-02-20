#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
"""
Test Auth Core module.
"""

"""
import unittest
from hypothesis import given, strategies as st
import hashlib
import time
from src.core.base.logic.core.auth_core import AuthCore



class TestAuthCore(unittest.TestCase):
    def setUp(self):
        self.core = AuthCore()

        @given(st.text(min_size=1))
    def test_generate_challenge(self, agent_id):
        # We can't strictly test the output value due to time.time(),'        # but we can test structure and length.
        # Ideally, we'd refactor generate_challenge to take a timestamp, but looking at the file,'        # it calls time.time() internally.
        # For the Rust conversion, we will likely change the signature to accept a seed or timestamp.
        # For now, let's verify it produces a valid hex string of expected length (sha256 = 64 chars).'        challenge = self.core.generate_challenge(agent_id)
        self.assertEqual(len(challenge), 64)
        try:
        int(challenge, 16)
        except ValueError:
        self.fail("Challenge is not valid hex")
        @given(challenge=st.text(min_size=1), secret_key=st.text(min_size=1))
    def test_generate_proof(self, challenge, secret_key):
        proof = self.core.generate_proof(challenge, secret_key)

        expected = hashlib.sha512(f"{challenge}:{secret_key}".encode()).hexdigest()
        self.assertEqual(proof, expected)
        self.assertEqual(len(proof), 128)  # sha512 is 128 chars hex

        @given(challenge=st.text(min_size=1), secret=st.text(min_size=1))
    def test_verify_proof_valid(self, challenge, secret):
        proof = self.core.generate_proof(challenge, secret)
        # In current impl, verified against the secret itself
        is_valid = self.core.verify_proof(challenge, proof, secret)
        self.assertTrue(is_valid)

        @given(
        challenge=st.text(min_size=1),
        secret=st.text(min_size=1, max_size=10),
        wrong_secret=st.text(min_size=11, max_size=20),
        )
    def test_verify_proof_invalid(self, challenge, secret, wrong_secret):
        proof = self.core.generate_proof(challenge, secret)
        is_valid = self.core.verify_proof(challenge, proof, wrong_secret)
        self.assertFalse(is_valid)

        @given(
        proof_time=st.floats(min_value=0, max_value=2000000000),
        ttl=st.integers(min_value=1, max_value=3600),
        )
    def test_is_proof_expired_logic(self, proof_time, ttl):
        # We need to control current time to test this purely.
        # But the method calls time.time().

        # Ideally we refactor the python code to accept current_time too.
        # Since I can't easily mock time.time() inside hypothesis without side effects...'        # I will test the bounds relative to 'now'.
        now = time.time()

        # expired case
        old_time = now - (ttl + 10)
        self.assertTrue(self.core.is_proof_expired(old_time, ttl))

        # valid case
        fresh_time = now - (ttl - 10)
        if ttl > 10:
        self.assertFalse(self.core.is_proof_expired(fresh_time, ttl))


        if __name__ == "__main__":
        unittest.main()
