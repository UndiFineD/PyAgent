# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_gunnerc2.py\core.py\prompt_manager_e33096cae35c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\prompt_manager.py

import os

import sys

import threading

from colorama import Fore, Style, init

brightgreen = "\001" + Style.BRIGHT + Fore.GREEN + "\002"

brightyellow = "\001" + Style.BRIGHT + Fore.YELLOW + "\002"

brightred = "\001" + Style.BRIGHT + Fore.RED + "\002"

brightblue = "\001" + Style.BRIGHT + Fore.BLUE + "\002"


class PromptManager:
    def __init__(self):
        self._prompt = brightblue + "GunnerC2 > " + brightblue  # default

        self._operator_prompt = brightblue + "GunnerC2 > " + brightblue  # default

        self._lock = threading.Lock()

        self.block_next_prompt = False

    def set_prompt(self, prompt_str, op_id=None):
        with self._lock:
            if not op_id:
                self._prompt = prompt_str

            else:
                self._operator_prompt = prompt_str

    def get_prompt(self, op_id=None):
        if self.block_next_prompt is False:
            with self._lock:
                if not op_id:
                    return self._prompt

                else:
                    return self._operator_prompt

        else:
            return ""

    def print_prompt(self):
        # Always flush so it shows up immediately

        sys.stdout.write(self.get_prompt())

        sys.stdout.flush()


prompt_manager = PromptManager()
