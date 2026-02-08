# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\VolatilitySurgeBreakout_BTFinal.py
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class VolatilitySurgeBreakout(Strategy):
    risk_percent = 0.01
    atr_period = 14
    bb_period = 20
    bb_dev = 2
    bbwp_window = 100
    volume_ma_period = 20
    exit_bars = 5

    def init(self):
        self.entry_bar = None
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        def bb_width(close):
            upper, middle, lower = talib.BBANDS(
                close,
                timeperiod=self.bb_period,
                nbdevup=self.bb_dev,
                nbdevdn=self.bb_dev,
            )
            return (upper - lower) / middle

        self.bb_width = self.I(bb_width, close)
        self.bbwp = self.I(ta.percentrank, self.bb_width, length=self.bbwp_window) * 100
        self.volume_ma = self.I(talib.SMA, volume, timeperiod=self.volume_ma_period)
        self.bb_width_sma = self.I(talib.SMA, self.bb_width, timeperiod=20)
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)

    def next(self):
        if self.position:
            if self.bb_width[-1] < self.bb_width_sma[-1]:
                self.position.close()
                print(f"🌙 Exit {self.position.type}! Closed due to BB contraction! ✨")
            elif (len(self.data) - 1) - self.entry_bar >= self.exit_bars:
                self.position.close()
                print(f"🌙 Time Exit! Held {self.exit_bars} bars! 🕒")

        else:
            if self.bbwp[-2] < 90 and self.bbwp[-1] >= 90 and self.data.Volume[-1] >= 1.5 * self.volume_ma[-1]:
                direction = "long" if self.data.Close[-1] > self.data.Open[-1] else "short"
                atr_value = self.atr[-1]
                risk_amount = self.equity * self.risk_percent
                entry_price = self.data.Close[-1]

                if direction == "long":
                    stop_loss = entry_price - 2 * atr_value
                    risk_per_share = entry_price - stop_loss
                else:
                    stop_loss = entry_price + 2 * atr_value
                    risk_per_share = stop_loss - entry_price

                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    if direction == "long":
                        self.buy(size=position_size, sl=stop_loss)
                        print(
                            f"🌙 Moon Dev LONG! 🚀 Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_loss:.2f}"
                        )
                    else:
                        self.sell(size=position_size, sl=stop_loss)
                        print(
                            f"🌙 Moon Dev SHORT! 🚀 Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_loss:.2f}"
                        )

                    self.entry_bar = len(self.data) - 1


data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

bt = Backtest(data, VolatilitySurgeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
