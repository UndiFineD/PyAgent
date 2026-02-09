# Extracted from: C:\DEV\PyAgent\.external\agentkit\backend\app\app\utils\exceptions\common_exceptions.py
# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional


class AgentCancelledException(Exception):
    def __init__(
        self,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.headers = headers
