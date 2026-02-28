# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\VolSqueezeBreakout_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolSqueezeBreakout(Strategy):
    risk_percent = 0.01
    lookback_period = 100
    bb_period = 20
    vol_ma_period = 30

    def init(self):
        close = self.data.Close
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS,
            close,
            timeperiod=self.bb_period,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
        )
        self.bb_width = (self.upper - self.lower) / self.middle
        self.volume_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=self.vol_ma_period
        )

    def next(self):
        current_idx = len(self.data) - 1
        if current_idx < self.lookback_period + 1:
            return

        start_idx = current_idx - self.lookback_period
        recent_bb_width = self.bb_width[start_idx:current_idx]
        current_bb_width = self.bb_width[current_idx]
        percentile_10 = np.percentile(recent_bb_width, 10)
        bb_squeeze = current_bb_width <= percentile_10

        current_volume = self.data.Volume[current_idx]
        volume_spike = current_volume > self.volume_sma[current_idx]

        entry_price = self.data.Close[current_idx]
        upper = self.upper[current_idx]
        lower = self.lower[current_idx]

        if not self.position:
            if bb_squeeze and volume_spike:
                if (
                    entry_price > upper
                    and self.data.Close[current_idx - 1] <= self.upper[current_idx - 1]
                ):
                    sl_price = lower
                    risk_per_share = entry_price - sl_price
                    if risk_per_share <= 0:
                        return
                    risk_amount = self.equity * self.risk_percent
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(
                            size=position_size,
                            sl=sl_price,
                            tp=entry_price + 2 * risk_per_share,
                        )
                        print(
                            f"🌙🚀 MOON DEV LONG ENTRY | Price: {entry_price:.2f} | Size: {position_size} | SL: {sl_price:.2f} | TP: {entry_price + 2 * risk_per_share:.2f}"
                        )

                elif (
                    entry_price < lower
                    and self.data.Close[current_idx - 1] >= self.lower[current_idx - 1]
                ):
                    sl_price = upper
                    risk_per_share = sl_price - entry_price
                    if risk_per_share <= 0:
                        return
                    risk_amount = self.equity * self.risk_percent
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.sell(
                            size=position_size,
                            sl=sl_price,
                            tp=entry_price - 2 * risk_per_share,
                        )
                        print(
                            f"🌙🌑 MOON DEV SHORT ENTRY | Price: {entry_price:.2f} | Size: {position_size} | SL: {sl_price:.2f} | TP: {entry_price - 2 * risk_per_share:.2f}"
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

bt = Backtest(data, VolSqueezeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
