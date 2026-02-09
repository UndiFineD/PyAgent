# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\gunnershell\commands\windows\specialcommands\bofcount.py
import logging

logger = logging.getLogger(__name__)

from colorama import Fore, Style

from core.gunnershell.bofs.base import BOFS
from core.gunnershell.commands.base import Command, register

brightgreen = "\001" + Style.BRIGHT + Fore.GREEN + "\002"
reset = Style.RESET_ALL


@register("bofcount")
class BofCountCommand(Command):
    """
    Show how many BOFs are currently loaded in the BOF library.
    """

    @property
    def help(self):
        return "bofcount -- display the number of BOFs loaded into the BOF library"

    def execute(self, args):
        out = self.logic()
        if out:
            print(out)

    def logic(self):
        count = len(BOFS)
        return brightgreen + f"[+] BOFs loaded: {count}" + reset
