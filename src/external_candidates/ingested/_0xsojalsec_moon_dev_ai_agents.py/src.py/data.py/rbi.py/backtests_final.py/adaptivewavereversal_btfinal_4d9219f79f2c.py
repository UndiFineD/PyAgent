# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\backtests_final\AdaptiveWaveReversal_BTFinal.py
#!/usr/bin/env python3
"""
Moon Dev’s Backtest AI 🌙
Strategy: AdaptiveWaveReversal
--------------------------------------------------
Instructions:
• Cleans the CSV column names and drops unnamed columns.
• Uses TA‑lib for indicator calculations via self.I().
• Implements long/short entries based on a higher timeframe “trend” (approximated using VWAP),
  swing highs/lows (via talib.MAX/min), and pivot points for dynamic support/resistance.
• Uses risk management (1% risk per trade on a 1,000,000 account) and proper integer position sizing.
• Prints themed debug messages.
• Finally, prints full backtest stats.
--------------------------------------------------
NOTE: No charting is invoked. Only stats are printed.
"""

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# ***********************************************
# Helper functions using TA‑lib / pandas for indicators
# ***********************************************


def calc_vwap(close, high, low, volume):
    # VWAP computation using typical price and cumulative sum.
    # Typical Price = (High + Low + Close) / 3.0
    typical_price = (high + low + close) / 3.0
    cumulative_tp_volume = np.cumsum(typical_price * volume)
    cumulative_volume = np.cumsum(volume)
    vwap = cumulative_tp_volume / cumulative_volume
    return vwap


def calc_pivot(high, low, close):
    # Standard pivot point: (High + Low + Close) / 3.0
    return (high + low + close) / 3.0


# ***********************************************
# Strategy Class Definition
# ***********************************************


class AdaptiveWaveReversal(Strategy):
    cash = 1_000_000  # default cash size

    def init(self):
        # *******************************
        # Compute Indicators via self.I wrapper
        # *******************************
        # Swing High: rolling maximum over a 20-bar window
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=20)
        # Swing Low: rolling minimum over a 20-bar window
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20)

        # VWAP computed using our custom function (since TA‑lib lacks VWAP)
        self.vwap = self.I(
            calc_vwap, self.data.Close, self.data.High, self.data.Low, self.data.Volume
        )

        # Pivot value acting as a dynamic support/resistance level
        self.pivot = self.I(calc_pivot, self.data.High, self.data.Low, self.data.Close)

        # Debug print for initialization
        print("🌙🚀 [Moon Dev] Strategy Initialized with indicators!")

    def next(self):
        price = self.data.Close[-1]
        current_vwap = self.vwap[-1]
        current_pivot = self.pivot[-1]

        # Using previous swing values for entry thresholds (index -2 because current bar might not be closed fully)
        prev_swing_high = self.swing_high[-2] if len(self.swing_high) > 1 else None
        prev_swing_low = self.swing_low[-2] if len(self.swing_low) > 1 else None

        # Determine trend direction using VWAP
        trend = "uptrend" if price > current_vwap else "downtrend"

        # Debug print for current bar data
        print(
            f"🌙✨ [Moon Dev] Bar: {self.data.index[-1]} | Price: {price:.2f} | Trend: {trend}"
        )

        # If we are flat, evaluate entry conditions
        if not self.position:
            # LONG ENTRY: in an uptrend and breaking above previous swing high
            if (
                trend == "uptrend"
                and prev_swing_high is not None
                and price > prev_swing_high
            ):
                # Set stop loss: use previous swing low if available; otherwise, use a 1% buffer
                stop_loss = (
                    prev_swing_low
                    if (prev_swing_low is not None and prev_swing_low < price)
                    else price * 0.99
                )
                # Set a take profit level relative to the entry (here using a fixed 10-point move)
                take_profit = price + 10
                # Calculate risk in dollars (1% of cash)
                risk_amount = self.cash * 0.01
                risk_per_unit = price - stop_loss
                if risk_per_unit <= 0:
                    risk_per_unit = (
                        1  # safeguard against division by zero or negative risk
                    )
                # Compute units ensuring whole numbers (integer sizing)
                units = int(risk_amount / risk_per_unit)
                if units <= 0:
                    units = 1
                self.buy(size=units, sl=stop_loss, tp=take_profit)
                print(
                    f"🌙🚀 [Moon Dev] Entering LONG at {price:.2f} with SL {stop_loss:.2f} and TP {take_profit:.2f}, units: {units}"
                )

            # SHORT ENTRY: in a downtrend and breaking below previous swing low
            elif (
                trend == "downtrend"
                and prev_swing_low is not None
                and price < prev_swing_low
            ):
                # Set stop loss: use previous swing high if available; otherwise, use a 1% buffer above price
                stop_loss = (
                    prev_swing_high
                    if (prev_swing_high is not None and prev_swing_high > price)
                    else price * 1.01
                )
                # Set a take profit level relative to the entry (here using a fixed 10-point move)
                take_profit = price - 10
                risk_amount = self.cash * 0.01
                risk_per_unit = stop_loss - price
                if risk_per_unit <= 0:
                    risk_per_unit = 1
                units = int(risk_amount / risk_per_unit)
                if units <= 0:
                    units = 1
                self.sell(size=units, sl=stop_loss, tp=take_profit)
                print(
                    f"🌙🚀 [Moon Dev] Entering SHORT at {price:.2f} with SL {stop_loss:.2f} and TP {take_profit:.2f}, units: {units}"
                )

        # Exit conditions based on pivot breach (could be viewed as a dynamic trailing stop)
        else:
            if self.position.is_long and price < current_pivot:
                self.position.close()
                print(
                    f"🌙💡 [Moon Dev] Exiting LONG at {price:.2f} (Price dropped below Pivot: {current_pivot:.2f})"
                )
            elif self.position.is_short and price > current_pivot:
                self.position.close()
                print(
                    f"🌙💡 [Moon Dev] Exiting SHORT at {price:.2f} (Price rose above Pivot: {current_pivot:.2f})"
                )


# ***********************************************
# Main Backtest Execution
# ***********************************************

if __name__ == "__main__":
    # Load market data from CSV
    try:
        df = pd.read_csv("data.csv")
        # Clean CSV column names
        df.columns = [c.strip() for c in df.columns]
        # Drop any unnamed columns that might have been introduced
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # Ensure the CSV has a 'Date' column; if so, set it as the index
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)

        print("🌙🔥 [Moon Dev] CSV data loaded and cleaned!")
    except Exception as e:
        print(f"🌙❌ [Moon Dev] Error loading CSV data: {e}")
        raise

    # Run the backtest using the AdaptiveWaveReversal strategy
    try:
        bt = Backtest(df, AdaptiveWaveReversal, cash=1_000_000, commission=0.0)
        stats = bt.run()
        print("🌙🔥 [Moon Dev] Backtest Completed!")
        print(stats)
    except Exception as e:
        print(f"🌙❌ [Moon Dev] Backtest Error: {e}")
        raise
