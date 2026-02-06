# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-malpacks\core\cli.py
from colorama import Fore, Style


def banner():
    banner = Fore.BLUE + """
 #    #    ##    #       #####     ##     ####   #    #   ####  
 ##  ##   #  #   #       #    #   #  #   #    #  #   #   #      
 # ## #  #    #  #       #    #  #    #  #       ####     ####  
 #    #  ######  #       #####   ######  #       #  #         # 
 #    #  #    #  #       #       #    #  #    #  #   #   #    # 
 #    #  #    #  ######  #       #    #   ####   #    #   ####  

Version: 1.0.0
Author: daffainfo
"""

    print(banner + Style.RESET_ALL)
