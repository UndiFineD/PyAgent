# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests\VolatilitySurge_BT.py
import numpy as np
import pandas as pd
import scipy.stats as stats
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and format columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "DateTime",
    },
    inplace=True,
)
data["DateTime"] = pd.to_datetime(data["DateTime"])
data.set_index("DateTime", inplace=True)


class VolatilitySurge(Strategy):
    def init(self):
        # 🌙 Core Indicators
        self.sma_200 = self.I(talib.SMA, self.data.Close, 200)
        self.atr_14 = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.hv_20 = self.I(talib.STDDEV, self.data.Close, 20)

    def next(self):
        # Skip initial bars without indicator data
        if len(self.data) < 200 or np.isnan(self.hv_20[-1]):
            return

        # 🌗 Volatility Calculation
        current_hv = self.hv_20[-1]
        historical_hv = [x for x in self.hv_20[:-1] if not np.isnan(x)]
        if not historical_hv:
            return

        hv_percentile = stats.percentileofscore(historical_hv, current_hv)
        volatility_ok = hv_percentile <= 10

        # 🌄 Trend Filter
        price_above_sma = self.data.Close[-1] > self.sma_200[-1]

        # 🚀 ENTRY LOGIC
        if not self.position and volatility_ok and price_above_sma:
            atr_value = self.atr_14[-1]
            if atr_value <= 0:
                return

            # 🌕 Position Sizing
            risk_amount = self.equity * 0.01
            position_size = risk_amount / (2 * atr_value)
            position_size = int(round(position_size))

            if position_size > 0:
                self.entry_price = self.data.Close[-1]
                self.trailing_high = self.entry_price
                self.buy(size=position_size)
                print(f"🌙✨ MOON ENTRY @ {self.entry_price:.2f} | Size: {position_size} 🚀")

        # 🛑 EXIT LOGIC
        if self.position.is_long:
            # 🌟 Update trailing high
            self.trailing_high = max(self.trailing_high, self.data.High[-1])

            # 🎯 Take Profit Check
            if self.data.Close[-1] >= self.entry_price * 1.05:
                self.sell()
                print(f"🎯🌙 PROFIT LANDED @ {self.data.Close[-1]:.2f}")
                return

            # 🌪️ Trailing Stop
            stop_level = self.trailing_high - 2 * self.atr_14[-1]
            if self.data.Close[-1] < stop_level:
                self.sell()
                print(f"🛑🌒 STOPPED OUT @ {self.data.Close[-1]:.2f}")
                return

            # ⚡ Volatility Spike Exit
            current_hv_percentile = stats.percentileofscore(historical_hv, current_hv)
            if current_hv_percentile >= 90:
                self.sell()
                print(f"⚡🌑 VOLATILITY SPIKE @ {self.data.Close[-1]:.2f}")


# 🌕 BACKTEST EXECUTION
bt = Backtest(data, VolatilitySurge, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙✨ FULL BACKTEST STATS:")
print(stats)
print("\n🌙💫 STRATEGY DETAILS:")
print(stats._strategy)
