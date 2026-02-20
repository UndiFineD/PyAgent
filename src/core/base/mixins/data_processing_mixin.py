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



"""Data Processing Mixin for PyAgent.

Provides utilities for processing and converting raw data into human-readable formats.
This is a small, well-tested shim used by unit tests.
"""

import datetime
from typing import Any, Dict, List, Union


class DataProcessingMixin:
    """Mixin providing data processing utilities for agents.

    Includes functions for converting binary flags, timestamps, and other
    raw data formats to human-readable representations.
    """

    UAC_MAP = {
        0x0001: "SCRIPT",
        0x0002: "ACCOUNTDISABLE",
        0x0008: "LOCKOUT",
        0x0010: "PASSWD_NOTREQD",
        0x0020: "PASSWD_CANT_CHANGE",
        0x0040: "ENCRYPTED_TEXT_PWD_ALLOWED",
        0x0080: "TEMP_DUPLICATE_ACCOUNT",
        0x0200: "NORMAL_ACCOUNT",
        0x0400: "INTERDOMAIN_TRUST_ACCOUNT",
        0x0800: "WORKSTATION_TRUST_ACCOUNT",
        0x1000: "SERVER_TRUST_ACCOUNT",
        0x00020000: "SMARTCARD_REQUIRED",
        0x00040000: "TRUSTED_FOR_DELEGATION",
        0x00080000: "NOT_DELEGATED",
        0x00200000: "DONT_EXPIRE_PASSWORD",
    }

    def convert_user_account_control(self, uac_value: int) -> str:
        enabled = [name for bit, name in self.UAC_MAP.items() if uac_value & bit]
        return " | ".join(enabled) if enabled else "NONE"

    def convert_filetime_to_datetime(self, filetime_value: Union[int, str]) -> datetime.datetime:
        try:
            filetime = int(filetime_value)
            # FILETIME is in 100-nanosecond intervals since 1601-01-01
            epoch = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
            return epoch + datetime.timedelta(microseconds=filetime // 10)
        except (ValueError, TypeError):
            return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)

    def convert_account_expires(self, expires_value: Union[int, str]) -> str:
        try:
            expires = int(expires_value)
            # Treat sentinel values as never expires
            if expires == 0 or expires >= 2**62:
                return "Never Expires"
            dt = self.convert_filetime_to_datetime(expires)
            return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        except (ValueError, TypeError):
            return "Invalid"

    def process_change_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        rec = record.copy()
        attr_name = rec.get("attribute_name", "").lower()
        attr_value = rec.get("attribute_value")
        explanation = None

        if attr_name == "useraccountcontrol":
            explanation = self.convert_user_account_control(int(attr_value) if attr_value else 0)
        elif attr_name == "size":
            try:
                explanation = f"{int(attr_value)} bytes"
            except Exception:
                explanation = None
        elif attr_name in ["lastlogontimestamp", "pwdlastset", "lockouttime", "ms-mcs-admpwdexpirationtime"]:
            explanation = self.convert_filetime_to_datetime(attr_value) if attr_value else None
        elif attr_name == "accountexpires":
            explanation = self.convert_account_expires(attr_value) if attr_value else None
        elif attr_name == "member":
            version = rec.get("version", 0)
            explanation = "Added to group" if version % 2 == 1 else "Removed from group"

        if explanation is not None:
            rec["explanation"] = explanation
        return rec

    def format_change_output(self, changes: List[Dict[str, Any]], format_type: str = "table") -> str:
        if format_type == "json":
            import json

            return json.dumps(changes, indent=2, default=str)

        if format_type == "list":
            lines: List[str] = []
            for change in changes:
                lines.append(f"Object: {change.get('object', 'N/A')}")
                lines.append(f"Attribute: {change.get('attribute_name', 'N/A')}")
                lines.append(f"Value: {change.get('attribute_value', 'N/A')}")
                lines.append(f"Time: {change.get('last_orig_change_time', 'N/A')}")
                lines.append(f"Explanation: {change.get('explanation', 'N/A')}")
                lines.append("-" * 50)
            return "\n".join(lines)

        # Default table format
        header = f"{'Object':<30} {'Attribute':<20} {'Value':<20} {'Time':<20} {'Explanation':<30}"
        lines = [header, "-" * len(header)]
        for change in changes:
            obj = str(change.get("object", ""))[:29]
            attr = str(change.get("attribute_name", ""))[:19]
            val = str(change.get("attribute_value", ""))[:19]
            time_str = str(change.get("last_orig_change_time", ""))[:19]
            exp = str(change.get("explanation", ""))[:29]
            lines.append(f"{obj:<30} {attr:<20} {val:<20} {time_str:<20} {exp:<30}")
        return "\n".join(lines)








