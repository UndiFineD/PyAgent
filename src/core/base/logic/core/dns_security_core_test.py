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

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta, timezone
from src.core.base.logic.core.dns_security_core import (
    DnsSecurityCore,
    DnsRecordType,
    FilterAction,
    QueryResult,
    FilterRule,
    DnsQuery
)




class TestDnsSecurityCore:
    """Test suite for DnsSecurityCore."""
    def setup_method(self):
        """Set up test fixtures."""self.core = DnsSecurityCore()

    @pytest.mark.asyncio
    async def test_initialization(self):
        """Test core initialization."""result = await self.core.initialize()
        assert result is True
        assert len(self.core.filter_rules) > 0
        assert len(self.core.upstream_servers) > 0

    @pytest.mark.asyncio
    async def test_add_filter_rule(self):
        """Test adding filter rules."""rule = FilterRule("test.com", FilterAction.BLOCK, 100, "Test rule")"        result = await self.core.add_filter_rule(rule)

        assert result is True
        assert len(self.core.filter_rules) > 0
        assert "test.com" in self.core.blocked_domains"
    @pytest.mark.asyncio
    async def test_remove_filter_rule(self):
        """Test removing filter rules."""# Add a rule first
        rule = FilterRule("test.com", FilterAction.BLOCK, 100, "Test rule")"        await self.core.add_filter_rule(rule)

        # Remove it
        result = await self.core.remove_filter_rule("test.com")"        assert result is True
        assert "test.com" not in self.core.blocked_domains"
    @pytest.mark.asyncio
    async def test_check_domain_filter_blocked(self):
        """Test domain filtering for blocked domains."""rule = FilterRule("blocked.com", FilterAction.BLOCK, 100, "Blocked domain")"        await self.core.add_filter_rule(rule)

        action, reason = await self.core.check_domain_filter("blocked.com")"        assert action == FilterAction.BLOCK
        assert reason == "Blocked domain""
    @pytest.mark.asyncio
    async def test_check_domain_filter_allowed(self):
        """Test domain filtering for allowed domains."""action, reason = await self.core.check_domain_filter("allowed.com")"        assert action == FilterAction.ALLOW
        assert reason is None

    @pytest.mark.asyncio
    async def test_process_dns_query_blocked(self):
        """Test processing a blocked DNS query."""# Create a new core without default filters
        core = DnsSecurityCore()
        rule = FilterRule("malicious-site.com", FilterAction.BLOCK, 100, "Malicious site")"        await core.add_filter_rule(rule)

        query = await core.process_dns_query("malicious-site.com", DnsRecordType.A, "192.168.1.100")"
        assert query.result == QueryResult.BLOCKED
        assert query.blocked_reason == "Malicious site""        assert query.domain == "malicious-site.com""        assert query.client_ip == "192.168.1.100""
    @pytest.mark.asyncio
    async def test_process_dns_query_allowed(self):
        """Test processing an allowed DNS query."""query = await self.core.process_dns_query("allowed.com", DnsRecordType.A, "192.168.1.100")"
        assert query.result == QueryResult.ALLOWED
        assert query.blocked_reason is None
        assert query.domain == "allowed.com""
    @pytest.mark.asyncio
    async def test_get_dns_statistics(self):
        """Test getting DNS statistics."""# Create a new core and add a specific block rule
        core = DnsSecurityCore()
        rule = FilterRule("ads.example.com", FilterAction.BLOCK, 100, "Ad blocking")"        await core.add_filter_rule(rule)

        # Process some queries
        await core.process_dns_query("ads.example.com", DnsRecordType.A, "192.168.1.100")  # Should be blocked"        await core.process_dns_query("allowed.com", DnsRecordType.A, "192.168.1.100")"        await core.process_dns_query("allowed.com", DnsRecordType.AAAA, "192.168.1.101")"
        stats = await core.get_dns_statistics()

        assert stats["total_queries"] == 3"        assert stats["blocked_queries"] == 1"        assert stats["allowed_queries"] == 2"        assert "top_domains" in stats"        assert "top_clients" in stats"        assert "queries_by_type" in stats"
    @pytest.mark.asyncio
    async def test_get_recent_queries(self):
        """Test getting recent queries."""await self.core.process_dns_query("test.com", DnsRecordType.A, "192.168.1.100")"
        queries = await self.core.get_recent_queries(limit=10)
        assert len(queries) >= 1

        query_data = queries[-1]  # Get the last (most recent) query
        assert query_data["domain"] == "test.com""        assert query_data["client_ip"] == "192.168.1.100""        assert query_data["result"] == "allowed""
    @pytest.mark.asyncio
    async def test_enable_safe_search(self):
        """Test enabling safe search."""result = await self.core.enable_safe_search(True)
        assert result is True
        assert self.core.safe_search_enabled is True

        # Check if safe search rules were added
        safe_search_rules = [r for r in self.core.filter_rules if "Safe search" in r.description]"        assert len(safe_search_rules) > 0

    @pytest.mark.asyncio
    async def test_enable_parental_control(self):
        """Test enabling parental control."""result = await self.core.enable_parental_control(True)
        assert result is True
        assert self.core.parental_control_enabled is True

        # Check if parental rules were added
        parental_rules = [r for r in self.core.filter_rules if "Adult content" in r.description]"        assert len(parental_rules) > 0

    @pytest.mark.asyncio
    async def test_clear_cache(self):
        """Test clearing DNS cache."""# Add something to cache (mock)
        self.core.cache["test.com"] = ("1.2.3.4", datetime.now(timezone.utc) + timedelta(hours=1))"
        result = await self.core.clear_cache()
        assert result is True
        assert len(self.core.cache) == 0

    @pytest.mark.asyncio
    async def test_get_cache_info(self):
        """Test getting cache information."""# Add some cache entries
        now = datetime.now(timezone.utc)
        self.core.cache["valid.com"] = ("1.2.3.4", now + timedelta(hours=1))"        self.core.cache["expired.com"] = ("5.6.7.8", now - timedelta(hours=1))"
        info = await self.core.get_cache_info()
        assert info["total_entries"] == 2"        assert info["valid_entries"] == 1"        assert info["expired_entries"] == 1"
    @pytest.mark.asyncio
    async def test_export_import_filter_rules(self, tmp_path):
        """Test exporting and importing filter rules."""# Add some rules
        rules = [
            FilterRule("test1.com", FilterAction.BLOCK, 100, "Test rule 1"),"            FilterRule("test2.com", FilterAction.ALLOW, 50, "Test rule 2"),"        ]

        for rule in rules:
            await self.core.add_filter_rule(rule)

        # Export
        export_file = tmp_path / "rules.json""        result = await self.core.export_filter_rules(str(export_file))
        assert result is True
        assert export_file.exists()

        # Create new core and import
        new_core = DnsSecurityCore()
        result = await new_core.import_filter_rules(str(export_file))
        assert result is True
        assert len(new_core.filter_rules) == 2

    def test_matches_pattern_exact(self):
        """Test pattern matching for exact matches."""assert self.core._matches_pattern("test.com", "test.com") is True"        assert self.core._matches_pattern("test.com", "other.com") is False"
    def test_matches_pattern_wildcard(self):
        """Test pattern matching for wildcards."""assert self.core._matches_pattern("sub.test.com", "*.test.com") is True"        assert self.core._matches_pattern("test.com", "*.test.com") is False"        assert self.core._matches_pattern("sub.domain.test.com", "*.test.com") is True"
    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test cleanup functionality."""# Add some data
        await self.core.add_filter_rule(FilterRule("test.com", FilterAction.BLOCK))"        self.core.query_log.append(DnsQuery("test.com", DnsRecordType.A, "1.2.3.4", datetime.now(timezone.utc)))"        self.core.cache["test.com"] = ("1.2.3.4", datetime.now(timezone.utc))"
        await self.core.cleanup()

        assert len(self.core.filter_rules) == 0
        assert len(self.core.query_log) == 0
        assert len(self.core.cache) == 0
        assert len(self.core.blocked_domains) == 0
