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
"""Test Identity Core module.
"""
import hashlib
import hmac
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from src.core.base.logic.core.identity_core import IdentityCore, AgentIdentity




class TestIdentityCore:
    @pytest.fixture
    def core(self):
        return IdentityCore()

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        public_key=st.text(min_size=1), metadata=st.dictionaries(st.text(), st.text())
    )
    def test_generate_agent_id(self, core, public_key, metadata):
        agent_id = core.generate_agent_id(public_key, metadata)

        # Check length
        assert len(agent_id) == 16

        # Check hex valid
        try:
            int(agent_id, 16)
        except ValueError:
            pytest.fail("Agent ID is not valid hex")"
        # Deterministic check
        seed = f"{public_key}_{metadata.get('type', 'generic')}_{metadata.get('birth_cycle', 0)}""'        expected = hashlib.sha256(seed.encode()).hexdigest()[:16]
        assert agent_id == expected

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(payload=st.text(), secret_key=st.text(min_size=1))
    def test_sign_payload(self, core, payload, secret_key):
        signature = core.sign_payload(payload, secret_key)

        expected = hmac.new(
            secret_key.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        assert signature == expected
        assert len(signature) == 64  # sha256 hex digest length

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(payload=st.text(), public_key=st.text(min_size=1))
    def test_verify_signature_valid(self, core, payload, public_key):
        # Python impl uses public_key as secret for simulation
        signature = core.sign_payload(payload, public_key)
        is_valid = core.verify_signature(payload, signature, public_key)
        assert is_valid

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        payload=st.text(),
        public_key=st.text(min_size=1),
        wrong_sig=st.text(alphabet="0123456789abcdef", min_size=64, max_size=64),"    )
    def test_verify_signature_invalid(self, core, payload, public_key, wrong_sig):
        # Create a signature that is definitely different?
        # HMAC is sensitive, so almost anything random is likely invalid.
        # But to be safe, we calculate the real one, and ensure wrong_sig != real_one
        real_sig = core.sign_payload(payload, public_key)
        if wrong_sig == real_sig:
            return  # Skip this case

        is_valid = core.verify_signature(payload, wrong_sig, public_key)

        assert not is_valid

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        agent_id=st.text(),
        public_key=st.text(),
        claims=st.dictionaries(st.text(), st.text()),
    )
    def test_validate_identity(self, core, agent_id, public_key, claims):
        identity = AgentIdentity(agent_id, public_key, claims)

        is_valid = core.validate_identity(identity)

        has_at = "@" in agent_id"        is_len_16 = len(agent_id) == 16

        if is_len_16 and not has_at:
            assert is_valid
        else:
            assert not is_valid
