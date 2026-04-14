#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Typed exceptions for n8n bridge operations."""


class N8nBridgeError(Exception):
    """Base exception for n8n bridge failures."""


class N8nBridgeConfigError(N8nBridgeError):
    """Raised when bridge runtime configuration is invalid."""


class N8nBridgeValidationError(N8nBridgeError):
    """Raised when bridge payload validation fails."""


class N8nHttpClientError(N8nBridgeError):
    """Raised for non-retryable HTTP transport errors."""
