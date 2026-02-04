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

"""
Data Processing Mixin for PyAgent.

Provides utilities for processing and converting raw data into human-readable formats,
inspired by ADSpider's data transformation patterns.
"""

import datetime
from typing import Any, Dict, List, Optional, Union


class DataProcessingMixin:
    """
    Mixin providing data processing utilities for agents.

    Includes functions for converting binary flags, timestamps, and other
    raw data formats to human-readable representations.
    """

    def convert_user_account_control(self, uac_value: int) -> str:
        """
        Convert Windows User Account Control flags to human-readable format.

        Args:
            uac_value: Integer representing UAC flags

        Returns:
            String with human-readable UAC flags separated by " | "
        """
        uac_flags = [
            "SCRIPT",
            "ACCOUNTDISABLE",
            "HOMEDIR_REQUIRED",
            "LOCKOUT",
            "PASSWD_NOTREQD",
            "PASSWD_CANT_CHANGE",
            "ENCRYPTED_TEXT_PWD_ALLOWED",
            "TEMP_DUPLICATE_ACCOUNT",
            "NORMAL_ACCOUNT",
            "INTERDOMAIN_TRUST_ACCOUNT",
            "WORKSTATION_TRUST_ACCOUNT",
            "SERVER_TRUST_ACCOUNT",
            "DONT_EXPIRE_PASSWORD",
            "MNS_LOGON_ACCOUNT",
            "SMARTCARD_REQUIRED",
            "TRUSTED_FOR_DELEGATION",
            "NOT_DELEGATED",
            "USE_DES_KEY_ONLY",
            "DONT_REQ_PREAUTH",
            "PASSWORD_EXPIRED",
            "TRUSTED_TO_AUTH_FOR_DELEGATION",
            "PARTIAL_SECRETS_ACCOUNT"
        ]

        enabled_flags = []
        for i, flag in enumerate(uac_flags):
            if uac_value & (1 << i):
                enabled_flags.append(flag)

        return " | ".join(enabled_flags) if enabled_flags else "NONE"

    def convert_filetime_to_datetime(self, filetime_value: Union[int, str]) -> datetime.datetime:
        """
        Convert Windows FILETIME to Python datetime.

        Args:
            filetime_value: FILETIME value as int or string

        Returns:
            datetime object
        """
        try:
            filetime = int(filetime_value)
            # FILETIME is in 100-nanosecond intervals since 1601-01-01
            return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=filetime // 10)
        except (ValueError, TypeError):
            return datetime.datetime.min

    def convert_account_expires(self, expires_value: Union[int, str]) -> str:
        """
        Convert account expires timestamp to human-readable format.

        Args:
            expires_value: Expires timestamp

        Returns:
            Human-readable expiration string
        """
        try:
            expires = int(expires_value)
            if expires == 0 or expires > datetime.datetime.max.timestamp() * 1_000_000:
                return "Never Expires"
            # Assuming it's in FILETIME format
            dt = self.convert_filetime_to_datetime(expires)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return "Invalid"

    def process_change_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a change record and add human-readable explanations.

        Args:
            record: Dictionary containing change data

        Returns:
            Enhanced record with explanation field
        """
        record = record.copy()
        attr_name = record.get('attribute_name', '').lower()
        attr_value = record.get('attribute_value')

        explanation = None

        if attr_name == 'useraccountcontrol':
            explanation = self.convert_user_account_control(int(attr_value) if attr_value else 0)
        elif attr_name in ['lastlogontimestamp', 'pwdlastset', 'lockouttime', 'ms-mcs-admpwdexpirationtime']:
            explanation = self.convert_filetime_to_datetime(attr_value) if attr_value else None
        elif attr_name == 'accountexpires':
            explanation = self.convert_account_expires(attr_value) if attr_value else None
        elif attr_name == 'member':
            # For group membership changes
            version = record.get('version', 0)
            explanation = "Added to group" if version % 2 == 1 else "Removed from group"

        if explanation is not None:
            record['explanation'] = explanation

        return record

    def format_change_output(self, changes: List[Dict[str, Any]], format_type: str = 'table') -> str:
        """
        Format change records for output.

        Args:
            changes: List of change records
            format_type: Output format ('table', 'list', 'json')

        Returns:
            Formatted output string
        """
        if format_type == 'json':
            import json
            return json.dumps(changes, indent=2, default=str)

        if format_type == 'list':
            lines = []
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
            obj = str(change.get('object', ''))[:29]
            attr = str(change.get('attribute_name', ''))[:19]
            val = str(change.get('attribute_value', ''))[:19]
            time_str = str(change.get('last_orig_change_time', ''))[:19]
            exp = str(change.get('explanation', ''))[:29]

            lines.append(f"{obj:<30} {attr:<20} {val:<20} {time_str:<20} {exp:<30}")

        return "\n".join(lines)
