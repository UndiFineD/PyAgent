# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\BandwidthBreakout_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandwidthBreakout(Strategy):
    def init(self):
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)

        def bb_width(close):
            upper, middle, lower = talib.BBANDS(
                close, timeperiod=20, nbdevup=2, nbdevdn=2
            )
            return (upper - lower) / middle

        self.bbw = self.I(bb_width, self.data.Close)
        self.bbw_min = self.I(talib.MIN, self.bbw, timeperiod=12096)

        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.trailing_stop = 0
        self.highest_high = 0
        self.lowest_low = float("inf")

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            if price > self.ema50[-1] and self.bbw[-1] <= self.bbw_min[-1]:
                risk = self.equity * 0.01
                atr_val = self.atr[-1] * 2
                size = int(round(risk / atr_val)) if atr_val else 0
                if size:
                    self.buy(size=size)
                    self.trailing_stop = price - atr_val
                    self.highest_high = self.data.High[-1]
                    print(
                        f"🚀 Moon Dev LONG 🌙 | Size: {size} @ {price:.2f} | ATR: {atr_val:.2f}"
                    )

            elif price < self.ema50[-1] and self.bbw[-1] <= self.bbw_min[-1]:
                risk = self.equity * 0.01
                atr_val = self.atr[-1] * 2
                size = int(round(risk / atr_val)) if atr_val else 0
                if size:
                    self.sell(size=size)
                    self.trailing_stop = price + atr_val
                    self.lowest_low = self.data.Low[-1]
                    print(
                        f"🌑 Moon Dev SHORT 🌙 | Size: {size} @ {price:.2f} | ATR: {atr_val:.2f}"
                    )

        else:
            if self.position.is_long:
                self.highest_high = max(self.highest_high, self.data.High[-1])
                new_stop = self.highest_high - 2 * self.atr[-1]
                self.trailing_stop = max(self.trailing_stop, new_stop)
                if price <= self.trailing_stop:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev EXIT LONG ✨ | Price: {price:.2f} | Trail: {self.trailing_stop:.2f}"
                    )

            elif self.position.is_short:
                self.lowest_low = min(self.lowest_low, self.data.Low[-1])
                new_stop = self.lowest_low + 2 * self.atr[-1]
                self.trailing_stop = min(self.trailing_stop, new_stop)
                if price >= self.trailing_stop:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev EXIT SHORT ✨ | Price: {price:.2f} | Trail: {self.trailing_stop:.2f}"
                    )


data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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

bt = Backtest(data, BandwidthBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
