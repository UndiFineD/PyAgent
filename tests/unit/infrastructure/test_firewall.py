#!/usr/bin/env python3
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
