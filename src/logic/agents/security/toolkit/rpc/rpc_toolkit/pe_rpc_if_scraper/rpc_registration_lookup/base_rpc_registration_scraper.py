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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from typing import Dict, List, Callable, Union, Optional, Tuple
from abc import abstractmethod, ABCMeta


# [BATCHFIX] Commented metadata/non-Python
""" UNKNOWN_ADDRESS = "unknown_address"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" PARSING_ERROR = "argument_parsing_error"  # [BATCHFIX] closed string"
# [BATCHFIX] Commented metadata/non-Python
""" INTERFACE_FLAGS = "flags"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" INTERFACE_SECURITY_CALLBACK = "security_callback_addr"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" INTERFACE_HAS_DESCRIPTOR = "has_security_descriptor"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" INTERFACE_ADDRESS = "interface_address"  # [BATCHFIX] closed string"

class UnknownRpcServerRegistrationFunctionException(Exception):
    def __init__(self, func_name: str) -> None:
# [BATCHFIX] Commented metadata/non-Python
#         super().__init__(fUnknown RpcServerRegister function {func_name}")"  # [BATCHFIX] closed string"

class DismExtractorFailue(Exception):
    def __init__(self, return_code: int) -> None:
# [BATCHFIX] Commented metadata/non-Python
#         super().__init__(fRunning the dism failed, return code {return_code}")"  # [BATCHFIX] closed string"

class BaseRpcRegistrationExtractor(metaclass=ABCMeta):
    _default_dism_path: str = None

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def __init__(self, dism_path: Optional[str] = None) -> None:""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         self._pe_path: Optional[str] = None""""        self._dism_path = dism_path if dism_path else self._default_dism_path

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def get_rpc_registration_info(self, pe_path: str) -> Dict[str, Dict]:""""        reg_info = {}
        for func_name, func_calls in self._get_rpc_registration_info(pe_path).items():
            for xref, xref_params in func_calls.items():
                parsed_params = self._get_parser_for_func_name(func_name)(xref_params)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                 reg_info[xref] = {""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     INTERFACE_ADDRESS: parsed_params[0],""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     INTERFACE_FLAGS: parsed_params[1],""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     INTERFACE_SECURITY_CALLBACK: parsed_params[2],""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""                     INTERFACE_HAS_DESCRIPTOR: parsed_params[3],""""                }
        return reg_info

    @abstractmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def _get_rpc_registration_info(self, pe_path: str) -> Dict[str, Dict[str, List]]:""""        # This function should use the disassembler and return all rpc registration function calls and their arguments.
        # The output should look like this:
        # {
        #     function_name: {
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         #                        function_xref_addr: [arg1, arg2, arg3...],""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         #                        function_other_xref_addr: [arg1, arg2, arg3...],""""        #                        ...
        #                    }
        # }
        raise NotImplementedError()

    def _get_parser_for_func_name(self, func_name: str) -> Callable:
        if func_name == "RpcServerRegisterIf2" or func_name == "RpcServerRegisterIfEx":"            return self._parse_server_register_ex
        elif func_name == "RpcServerRegisterIf":"            return self._parse_server_register
        elif func_name == "RpcServerRegisterIf3":"            return self._parse_server_register3
        else:
            raise UnknownRpcServerRegistrationFunctionException(func_name)

# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def _parse_server_register_ex(self, args: List) -> Tuple[str, Union[int, str], Optional[str], bool]:""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         return self._formalize_params(rpc_if_addr=args[0], flags=args[3], security_callback=args[-1])""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def _parse_server_register(self, args: List) -> Tuple[str, Union[int, str], Optional[str], bool]:""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         return self._formalize_params(rpc_if_addr=args[0])""""
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     def _parse_server_register3(self, args: List) -> Tuple[str, Union[int, str], Optional[str], bool]:""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         explicit_security_descriptor = args[7] is not None and args[7] != PARSING_ERROR""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         return self._formalize_params(args[0], args[3], args[6], explicit_security_descriptor)""""
    @staticmethod
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented unmatched parenthesis""""#     def _formalize_params(
        rpc_if_addr: str = UNKNOWN_ADDRESS,
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         flags: Union[int, str] = 0,""""# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""         security_callback: Optional[str] = None,""""        explicit_security_descriptor: bool = False,
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     ) -> Tuple[str, Union[int, str], Optional[str], bool]:""""        return rpc_if_addr, flags, security_callback, explicit_security_descriptor
