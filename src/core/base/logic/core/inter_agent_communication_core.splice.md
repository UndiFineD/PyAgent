# Class Breakdown: inter_agent_communication_core

**File**: `src\core\base\logic\core\inter_agent_communication_core.py`  
**Classes**: 19

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Role`

**Line**: 46  
**Inherits**: str, Enum  
**Methods**: 0

Message role enumeration.

[TIP] **Suggested split**: Move to `role.py`

---

### 2. `TaskState`

**Line**: 52  
**Inherits**: str, Enum  
**Methods**: 0

Task execution states.

[TIP] **Suggested split**: Move to `taskstate.py`

---

### 3. `SecuritySchemeType`

**Line**: 61  
**Inherits**: str, Enum  
**Methods**: 0

Supported security scheme types.

[TIP] **Suggested split**: Move to `securityschemetype.py`

---

### 4. `MessagePart`

**Line**: 69  
**Inherits**: BaseModel  
**Methods**: 0

Base class for message parts.

[TIP] **Suggested split**: Move to `messagepart.py`

---

### 5. `TextPart`

**Line**: 76  
**Inherits**: BaseModel  
**Methods**: 0

Text content part.

[TIP] **Suggested split**: Move to `textpart.py`

---

### 6. `FilePart`

**Line**: 84  
**Inherits**: BaseModel  
**Methods**: 0

File content part.

[TIP] **Suggested split**: Move to `filepart.py`

---

### 7. `DataPart`

**Line**: 94  
**Inherits**: BaseModel  
**Methods**: 0

Structured data part.

[TIP] **Suggested split**: Move to `datapart.py`

---

### 8. `Message`

**Line**: 103  
**Inherits**: BaseModel  
**Methods**: 1

Agent message with multi-part content.

[TIP] **Suggested split**: Move to `message.py`

---

### 9. `AgentCapabilities`

**Line**: 120  
**Inherits**: BaseModel  
**Methods**: 0

Agent capabilities declaration.

[TIP] **Suggested split**: Move to `agentcapabilities.py`

---

### 10. `AgentAuthentication`

**Line**: 128  
**Inherits**: BaseModel  
**Methods**: 0

Agent authentication configuration.

[TIP] **Suggested split**: Move to `agentauthentication.py`

---

### 11. `AgentCard`

**Line**: 134  
**Inherits**: BaseModel  
**Methods**: 0

Agent capability and configuration card.

[TIP] **Suggested split**: Move to `agentcard.py`

---

### 12. `TaskStatus`

**Line**: 155  
**Inherits**: BaseModel  
**Methods**: 0

Task execution status.

[TIP] **Suggested split**: Move to `taskstatus.py`

---

### 13. `Task`

**Line**: 164  
**Inherits**: BaseModel  
**Methods**: 0

Agent task representation.

[TIP] **Suggested split**: Move to `task.py`

---

### 14. `JsonRpcRequest`

**Line**: 176  
**Inherits**: BaseModel  
**Methods**: 0

JSON-RPC request structure.

[TIP] **Suggested split**: Move to `jsonrpcrequest.py`

---

### 15. `JsonRpcResponse`

**Line**: 184  
**Inherits**: BaseModel  
**Methods**: 0

JSON-RPC response structure.

[TIP] **Suggested split**: Move to `jsonrpcresponse.py`

---

### 16. `JsonRpcError`

**Line**: 191  
**Inherits**: BaseModel  
**Methods**: 0

JSON-RPC error structure.

[TIP] **Suggested split**: Move to `jsonrpcerror.py`

---

### 17. `A2AMessage`

**Line**: 198  
**Inherits**: BaseModel  
**Methods**: 0

A2A protocol message envelope.

[TIP] **Suggested split**: Move to `a2amessage.py`

---

### 18. `AgentEndpoint`

**Line**: 205  
**Inherits**: BaseModel  
**Methods**: 0

Agent endpoint configuration.

[TIP] **Suggested split**: Move to `agentendpoint.py`

---

### 19. `InterAgentCommunicationCore`

**Line**: 212  
**Inherits**: BaseCore  
**Methods**: 4

Core for inter-agent communication using A2A protocol.

Provides secure, structured communication between agents with:
- Agent discovery and capability negotiation
- JSON-RPC based message passing
- T...

[TIP] **Suggested split**: Move to `interagentcommunicationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
