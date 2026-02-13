# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\BandedMACD.py
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


class BandedMACD(Strategy):
    """
    Aggressive MACD Strategy with Bollinger Band Confirmation

    Strategy:
    - Use MACD crossovers for entry signals
    - Bollinger Bands for volatility confirmation
    - Momentum-based position sizing
    """

    def init(self):
        # MACD components
        self.ema_12 = self.I(
            lambda x: pd.Series(x).ewm(span=12).mean(), self.data.Close
        )
        self.ema_26 = self.I(
            lambda x: pd.Series(x).ewm(span=26).mean(), self.data.Close
        )

        # MACD line and signal
        def macd_line(close):
            ema12 = pd.Series(close).ewm(span=12).mean()
            ema26 = pd.Series(close).ewm(span=26).mean()
            return ema12 - ema26

        def macd_signal(close):
            macd = macd_line(close)
            return macd.ewm(span=9).mean()

        self.macd = self.I(macd_line, self.data.Close)
        self.macd_signal = self.I(macd_signal, self.data.Close)

        # Bollinger Bands
        self.sma_20 = self.I(SMA, self.data.Close, 20)

        def bb_upper(close):
            sma = pd.Series(close).rolling(20).mean()
            std = pd.Series(close).rolling(20).std()
            return sma + (2 * std)

        def bb_lower(close):
            sma = pd.Series(close).rolling(20).mean()
            std = pd.Series(close).rolling(20).std()
            return sma - (2 * std)

        self.bb_upper = self.I(bb_upper, self.data.Close)
        self.bb_lower = self.I(bb_lower, self.data.Close)

    def next(self):
        # Wait for enough data
        if len(self.data.Close) < 27:
            return

        current_price = self.data.Close[-1]

        # MACD values
        macd_current = self.macd[-1]
        macd_prev = self.macd[-2] if len(self.macd) > 1 else macd_current
        signal_current = self.macd_signal[-1]
        signal_prev = (
            self.macd_signal[-2] if len(self.macd_signal) > 1 else signal_current
        )

        # Bollinger Band values
        bb_upper = self.bb_upper[-1]
        bb_lower = self.bb_lower[-1]
        sma = self.sma_20[-1]

        # MACD crossover signals
        bullish_cross = macd_prev <= signal_prev and macd_current > signal_current
        bearish_cross = macd_prev >= signal_prev and macd_current < signal_current

        # Volatility and trend conditions
        near_lower_band = current_price < (
            bb_lower + (sma - bb_lower) * 0.3
        )  # Within 30% of lower band
        near_upper_band = current_price > (
            bb_upper - (bb_upper - sma) * 0.3
        )  # Within 30% of upper band
        above_sma = current_price > sma

        # Simplified momentum strategy - only enter on strong momentum breaks
        if not self.position:
            # Strong momentum breakout: price above upper band + MACD bullish + strong trend
            if (
                current_price > bb_upper
                and macd_current > signal_current
                and macd_current > 50  # Strong momentum only
                and above_sma
            ):

                self.buy(size=0.98)
                print(
                    f"STRONG MOMENTUM BUY: {current_price:.2f} | MACD: {macd_current:.2f}"
                )

        # Exit logic - Take profits quickly on momentum strategies
        else:
            # Exit on any bearish momentum or take profit at 3% gain
            if (
                bearish_cross
                or current_price < self.sma_20[-1]  # Below moving average
                or self.position.pl_pct > 3.0
            ):  # Take profit at 3%

                self.position.close()
                reason = "Bearish Cross" if bearish_cross else "Take Profit/Stop"
                print(
                    f"MOMENTUM EXIT: {current_price:.2f} | Reason: {reason} | P&L: {self.position.pl_pct:.2f}%"
                )


# Run backtest
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("BANDEDMACD BACKTEST RESULTS")
    print("=" * 60)

    # Run backtest with $1M portfolio
    bt = Backtest(data, BandedMACD, cash=1_000_000, commission=0.001)
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

    print("\nBandedMACD backtest complete!")
