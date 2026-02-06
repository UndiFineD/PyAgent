# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests_final\ChaikinSqueeze_BTFinal.py
# 🌙 Moon Dev's Chaikin Squeeze Backtest 🌙
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class ChaikinSqueeze(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    exit_bars = 20  # Bars until time exit

    def init(self):
        # 🌙 Indicator Calculation Phase
        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name=["BB_Upper", "BB_Middle", "BB_Lower"],
        )

        # Chaikin Money Flow
        self.cmf = self.I(
            talib.CMF,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            timeperiod=20,
            name="CMF",
        )

        # Bandwidth Calculation
        def calc_bandwidth(upper, middle, lower):
            return ((upper - lower) / middle) * 100

        self.bandwidth = self.I(
            calc_bandwidth,
            self.bb_upper,
            self.bb_middle,
            self.bb_lower,
            name="Bandwidth",
        )

        # Squeeze Threshold (20th percentile over 50 bars)
        self.squeeze_threshold = self.I(
            lambda x: ta.percentile(x, length=50, percentile=20),
            self.bandwidth,
            name="Squeeze_Threshold",
        )

        # Swing Low (20-period)
        self.swing_low = self.I(
            talib.MIN, self.data.Low, timeperiod=20, name="Swing_Low"
        )

        self.bars_held = 0  # For time exits

    def next(self):
        # 🌙 Trade Execution Logic
        price = self.data.Close[-1]

        if not self.position:
            # Entry Conditions
            squeeze_active = self.bandwidth[-1] <= self.squeeze_threshold[-1]
            cmf_cross = (self.cmf[-1] > 0) and (self.cmf[-2] <= 0)

            if squeeze_active and cmf_cross:
                # Risk Management Calculations
                entry_price = price
                stop_price = min(self.bb_lower[-1], self.swing_low[-1])
                risk_per_share = entry_price - stop_price

                if risk_per_share <= 0:
                    print(
                        f"🌙 Moon Dev Alert: Invalid SL {stop_price:.2f} >= Entry {entry_price:.2f}"
                    )
                    return

                risk_amount = self.equity * self.risk_per_trade
                position_size = int(round(risk_amount / risk_per_share))
                position_size = min(position_size, int(self.equity // entry_price))

                if position_size > 0:
                    tp_price = self.bb_upper[-1]
                    self.buy(size=position_size, sl=stop_price, tp=tp_price)
                    print(
                        f"🚀 MOON DEV LONG ENTRY 🌙 Size: {position_size} @ {entry_price:.2f}"
                    )
                    print(
                        f"   SL: {stop_price:.2f} | TP: {tp_price:.2f} | Risk/Reward: {(tp_price-entry_price)/(entry_price-stop_price):.1f}"
                    )
        else:
            self.bars_held += 1
            if self.bars_held >= self.exit_bars:
                self.position.close()
                print(f"🌙 TIME EXIT: Held {self.exit_bars} bars")


# 🌙 DATA PREPARATION
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and format columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Run backtest 🌙
bt = Backtest(data, ChaikinSqueeze, cash=1_000_000, margin=1 / 1)
