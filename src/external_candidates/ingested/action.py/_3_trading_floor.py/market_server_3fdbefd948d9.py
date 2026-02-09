# Extracted from: C:\DEV\PyAgent\.external\action\3_trading_floor\market_server.py
from market import get_share_price
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("market_server")


@mcp.tool()
async def lookup_share_price(symbol: str) -> float:
    """This tool provides the current price of the given stock symbol.

    Args:
        symbol: the symbol of the stock
    """
    return get_share_price(symbol)


if __name__ == "__main__":
    mcp.run(transport="stdio")
