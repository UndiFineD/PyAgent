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

import aiohttp
import re
from typing import Dict, List, Optional

class CMSIntelligence:
    """Intelligence engine for CMS identification and version detection."""

    FINGERPRINTS = {
        "wordpress": {
            "path": "/wp-links-opml.php",
            "regex": r"generator=\"WordPress/([\d.]+)\"",
            "indicator": "/wp-content/"
        },
        "joomla": {
            "path": "/administrator/manifests/files/joomla.xml",
            "regex": r"<version>([\d.]+)</version>",
            "indicator": "/templates/system/css/system.css"
        },
        "drupal": {
            "path": "/core/install.php",
            "regex": r"Drupal ([\d.]+)",
            "indicator": "/sites/default/"
        },
        "magento": {
            "path": "/js/mage/cookies.js",
            "indicator": "Mage.Cookies"
        },
        "opencart": {
            "path": "/index.php?route=common/home",
            "indicator": "catalog/view/"
        },
        "oscommerce": {
            "path": "/admin/images/cal_date_over.gif",
            "indicator": "osCommerce"
        },
        "prestashop": {
            "path": "/js/jquery/plugins/fancybox/jquery.fancybox.js",
            "indicator": "prestashop"
        }
    }

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session

    async def identify_cms(self, url: str) -> Dict[str, str]:
        """Identify CMS and version from a URL."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        results = {}
        async with self.session.get(url, timeout=10) as resp:
            text = await resp.text()
            
            for cms, data in self.FINGERPRINTS.items():
                if data["indicator"] in text:
                    results["name"] = cms
                    
                    # Try version detection
                    try:
                        async with self.session.get(f"{url.rstrip('/')}{data['path']}", timeout=10) as vresp:
                            vtext = await vresp.text()
                            match = re.search(data["regex"], vtext)
                            if match:
                                results["version"] = match.group(1)
                    except:
                        pass
                    break
        return results
