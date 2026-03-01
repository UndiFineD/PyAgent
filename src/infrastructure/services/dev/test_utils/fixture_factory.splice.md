# Class Breakdown: fixture_factory

**File**: `src\infrastructure\services\dev\test_utils\fixture_factory.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `FixtureFactory`

**Line**: 28  
**Methods**: 3

Factory for creating test fixtures.

Creates pre-configured fixtures for tests including agents,
files, and other resources with optional dependencies.

[TIP] **Suggested split**: Move to `fixturefactory.py`

---

### 2. `AgentFixture`

**Line**: 60  
**Methods**: 1

Fixture representing a pre-configured agent for testing.

[TIP] **Suggested split**: Move to `agentfixture.py`

---

### 3. `FileFixture`

**Line**: 86  
**Methods**: 2

Fixture representing a file to be created during test setup.

[TIP] **Suggested split**: Move to `filefixture.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
