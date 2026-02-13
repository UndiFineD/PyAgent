# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\VolatilitySurge_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolatilitySurge(Strategy):
    def init(self):
        self.upper_band = self.I(self._calc_upper_band)
        self.middle_band = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.lower_band = self.I(self._calc_lower_band)

        self.bandwidth = self.I(
            lambda u, l, m: (u - l) / m,
            self.upper_band,
            self.lower_band,
            self.middle_band,
        )
        self.bandwidth_pct = self.I(
            lambda x: x.rolling(20).quantile(0.2), self.bandwidth
        )
        self.volume_roc = self.I(talib.ROC, self.data.Volume, timeperiod=1)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

    def _calc_upper_band(self, close):
        upper, _, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        return upper

    def _calc_lower_band(self, close):
        _, _, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        return lower

    def next(self):
        if not self.position:
            if (
                self.data.Close[-1] > self.upper_band[-1]
                and self.volume_roc[-1] > 200
                and self.bandwidth[-1] < self.bandwidth_pct[-1]
            ):

                risk = self.data.Close[-1] - self.lower_band[-1]
                if risk <= 0:
                    print("🌙 Risk <=0, aborting LONG")
                    return
                size = int(round((self.equity * 0.01) / risk))
                if size > 0:
                    self.buy(size=size, sl=self.lower_band[-1])
                    print(
                        f"🌕 MOON DEV LONG! Size: {size} @ {self.data.Close[-1]} SL: {self.lower_band[-1]}"
                    )

            elif (
                self.data.Close[-1] < self.lower_band[-1]
                and self.volume_roc[-1] > 200
                and self.bandwidth[-1] < self.bandwidth_pct[-1]
            ):

                risk = self.upper_band[-1] - self.data.Close[-1]
                if risk <= 0:
                    print("🌙 Risk <=0, aborting SHORT")
                    return
                size = int(round((self.equity * 0.01) / risk))
                if size > 0:
                    self.sell(size=size, sl=self.upper_band[-1])
                    print(
                        f"🌑 MOON DEV SHORT! Size: {size} @ {self.data.Close[-1]} SL: {self.upper_band[-1]}"
                    )

        else:
            if self.position.is_long and (
                self.lower_band[-2] > self.data.Close[-2]
                and self.lower_band[-1] < self.data.Close[-1]
            ):
                self.position.close()
                print("🚀 LONG TP HIT!")
            elif self.position.is_short and (
                self.data.Close[-2] < self.upper_band[-2]
                and self.data.Close[-1] > self.upper_band[-1]
            ):
                self.position.close()
                print("🚀 SHORT TP HIT!")


data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
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

bt = Backtest(data, VolatilitySurge, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
