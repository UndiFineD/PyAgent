# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\ChannelFlowBreakout_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
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


class ChannelFlowBreakout(Strategy):
    risk_percent = 0.01
    donchian_period = 20

    def init(self):
        self.upper = self.I(talib.MAX, self.data.High, timeperiod=self.donchian_period)
        self.lower = self.I(talib.MIN, self.data.Low, timeperiod=self.donchian_period)
        self.cmf = self.I(
            talib.CMF,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            timeperiod=self.donchian_period,
        )

    def next(self):
        if len(self.data) < self.donchian_period + 1 or len(self.cmf) < 3:
            return

        if not self.position:
            prev_close = self.data.Close[-2]
            prev_upper = self.upper[-2]
            prev_lower = self.lower[-2]
            prev_cmf = self.cmf[-2]
            prev_cmf_2 = self.cmf[-3]

            # Long entry logic
            if prev_close > prev_upper and prev_cmf > 0 and prev_cmf_2 <= 0:
                entry_price = self.data.Open[-1]
                sl = prev_lower
                risk_per_share = entry_price - sl
                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_percent
                    size = int(round(risk_amount / risk_per_share))
                    if size > 0:
                        tp = entry_price + 2 * risk_per_share
                        self.buy(size=size, sl=sl, tp=tp)
                        print(
                            f"🌙🚀 MOON DEV LONG! Entry: {entry_price:.2f}, Size: {size} | SL: {sl:.2f} | TP: {tp:.2f} | 1-2-3 LIFT OFF!"
                        )

            # Short entry logic
            elif prev_close < prev_lower and prev_cmf < 0 and prev_cmf_2 >= 0:
                entry_price = self.data.Open[-1]
                sl = prev_upper
                risk_per_share = sl - entry_price
                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_percent
                    size = int(round(risk_amount / risk_per_share))
                    if size > 0:
                        tp = entry_price - 2 * risk_per_share
                        self.sell(size=size, sl=sl, tp=tp)
                        print(
                            f"🌙🌌 MOON DEV SHORT! Entry: {entry_price:.2f}, Size: {size} | SL: {sl:.2f} | TP: {tp:.2f} | TO THE DARK SIDE!"
                        )


bt = Backtest(data, ChannelFlowBreakout, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
