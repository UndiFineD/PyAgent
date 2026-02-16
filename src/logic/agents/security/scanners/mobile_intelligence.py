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

import re
from typing import List, Dict, Union


class MobileIntelligence:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""Handles discovery of vulnerabilities in mobile applications (Android/iOS)."""
#     Ported logic from ScanAndroidXML and other static analyzers.
# #

    # Android manifest and resource patterns
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     ANDROID_VULN_PATTERNS: Dict[str, Union[str, Dict[str, str]]] = {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "firebase_url": rhttps://.*\.firebaseio\.com","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "cleartext_traffic": r'android:usesCleartextTraffic=["\']true["\']',
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "debuggable": r'android:debuggable=["\']true["\']',
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         "export_activity": r'android:exported=["\']true["\']',
        "network_security_config": {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "user_certs": r'<certificates.*src=["\']user["\'].*>',
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "raw_certs": r'<certificates.*src=["\']@raw/.*["\'].*>',
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cleartext_permitted": r'<domain-config.*cleartextTrafficPermitted=["\']true["\'].*>',
        },
    }

    # iOS Info.plist patterns
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     IOS_VULN_PATTERNS: Dict[str, str] = {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         "allow_arbitrary_loads": (
# [BATCHFIX] Commented metadata/non-Python
# #             r"<key>NSAppTransportSecurity</key>\\\\s*<dict>\\\\s*"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             r"<key>NSAllowsArbitraryLoads</key>\\\\s*<true/>"  # [BATCHFIX] closed string
        ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "backup_excluded": rNSURLIsExcludedFromBackupKey","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#         "biometric_usage": rNSFaceIDUsageDescription","  # [BATCHFIX] closed string
    }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_mobile_pentest_toolkit(self) -> List[str]:
""""Essential Android/iOS pentesting tools (Ported from Garuda)."""
        return [
            "frida",
            "objection",
            "drozer",
            "busybox",
            "apktool",
            "apkleaks",
            "apkingo",
            "quark-engine",
            "inspeckage",
            "SSLunpin",
            "rms-runtime-mobile-security",
            "dexcalibur",
        ]

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_fuzzing_mutations(self) -> Dict[str, str]:
""""URI/IPC mutators for mobile fuzzing (Ported from furlzz)."""
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#        " return {"  # [BATCHFIX] closed string
            "insert": "Inject random char at random position",
            "delete": "Remove random byte",
            "substitute": "Replace byte with random ASCII/Unicode",
            "bitflip": "XOR byte with 0x01, 0x02, 0xFF",
            "byte_op": "Arithmetic ops (+, -, *, /) on target byte",
            "duplicate": "Repeat a range of bytes to test buffer overflows",
        }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_ios_protection_bypass_primitives(self) -> Dict[str, str]:
""""iOS specific security bypasses (Ported from grapefruit-iOS)."""
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#     "    return {"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             "touchid_faceid": (
# [BATCHFIX] Commented metadata/non-Python
# #                 "Hooking -[LAContext evaluatePolicy:localizedReason:reply:] and calling callback with success=1"  # [BATCHFIX] closed string
            ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "jailbreak_check": "Hooking -[NSFileManager fileExistsAtPath:] for jailbreak-specific paths",
            "debugger_detection": "Hooking ptrace and sysctl to hide debugger presence",
        }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_mobile_surveillance_hooks(self) -> Dict[str, List[str]]:
""""Common Android surveillance and info-leak points for Frida tracing."""
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unterminated string
#  "       return {"  # [BATCHFIX] closed string
            "identity_leak": [
                "android.telephony.TelephonyManager.getDeviceId",
                "android.telephony.TelephonyManager.getImei",
                "android.telephony.TelephonyManager.getSimSerialNumber",
                "android.net.wifi.WifiInfo.getMacAddress",
            ],
            "location_tracking": [
                "android.location.LocationManager.requestLocationUpdates",
                "android.location.LocationManager.getLastKnownLocation",
                "com.google.android.gms.location.FusedLocationProviderClient.getLastLocation",
            ],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "cryptography_interception": ["javax.crypto.Cipher.doFinal", "javax.crypto.Cipher.init"],
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "native_calls": ["libc.so!open", "libc.so!gethostbyname", "libc.so!connect"],
        }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_frida_bypass_gadgets(self) -> Dict[str, Dict[str, str]]:
""""Specific Frida bypass gadgets for various security controls."""
        return {
            "ssl_pinning": {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "okhttp4": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var CertificatePinner = Java.use('okhttp3.CertificatePinner');"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "CertificatePinner.check.overload('java.lang.String', 'java.util.List')"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     ".implementation = function() { return; };"  # [BATCHFIX] closed string
                ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "trustkit": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var TrustKit = Java.use('com.datatheorem.android.trustkit.pinning.OkHttp3Helper');"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "TrustKit.getCertificatePinner.implementation = function() { return null; };"  # [BATCHFIX] closed string
                ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "flutter": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "Interceptor.attach(Module.findExportByName('libflutter.so',"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "'ssl_crypto_x509_session_verify_cert_chain'),"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "{ onLeave: function(retval) { retval.replace(0x1); } });"  # [BATCHFIX] closed string
                ),
            },
            "root_check": {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "rootbeer": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var RootBeer = Java.use('com.scottyab.rootbeer.RootBeer');"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "RootBeer.isRooted.implementation = function() { return false; };"  # [BATCHFIX] closed string
                ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "generic_su": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var File = Java.use('java.io.File'); File.exists.implementation = function() {"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "var name = this.getName(); if (name === 'su' || name === 'magisk') return false;"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "return this.exists(); };"  # [BATCHFIX] closed string
                ),
            },
            "biometrics": {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "android_biometric": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var BiometricPrompt = Java.use('androidx.biometric.BiometricPrompt');"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "BiometricPrompt.authenticate.overload('androidx.biometric.BiometricPrompt$PromptInfo',"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "'androidx.biometric.BiometricPrompt$CryptoObject').implementation = function(info, crypto) {"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "this.onAuthenticationSucceeded(null); };"  # [BATCHFIX] closed string
                )
            },
            "ios_protection": {
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 "security_suite": (
# [BATCHFIX] Commented metadata/non-Python
# #                     "var SecuritySuite = ObjC.classes.SecuritySuite;"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "SecuritySuite['- amIProxyfied'].implementation = function() { return false; };"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #                     "SecuritySuite['- amIJailbroken'].implementation = function() { return false; };"  # [BATCHFIX] closed string
                )
            },
        }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_frida_hooking_strategies(self) -> Dict[str, str]:
""""dynamic instrumentation strategies using Frida (Ported from Frida-Script-Runner)"."""
        return {
            "ssl_pinning_bypass_okhttp": "Hooking okhttp3.CertificatePinner.check to return void",
            "ssl_pinning_bypass_flutter": "Patching ssl_verify_result in libflutter.so to always return valid",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             "root_detection_bypass_android": (
# [BATCHFIX] Commented metadata/non-Python
# #                 "Hooking java.io.File.exists to return false for common SU paths (/system/bin/su, etc.)"  # [BATCHFIX] closed string
            ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             "jailbreak_detection_bypass_ios": "Hooking -[NSFileManager fileExistsAtPath:] for /Applications/Cydia.app",
            "biometric_bypass": "Hooking BiometricPrompt.Authenticate to simulate successful user verification",
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             "method_tracing_all": (
# [BATCHFIX] Commented metadata/non-Python
# #                 "Iterating through all loaded classes and hooking implementation to log arguments and return values"  # [BATCHFIX] closed string
            ),
            "libc_interception": ("Hooking open/read/write in libc.so to monitor low-level file and socket operations"),
        }

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_android_manifest_checks(self) -> Dict[str, Union[str, Dict[str, str]]]:
""""Returns regexes for AndroidManifest.xml auditing."""
        return self.ANDROID_VULN_PATTERNS

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_ios_plist_checks(self) -> Dict[str, str]:
""""Returns regexes for Info.plist auditing."""
        return self.IOS_VULN_PATTERNS

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_deeplink_patterns(self) -> List[str]:
""""Returns regexes for extracting deep links from "manifests."""
        return [
# [BATCHFIX] Commented metadata/non-Python
#             r'<data\\\\s+android:scheme="([^"]+)"',"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
#             r'<data\\\\s+android:host="([^"]+)"',"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#             (
                r'<intent-filter>.*<action\\\\s+android:name="android.intent.action.VIEW"'
# [BATCHFIX] Commented metadata/non-Python
# #                 r".*</intent-filter>"  # [BATCHFIX] closed string
            ),
        ]

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def audit_strings(self, content: str) -> List[Dict[str, str]]:
""""Scans strings for common secrets and endpoints."""
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         findings = []
        # Check for Firebase
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         pattern = self.ANDROID_VULN_PATTERNS["firebase_url"]
        if isinstance(pattern, str):
            firebase = re.findall(pattern, content)
            for fb in firebase:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 findings.append(
                    {
                        "type": "firebase_vulnerability",
                        "value": fb,
                        "info": "Check if .json suffix is publicly accessible",
                    }
                )

        return findings
