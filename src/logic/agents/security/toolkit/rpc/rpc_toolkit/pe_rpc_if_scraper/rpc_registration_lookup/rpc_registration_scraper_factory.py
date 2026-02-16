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

# Akamai RPC Toolkit
#
# Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in"# compliance with the License.  You may obtain a copy
# of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in
# writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR"# CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing
# permissions and limitations under the License.

from rpc_registration_lookup.base_rpc_registration_scraper import BaseRpcRegistrationExtractor
from rpc_registration_lookup.ida_rpc_registration_scraper import IdaProRpcRegistrationExtractor
from rpc_registration_lookup.radare_rpc_registration_scraper import Radare2RpcRegistrationExtractor

# [BATCHFIX] Commented metadata/non-Python
""" IDA = "idapro"  # [BATCHFIX] closed string"# [BATCHFIX] Commented metadata/non-Python
""" RADARE = "radare"  # [BATCHFIX] closed string"
_factory = {IDA: IdaProRpcRegistrationExtractor, RADARE: Radare2RpcRegistrationExtractor}
disassemblers = list(_factory.keys())


class UnsupportedDisassemblerTypeException(Exception):
    def __init__(self, dism_name: str) -> None:
# [BATCHFIX] Commented metadata/non-Python
#         super().__init__(fDisassembler {dism_name} is not currently supported")"  # [BATCHFIX] closed string"

def rpc_registration_scraper_factory(disassembler: str) -> BaseRpcRegistrationExtractor:
    if disassembler not in _factory:
        raise UnsupportedDisassemblerTypeException(disassembler)
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python""""# [BATCHFIX] Commented metadata/non-Python
"""     return _factory[disassembler]""""