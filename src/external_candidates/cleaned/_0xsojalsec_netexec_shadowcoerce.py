# Extracted from: C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_NetExec_shadowcoerce.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NetExec\nxc\modules\shadowcoerce.py
# NOTE: extracted with static-only rules; review before use
class NXCModule:
    name = "shadowcoerce"
    description = (
        "[REMOVED] Module to check if the target is vulnerable to ShadowCoerce, credit to @Shutdown and @topotam"
    )
    supported_protocols = ["smb"]
    opsec_safe = True
    multiple_hosts = True

    def options(self, context, module_options):
        """
        IPSC             Use IsPathShadowCopied (default: False). ex. IPSC=true
        LISTENER         Listener IP address (default: 127.0.0.1)
        """
        self.ipsc = False
        self.listener = "127.0.0.1"
        if "LISTENER" in module_options:
            self.listener = module_options["LISTENER"]
        if "IPSC" in module_options:
            # Any string that's not empty can be casted to bool True
            self.ipsc = bool(module_options["IPSC"])

    def on_login(self, context, connection):
        context.log.fail('[REMOVED] This module moved to the new module "coerce_plus"')
