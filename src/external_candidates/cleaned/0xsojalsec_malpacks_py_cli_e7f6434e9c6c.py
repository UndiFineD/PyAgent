# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_malpacks.py\core.py\cli_e7f6434e9c6c.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-malpacks\core\cli.py

from colorama import Fore, Style


def banner():

    banner = (
        Fore.BLUE
        + """

 #    #    ##    #       #####     ##     ####   #    #   ####  

 ##  ##   #  #   #       #    #   #  #   #    #  #   #   #      

 # ## #  #    #  #       #    #  #    #  #       ####     ####  

 #    #  ######  #       #####   ######  #       #  #         # 

 #    #  #    #  #       #       #    #  #    #  #   #   #    # 

 #    #  #    #  ######  #       #    #   ####   #    #   ####  

Version: 1.0.0

Author: daffainfo

"""
    )

    print(banner + Style.RESET_ALL)
