# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\src\atopile\parser\AtopileParserBase.py
from antlr4 import Parser


class AtopileParserBase(Parser):
    def CannotBePlusMinus(self) -> bool:
        return True

    def CannotBeDotLpEq(self) -> bool:
        return True
