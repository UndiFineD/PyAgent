# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_make_circuit_boards.py\src.py\atopile.py\parse_utils_92c3819333a3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\src\atopile\parse_utils.py

"""

Utils related to handling the parse tree

"""

from antlr4 import InputStream, ParserRuleContext, Token


def get_src_info_from_token(token: Token) -> tuple[str, int, int]:
    """Get the source path, line, and column from a context"""

    input_stream: InputStream = token.getInputStream()

    return input_stream.name, token.line, token.column


def get_src_info_from_ctx(ctx: ParserRuleContext) -> tuple[str, int, int]:
    """Get the source path, line, and column from a context"""

    token: Token = ctx.start

    return get_src_info_from_token(token)
