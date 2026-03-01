# Class Breakdown: c2_framework_core

**File**: `src\core\base\logic\core\c2_framework_core.py`  
**Classes**: 13

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CommunicationProtocol`

**Line**: 32  
**Inherits**: Enum  
**Methods**: 0

C2 communication protocols

[TIP] **Suggested split**: Move to `communicationprotocol.py`

---

### 2. `AgentStatus`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Agent status states

[TIP] **Suggested split**: Move to `agentstatus.py`

---

### 3. `TaskStatus`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

Task execution status

[TIP] **Suggested split**: Move to `taskstatus.py`

---

### 4. `ListenerType`

**Line**: 61  
**Inherits**: Enum  
**Methods**: 0

Listener types

[TIP] **Suggested split**: Move to `listenertype.py`

---

### 5. `C2Profile`

**Line**: 70  
**Methods**: 0

C2 server profile configuration

[TIP] **Suggested split**: Move to `c2profile.py`

---

### 6. `C2Agent`

**Line**: 84  
**Methods**: 0

C2 agent representation

[TIP] **Suggested split**: Move to `c2agent.py`

---

### 7. `C2Listener`

**Line**: 110  
**Methods**: 0

C2 listener configuration

[TIP] **Suggested split**: Move to `c2listener.py`

---

### 8. `C2Task`

**Line**: 126  
**Methods**: 0

C2 task/job representation

[TIP] **Suggested split**: Move to `c2task.py`

---

### 9. `C2Extender`

**Line**: 143  
**Methods**: 0

C2 extender/plugin

[TIP] **Suggested split**: Move to `c2extender.py`

---

### 10. `C2Session`

**Line**: 155  
**Methods**: 0

C2 operator session

[TIP] **Suggested split**: Move to `c2session.py`

---

### 11. `C2Tunnel`

**Line**: 166  
**Methods**: 0

C2 tunnel for pivoting/port forwarding

[TIP] **Suggested split**: Move to `c2tunnel.py`

---

### 12. `C2Framework`

**Line**: 180  
**Methods**: 0

Complete C2 framework state

[TIP] **Suggested split**: Move to `c2framework.py`

---

### 13. `C2FrameworkCore`

**Line**: 194  
**Methods**: 3

C2 Framework Core for command and control operations.

Provides comprehensive C2 capabilities including agent management,
task scheduling, listener operations, and post-exploitation workflows.

[TIP] **Suggested split**: Move to `c2frameworkcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
