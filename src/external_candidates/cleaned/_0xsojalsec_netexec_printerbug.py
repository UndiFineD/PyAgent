# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_NetExec_printerbug.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NetExec\nxc\modules\printerbug.py
# NOTE: extracted with static-only rules; review before use

class NXCModule:

    name = "printerbug"

    description = "[REMOVED] Module to check if the Target is vulnerable to PrinterBug. Set LISTENER IP for coercion."

    supported_protocols = ["smb"]

    opsec_safe = True

    multiple_hosts = True



    def __init__(self, context=None, module_options=None):

        self.context = context

        self.module_options = module_options

        self.listener = None



    def options(self, context, module_options):

        """LISTENER    Listener Address (defaults to 127.0.0.1)"""

        self.listener = "127.0.0.1"

        if "LISTENER" in module_options:

            self.listener = module_options["LISTENER"]



    def on_login(self, context, connection):

        context.log.fail('[REMOVED] This module moved to the new module "coerce_plus"')