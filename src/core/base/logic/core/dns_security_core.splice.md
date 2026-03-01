# Class Breakdown: dns_security_core

**File**: `src\core\base\logic\core\dns_security_core.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DnsRecordType`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

DNS record types

[TIP] **Suggested split**: Move to `dnsrecordtype.py`

---

### 2. `FilterAction`

**Line**: 46  
**Inherits**: Enum  
**Methods**: 0

DNS filtering actions

[TIP] **Suggested split**: Move to `filteraction.py`

---

### 3. `QueryResult`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

DNS query results

[TIP] **Suggested split**: Move to `queryresult.py`

---

### 4. `DnsQuery`

**Line**: 63  
**Methods**: 0

DNS query representation

[TIP] **Suggested split**: Move to `dnsquery.py`

---

### 5. `FilterRule`

**Line**: 76  
**Methods**: 0

DNS filtering rule

[TIP] **Suggested split**: Move to `filterrule.py`

---

### 6. `DnsStatistics`

**Line**: 88  
**Methods**: 0

DNS statistics container

[TIP] **Suggested split**: Move to `dnsstatistics.py`

---

### 7. `DnsSecurityCore`

**Line**: 101  
**Methods**: 3

DNS Security Core for network-level filtering and analysis.

Provides comprehensive DNS filtering, logging, and security analysis
based on AdGuard Home methodologies.

[TIP] **Suggested split**: Move to `dnssecuritycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
