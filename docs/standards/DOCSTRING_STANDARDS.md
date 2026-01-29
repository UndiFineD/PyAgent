# PyAgent Docstring Standards

## Overview

This document defines the docstring formatting standards for the PyAgent project. Consistent documentation is crucial for maintainability, especially given our goal of preparing the codebase for Rust port compatibility.

## Standards

### 1. Style Guide
- **Primary Style**: Google-style docstrings
- **Fallback**: NumPy-style for numerical/scientific code
- **Consistency**: All docstrings in a file must use the same style

### 2. Module Docstrings

**Required**: Every Python module must have a module-level docstring.

**Format**:
```python
"""
Module description.

This module provides functionality for [brief description].
It includes classes and functions for [main purpose].
"""

# Copyright notice and imports follow...
```

**Rules**:
- Must be the first statement in the file (after copyright header)
- Use triple double quotes (`"""`)
- Brief but descriptive summary
- End with closing triple quotes on their own line

### 3. Function and Method Docstrings

**Required**: Functions with parameters, complex logic, or public API must have docstrings.

**Format** (Google-style):
```python
def process_data(data: List[str], config: Dict[str, Any]) -> bool:
    """
    Process input data according to configuration.

    Args:
        data: List of strings to process.
        config: Configuration dictionary containing processing parameters.

    Returns:
        True if processing succeeded, False otherwise.

    Raises:
        ValueError: If data is empty or config is invalid.
        ProcessingError: If an error occurs during processing.
    """
```

**Rules**:
- One line summary followed by detailed description
- Args section for all parameters
- Returns section for return values (except None returns)
- Raises section for all exceptions that can be raised
- Proper indentation (4 spaces from docstring start)

### 4. Class Docstrings

**Required**: All classes must have docstrings.

**Format**:
```python
class DataProcessor:
    """
    Processes data according to configurable rules.

    This class provides methods for transforming, validating, and
    exporting data in various formats.

    Attributes:
        config: Configuration dictionary for processing rules.
        logger: Logger instance for operation tracking.
    """
```

**Rules**:
- Brief description of class purpose
- Detailed explanation if needed
- Attributes section listing important instance attributes

### 5. Formatting Rules

#### Indentation
- First line of docstring: no indentation
- All subsequent lines: 4 spaces indentation
- Closing triple quotes: no indentation

#### Line Length
- Maximum 120 characters per line (following project max-line-length)
- Break long lines appropriately

#### Sections
- Use proper section headers (Args:, Returns:, Raises:, etc.)
- Empty line before each section
- Consistent formatting within sections

### 6. Content Guidelines

#### Completeness
- Describe what the function/class does, not how it does it
- Include all parameters, return values, and exceptions
- Reference related functions/classes when relevant

#### Clarity
- Use clear, concise language
- Avoid jargon unless well-defined
- Include examples for complex functionality

#### Accuracy
- Keep docstrings synchronized with code changes
- Update when function signatures change
- Remove outdated information

### 7. Special Cases

#### Private Methods
- May omit detailed docstrings if implementation is obvious
- Still require at least a one-line summary

#### Simple Functions
- One-line docstrings acceptable for simple functions
- Example: `"""Calculate the sum of two numbers."""`

#### Property Methods
- Document the property's purpose and type
- Example:
```python
@property
def is_valid(self) -> bool:
    """True if the object is in a valid state."""
```

### 8. Validation

Docstrings are validated using automated tools that check:
- Presence of required docstrings
- Proper formatting and indentation
- Section completeness
- Style consistency

### 9. Tools

#### batch_docstring_formatter.py
- Analyzes Python files for docstring issues
- Can automatically fix common problems
- Supports both validation and correction modes

#### Integration with Fleet Script
- The fleet self-improvement script includes docstring validation
- Automatically flags missing or malformed docstrings
- Integrates with the batch formatter for systematic fixes

### 10. Migration

#### Existing Code
- Gradually migrate existing docstrings to these standards
- Use the batch formatter to identify and fix issues
- Prioritize public APIs and complex functions

#### New Code
- All new code must follow these standards
- Code reviews will enforce docstring requirements
- Automated checks prevent merging non-compliant code

## Examples

### Good Module Docstring
```python
"""
Data processing utilities for PyAgent.

This module contains classes and functions for processing,
transforming, and validating data used throughout the PyAgent system.
"""
```

### Good Function Docstring
```python
def validate_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a configuration dictionary.

    Checks that all required fields are present and have valid values.
    Performs type checking and range validation where applicable.

    Args:
        config: Configuration dictionary to validate.

    Returns:
        Tuple of (is_valid, error_messages). If is_valid is True,
        error_messages will be empty.

    Raises:
        TypeError: If config is not a dictionary.
    """
```

### Good Class Docstring
```python
class ConfigValidator:
    """
    Validates configuration objects against schemas.

    This class provides methods for validating configuration dictionaries
    against predefined schemas, with support for custom validation rules
    and detailed error reporting.

    Attributes:
        schema: Validation schema dictionary.
        strict_mode: If True, unknown fields cause validation failure.
    """
```