# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\VortexSurge_BT.py
# 🌙 Moon Dev's VortexSurge Backtest Script 🚀

import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VortexSurge(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌟
    swing_period = 20
    keltner_period = 20
    volume_window = 960  # 10 days in 15m intervals (10*24*4=960) 📅

    def init(self):
        # 🌀 Vortex Indicator Calculations
        self.vi_plus = self.I(
            self._calculate_vortex_plus, self.data.High, self.data.Low, self.data.Close
        )
        self.vi_minus = self.I(
            self._calculate_vortex_minus, self.data.High, self.data.Low, self.data.Close
        )

        # 📊 Volume Filter Indicators
        self.volume_avg = self.I(talib.SMA, self.data.Volume, self.volume_window)

        # 📈 Keltner Channel Components
        self.ema = self.I(talib.EMA, self.data.Close, self.keltner_period)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.keltner_period,
        )

        # 🛑 Swing Low for Stop Loss
        self.swing_low = self.I(talib.MIN, self.data.Low, self.swing_period)

    def _calculate_vortex_plus(self, high, low, close):
        vortex = ta.vortex(high=high, low=low, close=close, length=14)
        return vortex["VIp"]

    def _calculate_vortex_minus(self, high, low, close):
        vortex = ta.vortex(high=high, low=low, close=close, length=14)
        return vortex["VIm"]

    def next(self):
        if not self.position:
            # 🌪️ Entry Logic: VI+ crosses VI- with volume surge
            if crossover(self.vi_plus, self.vi_minus):
                if self.data.Volume[-1] >= 1.5 * self.volume_avg[-1]:
                    stop_price = self.swing_low[-1]
                    entry_price = self.data.Close[-1]
                    risk_per_share = entry_price - stop_price

                    if risk_per_share > 0:
                        position_size = int(
                            round((self.equity * self.risk_percent) / risk_per_share)
                        )
                        if position_size > 0:
                            self.buy(size=position_size, sl=stop_price)
                            print(
                                f"🌙✨ MOON DEV ALERT: Long entry at {entry_price:.2f}! "
                                f"VI+ SURGE + VOLUME BOOST 🚀 (Size: {position_size})"
                            )
        else:
            # 💰 Exit Logic: Keltner Upper or VI reversal
            current_upper = self.ema[-1] + 2 * self.atr[-1]

            if self.data.High[-1] >= current_upper:
                self.position.close()
                print(f"🌙💎 PROFIT TAKEN: Kissed Keltner Upper {current_upper:.2f} 💋")

            elif crossover(self.vi_minus, self.vi_plus):
                self.position.close()
                print("🌙⚡ VI REVERSAL DETECTED! Abandoning position ⚠️")


# 🧹 Data Cleaning Ritual
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
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

# 🚀 Launch Backtest
bt = Backtest(data, VortexSurge, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print("\n🌙✨ MOON DEV FINAL STATS ✨🌙")
print(stats)
print(stats._strategy)
