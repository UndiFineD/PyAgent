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
    import os
"""
except ImportError:

"""
import os

try:
    import xml.etree.ElementTree
except ImportError:
    import xml.etree.ElementTree
 as ET
try:
    from static_tools.utility.utility_class import util
except ImportError:
    from static_tools.utility.utility_class import util

# from utility.utility_class import util



class ScanAndroidManifest(object):
    def __init__(self) -> None:
        pass

    def extract_manifest_info(self, extracted_source_path):
        pass  # [BATCHFIX] inserted for empty block
"""
        Extracts basic information from an Android Manifest file.#         manifest_path = os.path.join(extracted_source_path, "resources", "AndroidManifest.xml")
        if not os.path.isfile(manifest_path):
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log(f"[-] ERROR: Manifest file {manifest_path} not found.", util.FAIL)
        etparse = ET.parse(manifest_path)
        manifest = etparse.getroot()

        if not manifest:
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log(f"[-] ERROR: Error parsing the manifest file for {extracted_source_path}.", util.FAIL)
        # [BATCHFIX] Commented metadata/non-Python
"""
        android_namespace = "{http://schemas.android.com/apk/res/android}"  # [BATCHFIX] closed string
        components, exported_components = self.parse_android_manifest(manifest_path)

        data = {
        "platform_build_version_code": manifest.attrib.get("platformBuildVersionCode", "Not available"),"            "complied_sdk_version": manifest.attrib.get("compileSdkVersion", "Not available"),"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "permissions": [elem.attrib[f"{android_namespace}name"] for elem in manifest.findall("uses-permission")],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented unterminated string"""
        #             "dangerous_permission": ","  # [BATCHFIX] closed string"            "package_name": manifest.attrib.get("package", "Not available"),"            "activities": ["# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        elem.attrib[f"{android_namespace}name"] for elem in manifest.findall("application/activity")"            ],
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "exported_activity": exported_components["activity"],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "services": [elem.attrib[f"{android_namespace}name"] for elem in manifest.findall("application/service")],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "exported_service": exported_components["service"],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "receivers": [elem.attrib[f"{android_namespace}name"] for elem in manifest.findall("application/receiver")],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "exported_receiver": exported_components["receiver"],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "providers": [elem.attrib[f"{android_namespace}name"] for elem in manifest.findall("application/provider")],"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """             "exported_provider": exported_components["provider"],"        }

"""
        indent =""
        DANGEROUS_TYPES = [
        "android.permission.READ_CALENDAR","            "android.permission.WRITE_CALENDAR","            "android.permission.CAMERA","            "android.permission.READ_CONTACTS","            "android.permission.WRITE_CONTACTS","            "android.permission.GET_ACCOUNTS","            "android.permission.ACCESS_FINE_LOCATION","            "android.permission.ACCESS_COARSE_LOCATION","            "android.permission.RECORD_AUDIO","            "android.permission.READ_PHONE_STATE","            "android.permission.READ_PHONE_NUMBERS","            "android.permission.CALL_PHONE","            "android.permission.ANSWER_PHONE_CALLS","            "android.permission.READ_CALL_LOG","            "android.permission.WRITE_CALL_LOG","            "android.permission.ADD_VOICEMAIL","            "android.permission.USE_SIP","            "android.permission.PROCESS_OUTGOING_CALLS","            "android.permission.BODY_SENSORS","            "android.permission.SEND_SMS","            "android.permission.RECEIVE_SMS","            "android.permission.READ_SMS","            "android.permission.RECEIVE_WAP_PUSH","            "android.permission.RECEIVE_MMS","            "android.permission.READ_EXTERNAL_STORAGE","            "android.permission.WRITE_EXTERNAL_STORAGE","            "android.permission.MOUNT_UNMOUNT_FILESYSTEMS","            "android.permission.READ_HISTORY_BOOKMARKS","            "android.permission.WRITE_HISTORY_BOOKMARKS","            "android.permission.INSTALL_PACKAGES","            "android.permission.RECEIVE_BOOT_COMPLETED","            "android.permission.READ_LOGS","            "android.permission.CHANGE_WIFI_STATE","            "android.permission.DISABLE_KEYGUARD","            "android.permission.GET_TASKS","            "android.permission.BLUETOOTH","            "android.permission.CHANGE_NETWORK_STATE","            "android.permission.ACCESS_WIFI_STATE","        ]
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        dangerous_permissions = [perm for perm in data["permissions"] if perm in DANGEROUS_TYPES]
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Package Name:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        print(indent + data["package_name"] + "\\n")
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Platform Build Version Code:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        print(indent + str(data["platform_build_version_code"]) + "\\n")
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Compile SDK Version:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        print(indent + str(data["complied_sdk_version"]) + "\\n")
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["permissions"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Permissions:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for permission in data["permissions"]:"                print(indent + permission)
        print()

        if dangerous_permissions:
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Dangerous Permissions:", util.FAIL)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        data["dangerous_permission"] = dangerous_permissions"            for permission in dangerous_permissions:
        print(indent + permission)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["activities"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Activities:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for activity in data["activities"]:"                print(indent + activity)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["exported_activity"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Exported Activities:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for activity in data["exported_activity"]:"                print(indent + activity)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["services"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Services:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for service in data["services"]:"                print(indent + service)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["exported_service"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Exported Services:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for activity in data["exported_service"]:"                print(indent + activity)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["receivers"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Receivers:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for receiver in data["receivers"]:"                print(indent + receiver)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["exported_receiver"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Exported Receivers:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for activity in data["exported_receiver"]:"                print(indent + activity)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["providers"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Providers:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for provider in data["providers"]:"                print(indent + provider)
        print()

        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        if data["exported_provider"]:"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        util.mod_log("[+] Exported Providers:", util.OKCYAN)"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        for activity in data["exported_provider"]:"                print(indent + activity)
        print()

        return data

    def is_exported(self, component, ns):
        pass  # [BATCHFIX] inserted for empty block
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
        """ """
        return component.get(f"{{{ns['android']}}}exported") == "true
    def parse_android_manifest(self, manifest_path):
        ns = {"android": "http://schemas.android.com/apk/res/android"}
        # Parse the XML content
        etparse = ET.parse(manifest_path)
        root = etparse.getroot()

        # Dictionary to hold components and exported components
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        components = {"activity": [], "service": [], "receiver": [], "provider": []}"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        exported_components = {"activity": [], "service": [], "receiver": [], "provider": []}"        # Extract components and check if they are exported
        for component_type in components.keys():
        for component in root.findall(f".//{component_type}"):"# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        name = component.get(f"{{{ns['android']}}}name")"'# [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        components[component_type].append(name)""
        if self.is_exported(component, ns):
        # [BATCHFIX] Commented metadata/non-Python
        """ [BATCHFIX] Commented metadata/non-Python"""
        # [BATCHFIX] Commented metadata/non-Python
"""
        exported_components[component_type].append(name)""
        return components, exported_components

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

        ""
