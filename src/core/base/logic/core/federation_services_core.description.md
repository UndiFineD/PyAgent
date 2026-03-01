# federation_services_core

**File**: `src\core\base\logic\core\federation_services_core.py`  
**Type**: Python Module  
**Summary**: 10 classes, 0 functions, 29 imports  
**Lines**: 662  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for federation_services_core.

## Classes (10)

### `SAMLVersion`

**Inherits from**: Enum

SAML protocol versions

### `FederationProvider`

**Inherits from**: Enum

Supported federation providers

### `SignatureAlgorithm`

**Inherits from**: Enum

SAML signature algorithms

### `DigestAlgorithm`

**Inherits from**: Enum

SAML digest algorithms

### `FederationService`

AD FS federation service configuration

### `SAMLToken`

SAML security token

### `RelyingParty`

Relying party configuration

### `FederationUser`

Federated user information

### `TokenGenerationRequest`

Request to generate a SAML token

### `FederationServicesCore`

Federation Services Core for AD FS token forgery and SAML management.

Provides comprehensive SAML token generation, signing, and federation
service management based on ADFSpoof methodologies.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (29):
- `asyncio`
- `base64`
- `cryptography.hazmat.backends.default_backend`
- `cryptography.hazmat.primitives.asymmetric.rsa`
- `cryptography.hazmat.primitives.hashes`
- `cryptography.hazmat.primitives.serialization`
- `cryptography.x509`
- `cryptography.x509.oid.NameOID`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `hashlib`
- `json`
- ... and 14 more

---
*Auto-generated documentation*
