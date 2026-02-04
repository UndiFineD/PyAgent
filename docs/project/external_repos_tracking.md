# External Repository Tracking

This document tracks the status of external repositories processed from `.external/`.

## Status Legend
- **Ported**: Logic extracted and integrated into PyAgent.
- **Integrated**: Entire tool or significant portion integrated.
- **Harvested**: Data (wordlists, templates) extracted.
- **Ignored**: Reviewed and determined not relevant (educational, binary, obsolete, platform mismatch).
- **Deprecated**: Original repo deleted after processing.

## Batch: 0-9, A

| Repository | Status | Logic Location | Notes |
|------------|--------|----------------|-------|
| 0day-templates | Harvested | `data/templates/nuclei/custom/` | Integrated 0day templates. |
| 0dayex-checker | Ignored | - | PHP/Python scanner, redundant. |
| 0xSojalSec-4o-ghibli-at-home | Ignored | - | Fun project, not relevant. |
| aem-eye | Ignored | - | Redundant AEM scanner. |
| aem-hacker | Ported | `src/logic/agents/security/scanners/cms/aem_hacker.py` | Ported scanner logic. |
| AEnvironment | Ported | `src/core/integrations/mcp/mcp_tool.py` | Extracted MCP tooling logic. |
| aerospace-cybersecurity-resources | Ignored | - | Resource list only. |
| agentheroes | Ignored | - | Game/Fun agent. |
| 0xSojalSec-AirMasifv2 | Ignored | - | Empty/Unknown. |
| 0xSojalSec-AirPosture | Ignored | - | Empty/Unknown. |
| 0xSojalSec-AISuperDomain | Ignored | - | Desktop GUI application. |
| 0xSojalSec-akamai-security-research | Integrated | `src/logic/agents/security/toolkit/rpc/` | Integrated RPC toolkit. Ignored C++ PoCs. |
| 0xSojalSec-all-things-reentrancy | Ignored | - | Educational Foundry repo. |
| 0xSojalSec-AllForOne | Ported | `src/logic/tools/nuclei/template_collector.py` | Logic adapted for tool use. |
| 0xSojalSec-Alphabetfuscation | Ignored | - | C based shellcode obfuscator. |
| 0xSojalSec-alterx | Harvested | `data/wordlists/subdomains/alterx_patterns.yaml` | Extracted permutation patterns. |
| 0xSojalSec-althea | Ignored | - | iOS sideloading GUI. |
| 0xSojalSec-amap | Ignored | - | Obsolete C application mapper. |
| 0xSojalSec-AmsiProvider | Ignored | - | C# AMSI Provider. |
| 0xSojalSec-android-action-kernel | Integrated | `src/logic/agents/android/core/` | Android automation kernel. |
| 0xSojalSec-Android-agent | Ignored | - | Empty repo. |
| 0xSojalSec-android-hacking-101 | Ignored | - | Educational content. |
| 0xSojalSec-android-keylogger | Ignored | - | Malware/Java. |
| 0xSojalSec-android-scanner-ai | Integrated | `src/logic/agents/security/scanners/mobile/android_scanner/` | AI-based APK scanner. |
| 0xSojalSec-android-scripts | Ignored | - | Shell scripts. |
| 0xSojalSec-Android-Security | Ignored | - | Resource list. |
| 0xSojalSec-angularjs-csti-scanner | Integrated | `src/logic/agents/security/scanners/web/angular_csti/` | Angular CSTI scanner. |
| 0xSojalSec-anse | Ignored | - | Web UI/Chat app. |
