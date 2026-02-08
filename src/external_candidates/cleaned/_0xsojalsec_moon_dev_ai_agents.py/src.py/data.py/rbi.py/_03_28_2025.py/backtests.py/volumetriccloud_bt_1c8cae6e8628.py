# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\VolumetricCloud_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolumetricCloud(Strategy):
    def init(self):
        # 🌙 Calculate Volume Indicators
        self.ema5_vol = self.I(talib.EMA, self.data.Volume, 5, name="EMA5 Vol")
        self.ema20_vol = self.I(talib.EMA, self.data.Volume, 20, name="EMA20 Vol")

        # ✨ Volume Difference and STDDEV
        def calculate_diff(data):
            return talib.EMA(data.Volume, 5) - talib.EMA(data.Volume, 20)

        self.diff_vol = self.I(calculate_diff, name="DIFF Vol")
        self.std_diff = self.I(talib.STDDEV, self.diff_vol, 20, name="STDDEV Diff")

        # 🚀 Ichimoku Cloud Components
        def tenkan_sen(data):
            high = talib.MAX(data.High, 9)
            low = talib.MIN(data.Low, 9)
            return (high + low) / 2

        self.tenkan = self.I(tenkan_sen, name="Tenkan")

        def kijun_sen(data):
            high = talib.MAX(data.High, 26)
            low = talib.MIN(data.Low, 26)
            return (high + low) / 2

        self.kijun = self.I(kijun_sen, name="Kijun")

        def senkou_a(data):
            return (self.tenkan + self.kijun) / 2

        self.senkou_a = self.I(senkou_a, name="Senkou A")

        def senkou_b(data):
            high = talib.MAX(data.High, 52)
            low = talib.MIN(data.Low, 52)
            return (high + low) / 2

        self.senkou_b = self.I(senkou_b, name="Senkou B")

    def next(self):
        current_idx = len(self.data) - 1

        # 🌙 Check minimum data requirements
        if current_idx < 26:
            return

        # ✨ Get cloud values from 26 periods ago
        cloud_a = self.senkou_a[current_idx - 26]
        cloud_b = self.senkou_b[current_idx - 26]
        current_close = self.data.Close[current_idx]

        # 🚀 Entry Conditions
        volume_surge = self.ema5_vol[current_idx] > (self.ema20_vol[current_idx] + 2 * self.std_diff[current_idx])
        price_above_cloud = current_close > max(cloud_a, cloud_b)

        # 🌟 Long Entry Logic
        if not self.position and volume_surge and price_above_cloud:
            # Risk Management
            risk_percent = 0.01  # 1% of equity
            risk_amount = self.equity * risk_percent
            position_size = risk_amount / current_close
            position_size = int(round(position_size))

            if position_size > 0:
                self.buy(size=position_size, trailing_sl=0.05)
                print(f"🌕✨🚀 MOON DEV ALERT: LONG ENTRY @ {current_close:.2f}")
                print(f"📈 Size: {position_size} | Equity: {self.equity:.2f}")

        # 💫 Exit handled automatically by trailing stop


# 🌙 Data Preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean columns
data.columns = data.columns.str.strip().str.lower()
data = data.loc[:, ~data.columns.str.contains("unnamed")]

# Format columns
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

# Set index
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# 🌟 Run Backtest
bt = Backtest(data, VolumetricCloud, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🚀 Print Results
print("\n🌕🌕🌕 MOON DEV BACKTEST RESULTS 🌕🌕🌕")
print(stats)
print(stats._strategy)
