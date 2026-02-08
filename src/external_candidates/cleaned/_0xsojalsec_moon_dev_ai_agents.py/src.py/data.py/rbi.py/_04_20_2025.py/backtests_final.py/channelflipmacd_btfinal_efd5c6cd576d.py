# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\ChannelFlipMACD_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ChannelFlipMACD(Strategy):
    def init(self):
        self.donchian_upper = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.macd_hist = self.I(
            lambda c: talib.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)[2],
            self.data.Close,
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.highest_high = None

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            hist = self.macd_hist
            if (
                len(hist) > 1
                and hist[-1] > 0
                and hist[-2] <= 0
                and price > self.donchian_upper[-1]
                and (self.atr[-1] / price) <= 0.03
            ):
                risk_amount = self.equity * 0.01
                stop_distance = 2 * self.atr[-1]
                stop_price = price - stop_distance
                size = int(round(risk_amount / stop_distance))

                if size > 0:
                    self.buy(size=size, sl=stop_price)
                    self.highest_high = self.data.High[-1]
                    print(f"🌙✨🚀 MOON DEV LONG ENTRY @ {price:.2f} | Size: {size} | SL: {stop_price:.2f}")

        elif self.position.is_long:
            self.highest_high = max(self.highest_high, self.data.High[-1])
            new_sl = self.highest_high - (2 * self.atr[-1])
            if new_sl > self.position.sl:
                self.position.sl = new_sl
                print(f"🌙🔧 Updated Moon Trail SL: {new_sl:.2f}")


# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(columns={k: k.title() for k in data.columns}, inplace=True)
data["Datetime"] = pd.to_datetime(data["datetime"])
data.set_index("Datetime", inplace=True)
data = data[["Open", "High", "Low", "Close", "Volume"]]

bt = Backtest(data, ChannelFlipMACD, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
