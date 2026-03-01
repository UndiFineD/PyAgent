# Class Breakdown: cloud_asset_discovery_core

**File**: `src\core\base\logic\core\cloud_asset_discovery_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CertificateInfo`

**Line**: 38  
**Methods**: 0

SSL certificate information

[TIP] **Suggested split**: Move to `certificateinfo.py`

---

### 2. `AssetFinding`

**Line**: 54  
**Methods**: 0

Discovered cloud asset

[TIP] **Suggested split**: Move to `assetfinding.py`

---

### 3. `DiscoveryResult`

**Line**: 66  
**Methods**: 0

Result from asset discovery scan

[TIP] **Suggested split**: Move to `discoveryresult.py`

---

### 4. `CloudAssetDiscoveryCore`

**Line**: 75  
**Methods**: 6

Core for discovering cloud assets through SSL certificate inspection.

Based on CloudRecon patterns for finding ephemeral and development assets
by inspecting SSL certificates in IP ranges.

[TIP] **Suggested split**: Move to `cloudassetdiscoverycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
