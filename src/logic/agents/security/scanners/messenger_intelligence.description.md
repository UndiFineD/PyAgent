# messenger_intelligence

**File**: `src\logic\agents\security\scanners\messenger_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 54  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for messenger_intelligence.

## Classes (1)

### `MessengerIntelligence`

Handles discovery and OSINT for messenger platforms (Telegram, Discord, etc.).
Ported logic from various Telegram OSINT tools.

**Methods** (4):
- `get_telegram_recon_endpoints(self, username)`
- `get_discord_patterns(self)`
- `get_telegram_nearby_params(self)`
- `audit_bot_token(self, token)`

## Dependencies

**Imports** (4):
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
