# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\BandSyncMomentum.py
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


class BandSyncMomentum(Strategy):
    """
    High-Performance Momentum Strategy

    Strategy:
    - Buy on strong momentum with trend confirmation
    - Use leverage through position sizing
    - Quick exits on momentum reversal
    """

    def init(self):
        # Moving averages for trend
        self.sma_short = self.I(SMA, self.data.Close, 5)
        self.sma_long = self.I(SMA, self.data.Close, 20)

        # High and low for breakouts
        self.high_20 = self.I(lambda x: pd.Series(x).rolling(20).max(), self.data.High)
        self.low_20 = self.I(lambda x: pd.Series(x).rolling(20).min(), self.data.Low)

    def next(self):
        # Wait for enough data
        if len(self.data.Close) < 21:
            return

        current_price = self.data.Close[-1]
        prev_high = self.high_20[-2]  # Previous 20-period high
        prev_low = self.low_20[-2]  # Previous 20-period low

        sma_short = self.sma_short[-1]
        sma_long = self.sma_long[-1]

        # Entry: Breakout above 20-period high with trend confirmation
        if not self.position:
            if (
                current_price > prev_high  # Breakout
                and sma_short > sma_long  # Uptrend
                and current_price > sma_long
            ):  # Above long-term trend

                # Aggressive position sizing
                self.buy(size=0.99)
                print(f"BREAKOUT BUY: {current_price:.2f} > {prev_high:.2f} (20H)")

        # Exit: Quick exit on momentum loss
        else:
            if (
                current_price < sma_short  # Below short-term trend
                or current_price < prev_low
            ):  # Below support

                self.position.close()
                print(f"MOMENTUM EXIT: {current_price:.2f}")


# Run backtest
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("BANDSYNCMOMENTUM BACKTEST RESULTS")
    print("=" * 60)

    # Run backtest with $1M portfolio
    bt = Backtest(data, BandSyncMomentum, cash=1_000_000, commission=0.001)
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

    print("\nBandSyncMomentum backtest complete!")
