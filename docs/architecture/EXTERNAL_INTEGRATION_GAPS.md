# External Intelligence Gaps & Lessons Learned

This document tracks identified functionality gaps between external security tools and the current PyAgent `src/` implementation, along with architectural lessons learned during the porting process.

## Functionality Gaps

| Category | Gap Description | Source Tool(s) | Priority |
| :--- | :--- | :--- | :--- |
| **Response Validation** | Automated headless browser verification for CRLF, XSS, and Open Redirect to eliminate false positives. | `crlfmap`, `XSLeaker` | High |
| **Mail Security** | Automated SPF/DKIM/DMARC configuration auditing and spoofing probability calculation. | `Artemis` | Medium |
| **CMS Intelligence** | Deep, version-specific vulnerability detection for WordPress, Joomla, and Drupal. | `attacking-drupal`, `Vulnerable-WordPress` | Medium |
| **SQLi Automation** | Automated generation of tamper scripts based on detected WAF/Filter signatures. | `Atlas`, `sqlmap` | Low |
| **Active Directory** | Comprehensive Python-based implementation of complex AD attacks (Porting C# logic safely). | `SharpRDP`, `PassTheCert` | Low (Security Risk) |
| **JS Sandbox** | Secure execution of extracted JS code to deobfuscate hidden endpoints or secrets. | `jsluice`, `jscythe` | Medium |

## Architectural Lessons Learned

1. **Transactional FS is Critical**: When porting tools that generate many artifacts (e.g., wordlist generators), using `StateTransaction` prevents workspace clutter and ensures atomic rollback.
2. **Regex Limitations**: Secret extraction via regex (as in `js_intelligence.py`) is high-speed but prone to entropy-based false positives. Entropy-based scanning should supplement regex.
3. **Async IO vs. Subprocess**: Many tools (`subjack`, `RustScan`) are preferred in their native Go/Rust binaries for performance. Porting logic to Python usually requires a `rust_core` implementation to maintain comparable throughput.
4. **Credential Safety**: External tools often hardcode API keys or require them in plain text. PyAgent must enforce the use of `SecretVault` for any ported logic involving cloud or OSINT APIs.

## Logic Porting Strategy

- **Phase 1: Fingerprints/Signatures**: Port regex, headers, and known vulnerabilities (E.g., `dns_takeover_signatures.py`).
- **Phase 2: Execution Logic**: Port the orchestration (E.g., `recon_intelligence.py`).
- **Phase 3: Performance Optimization**: Move bottleneck logic (hashing, scanning) to `rust_core/`.
