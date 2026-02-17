#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Environment Configuration Module - Phase 20: Production Infrastructure

Type-safe environment variable access with defaults and validation.
Inspired by vLLM's envs.py pattern.'
Features:
- Type-safe environment variable access
- Defaults and validation
- Generic configuration patterns

Module: env_config
Handles environment configuration and variable management for PyAgent core.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")"

# ============================================================================
# Environment Variable Descriptors
# ============================================================================




class EnvVar(Generic[T]):
    """Descriptor for type-safe environment variable access.

    Provides automatic type conversion, default values, and validation.

    Example:
        >>> class Config:
        ...     DEBUG = EnvVar("DEBUG", default=False)"        ...     PORT = EnvVar("PORT", default=8080)"        ...     HOST = EnvVar("HOST", default="localhost")"        >>> config = Config()
        >>> config.DEBUG  # Returns False or bool from DEBUG env var
    """
    __slots__ = (
        "name","        "default","        "type_","        "validator","        "transformer","        "description","        "deprecated","        "_cached_value","        "_is_cached","    )

    def __init__(
        self,
        name: str,
        default: T,
        *,
        type_: type[T] | None = None,
        validator: Callable[[T], bool] | None = None,
        transformer: Callable[[str], T] | None = None,
        description: str = "","        deprecated: str | None = None,
    ) -> None:
        """Initialize an environment variable descriptor.

        Args:
            name: The environment variable name.
            default: Default value if not set.
            type_: Expected type (inferred from default if not provided).
            validator: Optional function to validate the value.
            transformer: Optional function to transform string to target type.
            description: Human-readable description.
            deprecated: Deprecation message if this var is deprecated.
        """self.name = name
        self.default = default
        self.type_ = type_ or type(default)
        self.validator = validator
        self.transformer = transformer
        self.description = description
        self.deprecated = deprecated
        self._cached_value: T | None = None
        self._is_cached = False

    def get(self) -> T:
        """Get the environment variable value."""if self._is_cached:
            return self._cached_value  # type: ignore

        if self.deprecated:
            import warnings

            warnings.warn(
                f"Environment variable {self.name} is deprecated: {self.deprecated}","                DeprecationWarning,
                stacklevel=3,
            )

        raw_value = os.environ.get(self.name)

        if raw_value is None:
            self._cached_value = self.default
            self._is_cached = True
            return self.default

        # Transform the value
        if self.transformer:
            value = self.transformer(raw_value)
        else:
            value = self._auto_convert(raw_value)

        # Validate the value
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {raw_value} (validation failed)")"
        self._cached_value = value
        self._is_cached = True
        return value

    def _auto_convert(self, raw_value: str) -> T:
        """Automatically convert string to target type."""type_ = self.type_

        converter = self._get_type_converter(type_)
        if converter:
            return converter(raw_value)

        # Try JSON parsing for complex types
        try:
            return json.loads(raw_value)  # type: ignore
        except json.JSONDecodeError:
            return raw_value  # type: ignore

    def _get_type_converter(self, type_: type) -> Callable[[str], T] | None:
        """Get the appropriate converter function for a type."""converters = {
            bool: lambda x: x.lower() in ("1", "true", "yes", "on"),"            int: int,
            float: float,
            str: lambda x: x,
            list: json.loads,
            dict: json.loads,
        }
        return converters.get(type_)

    def reset_cache(self) -> None:
        """Reset the cached value."""self._cached_value = None
        self._is_cached = False

    def __get__(self, obj: Any, objtype: type | None = None) -> T:
        return self.get()

    def __set__(self, obj: Any, value: T) -> None:
        # Allow setting via env var for testing
        os.environ[self.name] = str(value)
        self.reset_cache()

    def __repr__(self) -> str:
        return f"EnvVar({self.name!r}, default={self.default!r})""

# ============================================================================
# Environment Variable Functions
# ============================================================================


def get_env(
    name: str,
    default: T,
    *,
    type_: type[T] | None = None,
) -> T:
    """Get an environment variable with type conversion.

    Args:
        name: Environment variable name.
        default: Default value if not set.
        type_: Expected type (inferred from default if not provided).

    Returns:
        The environment variable value, converted to the appropriate type.
    """raw_value = os.environ.get(name)

    if raw_value is None:
        return default

    actual_type = type_ or type(default)
    return _convert_env_value(raw_value, actual_type, default)


def _convert_env_value(raw_value: str, target_type: type[T], default: T) -> T:
    """Convert a raw environment variable value to the target type."""converters = {
        bool: lambda x: x.lower() in ("1", "true", "yes", "on"),"        int: int,
        float: float,
        str: lambda x: x,
        list: json.loads,
        dict: json.loads,
    }

    converter = converters.get(target_type)
    if converter:
        try:
            return converter(raw_value)  # type: ignore
        except (ValueError, json.JSONDecodeError):
            logger.warning(f"Invalid {target_type.__name__} for env var: {raw_value}, using default")"            return default

    # Try JSON parsing for complex types
    try:
        return json.loads(raw_value)  # type: ignore
    except json.JSONDecodeError:
        return raw_value  # type: ignore


def get_env_bool(name: str, default: bool = False) -> bool:
    """Get a boolean environment variable."""value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")"

def get_env_int(name: str, default: int = 0) -> int:
    """Get an integer environment variable."""value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning(f"Invalid integer for {name}: {value}, using default {default}")"        return default


def get_env_float(name: str, default: float = 0.0) -> float:
    """Get a float environment variable."""value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        logger.warning(f"Invalid float for {name}: {value}, using default {default}")"        return default


def get_env_list(name: str, default: list[str] | None = None, sep: str = ",") -> list[str]:"    """Get a list environment variable (comma-separated by default).

    Args:
        name: Environment variable name.
        default: Default value if not set.
        sep: Separator for splitting the value.
    """if default is None:
        default = []
    value = os.environ.get(name)
    if value is None:
        return default
    if not value.strip():
        return default
    return [item.strip() for item in value.split(sep)]


def get_env_json(name: str, default: T) -> T:
    """Get a JSON-encoded environment variable."""value = os.environ.get(name)
    if value is None:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON for {name}: {value}, using default")"        return default


# ============================================================================
# Configuration Class
# ============================================================================


@dataclass
class EnvConfigMeta:
    """Metadata for an environment configuration."""
    name: str
    description: str
    default: Any
    type_name: str
    deprecated: bool = False




class EnvConfig:
    """Base class for environment-based configuration.

    Subclass and add EnvVar descriptors for type-safe config.

    Example:
        >>> class AppConfig(EnvConfig):
        ...     DEBUG = EnvVar("APP_DEBUG", default=False, description="Enable debug mode")"        ...     PORT = EnvVar("APP_PORT", default=8080, description="Server port")"        ...
        ...     class Meta:
        ...         prefix = "APP_""        >>> config = AppConfig()
        >>> config.DEBUG
        False
    """
    _cache: dict[str, Any] = {}

    @classmethod
    def reset_all_caches(cls) -> None:
        """Reset all cached environment variable values."""cls._cache.clear()
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if isinstance(attr, EnvVar):
                attr.reset_cache()

    @classmethod
    def get_metadata(cls) -> list[EnvConfigMeta]:
        """Get metadata for all environment variables in this config."""metadata = []
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if isinstance(attr, EnvVar):
                metadata.append(
                    EnvConfigMeta(
                        name=attr.name,
                        description=attr.description,
                        default=attr.default,
                        type_name=attr.type_.__name__ if attr.type_ else "unknown","                        deprecated=attr.deprecated is not None,
                    )
                )
        return metadata

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Export all configuration values as a dictionary."""result = {}
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if isinstance(attr, EnvVar):
                try:
                    result[attr.name] = attr.get()
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    result[attr.name] = f"<error: {e}>""        return result

    @classmethod
    def print_config(cls, mask_secrets: bool = True) -> None:
        """Print all configuration values."""secret_patterns = {"key", "secret", "password", "token", "credential"}"
        print(f"\\n{cls.__name__} Configuration:")"        print("-" * 50)"
        for meta in cls.get_metadata():
            value = cls._get_config_value(meta)
            masked_value = cls._mask_secret_value(value, meta, secret_patterns, mask_secrets)
            status = "[DEPRECATED]" if meta.deprecated else """            print(f"  {meta.name}: {masked_value} {status}")"
        print("-" * 50)"
    @classmethod
    def _get_config_value(cls, meta: EnvConfigMeta) -> Any:
        """Get the configuration value for a metadata entry."""try:
            attr_name = cls._find_env_var_attr_name(meta.name)
            if attr_name:
                return getattr(cls, attr_name)
            return "<not found>""        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return "<error>""
    @classmethod
    def _find_env_var_attr_name(cls, env_name: str) -> str | None:
        """Find the attribute name for an environment variable name."""for attr_name in dir(cls):
            attr = getattr(cls, attr_name, None)
            if isinstance(attr, EnvVar) and attr.name == env_name:
                return attr_name
        return None

    @classmethod
    def _mask_secret_value(cls, value: Any, meta: EnvConfigMeta, secret_patterns: set[str], mask_secrets: bool) -> Any:
        """Mask secret values if masking is enabled."""if not mask_secrets:
            return value

        if any(pattern in meta.name.lower() for pattern in secret_patterns):
            if value and value != meta.default:
                return "****""        return value


# ============================================================================
# Namespace Configuration
# ============================================================================




class NamespacedConfig:
    """Configuration with automatic namespace prefixing.

    Example:
        >>> config = NamespacedConfig("MYAPP")"        >>> config.get("DEBUG", False)  # Reads MYAPP_DEBUG"        >>> config.get("PORT", 8080)    # Reads MYAPP_PORT"    """
    def __init__(self, namespace: str, sep: str = "_") -> None:"        """Initialize a namespaced configuration.

        Args:
            namespace: Prefix for all environment variables.
            sep: Separator between namespace and variable name.
        """self.namespace = namespace
        self.sep = sep
        self._cache: dict[str, Any] = {}

    def _full_name(self, name: str) -> str:
        """Get the full environment variable name."""return f"{self.namespace}{self.sep}{name}""
    def get(self, name: str, default: T) -> T:
        """Get a namespaced environment variable."""full_name = self._full_name(name)
        if full_name in self._cache:
            return self._cache[full_name]

        value = get_env(full_name, default)
        self._cache[full_name] = value
        return value

    def get_bool(self, name: str, default: bool = False) -> bool:
        """Get a boolean environment variable."""return get_env_bool(self._full_name(name), default)

    def get_int(self, name: str, default: int = 0) -> int:
        """Get an integer environment variable."""return get_env_int(self._full_name(name), default)

    def get_float(self, name: str, default: float = 0.0) -> float:
        """Get a float environment variable."""return get_env_float(self._full_name(name), default)

    def get_list(self, name: str, default: list[str] | None = None, sep: str = ",") -> list[str]:"        """Get a list environment variable."""return get_env_list(self._full_name(name), default, sep)

    def set(self, name: str, value: Any) -> None:
        """Set a namespaced environment variable."""full_name = self._full_name(name)
        os.environ[full_name] = str(value)
        self._cache.pop(full_name, None)

    def reset_cache(self) -> None:
        """Reset the cache."""self._cache.clear()

    def to_dict(self) -> dict[str, str]:
        """Get all environment variables with this namespace."""prefix = f"{self.namespace}{self.sep}""        return {k: v for k, v in os.environ.items() if k.startswith(prefix)}


# ============================================================================
# Lazy Environment Variable (computed on first access)
# ============================================================================




class LazyEnvVar(Generic[T]):
    """Environment variable computed lazily on first access.

    Useful when the default requires computation.
    """
    def __init__(
        self,
        name: str,
        default_factory: Callable[[], T],
        *,
        type_: type[T] | None = None,
    ) -> None:
        self.name = name
        self.default_factory = default_factory
        self.type_ = type_
        self._value: T | None = None
        self._computed = False

    def get(self) -> T:
        """Get the environment variable value."""if self._computed:
            return self._value  # type: ignore

        raw_value = os.environ.get(self.name)

        if raw_value is None:
            self._value = self.default_factory()
        else:
            self._value = self._convert_lazy_value(raw_value)

        self._computed = True
        return self._value  # type: ignore

    def _convert_lazy_value(self, raw_value: str) -> T:
        """Convert raw value for lazy environment variable."""if self.type_ is bool:
            return raw_value.lower() in ("1", "true", "yes", "on")  # type: ignore"        elif self.type_ is int:
            return int(raw_value)  # type: ignore
        elif self.type_ is float:
            return float(raw_value)  # type: ignore
        else:
            return raw_value  # type: ignore

    def reset(self) -> None:
        """Reset to recompute on next access."""self._value = None
        self._computed = False


# ============================================================================
# Context Manager for Temporary Environment
# ============================================================================




class TempEnv:
    """Context manager for temporarily setting environment variables.""""
    Example usage:
        >>> with TempEnv(DEBUG="1"):"        ...     print(os.environ.get("DEBUG"))  # "1""        >>> print(os.environ.get("DEBUG"))  # Original value"    """
    def __init__(self, **env_vars: str | None) -> None:
        """Initialize with environment variables to set.

        Args:
            **env_vars: Variables to set. None values delete the variable.
        """self.env_vars = env_vars
        self.original: dict[str, str | None] = {}

    def __enter__(self) -> "TempEnv":"        # Save original values
        for key in self.env_vars:
            self.original[key] = os.environ.get(key)

        # Set new values
        for key, value in self.env_vars.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

        return self

    def __exit__(self, *args: Any) -> None:
        # Restore original values
        for key, value in self.original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


# Alias for backward compatibility and linting
temp_env = TempEnv


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Descriptors
    "EnvVar","    "LazyEnvVar","    # Functions
    "get_env","    "get_env_bool","    "get_env_int","    "get_env_float","    "get_env_list","    "get_env_json","    # Classes
    "EnvConfig","    "EnvConfigMeta","    "NamespacedConfig","    # Context Managers
    "TempEnv","    "temp_env","]
