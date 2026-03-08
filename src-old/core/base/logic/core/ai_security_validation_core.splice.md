# Class Breakdown: ai_security_validation_core

**File**: `src\core\base\logic\core\ai_security_validation_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SecurityIssue`

**Line**: 33  
**Methods**: 0

Security issue found in AI interaction

[TIP] **Suggested split**: Move to `securityissue.py`

---

### 2. `SecurityScanResult`

**Line**: 45  
**Methods**: 0

Result from AI security scan

[TIP] **Suggested split**: Move to `securityscanresult.py`

---

### 3. `JailbreakAttempt`

**Line**: 56  
**Methods**: 0

Detected jailbreak attempt

[TIP] **Suggested split**: Move to `jailbreakattempt.py`

---

### 4. `AISecurityValidationCore`

**Line**: 64  
**Methods**: 14

Core for AI/LLM security validation and threat detection.

Based on patterns from ai-security-llm repository, implementing
prompt injection detection, jailbreak prevention, and security assessment.

[TIP] **Suggested split**: Move to `aisecurityvalidationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
