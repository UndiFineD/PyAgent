# Class Breakdown: federation_services_core

**File**: `src\core\base\logic\core\federation_services_core.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SAMLVersion`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

SAML protocol versions

[TIP] **Suggested split**: Move to `samlversion.py`

---

### 2. `FederationProvider`

**Line**: 46  
**Inherits**: Enum  
**Methods**: 0

Supported federation providers

[TIP] **Suggested split**: Move to `federationprovider.py`

---

### 3. `SignatureAlgorithm`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

SAML signature algorithms

[TIP] **Suggested split**: Move to `signaturealgorithm.py`

---

### 4. `DigestAlgorithm`

**Line**: 62  
**Inherits**: Enum  
**Methods**: 0

SAML digest algorithms

[TIP] **Suggested split**: Move to `digestalgorithm.py`

---

### 5. `FederationService`

**Line**: 70  
**Methods**: 0

AD FS federation service configuration

[TIP] **Suggested split**: Move to `federationservice.py`

---

### 6. `SAMLToken`

**Line**: 85  
**Methods**: 0

SAML security token

[TIP] **Suggested split**: Move to `samltoken.py`

---

### 7. `RelyingParty`

**Line**: 102  
**Methods**: 0

Relying party configuration

[TIP] **Suggested split**: Move to `relyingparty.py`

---

### 8. `FederationUser`

**Line**: 114  
**Methods**: 0

Federated user information

[TIP] **Suggested split**: Move to `federationuser.py`

---

### 9. `TokenGenerationRequest`

**Line**: 125  
**Methods**: 0

Request to generate a SAML token

[TIP] **Suggested split**: Move to `tokengenerationrequest.py`

---

### 10. `FederationServicesCore`

**Line**: 135  
**Methods**: 1

Federation Services Core for AD FS token forgery and SAML management.

Provides comprehensive SAML token generation, signing, and federation
service management based on ADFSpoof methodologies.

[TIP] **Suggested split**: Move to `federationservicescore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
