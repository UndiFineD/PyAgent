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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

import pytest
from src.infrastructure.swarm.network.censys_intelligence import CensysIntelligence
from src.logic.agents.forensics.file_classifier import FileClassifier
from src.infrastructure.swarm.network.dns_takeover_signatures import DNS_TAKEOVER_SIGNATURES
from src.logic.agents.security.cors_scanner import CORSScanner

@pytest.mark.asyncio
async def test_censys_intel_instantiation():
    ci = CensysIntelligence(api_id="migrated", api_secret="test")
    assert ci.api_id == "migrated"

@pytest.mark.asyncio
async def test_file_classifier_instantiation():
    fc = FileClassifier()
    assert fc.MAGIC_DB_PATH.parts[-1] == "file_magics.json"
    hashes = await fc.analyze_file(__file__)
    assert hashes.size_bytes > 0
    assert "https://" not in hashes.extracted_urls # This file has no urls like that

@pytest.mark.asyncio
async def test_cors_scanner_instantiation():
    scanner = CORSScanner()
    assert "wildcard value" in scanner.DETAILS

def test_dns_takeover_sigs():
    assert "AWS Route 53" in DNS_TAKEOVER_SIGNATURES
    assert len(DNS_TAKEOVER_SIGNATURES) > 10
