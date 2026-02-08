# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_gunnerc2.py\core.py\banner_da12d69518fe.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-GunnerC2\core\banner.py

from colorama import Fore, Style, init

brightgreen = "\001" + Style.BRIGHT + Fore.GREEN + "\002"

brightyellow = "\001" + Style.BRIGHT + Fore.YELLOW + "\002"

brightred = "\001" + Style.BRIGHT + Fore.RED + "\002"

brightblue = "\001" + Style.BRIGHT + Fore.BLUE + "\002"


def print_banner():
    """

    Print a red ASCII-art banner saying 'GUNNER'.

    """

    # Initialize colorama

    init(autoreset=True)

    banner = r"""

   ______   __  __    _   __    _   __    ______    ____ 

  / ____/  / / / /   / | / /   / | / /   / ____/   / __ \

 / / __   / / / /   /  |/ /   /  |/ /   / __/     / /_/ /

/ /_/ /  / /_/ /   / /|  /   / /|  /   / /___    / _, _/ 

\____/   \____/   /_/ |_/   /_/ |_/   /_____/   /_/ |_|

"""

    print(brightred + banner)

    print("\n")

    # print("\n")
