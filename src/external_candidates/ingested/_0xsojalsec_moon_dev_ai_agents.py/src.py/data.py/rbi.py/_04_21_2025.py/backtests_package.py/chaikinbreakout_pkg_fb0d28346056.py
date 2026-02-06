# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_package\ChaikinBreakout_PKG.py
import pandas as pd
import pandas_ta
import talib
from backtesting import Backtest, Strategy


class ChaikinBreakout(Strategy):
    def init(self):
        self.high_20 = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.low_20 = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.cmf = self.I(
            self._calculate_cmf,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            20,
        )

    def _calculate_cmf(self, high, low, close, volume, length):
        return pandas_ta.cmf(
            high=high, low=low, close=close, volume=volume, length=length
        )

    def next(self):
        if self.position:
            return

        current_close = self.data.Close[-1]
        high_20 = self.high_20[-1]
        low_20 = self.low_20[-1]
        cmf = self.cmf[-1]

        if current_close > high_20 and cmf > 0:
            sl = low_20
            risk = current_close - sl
            if risk > 0:
                size = int(round((self.equity * 0.01) / risk))
                if size > 0:
                    tp = current_close + 2 * risk
                    self.buy(size=size, sl=sl, tp=tp)
                    print(
                        f"🌙🚀 MOON DEV LONG SIGNAL! Entry: {current_close:.2f} | Size: {size} | Risk: {risk:.2f} | TP: {tp:.2f} | SL: {sl:.2f}"
                    )

        elif current_close < low_20 and cmf < 0:
            sl = high_20
            risk = sl - current_close
            if risk > 0:
                size = int(round((self.equity * 0.01) / risk))
                if size > 0:
                    tp = current_close - 2 * risk
                    self.sell(size=size, sl=sl, tp=tp)
                    print(
                        f"🌙📉 MOON DEV SHORT SIGNAL! Entry: {current_close:.2f} | Size: {size} | Risk: {risk:.2f} | TP: {tp:.2f} | SL: {sl:.2f}"
                    )


data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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

bt = Backtest(data, ChaikinBreakout, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
