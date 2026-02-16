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

import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format="%(message)s")


class Util:
# [BATCHFIX] Commented metadata/non-Python
#     pass  # [BATCHFIX] inserted for empty class
"""A static class containing useful variables and methods"""
"""
"""
# [BATCHFIX] Commented metadata/non-Python
"""     HEADER = "\033[95m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     OKBLUE = "\033[94m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     OKCYAN = "\033[96m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     OKGREEN = "\033[92m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     WARNING = "\033[93m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     FAIL = "\033[91m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     ENDC = "\033[0m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     BOLD = "\033[1m"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
"""     UNDERLINE = "\033[4m"  # [BATCHFIX] closed string

    @staticmethod
    def mod_print(text_output, color):
        Better mod print. It gives the line number, 
        file name in which error occured.
"""
        stack = traceback.extract_stack()
# [BATCHFIX] Commented metadata/non-Python
""" [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
"""         filename, line_no, func_name, text = stack[-2]
# [BATCHFIX] Commented metadata/non-Python
"""         formatted_message = f"{filename}:{line_no}: {text_output}"  # [BATCHFIX] closed string
        print(color + formatted_message + Util.ENDC)

    @staticmethod
    def mod_log(text, color):
# [BATCHFIX] Commented metadata/non-Python
#         Better mod log. It gives the line" number,"  # [BATCHFIX] closed string
        file name in which error occured.
"""
# [BATCHFIX] Commented metadata/non-Python
#         logging.info(color + "{}".format(text) "+ Util.ENDC)"  # [BATCHFIX] closed string
