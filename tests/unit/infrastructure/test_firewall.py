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

import pytest
from unittest.mock import patch
from src.infrastructure.security.network.firewall import ReverseProxyFirewall


@pytest.fixture
def mock_config(tmp_path):
    with patch("src.infrastructure.security.network.firewall.config") as m:
        m.workspace_root = tmp_path

        def side_effect(key, default=None):
            data = {
                "firewall.blocked_domains": ["malicious.com"],
                "voyager.allowed_networks": ["127.0.0.1/32", "192.168.1.0/24", "8.8.8.8/32"],
                "firewall.local_only": False
            }
            return data.get(key, default)
        m.get.side_effect = side_effect
        yield m


def test_firewall_blocks_blocked_domain(mock_config):
    # Reset singleton for clean test
    ReverseProxyFirewall._instance = None
    ReverseProxyFirewall._initialized = False

    fw = ReverseProxyFirewall()
    assert fw.validate_request("http://malicious.com/api", "GET") is False
    assert fw.validate_request("http://google.com", "GET") is True


def test_firewall_blocks_invalid_ip(mock_config):
    ReverseProxyFirewall._instance = None
    ReverseProxyFirewall._initialized = False

    fw = ReverseProxyFirewall()
    # 10.0.0.5 is not in allowed networks
    assert fw.validate_request("http://10.0.0.5", "GET") is False
    # 192.168.1.50 is in 192.168.1.0/24
    assert fw.validate_request("http://192.168.1.50", "GET") is True


def test_firewall_local_only_mode(tmp_path):
    with patch("src.infrastructure.security.network.firewall.config") as m:
        m.workspace_root = tmp_path
        m.get.side_effect = lambda key, default: {
            "firewall.local_only": True
        }.get(key, default)

        ReverseProxyFirewall._instance = None
        ReverseProxyFirewall._initialized = False

        fw = ReverseProxyFirewall()
        assert fw.validate_request("http://localhost/status", "GET") is True
        # google.com should fail in local_only
        assert fw.validate_request("http://google.com", "GET") is False

def test_firewall_invalid_scheme(mock_config):
    ReverseProxyFirewall._instance = None
    ReverseProxyFirewall._initialized = False

    fw = ReverseProxyFirewall()
    assert fw.validate_request("ftp://fileserver.local", "GET") is False
    assert fw.validate_request("gopher://old.internet", "GET") is False
