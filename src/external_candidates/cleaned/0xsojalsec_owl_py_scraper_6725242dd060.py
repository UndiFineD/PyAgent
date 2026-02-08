# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_owl.py\owl.py\camel.py\toolkits.py\open_api_specs.py\web_scraper.py\paths.py\scraper_6725242dd060.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\camel\toolkits\open_api_specs\web_scraper\paths\scraper.py

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

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

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

"""Scrape data from a website using the Scraper API."""

from typing import Any, Dict

import requests


def call_api(input_json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("https://scraper.gafo.tech/scrape", json=input_json)

    if response.status_code == 200:
        return response.json()

    else:
        return {"status_code": response.status_code, "text": response.text}
