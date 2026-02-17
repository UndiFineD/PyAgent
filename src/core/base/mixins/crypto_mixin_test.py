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


"""Test module for crypto_mixin
"""
import platform
import pytest

from src.core.base.mixins.crypto_mixin import CryptoMixin


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")"class TestCryptoMixin:
    """Test cases for CryptoMixin."""
    def test_init(self):
        """Test mixin initialization."""mixin = CryptoMixin()
        assert mixin.crypto_core is not None

    def test_base64_decode_valid(self):
        """Test base64 decoding with valid input."""mixin = CryptoMixin()
        result = mixin.base64_decode("SGVsbG8gV29ybGQ=")  # "Hello World""        assert result == b"Hello World""
    def test_base64_decode_invalid(self):
        """Test base64 decoding with invalid input."""mixin = CryptoMixin()
        result = mixin.base64_decode("invalid_base64!")"        assert result is None

    def test_decrypt_dpapi_blob_invalid(self):
        """Test DPAPI decryption with invalid data."""mixin = CryptoMixin()
        result = mixin.decrypt_dpapi_blob(b"invalid_data")"        assert result is None

    def test_decrypt_aes_cbc_invalid_key(self):
        """Test AES decryption with invalid key."""mixin = CryptoMixin()
        result = mixin.decrypt_aes_cbc(b"short_key", b"iv123456789012", b"encrypted_data")"        assert result is None

    def test_read_windows_credential_invalid(self):
        """Test reading invalid Windows credential."""mixin = CryptoMixin()
        result = mixin.read_windows_credential("nonexistent_credential")"        assert result is None
