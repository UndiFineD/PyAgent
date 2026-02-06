# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\modules\windows\x64\basic_info\whoami.py
from colorama import Fore, Style, init

from core import session_manager, shell
from core.module_base import ModuleBase

brightgreen = "\001" + Style.BRIGHT + Fore.GREEN + "\002"
brightyellow = "\001" + Style.BRIGHT + Fore.YELLOW + "\002"
brightred = "\001" + Style.BRIGHT + Fore.RED + "\002"
brightblue = "\001" + Style.BRIGHT + Fore.BLUE + "\002"


class WhoamiModule(ModuleBase):
    def __init__(self):
        super().__init__()
        self.name = "whoami"
        self.description = "Runs 'whoami' on a remote session (HTTP or TCP)"
        self.options = {
            "session": {
                "description": "Target session ID or alias",
                "required": True,
                "value": "",
            }
        }

    def run(self):
        sid_input = self.options["session"]["value"]

        if not sid_input:
            print(brightred + "[!] You must set a session ID first (set session <sid>)")
            return

        sid = session_manager.resolve_sid(sid_input)

        if not sid or sid not in session_manager.sessions:
            print(brightred + f"[!] Invalid session: {sid_input}")
            return

        session = session_manager.sessions[sid]
        meta = session.metadata
        os_type = meta.get("os", "").lower()

        print(brightyellow + f"[*] Running 'whoami' on {sid}")

        try:
            if session_manager.is_http_session(sid):
                output = shell.run_command_http(sid, "whoami")

            elif session_manager.is_tcp_session(sid):
                output = shell.run_command_tcp(sid, "whoami", timeout=0.5)

            else:
                print(brightred + "[!] Unknown session type")
                return

            print(f"\n[+] Output:\n{output.strip()}")

        except Exception as e:
            print(brightred + f"[!] Unknown error ocurred: {e}")
