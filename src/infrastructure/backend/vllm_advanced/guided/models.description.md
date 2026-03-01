# models

**File**: `src\infrastructure\backend\vllm_advanced\guided\models.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 11 imports  
**Lines**: 169  
**Complexity**: 15 (moderate)

## Overview

Models for guided decoding.

## Classes (4)

### `GuidedMode`

**Inherits from**: Enum

Mode of guided decoding.

### `GuidedConfig`

Configuration for guided decoding.

**Methods** (1):
- `to_sampling_params_kwargs(self)`

### `RegexPattern`

Regex pattern builder for guided decoding.

**Methods** (8):
- `__post_init__(self)`
- `to_guided_config(self)`
- `email(cls)`
- `phone_us(cls)`
- `url(cls)`
- `date_iso(cls)`
- `one_of(cls)`
- `sequence(cls)`

### `ChoiceConstraint`

Choice constraint for limiting output to specific options.

**Methods** (6):
- `__post_init__(self)`
- `to_guided_config(self)`
- `yes_no(cls)`
- `true_false(cls)`
- `sentiment(cls)`
- `rating(cls, min_val, max_val)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
