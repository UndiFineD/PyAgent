# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests\VolatilitySurge_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Data handling
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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
        self.upper_band = self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close)
        self.lower_band = self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 30)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if not self.position:
            if len(self.data.Close) < 2 or len(self.upper_band) < 2:
                return

            close_cross = self.data.Close[-2] <= self.upper_band[-2] and self.data.Close[-1] > self.upper_band[-1]

            if close_cross and self.adx[-1] > 25:
                vol_ratio = self.data.Volume[-1] / self.volume_sma[-1]
                if vol_ratio >= 1.2:
                    sl = min(self.lower_band[-1], self.swing_low[-1])
                    risk = self.data.Close[-1] - sl
                    if risk <= 0:
                        return

                    risk_amount = 0.01 * self.equity
                    position_size = int(round(risk_amount / risk))
                    tp = self.data.Close[-1] + 2 * risk

                    if position_size > 0:
                        print(f"🌙🚀 MOON ENTRY: Size {position_size} @ {self.data.Close[-1]:.2f} | SL: {sl:.2f} ✨")
                        self.buy(size=position_size, sl=sl, tp=tp)


bt = Backtest(data, VolatilitySurge, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
