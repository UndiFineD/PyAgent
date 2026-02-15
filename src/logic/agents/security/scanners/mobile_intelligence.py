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
    """
    Handles discovery of vulnerabilities in mobile applications (Android/iOS).
    Ported logic from ScanAndroidXML and other static analyzers.
    """

    # Android manifest and resource patterns
    ANDROID_VULN_PATTERNS: Dict[str, Union[str, Dict[str, str]]] = {
        "firebase_url": r"https://.*\.firebaseio\.com",
        "cleartext_traffic": r'android:usesCleartextTraffic=["\']true["\']',
        "debuggable": r'android:debuggable=["\']true["\']',
        "export_activity": r'android:exported=["\']true["\']',
        "network_security_config": {
            "user_certs": r'<certificates.*src=["\']user["\'].*>',
            "raw_certs": r'<certificates.*src=["\']@raw/.*["\'].*>',
            "cleartext_permitted": r'<domain-config.*cleartextTrafficPermitted=["\']true["\'].*>',
        },
    }

    # iOS Info.plist patterns
    IOS_VULN_PATTERNS: Dict[str, str] = {
        "allow_arbitrary_loads": (
            r"<key>NSAppTransportSecurity</key>\s*<dict>\s*"
            r"<key>NSAllowsArbitraryLoads</key>\s*<true/>"
        ),
        "backup_excluded": r"NSURLIsExcludedFromBackupKey",
        "biometric_usage": r"NSFaceIDUsageDescription",
    }

    def get_mobile_pentest_toolkit(self) -> List[str]:
        """Essential Android/iOS pentesting tools (Ported from Garuda)."""
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

    def get_fuzzing_mutations(self) -> Dict[str, str]:
        """URI/IPC mutators for mobile fuzzing (Ported from furlzz)."""
        return {
            "insert": "Inject random char at random position",
            "delete": "Remove random byte",
            "substitute": "Replace byte with random ASCII/Unicode",
            "bitflip": "XOR byte with 0x01, 0x02, 0xFF",
            "byte_op": "Arithmetic ops (+, -, *, /) on target byte",
            "duplicate": "Repeat a range of bytes to test buffer overflows",
        }

    def get_ios_protection_bypass_primitives(self) -> Dict[str, str]:
        """iOS specific security bypasses (Ported from grapefruit-iOS)."""
        return {
            "touchid_faceid": (
                "Hooking -[LAContext evaluatePolicy:localizedReason:reply:] and calling callback with success=1"
            ),
            "jailbreak_check": "Hooking -[NSFileManager fileExistsAtPath:] for jailbreak-specific paths",
            "debugger_detection": "Hooking ptrace and sysctl to hide debugger presence",
        }

    def get_mobile_surveillance_hooks(self) -> Dict[str, List[str]]:
        """Common Android surveillance and info-leak points for Frida tracing."""
        return {
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
            "cryptography_interception": ["javax.crypto.Cipher.doFinal", "javax.crypto.Cipher.init"],
            "native_calls": ["libc.so!open", "libc.so!gethostbyname", "libc.so!connect"],
        }

    def get_frida_bypass_gadgets(self) -> Dict[str, Dict[str, str]]:
        """Specific Frida bypass gadgets for various security controls."""
        return {
            "ssl_pinning": {
                "okhttp4": (
                    "var CertificatePinner = Java.use('okhttp3.CertificatePinner'); "
                    "CertificatePinner.check.overload('java.lang.String', 'java.util.List')"
                    ".implementation = function() { return; };"
                ),
                "trustkit": (
                    "var TrustKit = Java.use('com.datatheorem.android.trustkit.pinning.OkHttp3Helper'); "
                    "TrustKit.getCertificatePinner.implementation = function() { return null; };"
                ),
                "flutter": (
                    "Interceptor.attach(Module.findExportByName('libflutter.so', "
                    "'ssl_crypto_x509_session_verify_cert_chain'), "
                    "{ onLeave: function(retval) { retval.replace(0x1); } });"
                ),
            },
            "root_check": {
                "rootbeer": (
                    "var RootBeer = Java.use('com.scottyab.rootbeer.RootBeer'); "
                    "RootBeer.isRooted.implementation = function() { return false; };"
                ),
                "generic_su": (
                    "var File = Java.use('java.io.File'); File.exists.implementation = function() { "
                    "var name = this.getName(); if (name === 'su' || name === 'magisk') return false; "
                    "return this.exists(); };"
                ),
            },
            "biometrics": {
                "android_biometric": (
                    "var BiometricPrompt = Java.use('androidx.biometric.BiometricPrompt'); "
                    "BiometricPrompt.authenticate.overload('androidx.biometric.BiometricPrompt$PromptInfo', "
                    "'androidx.biometric.BiometricPrompt$CryptoObject').implementation = function(info, crypto) { "
                    "this.onAuthenticationSucceeded(null); };"
                )
            },
            "ios_protection": {
                "security_suite": (
                    "var SecuritySuite = ObjC.classes.SecuritySuite; "
                    "SecuritySuite['- amIProxyfied'].implementation = function() { return false; }; "
                    "SecuritySuite['- amIJailbroken'].implementation = function() { return false; };"
                )
            },
        }

    def get_frida_hooking_strategies(self) -> Dict[str, str]:
        """dynamic instrumentation strategies using Frida (Ported from Frida-Script-Runner)."""
        return {
            "ssl_pinning_bypass_okhttp": "Hooking okhttp3.CertificatePinner.check to return void",
            "ssl_pinning_bypass_flutter": "Patching ssl_verify_result in libflutter.so to always return valid",
            "root_detection_bypass_android": (
                "Hooking java.io.File.exists to return false for common SU paths (/system/bin/su, etc.)"
            ),
            "jailbreak_detection_bypass_ios": "Hooking -[NSFileManager fileExistsAtPath:] for /Applications/Cydia.app",
            "biometric_bypass": "Hooking BiometricPrompt.Authenticate to simulate successful user verification",
            "method_tracing_all": (
                "Iterating through all loaded classes and hooking implementation to log arguments and return values"
            ),
            "libc_interception": ("Hooking open/read/write in libc.so to monitor low-level file and socket operations"),
        }

    def get_android_manifest_checks(self) -> Dict[str, Union[str, Dict[str, str]]]:
        """Returns regexes for AndroidManifest.xml auditing."""
        return self.ANDROID_VULN_PATTERNS

    def get_ios_plist_checks(self) -> Dict[str, str]:
        """Returns regexes for Info.plist auditing."""
        return self.IOS_VULN_PATTERNS

    def get_deeplink_patterns(self) -> List[str]:
        """Returns regexes for extracting deep links from manifests."""
        return [
            r'<data\s+android:scheme="([^"]+)"',
            r'<data\s+android:host="([^"]+)"',
            (
                r'<intent-filter>.*<action\s+android:name="android.intent.action.VIEW"'
                r".*</intent-filter>"
            ),
        ]

    def audit_strings(self, content: str) -> List[Dict[str, str]]:
        """Scans strings for common secrets and endpoints."""
        findings = []
        # Check for Firebase
        pattern = self.ANDROID_VULN_PATTERNS["firebase_url"]
        if isinstance(pattern, str):
            firebase = re.findall(pattern, content)
            for fb in firebase:
                findings.append(
                    {
                        "type": "firebase_vulnerability",
                        "value": fb,
                        "info": "Check if .json suffix is publicly accessible",
                    }
                )

        return findings
