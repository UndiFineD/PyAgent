# Class Breakdown: rtp_server_core

**File**: `src\infrastructure\transport\rtp_server_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RTPSession`

**Line**: 22  
**Methods**: 0

Represents an active RTP session for a call.

[TIP] **Suggested split**: Move to `rtpsession.py`

---

### 2. `RTPServerCore`

**Line**: 38  
**Methods**: 3

Core logic for handling bidirectional RTP audio streams.
Harvested from .external/Asterisk-AI-Voice-Agent

[TIP] **Suggested split**: Move to `rtpservercore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
