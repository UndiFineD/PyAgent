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
    """
    A static class containing useful variables and methods
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def mod_print(text_output, color):
        """
        Better mod print. It gives the line number, 
        file name in which error occured.
        """
        stack = traceback.extract_stack()
        filename, line_no, func_name, text = stack[-2]
        formatted_message = f"{filename}:{line_no}: {text_output}"
        print(color + formatted_message + Util.ENDC)

    @staticmethod
    def mod_log(text, color):
        """
        Better mod log. It gives the line number, 
        file name in which error occured.
        """
        logging.info(color + "{}".format(text) + Util.ENDC)
