# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\BandwidthPulse_BT.py
# 🌙 Moon Dev Backtest Engine ✨
import pandas as pd
import pandas_ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder

# 🚀 Data Preparation Phase
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Cleanse data with Moon Dev precision 🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class BandwidthPulse(Strategy):
    def init(self):
        # 🌗 Bollinger Band Components
        self.upper_band = self.I(lambda close: talib.BBANDS(close, 20, 2, 2)[0], self.data.Close)
        self.lower_band = self.I(lambda close: talib.BBANDS(close, 20, 2, 2)[2], self.data.Close)
        self.bandwidth = self.I(lambda u, l: u - l, self.upper_band, self.lower_band)
        self.bandwidth_low = self.I(talib.MIN, self.bandwidth, 10)
        self.bandwidth_sma5 = self.I(talib.SMA, self.bandwidth, 5)

        # 🌊 Klinger Volume Oscillator Setup
        def compute_kvo(high, low, volume):
            kvo_line, _ = pandas_ta.kvo(high, low, volume, 34, 55, 13)
            return kvo_line

        self.kvo = self.I(compute_kvo, self.data.High, self.data.Low, self.data.Volume)
        self.kvo_sma100 = self.I(talib.SMA, self.kvo, 100)

        # 🛡️ ATR for Volatility Stop
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        print("🌕 Moon Dev Indicators Activated! Trading at Lightspeed 🚀")

    def next(self):
        # 💡 Wait for full indicator warmup
        if len(self.data) < 155:
            return

        # 📊 Current Market Conditions
        price = self.data.Close[-1]
        bw_contraction = self.bandwidth[-1] < self.bandwidth_low[-1]
        bw_expanding = crossover(self.bandwidth, self.bandwidth_sma5)
        kvo_bullish = crossover(self.kvo, self.kvo_sma100)
        kvo_bearish = crossunder(self.kvo, self.kvo_sma100)
        atr_value = self.atr[-1] * 1.5

        # 💰 Risk Management Calculations
        equity = self.equity
        risk_amount = equity * 0.02
        position_size = int(round(risk_amount / atr_value)) if atr_value != 0 else 0

        # 🚦 Entry/Exit Logic
        if not self.position:
            if bw_contraction:
                if kvo_bullish and position_size > 0:
                    self.buy(size=position_size, sl=price - atr_value)
                    print(f"🌙✨ BULLISH PULSE DETECTED! Long {position_size} @ {price} 🚀")

                elif kvo_bearish and position_size > 0:
                    self.sell(size=position_size, sl=price + atr_value)
                    print(f"🌙🌑 BEARISH VORTEX SPOTTED! Short {position_size} @ {price} 🚨")

        elif bw_expanding:
            self.position.close()
            print(f"🌗 VOLATILITY SURGE! Closing position @ {price} 💎")


# 🌟 Execute Moon Dev Backtest
bt = Backtest(data, BandwidthPulse, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙=== MOON DEV FINAL STATISTICS ===🌙")
print(stats)
print(stats._strategy)
