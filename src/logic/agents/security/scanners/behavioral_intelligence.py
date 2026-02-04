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

from typing import Dict, List, Any

class BehavioralIntelligence:
    """
    Intelligence engine for Windows behavioral indicators and TTPs.
    Ported from Fibratus rules and various EDR detection sets.
    """

    @staticmethod
    def get_detection_rules() -> Dict[str, Any]:
        """High-fidelity detection rules for Windows security events."""
        return {
            "RID Hijacking": {
                "description": "Modification of RID (Relative ID) in SAM for low-privilege accounts.",
                "indicators": {
                    "registry_path": r"HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\*\F",
                    "suspicious_processes": ["!lsass.exe"]
                }
            },
            "LSASS Memory Dumping": {
                "description": "Attempting to read LSASS memory or write minidumps.",
                "indicators": {
                    "target_process": r"C:\Windows\System32\lsass.exe",
                    "access_mask": ["ALL_ACCESS", "VM_READ"],
                    "dump_actions": ["write_minidump_file", "comsvcs.dll, MiniDump"]
                }
            },
            "AppDomainManager Injection": {
                "description": "Hijacking .NET CLR search order via AppDomainManager.",
                "indicators": {
                    "env_vars": ["COMPlus_AppDomainManagerType", "COMPlus_AppDomainManagerAsm"]
                }
            },
            "Phantom DLL Hijacking": {
                "description": "Hijacking a DLL that is loaded but missing from disk (e.g., version.dll in some apps).",
                "indicators": {
                    "dll_name": "version.dll",
                    "action": "Creation of known missing DLL in writable application directories"
                }
            },
            "Symbolic Link Creation": {
                "description": "Creation of symbolic links in Object Manager (Defense Evasion).",
                "indicators": {
                    "action": "create_symbolic_link_object",
                    "untrusted": True
                }
            }
        }

    @staticmethod
    def get_persistence_indicators() -> List[Dict[str, str]]:
        """Registry and file system indicators for advanced persistence."""
        return [
            {"path": r"HKCU\Software\Classes\*\shell\open\command", "name": "Registry Shell Command Hijack"},
            {"path": r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options", "name": "IFEO Debugger Hijack"},
            {"path": r"HKLM\SYSTEM\CurrentControlSet\Control\Lsa", "name": "Security Packages / Authentication Packages Persistence"},
            {"path": r"C:\Windows\System32\drivers\etc\hosts", "name": "Hosts File Hijack"}
        ]
