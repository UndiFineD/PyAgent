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
from src.core.base.mixins.payload_generator_mixin import PayloadGeneratorMixin


class TestPayloadGeneratorMixin:
    """Test cases for PayloadGeneratorMixin."""
    
    def setup_method(self):
        self.mixin = PayloadGeneratorMixin()
        
    def test_generate_ssrf_rce_payload(self):
        """Test SSRF to RCE payload generation."""
        payload = self.mixin.generate_ssrf_rce_payload('evil.com')
        assert 'evil%2Ecom' in payload  # URL encoded
        assert 'datacenter=http://localhost:4503/xxxx' in payload
        
    def test_generate_xss_payload(self):
        """Test XSS payload generation."""
        # Reflected XSS
        payload = self.mixin.generate_xss_payload('reflected', 0)
        assert '<script>' in payload or '<img' in payload
        
        # SWF XSS
        payload = self.mixin.generate_xss_payload('swf', 0)
        assert 'stagesize' in payload
        
    def test_generate_deserialization_payload(self):
        """Test deserialization payload generation."""
        payload = self.mixin.generate_deserialization_payload()
        assert isinstance(payload, bytes)
        assert len(payload) > 0
        
    def test_generate_groovy_rce_payload(self):
        """Test Groovy RCE payload generation."""
        # Default whoami
        payload = self.mixin.generate_groovy_rce_payload()
        assert 'whoami' in payload
        
        # Custom command
        payload = self.mixin.generate_groovy_rce_payload('id')
        assert 'id' in payload
        
    def test_add_custom_template(self):
        """Test adding custom payload template."""
        template = {'test': 'payload'}
        self.mixin.add_payload_template('custom', template)
        assert self.mixin.get_payload_template('custom') == template
        
    def test_list_templates(self):
        """Test listing payload templates."""
        templates = self.mixin.list_payload_templates()
        assert 'ssrf_rce' in templates
        assert 'xss' in templates
        assert 'groovy_rce' in templates
