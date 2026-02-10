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

# Subdomain Permutation Core - Inspired by AlterX patterns
# Intelligent subdomain wordlist generation using DSL patterns and enrichment

import re
import itertools
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any, Iterator
import tldextract

from src.core.base.common.base_core import BaseCore


@dataclass
class PermutationResult:
    """Result of subdomain permutation generation."""
    domain: str
    permutations: Set[str] = field(default_factory=set)
    enriched_words: Set[str] = field(default_factory=set)
    enriched_numbers: Set[str] = field(default_factory=set)
    total_generated: int = 0
    patterns_used: int = 0


@dataclass
class PermutationConfig:
    """Configuration for permutation generation."""
    max_permutations: int = 10000
    enrich_words: bool = True
    enrich_numbers: bool = True
    deduplicate: bool = True
    custom_patterns: Optional[List[str]] = None
    custom_payloads: Optional[Dict[str, List[str]]] = None


class SubdomainPermutationCore(BaseCore):
    """
    Subdomain Permutation Core implementing intelligent wordlist generation.

    Inspired by AlterX, this core provides:
    - DSL-based pattern generation
    - Automatic word enrichment from input domains
    - Cluster bomb permutation algorithms
    - Configurable payloads and patterns
    """

    def __init__(self, config: Optional[PermutationConfig] = None):
        super().__init__()
        self.config = config or PermutationConfig()

        # Default patterns inspired by AlterX
        self.default_patterns = [
            # Dash based patterns
            "{{word}}-{{sub}}.{{suffix}}",
            "{{sub}}-{{word}}.{{suffix}}",
            # Dot based patterns
            "{{word}}.{{sub}}.{{suffix}}",
            "{{sub}}.{{word}}.{{suffix}}",
            # Iteration based
            "{{sub}}{{number}}.{{suffix}}",
            # Replace current subdomain
            "{{word}}.{{suffix}}",
            # No separator
            "{{sub}}{{word}}.{{suffix}}",
            # Region prefix
            "{{region}}.{{sub}}.{{suffix}}",
            # Cluster bomb
            "{{word}}{{number}}.{{suffix}}",
        ]

        # Default payloads
        self.default_payloads = {
            'word': [
                'api', 'k8s', 'v1', 'v2', 'origin', 'raw', 'stage', 'test', 'qa', 'web',
                'prod', 'service', 'grafana', 'beta', 'admin', 'staging', 'wordpress', 'wp',
                'dev', 'app', 'mta-sts', 'tech', 'private', 'public', 'login', 'role',
                'backend', 'cloud', 'internal', 'mail', 'oauth', 'oauth2', 'vpn', 'lab',
                'local', 'live', 'data', 'mobile', 'search', 'stats', 'final', 'ldap',
                'media', 'docs', 'eng', 'engineering', 'market', 'compute', 'cdn', 'acc',
                'access', 'backup', 'blogs', 'blog', 'careers', 'client', 'cms', 'cms1',
                'conf', 'dmz', 'drupal', 'corp', 'faq', 'ir', 'legacy', 'log', 'logs',
                'dashboard', 'monitor', 'mysql', 'mssql', 'db', 'partner', 'payment', 'pay',
                'office', 'plugins', 'shop', 'store', 'support', 'secure', 'ssl', 'portal',
                'auth', 'sso', 'remote', 'aws', 'azure', 'gcp', 'static', 'assets', 'files',
                'download', 'upload', 'cache', 'session', 'graphql', 'soap', 'ws', 'tcp',
                'udp', 'ftp', 'ssh', 'git', 'svn', 'jenkins', 'docker', 'kubernetes', 'k8s'
            ],
            'number': ['1', '2', '3', '01', '02', '001', '2023', '2024', '2025'],
            'region': ['us', 'eu', 'asia', 'ap', 'na', 'sa', 'af', 'oc', 'us-east', 'us-west']
        }

        # Regex patterns for enrichment
        self.extract_numbers = re.compile(r'[0-9]+')
        self.extract_words = re.compile(r'[a-zA-Z0-9]+')
        self.extract_words_only = re.compile(r'[a-zA-Z]{3,}')

    def generate_permutations(self, domains: List[str]) -> PermutationResult:
        """
        Generate subdomain permutations for given domains.

        Args:
            domains: List of base domains to generate permutations for

        Returns:
            PermutationResult with all generated permutations
        """
        result = PermutationResult(domain=domains[0] if domains else "")

        # Process all input domains
        all_inputs = []
        for domain in domains:
            inputs = self._parse_domain(domain)
            all_inputs.extend(inputs)

        # Enrich payloads from input domains
        if self.config.enrich_words or self.config.enrich_numbers:
            enriched = self._enrich_payloads(all_inputs)
            result.enriched_words = enriched.get('words', set())
            result.enriched_numbers = enriched.get('numbers', set())

        # Get patterns and payloads
        patterns = self.config.custom_patterns or self.default_patterns
        payloads = self._get_payloads()

        # Generate permutations for each input
        for input_data in all_inputs:
            domain_perms = self._generate_domain_permutations(input_data, patterns, payloads)
            result.permutations.update(domain_perms)

            if len(result.permutations) >= self.config.max_permutations:
                break

        # Limit results
        if len(result.permutations) > self.config.max_permutations:
            result.permutations = set(list(result.permutations)[:self.config.max_permutations])

        result.total_generated = len(result.permutations)
        result.patterns_used = len(patterns)

        return result

    def _parse_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Parse domain into components for variable extraction.

        Returns list of dicts with variables like AlterX:
        - {{sub}}: subdomain prefix
        - {{suffix}}: everything except sub
        - {{root}}: eTLD+1
        - {{tld}}: top level domain
        - {{etld}}: effective TLD
        - {{sub1}}, {{sub2}}, etc.: multilevel subdomains
        """
        inputs = []

        # Clean domain
        domain = domain.lower().strip()

        # Extract TLD info
        extracted = tldextract.extract(domain)

        if not extracted.domain:
            return inputs

        root_domain = f"{extracted.domain}.{extracted.suffix}"
        subdomain = extracted.subdomain

        # Basic variables
        base_vars = {
            'root': root_domain,
            'tld': extracted.suffix,
            'etld': extracted.suffix if not extracted.suffix.startswith('.') else extracted.suffix[1:],
            'suffix': root_domain
        }

        if subdomain:
            # Has subdomain
            sub_parts = subdomain.split('.')
            base_vars['sub'] = subdomain

            # Multi-level subdomains
            for i, part in enumerate(sub_parts):
                base_vars[f'sub{i+1}'] = part

            inputs.append(base_vars)
        else:
            # No subdomain - generate permutations for root
            base_vars['sub'] = extracted.domain
            inputs.append(base_vars)

        return inputs

    def _enrich_payloads(self, inputs: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Extract words and numbers from input domains for enrichment."""
        enriched_words = set()
        enriched_numbers = set()

        for input_data in inputs:
            domain = input_data.get('sub', '') + '.' + input_data.get('suffix', '')

            if self.config.enrich_words:
                # Extract words
                words = self.extract_words.findall(domain)
                words_only = self.extract_words_only.findall(domain)
                enriched_words.update(words)
                enriched_words.update(words_only)

            if self.config.enrich_numbers:
                # Extract numbers
                numbers = self.extract_numbers.findall(domain)
                enriched_numbers.update(numbers)

        return {
            'words': enriched_words,
            'numbers': enriched_numbers
        }

    def _get_payloads(self) -> Dict[str, List[str]]:
        """Get combined payloads (default + custom + enriched)."""
        payloads = self.default_payloads.copy()

        # Add custom payloads
        if self.config.custom_payloads:
            for key, values in self.config.custom_payloads.items():
                if key in payloads:
                    payloads[key].extend(values)
                else:
                    payloads[key] = values

        return payloads

    def _generate_domain_permutations(
        self,
        input_data: Dict[str, Any],
        patterns: List[str],
        payloads: Dict[str, List[str]]
    ) -> Set[str]:
        """Generate permutations for a single domain input."""
        permutations = set()

        for pattern in patterns:
            try:
                # Replace variables in pattern
                resolved_pattern = self._resolve_pattern(pattern, input_data)

                # Generate permutations based on payload variables
                payload_vars = self._extract_payload_vars(pattern)

                if payload_vars:
                    # Use cluster bomb algorithm for payload variables
                    payload_perms = self._cluster_bomb(payloads, payload_vars)
                    for payload_combo in payload_perms:
                        perm = self._apply_payloads(resolved_pattern, payload_combo)
                        if perm:
                            permutations.add(perm)
                else:
                    # No payload variables, just add the resolved pattern
                    if resolved_pattern and '.' in resolved_pattern:
                        permutations.add(resolved_pattern)

            except Exception as e:
                self.logger.debug(f"Error generating permutation for pattern {pattern}: {e}")

            # Check limit
            if len(permutations) >= self.config.max_permutations:
                break

        return permutations

    def _resolve_pattern(self, pattern: str, input_data: Dict[str, Any]) -> str:
        """Resolve input variables in pattern (sub, suffix, root, etc.)."""
        result = pattern

        # Replace input variables
        for var, value in input_data.items():
            result = result.replace(f"{{{{{var}}}}}", str(value))

        return result

    def _extract_payload_vars(self, pattern: str) -> List[str]:
        """Extract payload variable names from pattern (word, number, region, etc.)."""
        # Find all {{variable}} patterns
        var_pattern = r'\{\{([^}]+)\}\}'
        matches = re.findall(var_pattern, pattern)

        # Filter to payload variables only (not input variables like sub, suffix)
        input_vars = {'sub', 'suffix', 'root', 'tld', 'etld', 'sub1', 'sub2', 'sub3'}
        payload_vars = [m for m in matches if m not in input_vars]

        return payload_vars

    def _cluster_bomb(self, payloads: Dict[str, List[str]], variables: List[str]) -> Iterator[Dict[str, str]]:
        """
        Cluster bomb algorithm to generate all combinations of payload variables.

        This is a simplified version of AlterX's cluster bomb algorithm.
        """
        if not variables:
            yield {}
            return

        # Get payload lists for each variable
        payload_lists = []
        for var in variables:
            payload_list = payloads.get(var, [])
            if not payload_list:
                payload_list = [var]  # Use variable name as fallback
            payload_lists.append(payload_list)

        # Generate all combinations
        for combo in itertools.product(*payload_lists):
            yield dict(zip(variables, combo))

    def _apply_payloads(self, pattern: str, payload_combo: Dict[str, str]) -> Optional[str]:
        """Apply payload values to pattern."""
        result = pattern

        for var, value in payload_combo.items():
            result = result.replace(f"{{{{{var}}}}}", value)

        # Validate result is a proper domain
        if '.' not in result or result.startswith('.') or result.endswith('.'):
            return None

        return result.lower()

    def get_permutation_stats(self, result: PermutationResult) -> Dict[str, Any]:
        """Get statistics about generated permutations."""
        return {
            'domain': result.domain,
            'total_permutations': result.total_generated,
            'patterns_used': result.patterns_used,
            'enriched_words': len(result.enriched_words),
            'enriched_numbers': len(result.enriched_numbers),
            'sample_permutations': list(result.permutations)[:10] if result.permutations else []
        }

    def export_wordlist(self, result: PermutationResult, filename: str) -> None:
        """Export permutations to a wordlist file."""
        try:
            with open(filename, 'w') as f:
                for perm in sorted(result.permutations):
                    f.write(f"{perm}\n")
            self.logger.info(f"Exported {len(result.permutations)} permutations to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to export wordlist: {e}")
