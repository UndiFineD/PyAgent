# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GPT_Vuln-analyzer\components\geo.py
from typing import Any, Optional

import requests


class geo_ip_recon:
    def geoip(key: Optional[str], target: str) -> Any:
        if key is None:
            raise ValueError("KeyNotFound: Key Not Provided")
        assert key is not None  # This will help the type checker
        if target is None:
            raise ValueError("InvalidTarget: Target Not Provided")
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={key}&ip={target}"
        response = requests.get(url)
        content = response.text
        return content
