# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\backtests\AdaptiveReversal_BT.py
#!/usr/bin/env python3
"""
Moon Dev's Backtest AI 🌙 - Adaptive Reversal Strategy Backtest
This script loads BTC-USD-15m data from the specified CSV, cleans and maps columns,
defines an Adaptive Reversal trading strategy with TA-Lib indicators and proper risk
management with Moon Dev themed debug prints, then runs a backtest using backtesting.py.
"""

import numpy as np

# 1. All necessary imports
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# 2. Define the Adaptive Reversal Strategy Class
class AdaptiveReversal(Strategy):
    """
    Adaptive Reversal Strategy:
    A meta-strategy to cultivate self-learning and adaptability. For demo purposes,
    we trade when price dips to its recent low (anticipating a reversal upward)
    and exit when price recovers above its 20-bar SMA.
    """

    # You can set risk percent here (1% of account risk per trade)
    risk_percent = 0.01
    sl_factor = 0.995  # Stop loss level as a fraction of entry price (0.5% risk buffer)

    def init(self):
        # Always use self.I() wrapper for indicator calculations 🌙
        # 20-period Simple Moving Average on Close using TA-Lib
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        # 20-bar lowest low using TA-Lib MIN function
        self.low20 = self.I(talib.MIN, self.data.Low, timeperiod=20)
        # 20-bar highest high (not used in this demo but computed for reference)
        self.high20 = self.I(talib.MAX, self.data.High, timeperiod=20)
        print("🌙✨ [Moon Dev Debug] Indicators initialized: SMA20, LOW20, HIGH20")

    def next(self):
        current_close = self.data.Close[-1]
        current_sma20 = self.sma20[-1]
        current_low20 = self.low20[-1]

        # -------------------------------
        # ENTRY LOGIC: Look for adaptive reversal buy signal
        # Condition: Price drops to the recent 20-bar low (oversold reversal condition)
        # -------------------------------
        if not self.position:
            if current_close <= current_low20:
                # Calculate a stop loss level as a fraction of the entry price
                stop_loss = current_close * self.sl_factor
                # Calculate the risk (per unit) for long position
                # Risk = difference between entry and stop loss
                risk_per_unit = current_close - stop_loss
                if risk_per_unit <= 0:
                    print(
                        "🚀🌙 [Moon Dev Warning] Computed risk per unit is non-positive. Skipping order!"
                    )
                    return

                # Calculate the risk amount using risk percent of current equity
                risk_amount = self.equity * self.risk_percent
                # Determine position size (number of units)
                raw_position_size = risk_amount / risk_per_unit
                position_size = int(round(raw_position_size))
                if position_size <= 0:
                    print(
                        "🚀🌙 [Moon Dev Warning] Calculated position size is zero. Skipping order!"
                    )
                    return

                print(
                    f"🚀🌙 [Moon Dev Signal] BUY triggered at {current_close:.2f} with stop-loss {stop_loss:.2f} "
                    f"and position size {position_size} (risk per unit: {risk_per_unit:.2f})."
                )
                # Submit market BUY order with calculated position size
                self.buy(size=position_size, sl=stop_loss)

        # -------------------------------
        # EXIT LOGIC: Exit position when price recovers above the SMA (adaptive exit)
        # -------------------------------
        if self.position:
            if current_close > current_sma20:
                print(
                    f"🌙✨ [Moon Dev Signal] SELL triggered at {current_close:.2f} as price recovers above SMA20 "
                    f"({current_sma20:.2f}). Exiting position."
                )
                self.position.close()


# 3. Data Handling: Load, clean, and map column names accordingly
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
try:
    data = pd.read_csv(data_path, parse_dates=["datetime"])
    print("🌙✨ [Moon Dev Debug] Data loaded successfully from CSV!")
except Exception as e:
    print(f"🚀🌙 [Moon Dev Error] Failed to load CSV: {e}")
    raise

# Clean column names: remove extra spaces, convert to lowercase
data.columns = data.columns.str.strip().str.lower()
# Drop any unnamed columns
unnamed_cols = [col for col in data.columns if "unnamed" in col.lower()]
if unnamed_cols:
    data.drop(columns=unnamed_cols, inplace=True)
    print("🌙✨ [Moon Dev Debug] Unnamed columns dropped:", unnamed_cols)

# Map the columns to Backtesting.py requirements using proper case:
rename_mapping = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data.rename(columns=rename_mapping, inplace=True)
print("🚀🌙 [Moon Dev Debug] Columns renamed to:", list(data.columns))

# Check if required columns exist
required_columns = ["Open", "High", "Low", "Close", "Volume"]
if not all(col in data.columns for col in required_columns):
    missing = [col for col in required_columns if col not in data.columns]
    raise ValueError(f"🚀🌙 [Moon Dev Error] Missing required columns: {missing}")

# 4. Backtest Execution
print(
    "🌙✨ [Moon Dev Debug] Starting Backtest execution with initial cash of 1,000,000!"
)
bt = Backtest(data, AdaptiveReversal, cash=1_000_000, commission=0.0)

# Run the backtest
stats = bt.run()

# Print full stats output and the strategy object details
print("🚀🌙 [Moon Dev Results] Final Backtest Stats:")
print(stats)
print("\n🚀🌙 [Moon Dev Results] Strategy details:")
print(stats._strategy)
