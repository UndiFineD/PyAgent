# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests_final\LiquidationRetrace_BTFinal.py
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


# 🌙 MOON DEV BACKTEST ENGINE START ✨
class LiquidationRetrace(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    oi_drop_threshold = -0.10  # 10% OI drop
    funding_threshold = -0.001  # -0.1%
    swing_period = 5  # Swing low period

    def init(self):
        # Clean and prepare data columns
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(columns=[col for col in self.data.df.columns if "unnamed" in col])

        # Calculate indicators with proper self.I() wrapper
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20, name="SMA20 🌙")
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period, name="SWING LOW 🚀")
        self.oi_pct_change = self.I(
            lambda x: x.pct_change(4), self.data.df["oi"], name="OI %Δ ⚡"
        )  # 4-period OI change

        print("🌕 MOON DEV INIT COMPLETE | Indicators Ready for Launch! 🚀\n")

    def next(self):
        current_idx = len(self.data) - 1

        # Skip initial bars for indicator warmup
        if current_idx < 20:
            return

        # Get recent values using .values[-n] for array access
        oi_change = self.oi_pct_change[-1]
        funding_rate = self.data.df["fundingrate"].values[-1]
        entry_conditions = (
            oi_change <= self.oi_drop_threshold
            and funding_rate <= self.funding_threshold
            and self.data.Close[-1] > self.data.Open[-1]  # Bullish candle
            and not self.position
        )

        if entry_conditions:
            # Risk management calculations
            entry_price = self.data.Close[-1]
            stop_loss = self.swing_low[-1]
            risk_amount = self.risk_per_trade * self.equity
            risk_per_share = entry_price - stop_loss
            position_size = int(round(risk_amount / risk_per_share))

            if position_size > 0:
                # Execute trade with Moon Dev flair 🌙
                self.buy(
                    size=position_size,
                    sl=stop_loss,
                    tp=self.sma20[-1],
                    tag="MOONSHOT ENTRY 🌙✨",
                )
                print(f"🚀 BLASTOFF! Long {position_size} units @ {entry_price:.2f}")
                print(f"   STOP LOSS: {stop_loss:.2f} | TP: {self.sma20[-1]:.2f}")

        # Check exits for any open positions
        for trade in self.trades:
            if trade.is_long:
                if self.data.Close[-1] >= trade.tp:
                    trade.close()
                    print(f"🌕 PROFIT CAPTURED AT MIDLINE! Closing @ {self.data.Close[-1]:.2f}")
                elif self.data.Close[-1] <= trade.sl:
                    print(f"🌑 LIQUIDATION AVOIDANCE! Stop Loss @ {self.data.Close[-1]:.2f}")


# 🌙 DATA PREP SECTION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean columns with Moon Dev precision 🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Map to backtesting.py requirements with proper case
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

print("🌙 DATA PREP COMPLETE | First 3 Rows:")
print(data.head(3), "\n")

# LAUNCH BACKTEST 🚀
bt = Backtest(data, LiquidationRetrace, cash=1_000_000, margin=1 / 1)
