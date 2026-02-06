# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-guardian-cli\utils\scope_validator.py
"""
Scope validation and target verification
Ensures all scanning is within authorized boundaries
"""

import ipaddress
import re
from pathlib import Path
from typing import List, Optional, Set
from urllib.parse import urlparse

from utils.logger import get_logger


class ScopeValidator:
    """Validates targets against authorized scope and blacklists"""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger()

        # Load blacklisted IP ranges
        self.blacklist_networks = []
        for cidr in config.get("scope", {}).get("blacklist", []):
            try:
                self.blacklist_networks.append(ipaddress.ip_network(cidr))
            except ValueError as e:
                self.logger.warning(f"Invalid blacklist CIDR: {cidr} - {e}")

        # Load authorized scope (if provided)
        self.authorized_domains: Set[str] = set()
        self.authorized_ips: Set[str] = set()
        self.authorized_networks: List[ipaddress.ip_network] = []

    def load_scope_file(self, scope_file: Path) -> bool:
        """Load authorized scope from file"""
        try:
            with open(scope_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Try to parse as IP/CIDR
                    if self._is_ip_or_cidr(line):
                        try:
                            if "/" in line:
                                self.authorized_networks.append(
                                    ipaddress.ip_network(line)
                                )
                            else:
                                self.authorized_ips.add(line)
                        except ValueError:
                            self.logger.warning(f"Invalid IP/CIDR in scope: {line}")
                    else:
                        # Treat as domain
                        self.authorized_domains.add(line.lower())

            self.logger.info(f"Loaded scope from {scope_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load scope file: {e}")
            return False

    def validate_target(self, target: str) -> tuple[bool, Optional[str]]:
        """
        Validate a target against scope and blacklists
        Returns (is_valid, reason)
        """
        # Parse target
        target = target.strip()

        # Check if it's a URL
        if target.startswith(("http://", "https://")):
            parsed = urlparse(target)
            host = parsed.hostname or parsed.netloc
        else:
            host = target

        # Check if blacklisted
        if self._is_blacklisted(host):
            reason = f"Target {host} is in blacklisted range"
            self.logger.log_security_event("SCOPE_VIOLATION", "CRITICAL", reason)
            return False, reason

        # If scope file is required, check authorization
        if self.config.get("scope", {}).get("require_scope_file", False):
            if not self._is_authorized(host):
                reason = f"Target {host} not in authorized scope"
                self.logger.log_security_event("SCOPE_VIOLATION", "HIGH", reason)
                return False, reason

        return True, None

    def _is_blacklisted(self, host: str) -> bool:
        """Check if host is in blacklist"""
        try:
            # Try to parse as IP
            ip = ipaddress.ip_address(host)
            for network in self.blacklist_networks:
                if ip in network:
                    return True
        except ValueError:
            # Not an IP, check domain patterns
            # Blacklist localhost variations
            if host.lower() in ["localhost", "127.0.0.1", "::1"]:
                return True

        return False

    def _is_authorized(self, host: str) -> bool:
        """Check if host is in authorized scope"""
        # Check if IP
        try:
            ip = ipaddress.ip_address(host)

            # Check authorized IPs
            if str(ip) in self.authorized_ips:
                return True

            # Check authorized networks
            for network in self.authorized_networks:
                if ip in network:
                    return True
        except ValueError:
            # Not an IP, check as domain
            host_lower = host.lower()

            # Exact match
            if host_lower in self.authorized_domains:
                return True

            # Subdomain match (*.example.com)
            for domain in self.authorized_domains:
                if domain.startswith("*."):
                    pattern = domain[2:]  # Remove *.
                    if host_lower.endswith(pattern):
                        return True
                elif domain.startswith("."):
                    # Matches domain and all subdomains
                    if host_lower.endswith(domain) or host_lower == domain[1:]:
                        return True

        return False

    def _is_ip_or_cidr(self, value: str) -> bool:
        """Check if value is an IP address or CIDR notation"""
        try:
            if "/" in value:
                ipaddress.ip_network(value)
            else:
                ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    def add_authorized_target(self, target: str):
        """Dynamically add a target to authorized scope"""
        if self._is_ip_or_cidr(target):
            try:
                if "/" in target:
                    self.authorized_networks.append(ipaddress.ip_network(target))
                else:
                    self.authorized_ips.add(target)
            except ValueError:
                self.logger.warning(f"Invalid IP/CIDR: {target}")
        else:
            self.authorized_domains.add(target.lower())

        self.logger.info(f"Added to authorized scope: {target}")
