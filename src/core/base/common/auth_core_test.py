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
import time
import hashlib
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from src.core.base.common.auth_core import AuthCore



class TestAuthCore:
    @pytest.fixture
    def core(self):
        return AuthCore()

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(agent_id=st.text(min_size=1))
    def test_generate_challenge(self, core, agent_id):
        # We can't strictly test the output value due to time.time(),
        # but we can test structure and length.
        challenge = core.generate_challenge(agent_id)
        assert len(challenge) == 64
        try:
            int(challenge, 16)
        except ValueError:
            pytest.fail("Challenge is not valid hex")

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(challenge=st.text(min_size=1), secret_key=st.text(min_size=1))
    def test_generate_proof(self, core, challenge, secret_key):
        proof = core.generate_proof(challenge, secret_key)

        expected = hashlib.sha512(f"{challenge}:{secret_key}".encode()).hexdigest()
        assert proof == expected
        assert len(proof) == 128  # sha512 is 128 chars hex

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(challenge=st.text(min_size=1), secret=st.text(min_size=1))
    def test_verify_proof_valid(self, core, challenge, secret):
        proof = core.generate_proof(challenge, secret)
        is_valid = core.verify_proof(challenge, proof, secret)
        assert is_valid

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        challenge=st.text(min_size=1),
        secret=st.text(min_size=1, max_size=10),
        wrong_secret=st.text(min_size=11, max_size=20),
    )
    def test_verify_proof_invalid(self, core, challenge, secret, wrong_secret):
        proof = core.generate_proof(challenge, secret)
        is_valid = core.verify_proof(challenge, proof, wrong_secret)
        assert not is_valid

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        proof_time=st.floats(min_value=0, max_value=2000000000),
        ttl=st.integers(min_value=1, max_value=3600),
    )
    def test_is_proof_expired_logic(self, core, proof_time, ttl):
        # We need to control current time to test this purely.
        # But the method calls time.time().
        # Test the bounds relative to 'now'.
        now = time.time()

        # expired case
        old_time = now - (ttl + 10)
        assert core.is_proof_expired(old_time, ttl)

        # valid case
        fresh_time = now - (ttl - 10)
        if ttl > 10:
            assert not core.is_proof_expired(fresh_time, ttl)
