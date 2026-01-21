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

# Ensure the project root is in PYTHONPATH

from __future__ import annotations
from src.core.base.version import VERSION
import os
import sys
import logging
from src.infrastructure.fleet.fleet_manager import FleetManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

__version__ = VERSION


def main() -> None:
    """Perform a comprehensive safety and compliance audit."""
    root = os.getcwd()
    fleet = FleetManager(root)

    logging.info("--- Starting Safety and Compliance Audit ---")

    # 1. Privacy Check (Latest Phase 95)
    logging.info("[Step 1] Privacy Check (PII Detection)")
    # Scan a few key files for PII
    privacy_files = ["src\infrastructure\fleet\fleet_manager.py", "requirements.txt"]
    for pf in privacy_files:
        path = os.path.join(root, pf)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
            res = fleet.privacy_guard.scan_and_redact(content)
            if res["pii_detected"]:
                logging.info(f"  - WARNING: PII found in {pf}")
                for find in res["findings"]:
                    logging.info(f"    - Found {find['type']}")
            else:
                logging.info(f"  - Clean: {pf}")

    # 2. Security Audit (Phase 84)
    logging.info("[Step 2] Security Audit (Secret Scanning)")
    security_findings = fleet.security_audit_agent.scan_file(
        os.path.join(root, "src\infrastructure\fleet\fleet_manager.py")
    )
    if security_findings:
        logging.info(f"  - Found {len(security_findings)} potential security issues.")
        for f in security_findings:
            logging.info(f"    - {f['type']}: {f['detail']} ({f['severity']})")
    else:
        logging.info("  - No critical security issues found in FleetManager.")

    # 3. Compliance Audit (Phase 93)
    logging.info("[Step 3] Compliance Check (SOC2/GDPR)")
    soc2_res = fleet.compliance_audit.run_compliance_check("SOC2")

    logging.info(f"  - SOC2 Compliance Score: {soc2_res['score']}%")
    if soc2_res["failed_checks"]:
        for find in soc2_res["failed_checks"]:
            logging.info(f"    - FAIL: {find['check']}")

    # 4. Code Quality (Phase 87)
    logging.info("[Step 4] Code Quality (Style/Complexity)")
    quality_res = fleet.code_quality_agent.analyze_file_quality(
        os.path.join(root, "src\infrastructure\fleet\fleet_manager.py")
    )
    logging.info(f"  - FleetManager Quality Score: {quality_res['score']}/100")
    if quality_res["issues"]:
        logging.info(f"    - Issues: {len(quality_res['issues'])}")

    logging.info("--- Summary ---")
    logging.info(
        "Safety Audit Complete. The codebase has multiple active monitoring agents in place."
    )


if __name__ == "__main__":
    main()
