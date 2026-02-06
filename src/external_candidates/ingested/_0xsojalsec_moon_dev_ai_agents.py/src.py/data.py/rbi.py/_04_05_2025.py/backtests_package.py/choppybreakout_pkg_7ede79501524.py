# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests_package\ChoppyBreakout_PKG.py
# 🌙 Moon Dev Backtest AI Implementation: ChoppyBreakout Strategy 🚀

import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Data Preparation 🌐
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class ChoppyBreakout(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌕
    trail_multiplier = 0.05  # 5% of ATR for trailing stop

    def init(self):
        # Choppiness Index (CI) 🌊
        self.ci = self.I(
            ta.chop, self.data.High, self.data.Low, self.data.Close, length=14
        )

        # Donchian Channel 📈
        self.donchian_upper = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, timeperiod=20)

        # ATR for Risk Management 🔐
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        self.trade_highest_high = None  # Track highest high during trade 🌙

    def next(self):
        # Skip early bars without indicator data ⏳
        if len(self.data) < 20:
            return

        # Entry Logic 🚀
        if not self.position:
            # Check CI filter and breakout condition
            if self.ci[-2] < 35 and self.data.Close[-2] > self.donchian_upper[-2]:

                # Calculate position size 🌕
                risk_amount = self.equity * self.risk_per_trade
                entry_price = self.data.Open[-1]
                stop_loss = self.donchian_lower[-2]
                risk_per_share = entry_price - stop_loss

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))

                    # Execute trade with Moon Dev precision 🌙
                    self.buy(size=position_size)
                    self.trade_highest_high = entry_price  # Initialize high tracker
                    print(
                        f"🚀 MOON DEV ALERT: Long Entry @ {entry_price:.2f} "
                        f"| Size: {position_size} Units 🌕"
                    )

        # Exit Logic 🌑
        else:
            # Update trailing stop logic
            current_high = self.data.High[-1]
            if current_high > self.trade_highest_high:
                self.trade_highest_high = current_high
                print(f"🌕 NEW MOON HIGH: {self.trade_highest_high:.2f} 🚀")

            # Calculate dynamic trailing stop
            atr_value = self.atr[-1]
            trail_stop = self.trade_highest_high - (atr_value * self.trail_multiplier)

            # Check exit condition
            if self.data.Low[-1] < trail_stop:
                self.position.close()
                print(
                    f"🌑 MOON DEV EXIT: Trailing Stop @ {trail_stop:.2f} "
                    f"| Profit: {self.position.pl_pct:.2f}% 🌙"
                )


# Run Backtest 📊
bt = Backtest(data, ChoppyBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print Full Moon Stats 🌕
print("\n" + "=" * 50)
print("🌙 MOON DEV FINAL BACKTEST STATS 🌕")
print("=" * 50)
print(stats)
print(stats._strategy)
print("🌑 MOON DEV ANALYSIS COMPLETE 🌙🚀")
