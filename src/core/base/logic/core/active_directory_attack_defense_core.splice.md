# Class Breakdown: active_directory_attack_defense_core

**File**: `src\core\base\logic\core\active_directory_attack_defense_core.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `KillChainPhase`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Active Directory Kill Chain phases

[TIP] **Suggested split**: Move to `killchainphase.py`

---

### 2. `AttackTechnique`

**Line**: 44  
**Inherits**: Enum  
**Methods**: 0

Common AD attack techniques

[TIP] **Suggested split**: Move to `attacktechnique.py`

---

### 3. `DefenseControl`

**Line**: 65  
**Inherits**: Enum  
**Methods**: 0

Defense and detection controls

[TIP] **Suggested split**: Move to `defensecontrol.py`

---

### 4. `AttackVector`

**Line**: 78  
**Methods**: 0

Represents an attack vector in AD

[TIP] **Suggested split**: Move to `attackvector.py`

---

### 5. `DefenseAssessment`

**Line**: 92  
**Methods**: 0

Assessment of defensive controls

[TIP] **Suggested split**: Move to `defenseassessment.py`

---

### 6. `KillChainAnalysis`

**Line**: 104  
**Methods**: 0

Analysis of AD kill chain progression

[TIP] **Suggested split**: Move to `killchainanalysis.py`

---

### 7. `SecurityPosture`

**Line**: 119  
**Methods**: 0

Overall AD security posture assessment

[TIP] **Suggested split**: Move to `securityposture.py`

---

### 8. `ActiveDirectoryAttackDefenseCore`

**Line**: 132  
**Methods**: 1

Active Directory Attack & Defense Core for comprehensive AD security analysis.

Provides kill chain analysis, attack simulation, defense assessment,
and security posture evaluation based on AD-Attack-...

[TIP] **Suggested split**: Move to `activedirectoryattackdefensecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
