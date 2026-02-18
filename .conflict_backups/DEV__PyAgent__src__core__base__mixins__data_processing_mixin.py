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


"""
Data Processing Mixin for PyAgent.

Provides utilities for processing and converting raw data into human-readable formats,
inspired by ADSpider's data transformation patterns.
"""

import datetime
from typing import Any, Dict, List, Union



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
<<<<<<< HEAD
        # Standard UAC flag values
        flags_map = {
            0x0001: "SCRIPT",
            0x0002: "ACCOUNTDISABLE",
            0x0008: "HOMEDIR_REQUIRED",
            0x0010: "LOCKOUT",
            0x0020: "PASSWD_NOTREQD",
            0x0040: "PASSWD_CANT_CHANGE",
            0x0080: "ENCRYPTED_TEXT_PWD_ALLOWED",
            0x0100: "TEMP_DUPLICATE_ACCOUNT",
            0x0200: "NORMAL_ACCOUNT",
            0x0800: "INTERDOMAIN_TRUST_ACCOUNT",
            0x1000: "WORKSTATION_TRUST_ACCOUNT",
            0x2000: "SERVER_TRUST_ACCOUNT",
            0x10000: "DONT_EXPIRE_PASSWORD",
            0x20000: "MNS_LOGON_ACCOUNT",
            0x40000: "SMARTCARD_REQUIRED",
            0x80000: "TRUSTED_FOR_DELEGATION",
            0x100000: "NOT_DELEGATED",
            0x200000: "USE_DES_KEY_ONLY",
            0x400000: "DONT_REQ_PREAUTH",
            0x800000: "PASSWORD_EXPIRED",
            0x1000000: "TRUSTED_TO_AUTH_FOR_DELEGATION",
            0x04000000: "PARTIAL_SECRETS_ACCOUNT"
        }

        enabled_flags = []
        for mask, flag in flags_map.items():
            if uac_value & mask:
                enabled_flags.append(flag)
=======
        # Use explicit mapping of known UAC bitmasks to names (sparse mapping)
        uac_map = {
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
            0x00200000: "DONT_EXPIRE_PASSWORD",
            0x00020000: "SMARTCARD_REQUIRED",
            0x00040000: "TRUSTED_FOR_DELEGATION",
            0x00080000: "NOT_DELEGATED",
        }

        enabled_flags = []
        for bitmask, name in uac_map.items():
            if uac_value & bitmask:
                enabled_flags.append(name)
>>>>>>> copilot/sub-pr-29

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
<<<<<<< HEAD
            # Return UTC datetime to ensure compatibility with comparisons
            base = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
            return base + datetime.timedelta(microseconds=filetime // 10)
=======
            epoch = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
            return epoch + datetime.timedelta(microseconds=filetime // 10)
>>>>>>> copilot/sub-pr-29
        except (ValueError, TypeError):
            return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)

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
<<<<<<< HEAD
            # Use a large threshold for "Never Expires" instead of datetime.max which can fail on Windows
            if expires == 0 or expires > 2650467743999999999:  # Approx AD "Never"
=======
            # Treat very large sentinel values as "Never Expires"
            if expires == 0 or expires >= 2**63 - 1:
>>>>>>> copilot/sub-pr-29
                return "Never Expires"
            # Assuming it's in FILETIME format
            dt = self.convert_filetime_to_datetime(expires)
            return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
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
        elif attr_name == 'size':
            # Human-readable size explanation
            try:
                explanation = f"{int(attr_value)} bytes"
            except Exception:
                explanation = None
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
