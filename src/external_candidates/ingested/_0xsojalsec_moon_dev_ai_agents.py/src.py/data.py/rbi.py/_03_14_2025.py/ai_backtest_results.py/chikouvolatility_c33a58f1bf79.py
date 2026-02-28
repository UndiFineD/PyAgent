# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\ChikouVolatility.py
#!/usr/bin/env python3

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.test import SMA

# Load data
print("Loading BTC data...")
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and prepare data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(
    columns=[col for col in data.columns if "unnamed" in col.lower()], errors="ignore"
)

# Proper column mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date",
    }
)

# Set datetime index
data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)

print(f"Data loaded: {len(data)} rows")
print(f"Date range: {data.index[0]} to {data.index[-1]}")


class ChikouVolatility(Strategy):
    """
    High-Frequency Momentum Strategy with Ichimoku Chikou

    Strategy:
    - Use aggressive momentum breakouts
    - Chikou span confirmation for direction
    - Quick exits on momentum reversal
    """

    def init(self):
        # Moving averages for trend
        self.sma_short = self.I(SMA, self.data.Close, 10)
        self.sma_long = self.I(SMA, self.data.Close, 30)

        # Volatility bands (simpler Bollinger Band approach)
        def volatility_upper(close):
            sma = pd.Series(close).rolling(20).mean()
            std = pd.Series(close).rolling(20).std()
            return sma + (1.5 * std)  # Tighter bands for more signals

        def volatility_lower(close):
            sma = pd.Series(close).rolling(20).mean()
            std = pd.Series(close).rolling(20).std()
            return sma - (1.5 * std)

        self.vol_upper = self.I(volatility_upper, self.data.Close)
        self.vol_lower = self.I(volatility_lower, self.data.Close)

        # Chikou reference (lagged price)
        def chikou_ref(close):
            return pd.Series(close).shift(26)

        self.chikou_ref = self.I(chikou_ref, self.data.Close)

    def next(self):
        # Wait for enough data
        if len(self.data.Close) < 31:
            return

        current_price = self.data.Close[-1]

        # Chikou momentum check (current price vs 26 periods ago)
        chikou_value = (
            self.chikou_ref[-1] if not pd.isna(self.chikou_ref[-1]) else current_price
        )
        chikou_bullish = current_price > chikou_value * 1.005  # 0.5% above for momentum

        # Volatility breakout conditions
        vol_upper = self.vol_upper[-1]
        vol_lower = self.vol_lower[-1]

        # Trend conditions
        sma_short = self.sma_short[-1]
        sma_long = self.sma_long[-1]
        strong_uptrend = sma_short > sma_long * 1.01  # 1% above for strong trend

        # Momentum breakout entries
        if not self.position:
            # Aggressive upside breakout with Chikou confirmation
            if current_price > vol_upper and chikou_bullish and strong_uptrend:

                self.buy(size=0.98)
                print(
                    f"CHIKOU BREAKOUT BUY: {current_price:.2f} | Chikou momentum confirmed"
                )

            # Reversal trade on oversold with momentum
            elif (
                current_price < vol_lower
                and chikou_bullish
                and current_price > sma_long
            ):  # Above long-term trend

                self.buy(size=0.85)
                print(
                    f"OVERSOLD REVERSAL BUY: {current_price:.2f} | Below vol band but momentum up"
                )

        # Exit logic
        else:
            # Quick profit taking or stop loss
            if (
                current_price < sma_short  # Below short-term trend
                or self.position.pl_pct > 2.5  # Take profit at 2.5%
                or self.position.pl_pct < -1.5
            ):  # Stop loss at -1.5%

                self.position.close()
                print(
                    f"CHIKOU EXIT: {current_price:.2f} | P&L: {self.position.pl_pct:.2f}%"
                )


# Run backtest
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CHIKOUVOLATILITY BACKTEST RESULTS")
    print("=" * 60)

    # Run backtest with $1M portfolio
    bt = Backtest(data, ChikouVolatility, cash=1_000_000, commission=0.001)
    stats = bt.run()

    # Print results
    print("\nBACKTEST STATISTICS:")
    print("-" * 40)
    print(f"Return [%]: {stats['Return [%]']:.2f}%")
    print(f"Buy & Hold Return [%]: {stats['Buy & Hold Return [%]']:.2f}%")
    print(f"Max Drawdown [%]: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"# Trades: {stats['# Trades']}")
    print(f"Win Rate [%]: {stats['Win Rate [%]']:.1f}%")
    print(f"Best Trade [%]: {stats['Best Trade [%]']:.2f}%")
    print(f"Worst Trade [%]: {stats['Worst Trade [%]']:.2f}%")

    # Success check
    strategy_return = stats["Return [%]"]
    buy_hold_return = stats["Buy & Hold Return [%]"]
    num_trades = stats["# Trades"]

    print(f"\nSTRATEGY PERFORMANCE:")
    print(f"Strategy Return: {strategy_return:.2f}%")
    print(f"Buy & Hold Return: {buy_hold_return:.2f}%")
    print(f"Number of Trades: {num_trades}")
    print(f"Outperformance: {strategy_return - buy_hold_return:.2f}%")

    if strategy_return > buy_hold_return and num_trades >= 5:
        print("✅ SUCCESS: Strategy beats buy & hold with 5+ trades!")
    else:
        print("❌ FAILED: Strategy does not meet requirements")

    print("\nChikouVolatility backtest complete!")
