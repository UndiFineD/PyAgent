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

# DNS Security Core - Network-level filtering and analysis
# Based on patterns from AdGuard Home repository

import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
<<<<<<< HEAD
from datetime import datetime, timezone
=======
from datetime import datetime, timedelta, timezone
>>>>>>> copilot/sub-pr-29
from enum import Enum
import re
from collections import deque
import time



class DnsRecordType(Enum):
    """DNS record types"""
    A = 1
    AAAA = 28
    CNAME = 5
    MX = 15
    TXT = 16
    PTR = 12
    SRV = 33
    SOA = 6
    NS = 2



class FilterAction(Enum):
    """DNS filtering actions"""
    ALLOW = "allow"
    BLOCK = "block"
    REDIRECT = "redirect"
    REWRITE = "rewrite"



class QueryResult(Enum):
    """DNS query results"""
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    FILTERED = "filtered"
    ERROR = "error"


@dataclass
class DnsQuery:
    """DNS query representation"""
    domain: str
    record_type: DnsRecordType
    client_ip: str
    timestamp: datetime
    result: QueryResult = QueryResult.ALLOWED
    blocked_reason: Optional[str] = None
    response_time: Optional[float] = None
    upstream_server: Optional[str] = None


@dataclass
class FilterRule:
    """DNS filtering rule"""
    pattern: str
    action: FilterAction
    priority: int = 0
    description: str = ""
    enabled: bool = True
    hit_count: int = 0
    last_hit: Optional[datetime] = None


@dataclass
class DnsStatistics:
    """DNS statistics container"""
    total_queries: int = 0
    blocked_queries: int = 0
    allowed_queries: int = 0
    error_queries: int = 0
    queries_by_domain: Dict[str, int] = field(default_factory=dict)
    queries_by_client: Dict[str, int] = field(default_factory=dict)
    queries_by_type: Dict[str, int] = field(default_factory=dict)
    response_times: List[float] = field(default_factory=list)
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))



class DnsSecurityCore:
    """
    DNS Security Core for network-level filtering and analysis.

    Provides comprehensive DNS filtering, logging, and security analysis
    based on AdGuard Home methodologies.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.filter_rules: List[FilterRule] = []
        self.query_log: deque[DnsQuery] = deque(maxlen=10000)  # Keep last 10k queries
        self.statistics = DnsStatistics()
        self.upstream_servers: List[str] = []
        self.cache: Dict[str, Tuple[Any, datetime]] = {}
        self.cache_ttl = 300  # 5 minutes default
        self.blocked_domains: Set[str] = set()
        self.allowed_domains: Set[str] = set()
        self.safe_search_enabled = False
        self.parental_control_enabled = False

    async def initialize(self) -> bool:
        """Initialize the DNS security core"""
        try:
            self.logger.info("Initializing DNS Security Core")

            # Load default filter lists
            await self._load_default_filters()

            # Initialize upstream servers
            self.upstream_servers = [
                "8.8.8.8",  # Google DNS
                "1.1.1.1",  # Cloudflare DNS
                "9.9.9.9",  # Quad9 DNS
            ]

            self.logger.info("DNS Security Core initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize DNS Security Core: {e}")
            return False

    async def _load_default_filters(self) -> None:
        """Load default filtering rules"""
        # Ad/tracking blocking rules
        default_rules = [
            FilterRule("*.doubleclick.net", FilterAction.BLOCK, 100, "Google DoubleClick ads"),
            FilterRule("*.googlesyndication.com", FilterAction.BLOCK, 100, "Google AdSense"),
            FilterRule("*.googleadservices.com", FilterAction.BLOCK, 100, "Google Ads"),
            FilterRule("*.facebook.com", FilterAction.BLOCK, 90, "Facebook tracking"),
            FilterRule("*.amazon-adsystem.com", FilterAction.BLOCK, 90, "Amazon advertising"),
            FilterRule("analytics.*", FilterAction.BLOCK, 80, "Analytics tracking"),
            FilterRule("tracking.*", FilterAction.BLOCK, 80, "General tracking"),
        ]

        self.filter_rules.extend(default_rules)

        # Update blocked domains set
        for rule in self.filter_rules:
            if rule.action == FilterAction.BLOCK and rule.enabled:
                # For now, just add exact matches
                if "*" not in rule.pattern:
                    self.blocked_domains.add(rule.pattern)

    async def add_filter_rule(self, rule: FilterRule) -> bool:
        """Add a new filtering rule"""
        try:
            self.filter_rules.append(rule)
            self.filter_rules.sort(key=lambda x: x.priority, reverse=True)

            # Update blocked domains if it's a block rule
            if rule.action == FilterAction.BLOCK and rule.enabled:
                if "*" not in rule.pattern:
                    self.blocked_domains.add(rule.pattern)

            self.logger.info(f"Added filter rule: {rule.pattern} -> {rule.action.value}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add filter rule: {e}")
            return False

    async def remove_filter_rule(self, pattern: str) -> bool:
        """Remove a filtering rule"""
        try:
            original_count = len(self.filter_rules)
            self.filter_rules = [r for r in self.filter_rules if r.pattern != pattern]

            if len(self.filter_rules) < original_count:
                # Remove from blocked domains if it was a block rule
                self.blocked_domains.discard(pattern)
                self.logger.info(f"Removed filter rule: {pattern}")
                return True
            else:
                self.logger.warning(f"Filter rule not found: {pattern}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to remove filter rule: {e}")
            return False

    async def check_domain_filter(self, domain: str) -> Tuple[FilterAction, Optional[str]]:
        """Check if a domain should be filtered"""
        try:
            # Normalize domain
            domain = domain.lower().strip()

            # Check filter rules (with wildcard support) - this is the primary check
            for rule in self.filter_rules:
                if not rule.enabled:
                    continue

                if self._matches_pattern(domain, rule.pattern):
                    rule.hit_count += 1
                    rule.last_hit = datetime.now(timezone.utc)
                    return rule.action, rule.description

            # Fallback: check blocked domains set for exact matches (optimization for default filters)
            if domain in self.blocked_domains:
                return FilterAction.BLOCK, "Blocked domain"

            return FilterAction.ALLOW, None

        except Exception as e:
            self.logger.error(f"Error checking domain filter: {e}")
            return FilterAction.ALLOW, None

    def _matches_pattern(self, domain: str, pattern: str) -> bool:
        """Check if domain matches a filter pattern"""
        try:
            # Handle wildcards
            if "*" in pattern:
                # Convert wildcard to regex
                regex_pattern = pattern.replace(".", "\\.").replace("*", ".*")
                return bool(re.match(f"^{regex_pattern}$", domain, re.IGNORECASE))

            # Exact match
            return domain == pattern.lower()

        except Exception:
            return False

    async def process_dns_query(
        self,
        domain: str,
        record_type: DnsRecordType,
        client_ip: str
    ) -> DnsQuery:
        """Process a DNS query through the security filters"""
        start_time = time.time()

        try:
            # Check filters
            action, reason = await self.check_domain_filter(domain)

            # Create query record
            query = DnsQuery(
                domain=domain,
                record_type=record_type,
                client_ip=client_ip,
                timestamp=datetime.now(timezone.utc),
                response_time=time.time() - start_time
            )

            # Determine result
            if action == FilterAction.BLOCK:
                query.result = QueryResult.BLOCKED
                query.blocked_reason = reason or "Blocked by filter"
            else:
                query.result = QueryResult.ALLOWED

            # Log query
            self.query_log.append(query)

            # Update statistics
            self._update_statistics(query)

            return query

        except Exception as e:
            self.logger.error(f"Error processing DNS query: {e}")
            query = DnsQuery(
                domain=domain,
                record_type=record_type,
                client_ip=client_ip,
                timestamp=datetime.now(timezone.utc),
                result=QueryResult.ERROR,
                response_time=time.time() - start_time
            )
            self.query_log.append(query)
            self._update_statistics(query)
            return query

    def _update_statistics(self, query: DnsQuery) -> None:
        """Update DNS statistics"""
        self.statistics.total_queries += 1

        if query.result == QueryResult.BLOCKED:
            self.statistics.blocked_queries += 1
        elif query.result == QueryResult.ALLOWED:
            self.statistics.allowed_queries += 1
        elif query.result == QueryResult.ERROR:
            self.statistics.error_queries += 1

        # Update domain stats
        domain = query.domain
        self.statistics.queries_by_domain[domain] = self.statistics.queries_by_domain.get(domain, 0) + 1

        # Update client stats
        client = query.client_ip
        self.statistics.queries_by_client[client] = self.statistics.queries_by_client.get(client, 0) + 1

        # Update type stats
        qtype = query.record_type.name
        self.statistics.queries_by_type[qtype] = self.statistics.queries_by_type.get(qtype, 0) + 1

        # Update response times
        if query.response_time:
            self.statistics.response_times.append(query.response_time)
            # Keep only last 1000 response times
            if len(self.statistics.response_times) > 1000:
                self.statistics.response_times.pop(0)

    async def get_dns_statistics(self) -> Dict[str, Any]:
        """Get comprehensive DNS statistics"""
        try:
            stats = {
                "total_queries": self.statistics.total_queries,
                "blocked_queries": self.statistics.blocked_queries,
                "allowed_queries": self.statistics.allowed_queries,
                "error_queries": self.statistics.error_queries,
                "block_percentage": (
                    (self.statistics.blocked_queries / self.statistics.total_queries * 100)
                    if self.statistics.total_queries > 0 else 0
                ),
                "top_domains": sorted(
                    self.statistics.queries_by_domain.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10],
                "top_clients": sorted(
                    self.statistics.queries_by_client.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10],
                "queries_by_type": self.statistics.queries_by_type,
                "average_response_time": (
                    sum(self.statistics.response_times) / len(self.statistics.response_times)
                    if self.statistics.response_times else 0
                ),
                "uptime_seconds": (datetime.now(timezone.utc) - self.statistics.start_time).total_seconds(),
                "filter_rules_count": len(self.filter_rules),
                "active_filters": len([r for r in self.filter_rules if r.enabled]),
            }

            return stats

        except Exception as e:
            self.logger.error(f"Error getting DNS statistics: {e}")
            return {}

    async def get_recent_queries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent DNS queries"""
        try:
            queries = list(self.query_log)[-limit:]
            return [
                {
                    "domain": q.domain,
                    "record_type": q.record_type.name,
                    "client_ip": q.client_ip,
                    "timestamp": q.timestamp.isoformat(),
                    "result": q.result.value,
                    "blocked_reason": q.blocked_reason,
                    "response_time": q.response_time,
                    "upstream_server": q.upstream_server,
                }
                for q in queries
            ]

        except Exception as e:
            self.logger.error(f"Error getting recent queries: {e}")
            return []

    async def enable_safe_search(self, enabled: bool = True) -> bool:
        """Enable or disable safe search filtering"""
        try:
            self.safe_search_enabled = enabled

            if enabled:
                # Add safe search rules
                safe_search_rules = [
                    FilterRule("www.google.com", FilterAction.REWRITE, 200, "Safe search for Google"),
                    FilterRule("www.bing.com", FilterAction.REWRITE, 200, "Safe search for Bing"),
                    FilterRule("www.youtube.com", FilterAction.REWRITE, 200, "Safe search for YouTube"),
                ]
                self.filter_rules.extend(safe_search_rules)

            self.logger.info(f"Safe search {'enabled' if enabled else 'disabled'}")
            return True

        except Exception as e:
            self.logger.error(f"Error setting safe search: {e}")
            return False

    async def enable_parental_control(self, enabled: bool = True) -> bool:
        """Enable or disable parental control filtering"""
        try:
            self.parental_control_enabled = enabled

            if enabled:
                # Add parental control rules
                parental_rules = [
                    FilterRule("*.porn", FilterAction.BLOCK, 150, "Adult content"),
                    FilterRule("*.sex", FilterAction.BLOCK, 150, "Adult content"),
                    FilterRule("*.adult", FilterAction.BLOCK, 150, "Adult content"),
                    FilterRule("*.gambling", FilterAction.BLOCK, 140, "Gambling sites"),
                    FilterRule("social-media.*", FilterAction.BLOCK, 130, "Social media restrictions"),
                ]
                self.filter_rules.extend(parental_rules)

            self.logger.info(f"Parental control {'enabled' if enabled else 'disabled'}")
            return True

        except Exception as e:
            self.logger.error(f"Error setting parental control: {e}")
            return False

    async def export_filter_rules(self, filepath: str) -> bool:
        """Export filter rules to a file"""
        try:
            rules_data = [
                {
                    "pattern": rule.pattern,
                    "action": rule.action.value,
                    "priority": rule.priority,
                    "description": rule.description,
                    "enabled": rule.enabled,
                    "hit_count": rule.hit_count,
                    "last_hit": rule.last_hit.isoformat() if rule.last_hit else None,
                }
                for rule in self.filter_rules
            ]

            with open(filepath, 'w') as f:
                json.dump(rules_data, f, indent=2)

            self.logger.info(f"Exported {len(rules_data)} filter rules to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting filter rules: {e}")
            return False

    async def import_filter_rules(self, filepath: str) -> bool:
        """Import filter rules from a file"""
        try:
            with open(filepath, 'r') as f:
                rules_data = json.load(f)

            imported_count = 0
            for rule_data in rules_data:
                rule = FilterRule(
                    pattern=rule_data["pattern"],
                    action=FilterAction(rule_data["action"]),
                    priority=rule_data.get("priority", 0),
                    description=rule_data.get("description", ""),
                    enabled=rule_data.get("enabled", True),
                )
                await self.add_filter_rule(rule)
                imported_count += 1

            self.logger.info(f"Imported {imported_count} filter rules from {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error importing filter rules: {e}")
            return False

    async def clear_cache(self) -> bool:
        """Clear the DNS cache"""
        try:
            cache_size = len(self.cache)
            self.cache.clear()
            self.logger.info(f"Cleared DNS cache ({cache_size} entries)")
            return True

        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
            return False

    async def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information"""
        try:
            now = datetime.now(timezone.utc)
            valid_entries = sum(1 for _, (_, expiry) in self.cache.items() if expiry > now)

            return {
                "total_entries": len(self.cache),
                "valid_entries": valid_entries,
                "expired_entries": len(self.cache) - valid_entries,
                "cache_ttl_seconds": self.cache_ttl,
            }

        except Exception as e:
            self.logger.error(f"Error getting cache info: {e}")
            return {}

    async def cleanup(self) -> None:
        """Clean up resources"""
        try:
            self.logger.info("Cleaning up DNS Security Core")
            self.query_log.clear()
            self.cache.clear()
            self.filter_rules.clear()
            self.blocked_domains.clear()
            self.allowed_domains.clear()

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
