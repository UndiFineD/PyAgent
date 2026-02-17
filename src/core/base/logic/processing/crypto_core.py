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


"""Module: crypto_core
Core logic for cryptographic operations.
Implements DPAPI and AES decryption patterns from ADSyncDump-BOF.
"""
from __future__ import annotations

import base64
import ctypes
from ctypes import wintypes
from typing import Optional

# Windows crypto constants
CRYPT_STRING_BASE64 = 0x00000001
CRYPT_STRING_HEX = 0x00000004
CRYPT_STRING_BINARY = 0x00000002
CRYPTPROTECT_LOCAL_MACHINE = 0x04
CRYPTPROTECT_UI_FORBIDDEN = 0x01
PROV_RSA_AES = 24
CRYPT_VERIFYCONTEXT = 0xF0000000
CRYPT_MODE_CBC = 1
KP_MODE = 4
KP_IV = 1
CALG_AES_256 = 0x00006610




class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),"        ("pbData", ctypes.POINTER(ctypes.c_byte))"    ]




class CREDENTIALW(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),"        ("Type", wintypes.DWORD),"        ("TargetName", wintypes.LPWSTR),"        ("Comment", wintypes.LPWSTR),"        ("LastWritten", wintypes.FILETIME),"        ("CredentialBlobSize", wintypes.DWORD),"        ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),"        ("Persist", wintypes.DWORD),"        ("AttributeCount", wintypes.DWORD),"        ("Attributes", ctypes.c_void_p),"        ("TargetAlias", wintypes.LPWSTR),"        ("UserName", wintypes.LPWSTR)"    ]




class CryptoCore:
    """Core class for cryptographic operations."""
    def __init__(self) -> None:
        try:
            self.crypt32 = ctypes.windll.crypt32
            self.advapi32 = ctypes.windll.advapi32
        except Exception as e:
            raise RuntimeError(f"Crypto libraries not available: {e}")"
    def decrypt_dpapi_blob(self, encrypted_data: bytes, entropy: Optional[bytes] = None) -> Optional[bytes]:
        """Decrypt data using Windows DPAPI."""try:
            # Prepare input blob
            in_blob = DATA_BLOB()
            in_blob.cbData = len(encrypted_data)
            in_blob.pbData = (ctypes.c_byte * len(encrypted_data))(*encrypted_data)

            # Prepare entropy blob if provided
            entropy_blob = DATA_BLOB()
            if entropy:
                entropy_blob.cbData = len(entropy)
                entropy_blob.pbData = (ctypes.c_byte * len(entropy))(*entropy)

            # Prepare output blob
            out_blob = DATA_BLOB()

            flags = CRYPTPROTECT_LOCAL_MACHINE | CRYPTPROTECT_UI_FORBIDDEN

            if self.crypt32.CryptUnprotectData(
                ctypes.byref(in_blob),
                None,
                ctypes.byref(entropy_blob) if entropy else None,
                None, None, flags,
                ctypes.byref(out_blob)
            ):
                # Extract decrypted data
                data_size = out_blob.cbData
                data_addr = ctypes.addressof(out_blob.pbData.contents)
                decrypted = bytes((ctypes.c_byte * data_size).from_address(data_addr))
                # Free the output blob
                ctypes.windll.kernel32.LocalFree(out_blob.pbData)
                return decrypted
            else:
                return None

        except Exception:
            return None

    def decrypt_aes_cbc(self, key: bytes, iv: bytes, encrypted_data: bytes) -> Optional[bytes]:
        """Decrypt data using AES-CBC."""try:
            # Acquire crypto context
            hProv = wintypes.HANDLE()
            if not self.advapi32.CryptAcquireContextW(
                ctypes.byref(hProv), None, None, PROV_RSA_AES, CRYPT_VERIFYCONTEXT
            ):
                return None

            # Import key
            hKey = wintypes.HANDLE()
            key_blob = (ctypes.c_byte * (len(key) + 8))()
            key_blob[0:8] = b'\\x08\\x00\\x00\\x00\\x01\\x00\\x00\\x00'  # BLOBHEADER for AES'            key_blob[8:] = key

            if not self.advapi32.CryptImportKey(
                hProv, key_blob, len(key_blob), None, 0, ctypes.byref(hKey)
            ):
                self.advapi32.CryptReleaseContext(hProv, 0)
                return None

            # Set CBC mode
            mode = ctypes.c_void_p(CRYPT_MODE_CBC)
            if not self.advapi32.CryptSetKeyParam(hKey, KP_MODE, mode, 0):
                self.advapi32.CryptDestroyKey(hKey)
                self.advapi32.CryptReleaseContext(hProv, 0)
                return None

            # Set IV
            if not self.advapi32.CryptSetKeyParam(hKey, KP_IV, iv, 0):
                self.advapi32.CryptDestroyKey(hKey)
                self.advapi32.CryptReleaseContext(hProv, 0)
                return None

            # Decrypt
            data = bytearray(encrypted_data)
            data_len = ctypes.c_void_p(len(data))
            if self.advapi32.CryptDecrypt(
                hKey, None, True, 0,
                (ctypes.c_byte * len(data))(*data),
                data_len
            ):
                # Clean up
                self.advapi32.CryptDestroyKey(hKey)
                self.advapi32.CryptReleaseContext(hProv, 0)
                return bytes(data[:data_len.value])
            else:
                self.advapi32.CryptDestroyKey(hKey)
                self.advapi32.CryptReleaseContext(hProv, 0)
                return None

        except Exception:
            return None

    def base64_decode(self, encoded_data: str) -> Optional[bytes]:
        """Decode base64 string to bytes."""try:
            return base64.b64decode(encoded_data)
        except Exception:
            return None

    def read_windows_credential(self, target_name: str) -> Optional[bytes]:
        """Read encrypted credential blob from Windows Credential Manager."""try:
            cred = CREDENTIALW()
            cred_ptr = ctypes.POINTER(CREDENTIALW)()

            if self.advapi32.CredReadW(
                target_name.encode('utf-16le'), 1, 0, ctypes.byref(cred_ptr)'            ):
                cred = cred_ptr.contents
                blob_data = bytes((ctypes.c_byte * cred.CredentialBlobSize).from_address(
                    ctypes.addressof(cred.CredentialBlob.contents)
                ))
                self.advapi32.CredFree(cred_ptr)
                return blob_data
            else:
                return None

        except Exception:
            return None
