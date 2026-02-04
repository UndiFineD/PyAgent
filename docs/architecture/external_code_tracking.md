Reference for the \.external\ directory analysis and integration into PyAgent.

## Strategy Reference
*   **Active Tracking**: [.external/tracking.md](../../.external/tracking.md) - Contains the active refactoring plan and functional "gaps" to be ported.
*   **Archived Work**: [.external/completed.md](../../.external/completed.md) - Record of all fully integrated or deprecated tools.

## Workflow
1.  See [.external/tracking.md](../../.external/tracking.md) for the granular status of each external repository.
## Workflow
1.  See [.external/tracking.md](../../.external/tracking.md) for the granular status of each external repository.
2.  Code is analyzed for reusable logic.
3.  Logic is refactored into `src/` following architectural standards (Async, Mixins).
4.  Original external code is deleted upon full integration.

## Key Integration Areas
- **Network Intelligence**: DNS, IP, Scanning (Integrating tools like `Neton`, `Amass` logic).
- **Security Agents**: Vulnerability scanning logic.
- **AI Agents**: Prompt templates and agent patterns.
- **Mobile Security**: APK Static Analysis (`APKDeepLens`) and Enumeration (`APKEnum`).
- **Azure Security**: Post-exploitation frameworks (`APEX`).

## Recent Integrations
- **WAF Intelligence**: Ported WAF signatures from `0xSojalSec-dnsresolver` to `src/infrastructure/swarm/network/waf_intelligence.py`.
- **Recon Orchestration**: Ported logic from `0xSojalSec-AutoRecon` to `src/logic/agents/security/external_recon_orchestrator.py`.
- **Pentest Prompts**: Extracted prompts from `0xSojalSec-PentestGPT` to `src/logic/agents/security/pentest_gpt_prompts.py`.
- **Wordlists**: Extracted assets (user-agents, alterations) from `0xSojalSec-amass` to `data/wordlists/`.
- **Mobile Scanner**: Integrated `APKDeepLens` and `APKEnum` to `src/logic/agents/security/scanners/mobile/`.
- **Azure Toolkit**: Integrated `APEX` PowerShell framework to `src/logic/agents/security/toolkit/azure/`.
- **Nuclei**: Integrated `AllForOne` template collector logic.
- **Subdomain Permutations**: Harvested patterns from `alterx`.

## Security Protocol
- Treat `.external` as untrusted.
- Do not execute `.external` code directly.
- Read-only analysis -> Clean implementation in `src`.
