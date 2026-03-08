# Class Breakdown: a2a_communication

**File**: `src\core\base\logic\a2a_communication.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `MessageType`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Types of inter-agent messages.

[TIP] **Suggested split**: Move to `messagetype.py`

---

### 2. `AgentCapability`

**Line**: 48  
**Inherits**: Enum  
**Methods**: 0

Standard agent capabilities.

[TIP] **Suggested split**: Move to `agentcapability.py`

---

### 3. `AgentSkill`

**Line**: 60  
**Inherits**: BaseModel  
**Methods**: 0

Represents a specific skill an agent can perform.

[TIP] **Suggested split**: Move to `agentskill.py`

---

### 4. `AgentCard`

**Line**: 69  
**Inherits**: BaseModel  
**Methods**: 1

Agent identity and capability card for A2A communication.

[TIP] **Suggested split**: Move to `agentcard.py`

---

### 5. `AgentCapabilities`

**Line**: 88  
**Inherits**: BaseModel  
**Methods**: 0

Agent capability flags.

[TIP] **Suggested split**: Move to `agentcapabilities.py`

---

### 6. `A2AMessage`

**Line**: 95  
**Inherits**: BaseModel  
**Methods**: 0

Standard A2A message format.

[TIP] **Suggested split**: Move to `a2amessage.py`

---

### 7. `A2AResponse`

**Line**: 108  
**Inherits**: BaseModel  
**Methods**: 0

Standard A2A response format.

[TIP] **Suggested split**: Move to `a2aresponse.py`

---

### 8. `AgentProtocol`

**Line**: 118  
**Inherits**: Protocol  
**Methods**: 1

Protocol that all agents must implement for A2A communication.

[TIP] **Suggested split**: Move to `agentprotocol.py`

---

### 9. `MessageRouter`

**Line**: 135  
**Methods**: 3

Routes messages between agents in the A2A network.

[TIP] **Suggested split**: Move to `messagerouter.py`

---

### 10. `A2ACommunicationMixin`

**Line**: 246  
**Methods**: 3

Mixin class that adds A2A communication capabilities to agents.

[TIP] **Suggested split**: Move to `a2acommunicationmixin.py`

---

### 11. `SimpleA2AAgent`

**Line**: 410  
**Inherits**: A2ACommunicationMixin  
**Methods**: 1

Simple example agent that can respond to basic requests.

[TIP] **Suggested split**: Move to `simplea2aagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
