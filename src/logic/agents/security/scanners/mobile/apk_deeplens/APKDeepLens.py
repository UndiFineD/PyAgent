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


import os
import subprocess
import traceback
import sys
import logging
import argparse
import time
import xml.etree.ElementTree as ET
from .static_tools import sensitive_info_extractor, scan_android_manifest
from .report_gen import ReportGen, util as ReportGenUtil

#     Title:      APKDeepLens
#     Desc:       Android security insights in full spectrum.
"""
Author:     Deepanshu Gajbhiye
    Version:    1.0.0
    GitHub URL: https://github.com/d78ui98/APKDeepLens

"""
logging.basicConfig(level=logging.ERROR, format="%(message)s")


class UtilHelper(ReportGenUtil):
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""
A static class for which contain some useful variables and methods
    @staticmethod
    def mod_print(text_output, color):
# [BATCHFIX] Commented metadata/non-Python
#         Better mod print. It gives the line number, file name in which error" occured."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         stack = traceback."extract_stack()"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
filename, line_no, func_name, text = stack[-2]""""
# [BATCHFIX] Commented metadata/non-Python
"""
formatted_message = f"{filename}:{line_no}: {text_output}"  # [BATCHFIX] closed string"        print(color + formatted_message + UtilHelper.ENDC)

    @staticmethod
    def print_logo():
# [BATCHFIX] Commented metadata/non-Python
#         Logo "for APKDeepLens"  # [BATCHFIX] closed string"#         logo = f
{UtilHelper.OKGREEN}           ( )                  (_ )                       "   " {UtilHelper.ENDC}"{UtilHelper.OKGREEN}           _| |  __     __  _ _   | |     __    ___    ___      {UtilHelper.ENDC}
{UtilHelper.OKGREEN}      /'_` | /'_`\\ /'_`\\( '_`\\ | |    /'_`\\/' _ `\\/',__)     {UtilHelper.ENDC}"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'{UtilHelper.OKGREEN}          ( (_| |(  __/(  __/| (_) )| |__ (  __/| ( ) |\\__, \\     {UtilHelper.ENDC}
{UtilHelper.OKGREEN}          `\\__,_)`\\___)`\\___)| ,__/'(____/`\\___)(_) (_)(____/     {UtilHelper.ENDC}"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'{UtilHelper.OKGREEN}                                       | |                                  {UtilHelper.ENDC}
{UtilHelper.OKGREEN}                                       (_)                                  {UtilHelper.ENDC}
{UtilHelper.OKCYAN}                                              - Made By Deepanshu{UtilHelper.ENDC}
        print(logo)


def parse_args():
# [BATCHFIX] Commented metadata/non-Python
#     Parse" command-line arguments."  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
# "    UtilHelper.print_logo()"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser = argparse.ArgumentParser(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         description=("{BOLD}{GREEN}APKDeepLens:{ENDC} Android security insights in full spectrum. ").format("            BOLD=UtilHelper.BOLD, GREEN=UtilHelper.OKCYAN, ENDC=UtilHelper.ENDC
        ),
        epilog=("For more information, visit our GitHub repository - https://github.com/d78ui98/APKDeepLens"),"        formatter_class=argparse.RawTextHelpFormatter,
    )

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
        "-apk","        metavar="APK","        type=str,
        required=True,
        help="Path to the APK file to be analyzed.","    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
        "-v","        "-version","        action="version","        version="APKDeepLens v1.0","        help="Display the version of APKDeepLens.","    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
        "-source_code_path","        metavar="APK","        type=str,
        help="Enter a valid path of extracted source for apk.","    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
        "-report","# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
choices=["json", "pdf", "html", "txt"],"        default="json","        help="Format of the report to be generated. Default is JSON.","    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
# [BATCHFIX] Commented metadata/non-Python
"""         "-o", metavar="output path or file", type=str, help="Output report path (can be filename or dir)"  # [BATCHFIX] closed string"    )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#     parser.add_argument(
        "--ignore_virtualenv","        action="store_true","        help="Ignore virtual environment check.","    )
    parser.add_argument("-l", metavar="log level", help="Set the logging level")"    return parser.parse_args()



class AutoApkScanner(object):
    def __init__(self):
        pass

    def create_dir_to_extract(self, apk_file, extracted_path=None):
# [BATCHFIX] Commented metadata/non-Python
#         Creating a "folder to extract apk source code"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
#         extracted_source_path = os.path.join(os.path.dirname(os.path.abspath"(__file__)), "app_source", apk_file)"  # [BATCHFIX] closed string
        resources_path = os.path.join(extracted_source_path, "resources")"        sources_path = os.path.join(extracted_source_path, "sources")"
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         if (
            os.path.exists(extracted_source_path)
            and os.path.isdir(extracted_source_path)
            and os.path.exists(resources_path)
            and os.path.isdir(resources_path)
            and os.path.exists(sources_path)
            and os.path.isdir(sources_path)
        ):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             UtilHelper.mod_log(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "[+] Source code for apk - {} Already extracted. Skipping this step.".format(apk_file),"                UtilHelper.OKCYAN,
            )
            return {"result": 0, "path": extracted_source_path}"        else:
            os.makedirs(extracted_source_path, exist_ok=True)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#             UtilHelper.mod_log(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "[+] Creating new directory for extracting apk : " + extracted_source_path,"                UtilHelper.OKCYAN,
            )
            return {"result": 1, "path": extracted_source_path}
    def extract_source_code(self, apk_file, target_dir):
 "   "    Extracting source code with Jdax"# [BATCHFIX] Commented metadata/non-Python
#         UtilHelper.mod_log("[+] Extracting the source code "to : " + target_dir, UtilHelper.OKCYAN)"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""
is_windows = os.name == "nt"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
"""
jadx_executable = "jadx.bat" if is_windows else "jadx"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         jadx_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "static_tools","            "jadx","            "bin","            jadx_executable,
        )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
output = subprocess.run([jadx_path, apk_file, "-d", target_dir])"        print(output)

    def return_abs_path(self, path):
    pass  # [BATCHFIX] inserted for empty block
""""   "        Returns the absolute path
""" ""        return os.path.abspath(path)

    def apk_exists(self, apk_filename):
    pass  # [BATCHFIX] inserted for empty block
""        Check if the apk file exists or not.
"""  ""        return os.path.isfile(apk_filename)


if __name__ == "__main__":"    try:
        args = parse_args()

        ignore_virtualenv = args.ignore_virtualenv
        # Check if virtual environment is activated
        if not os.path.exists("/.dockerenv") and not ignore_virtualenv:"            try:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
os.environ["VIRTUAL_ENV"]"            except KeyError:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#                 UtilHelper.mod_log(
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                     "[-] ERROR: Not inside virtualenv. Do source venv/bin/activate","                    UtilHelper.FAIL,
                )
                exit(1)

            if not args.apk:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log("[-] ERROR: Please provide the apk file using the -apk flag.", UtilHelper.FAIL)"                exit(1)

        apk = args.apk

        def is_path_or_filename(apk):
          "  Added function to better handle apk names and apk" paths"            global apk_name, apk_path

            if os.sep in apk:
                apk_name = os.path.basename(apk)  # Extracts the filename from the path
                apk_path = apk
# [BATCHFIX] Commented metadata/non-Python
"""
return "file path"  # [BATCHFIX] closed string"            else:
                apk_name = apk
                apk_path = apk
#                 return "It's just the filename"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string"'
        # Calling function to handle apk names and path.
        is_path_or_filename(apk)

        # Results dict store all the response in json.
        results_dict = {
            "apk_name": apk_name,"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "package_name": ","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "permission": ","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "dangerous_permission": ","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "manifest_analysis": ","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "hardcoded_secrets": ","  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unterminated string"""
#             "insecure_requests": ","  # [BATCHFIX] closed string"        }

        # Creating object for autoapkscanner class
        obj_self = AutoApkScanner()
        apk_file_abs_path = obj_self.return_abs_path(apk_path)
        if not obj_self.apk_exists(apk_file_abs_path):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log(f"[-] ERROR: {apk_file_abs_path} not found.", UtilHelper.FAIL)"            exit(1)
        else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log(f"[+] {apk_file_abs_path} found!", UtilHelper.OKGREEN)"        time.sleep(1)

        # Extracting source code
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis"""
#         target_dir = obj_self.create_dir_to_extract(
            apk_name,
            extracted_path=args.source_code_path if args.source_code_path else None,
        )
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
if target_dir["result"] == 1:"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
obj_self.extract_source_code(apk_file_abs_path, target_dir["path"])
        # Extracting abs path of extracted source code dir
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
extracted_apk_path = obj_self.return_abs_path(target_dir["path"])
        # Extraction useful infomration from android menifest file
        # obj_self.extract_manifest_info(apk_name)
        extracted_source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_source", apk_name)"        manifest_results = scan_android_manifest.ScanAndroidManifest().extract_manifest_info(extracted_source_path)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["package_name"] = manifest_results["package_name"]"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["permission"] = manifest_results["permissions"]"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["dangerous_permission"] = manifest_results["dangerous_permission"]"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["manifest_analysis"] = {"            "activities": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "all": manifest_results["activities"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "exported": manifest_results["exported_activity"],"            },
            "services": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "all": manifest_results["services"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "exported": manifest_results["exported_service"],"            },
            "receivers": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "all": manifest_results["receivers"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "exported": manifest_results["exported_receiver"],"            },
            "providers": {"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "all": manifest_results["providers"],"# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""                 "exported": manifest_results["exported_provider"],"            },
        }

        # Extracting hardcoded secrets
        obj = sensitive_info_extractor.SensitiveInfoExtractor()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log("[+] Reading all file paths ", UtilHelper.OKCYAN)"        file_paths = obj.get_all_file_paths(extracted_apk_path)
        relative_to = extracted_apk_path
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log("[+] Extracting all hardcoded secrets ", UtilHelper.OKCYAN)"        hardcoded_secrets_result = obj.extract_all_sensitive_info(file_paths, relative_to)
        if isinstance(hardcoded_secrets_result, list):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["hardcoded_secrets"] = hardcoded_secrets_result"        else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["hardcoded_secrets"] = []
        # extracting insecure connections
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_log("[+] Extracting all insecure connections ", UtilHelper.OKCYAN)"        all_file_path = obj.get_all_file_paths(extracted_apk_path)
        result = obj.extract_insecure_request_protocol(all_file_path)
        print(result)
        if isinstance(result, list):
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["insecure_requests"] = result"        else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
results_dict["insecure_requests"] = []
        # REPORT GENERATION

        if args.report:
            # Extracting all the required paths
            extracted_source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_source", apk_name)"            res_path = os.path.join(extracted_source_path, "resources")"            source_path = os.path.join(extracted_source_path, "sources")"            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, "report_template.html")
            # Reading the android manifest file.
            android_manifest_path = os.path.join(res_path, "AndroidManifest.xml")"            etparse = ET.parse(android_manifest_path)
            manifest = etparse.getroot()
            # Update the attributes by stripping out the namespace
            for elem in manifest.iter():
                elem.attrib = {
                    k.replace("{http://schemas.android.com/apk/res/android}", "android:"): v"                    for k, v in elem.attrib.items()
                }
            out_path = args.o

            # Creating object for report generation module.
            obj = ReportGen(apk_name, manifest, res_path, source_path, template_path, out_path)

            if args.report == "html":"                obj.generate_html_pdf_report(report_type="html")"            elif args.report == "pdf":"                obj.generate_html_pdf_report(report_type="pdf")"            elif args.report == "json":"                obj.generate_json_report(results_dict)
            elif args.report == "txt":"                obj.generate_txt_report(results_dict)
            else:
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_print("[-] Invalid Report type argument provided", UtilHelper.FAIL)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line_number = exc_traceback.tb_lineno
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python"""
# [BATCHFIX] Commented metadata/non-Python
"""
UtilHelper.mod_print(f"[-] {str(e)} at line {line_number}", UtilHelper.FAIL)"        exit(1)
