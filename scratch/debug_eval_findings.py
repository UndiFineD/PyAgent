#!/usr/bin/env python3
"""Debug evaluation findings from security analysis."""

from src.infrastructure.swarm.orchestration.core.self_improvement_core import SelfImprovementCore

FILE_PATH = 'src/infrastructure/storage/kv_transfer/k_vzap.py'
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
core = SelfImprovementCore('.')
findings = core._analyze_security(content, FILE_PATH)  # pylint: disable=protected-access
print('FINDINGS:')
for finding in findings:
    print(finding)
