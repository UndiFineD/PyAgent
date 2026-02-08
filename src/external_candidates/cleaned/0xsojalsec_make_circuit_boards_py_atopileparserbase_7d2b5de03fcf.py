# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_make_circuit_boards.py\src.py\atopile.py\parser.py\atopileparserbase_7d2b5de03fcf.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\src\atopile\parser\AtopileParserBase.py

from antlr4 import Parser


class AtopileParserBase(Parser):
    def CannotBePlusMinus(self) -> bool:
        return True

    def CannotBeDotLpEq(self) -> bool:
        return True
