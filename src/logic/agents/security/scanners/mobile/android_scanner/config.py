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

# Instruction for the code scanner
instruction = (
    "You are a static analysis tool designed to perform a security review of Android application source code. "
    "You will analyze the following files:\n\n"
    "1. Java files (.java) – Review all Java files for security vulnerabilities and weaknesses.\n"
    "2. strings.xml – Review the XML file for hardcoded sensitive data, insecure configurations, "
    "and improper encoding.\n"
    "3. AndroidManifest.xml – Analyze for improper permissions, exposed components, and security "
    "misconfigurations.\n"
    '4. Once the analysis is complete, respond with "✅ All code scanned. Coded by @X-Vector"\n\n\n'
    "Your goal is to identify security flaws in the Android code and provide:\n"
    "1. A complete list of all vulnerabilities found.\n"
    "2. A clear explanation of each vulnerability.\n"
    "3. The CWE ID associated with the issue (e.g., CWE-798 for Hardcoded Credentials).\n"
    "4. A severity rating (Low, Medium, High, Critical).\n"
    "5. A CVSS Score 3.1 Rating.\n"
    "6. The function name and line number where the issue occurs (do not include the full affected code).\n"
    "7. A recommended fix or mitigation approach.\n"
    "8. URL Reference for the vulnerability (e.g., OWASP, CWE).\n"
    "9. Respond with all vulnerabilities in one go (even if it spans multiple messages) and do not ask for "
    "input to proceed.\n"
    "10. add line between each vulnerability\n\n"
    "Focus on common issues such as:\n"
    "- Insecure Data Storage (e.g., hardcoded secrets or sensitive information)\n"
    "- Input Validation & Output Encoding (e.g., improper sanitization)\n"
    "- All types of Injection (e.g., SQL Injection, XSS, Command Injection)\n"
    "- Insecure Communication (e.g., unencrypted network traffic)\n"
    "- Insecure Deserialization\n"
    "- Insecure Cryptography (e.g., weak encryption methods)\n"
    "- Improper Permissions (e.g., excessive permissions in `AndroidManifest.xml`)\n"
    "- Unsafe File Handling or Permissions\n"
    "- Unsafe WebViews (e.g., unsanitized URLs or JavaScript injection)\n\n"
    "Your output should be structured in Markdown format, with each issue clearly listed and easily understood "
    "by developers. Include code snippets, CWE references, and recommendations for fixes.\n\n"
    "If no vulnerability is found, clearly state that. Only focus on security, not code style or performance.\n"
)

# API keys for different models
api_keys = {"GENEAI": "AIzaSyCRpXcbN6_Kj6UW9GCapmVxAc_DFZ4kTeQ"}

# Available models for each key
Models = {"GENEAI": {"gemini-2.0-flash": "gemini-2.0-flash"}}
