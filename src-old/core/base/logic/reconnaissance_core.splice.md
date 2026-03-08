# Class Breakdown: reconnaissance_core

**File**: `src\core\base\logic\reconnaissance_core.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SubdomainResult`

**Line**: 35  
**Methods**: 1

Result of subdomain enumeration

[TIP] **Suggested split**: Move to `subdomainresult.py`

---

### 2. `ReconConfig`

**Line**: 49  
**Methods**: 1

Configuration for reconnaissance operations

[TIP] **Suggested split**: Move to `reconconfig.py`

---

### 3. `IntelligenceSource`

**Line**: 65  
**Inherits**: ABC  
**Methods**: 1

Abstract base class for intelligence sources

[TIP] **Suggested split**: Move to `intelligencesource.py`

---

### 4. `DNSSource`

**Line**: 80  
**Inherits**: IntelligenceSource  
**Methods**: 2

DNS-based subdomain enumeration using brute force

[TIP] **Suggested split**: Move to `dnssource.py`

---

### 5. `CertificateTransparencySource`

**Line**: 150  
**Inherits**: IntelligenceSource  
**Methods**: 1

Certificate Transparency log enumeration

[TIP] **Suggested split**: Move to `certificatetransparencysource.py`

---

### 6. `ThreatCrowdSource`

**Line**: 191  
**Inherits**: IntelligenceSource  
**Methods**: 1

ThreatCrowd API enumeration

[TIP] **Suggested split**: Move to `threatcrowdsource.py`

---

### 7. `ReconnaissanceCore`

**Line**: 225  
**Methods**: 4

Intelligence gathering and asset discovery core
Combines patterns from alterx (DSL generation) and amass (multi-source intelligence)

[TIP] **Suggested split**: Move to `reconnaissancecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
