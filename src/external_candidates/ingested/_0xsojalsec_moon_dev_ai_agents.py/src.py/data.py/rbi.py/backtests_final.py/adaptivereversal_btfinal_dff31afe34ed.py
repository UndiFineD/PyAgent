# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\backtests_final\AdaptiveReversal_BTFinal.py
#!/usr/bin/env python3
"""
Moon Dev's Backtest AI 🌙 - Adaptive Reversal Strategy Backtest
This script loads BTC-USD-15m data from the specified CSV, cleans and maps columns,
defines an Adaptive Reversal trading strategy with TA-Lib indicators and proper risk
management with Moon Dev themed debug prints, then runs a backtest using a custom backtest function.
"""

import sys

import numpy as np
import pandas as pd
import talib
from pandas_ta import MAX, MIN


# Custom backtest function
def backtest(data, strategy):
    cash = 1_000_000
    equity = cash
    position_size = 0  # For unit-based sizing (always an integer number of units)
    position_price = None  # Track entry price of open position
    realized_pnl = 0

    print("🌙🚀 [Moon Dev Debug] Starting Backtest Loop")
    for idx in range(len(data)):
        close = data.Close.iloc[idx]
        sma20 = strategy.sma20[idx]
        low20 = strategy.low20[idx]
        high20 = strategy.high20[idx]  # Computed for reference

        # Detect entry: if no open position and price is at or below recent 20-bar low
        if position_size == 0:
            if close <= low20:
                stop_loss = close * strategy.sl_factor  # price level for stop loss
                risk_per_unit = close - stop_loss
                if risk_per_unit <= 0:
                    print(
                        "🚀🌙 [Moon Dev Warning] Computed risk per unit is non-positive. Skipping order!"
                    )
                    continue

                raw_position_size = equity * strategy.risk_percent / risk_per_unit
                # Position sizing rule: units must be a whole number
                position_size = round(raw_position_size)
                if position_size <= 0:
                    print(
                        "🚀🌙 [Moon Dev Warning] Calculated position size is zero. Skipping order!"
                    )
                    continue

                position_price = close
                print(
                    f"🚀🌙 [Moon Dev Signal] BUY triggered at {close:.2f} with stop-loss {stop_loss:.2f} and position size {position_size} (risk per unit: {risk_per_unit:.2f})."
                )

        # If in a position, check for exit conditions
        if position_size:
            if close > sma20:  # Exit if price recovers above its 20-bar SMA
                realized_pnl = position_size * (close - position_price)
                print(
                    f"🌙✨ [Moon Dev Signal] SELL triggered at {close:.2f} as price recovers above SMA20 ({sma20:.2f}). Exiting position with realized PnL: {realized_pnl:.2f}."
                )
                equity += realized_pnl
                # Reset position tracking variables after exit
                position_size = 0
                position_price = None

        # Mark-to-market update: if position is open then adjust equity for unrealized PnL
        if position_size and position_price is not None:
            equity += (close - position_price) * position_size

    print("🌙🚀 [Moon Dev Debug] Backtest Loop Completed")
    return equity


# Define the Adaptive Reversal Strategy Class
class AdaptiveReversal:
    """
    Adaptive Reversal Strategy:
    A meta-strategy to cultivate self-learning and adaptability. For demo purposes,
    we trade when price dips to its recent low (anticipating a reversal upward)
    and exit when price recovers above its 20-bar SMA.
    """

    # Risk management parameters
    risk_percent = 0.01  # 1% of account risk per trade (if using equity fraction)
    sl_factor = (
        0.995  # Stop loss level as a fraction of entry price (i.e. 0.5% risk buffer)
    )

    def __init__(self, data):
        self.data = data

    def I(self, func, series, **kwargs):
        """
        Indicator wrapper: Calls a given function (like talib.SMA) on the series with kwargs,
        prints a Moon Dev themed debug message, and returns the computed indicator.
        """
        result = func(np.array(series, dtype=float), **kwargs)
        print(
            f"🌙 [Moon Dev Debug] Calculated indicator {func.__name__} with kwargs {kwargs}."
        )
        return result

    def initialize_indicators(self):
        # 20-period Simple Moving Average on Close using TA-Lib
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        # 20-bar lowest low using pandas_ta's MIN function
        self.low20 = self.I(MIN, self.data.Low, timeperiod=20)
        # 20-bar highest high (computed for reference) using pandas_ta's MAX function
        self.high20 = self.I(MAX, self.data.High, timeperiod=20)
        print("🌙🚀 [Moon Dev Debug] Indicator initialization complete.")


# Main execution block
if __name__ == "__main__":
    print("🌙🚀 [Moon Dev] Starting Adaptive Reversal Backtest!")

    try:
        # Load CSV data
        data = pd.read_csv("BTC-USD-15m.csv")
        # Ensure date parsing and sorting
        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(data["Date"])
            data.sort_values("Date", inplace=True)
        # Ensure required columns are present and renamed if necessary
        required_columns = {"Open", "High", "Low", "Close", "Volume"}
        if not required_columns.issubset(set(data.columns)):
            raise ValueError(
                f"Data is missing one of the required columns: {required_columns}"
            )
        # Reset index after sorting
        data.reset_index(drop=True, inplace=True)
        print("🌙🚀 [Moon Dev] Data loaded and preprocessed successfully!")
    except Exception as e:
        print("🌙🚀 [Moon Dev ERROR] Loading data failed:", e)
        sys.exit(1)

    # Initialize strategy
    strategy = AdaptiveReversal(data)
    strategy.initialize_indicators()

    # Run backtest using the strategy and loaded data
    final_equity = backtest(data, strategy)
    print(f"🌙✨ [Moon Dev Complete] Final Equity: {final_equity:.2f}")

    print("🌙🚀 [Moon Dev] Backtest Finished. Happy Trading! ✨")
