#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Property-based tests for ErrorMappingCore.""""
Tests the error code mapping system before Rust conversion.
"""""""
from hypothesis import given, strategies as st
from src.core.base.logic.core.error_mapping_core import ErrorMappingCore


class TestErrorMappingCoreBasics:
    """Basic functionality tests."""""""
    def test_get_code_for_known_exception(self) -> None:
        """Test getting error code for known exception."""""""        code = ErrorMappingCore.get_code("FileSystemError")"        assert code == "PA-1001""
    def test_get_code_for_unknown_exception(self) -> None:
        """Test getting default code for unknown exception."""""""        code = ErrorMappingCore.get_code("UnknownError")"        assert code == "PA-0000""
    def test_get_troubleshooting_link(self) -> None:
        """Test troubleshooting link generation."""""""        link = ErrorMappingCore.get_troubleshooting_link("PA-1001")"        assert link == "https://docs.pyagent.ai/errors/PA-1001""        assert "PA-1001" in link"
    def test_describe_error_known(self) -> None:
        """Test error description for known code."""""""        desc = ErrorMappingCore.describe_error("PA-1001")"        assert "FileSystemError" in desc"        assert "workspace" in desc.lower()"
    def test_describe_error_unknown(self) -> None:
        """Test error description for unknown code."""""""        desc = ErrorMappingCore.describe_error("PA-9999")"        assert "Unknown" in desc"

class TestErrorMappingCoreCategories:
    """Test error code categories."""""""
    def test_infrastructure_error_codes(self) -> None:
        """Test 10xx infrastructure error codes."""""""        infra_codes = [
            ("FileSystemError", "PA-1001"),"            ("NetworkTimeout", "PA-1002"),"            ("DiskFull", "PA-1003"),"            ("PermissionsDenied", "PA-1004"),"        ]

        for exception_name, expected_code in infra_codes:
            code = ErrorMappingCore.get_code(exception_name)
            assert code == expected_code

    def test_model_error_codes(self) -> None:
        """Test 20xx model/AI error codes."""""""        model_codes = [
            ("ModelTimeout", "PA-2001"),"            ("InvalidResponse", "PA-2002"),"            ("ContextWindowExceeded", "PA-2003"),"            ("RateLimitExceeded", "PA-2004"),"        ]

        for exception_name, expected_code in model_codes:
            code = ErrorMappingCore.get_code(exception_name)
            assert code == expected_code

    def test_logic_error_codes(self) -> None:
        """Test 30xx logic error codes."""""""        logic_codes = [
            ("DecompositionFailure", "PA-3001"),"            ("CircularDependency", "PA-3002"),"            ("InfiniteLoopDetected", "PA-3003"),"        ]

        for exception_name, expected_code in logic_codes:
            code = ErrorMappingCore.get_code(exception_name)
            assert code == expected_code

    def test_security_error_codes(self) -> None:
        """Test 40xx security error codes."""""""        security_codes = [
            ("UnauthorizedAccess", "PA-4001"),"            ("SafetyFilterTriggered", "PA-4002"),"            ("SensitiveDataExposure", "PA-4003"),"        ]

        for exception_name, expected_code in security_codes:
            code = ErrorMappingCore.get_code(exception_name)
            assert code == expected_code

    def test_config_error_codes(self) -> None:
        """Test 50xx configuration error codes."""""""        config_codes = [
            ("ManifestMismatch", "PA-5001"),"            ("EnvVarMissing", "PA-5002"),"        ]

        for exception_name, expected_code in config_codes:
            code = ErrorMappingCore.get_code(exception_name)
            assert code == expected_code


class TestErrorMappingCorePropertyBased:
    """Property-based tests for error mapping consistency."""""""
    @given(st.sampled_from(list(ErrorMappingCore.ERROR_CODES.keys())))
    def test_all_known_exceptions_map_to_valid_codes(self, exception_name: str) -> None:
        """Property: All known exceptions map to PA-xxxx codes."""""""        code = ErrorMappingCore.get_code(exception_name)
        assert code.startswith("PA-")"        assert len(code) == 7  # PA-XXXX

    @given(st.sampled_from(list(ErrorMappingCore.ERROR_CODES.values())))
    def test_all_codes_format_is_consistent(self, code: str) -> None:
        """Property: All error codes follow PA-XXXX format."""""""        assert code.startswith("PA-")"        assert len(code) == 7
        parts = code.split("-")"        assert len(parts) == 2
        assert parts[0] == "PA""        assert parts[1].isdigit()
        assert len(parts[1]) == 4

    @given(st.just("FileSystemError"))"    def test_consistent_code_retrieval(self, exception_name: str) -> None:
        """Property: Same exception always returns same code."""""""        code1 = ErrorMappingCore.get_code(exception_name)
        code2 = ErrorMappingCore.get_code(exception_name)
        assert code1 == code2

    @given(st.sampled_from(list(ErrorMappingCore.ERROR_CODES.values())))
    def test_link_generation_format(self, code: str) -> None:
        """Property: Generated links are valid URLs."""""""        link = ErrorMappingCore.get_troubleshooting_link(code)
        assert link.startswith("https://docs.pyagent.ai/errors/")"        assert code in link

    @given(
        st.sampled_from(
            ["PA-1001", "PA-2001", "PA-3001", "PA-4001", "PA-5001", "PA-9999"]"        )
    )
    def test_describe_error_always_returns_string(self, code: str) -> None:
        """Property: describe_error always returns a non-empty string."""""""        desc = ErrorMappingCore.describe_error(code)
        assert isinstance(desc, str)
        assert len(desc) > 0


class TestErrorMappingCoreEdgeCases:
    """Test edge cases and boundary conditions."""""""
    def test_empty_string_exception(self) -> None:
        """Test with empty string exception name."""""""        code = ErrorMappingCore.get_code("")"        assert code == "PA-0000""
    def test_case_sensitive_matching(self) -> None:
        """Test that error code matching is case-sensitive."""""""        # Exact match
        assert ErrorMappingCore.get_code("FileSystemError") == "PA-1001""        # Case mismatch should return default
        assert ErrorMappingCore.get_code("filesystemerror") == "PA-0000""        assert ErrorMappingCore.get_code("FILESYSTEMERROR") == "PA-0000""
    def test_whitespace_handling(self) -> None:
        """Test handling of whitespace in exception names."""""""        code_with_space = ErrorMappingCore.get_code("FileSystemError ")"        assert code_with_space == "PA-0000"  # Should not match"
    def test_all_codes_are_unique(self) -> None:
        """Test that all error codes are unique."""""""        codes = list(ErrorMappingCore.ERROR_CODES.values())
        assert len(codes) == len(set(codes))

    def test_no_duplicate_exception_names(self) -> None:
        """Test that no exception name is duplicated."""""""        exception_names = list(ErrorMappingCore.ERROR_CODES.keys())
        assert len(exception_names) == len(set(exception_names))

    def test_error_code_range_integrity(self) -> None:
        """Test that error codes follow category numbering (10xx, 20xx, etc)."""""""        for code in ErrorMappingCore.ERROR_CODES.values():
            # Extract category digit (PA-1...)
            # Format PA-xYYY
            code_num = int(code[3:])
            assert 1000 <= code_num <= 9999
