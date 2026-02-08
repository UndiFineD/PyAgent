# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests\VolSqueezeBreakout_BT.py
import pandas as pd
import talib as ta
from backtesting import Backtest, Strategy

# Data preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
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


class VolSqueezeBreakout(Strategy):
    def init(self):
        # Bollinger Bands
        self.upper_bb = self.I(lambda c: ta.BBANDS(c, 20, 2, 2, 0)[0], self.data.Close, name="UpperBB")
        self.middle_bb = self.I(lambda c: ta.BBANDS(c, 20, 2, 2, 0)[1], self.data.Close, name="MiddleBB")
        self.lower_bb = self.I(lambda c: ta.BBANDS(c, 20, 2, 2, 0)[2], self.data.Close, name="LowerBB")

        # Volatility metrics
        self.bb_width = self.I(lambda u, l: u - l, self.upper_bb, self.lower_bb, name="BBWidth")
        self.min_width = self.I(ta.MIN, self.bb_width, 8640, name="MinWidth")

        # Volume indicators
        self.avg_volume = self.I(ta.SMA, self.data.Volume, 2880, name="AvgVolume")

    def next(self):
        if len(self.data) < 8640:
            return

        entry_long = (
            self.bb_width[-1] <= self.min_width[-1]
            and self.data.Close[-1] > self.upper_bb[-1]
            and self.data.Volume[-1] > 2 * self.avg_volume[-1]
        )

        entry_short = (
            self.bb_width[-1] <= self.min_width[-1]
            and self.data.Close[-1] < self.lower_bb[-1]
            and self.data.Volume[-1] > 2 * self.avg_volume[-1]
        )

        if not self.position:
            if entry_long:
                risk = 0.01 * self.equity
                entry_price = self.data.Close[-1]
                stop_loss = self.middle_bb[-1]
                risk_per_unit = entry_price - stop_loss

                if risk_per_unit > 0:
                    size = int(round(risk / risk_per_unit))
                    take_profit = entry_price + 1.5 * self.bb_width[-1]
                    print(
                        f"🌙✨🚀 LONG SIGNAL! Price: {entry_price:.2f}, Size: {size}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}"
                    )
                    self.buy(size=size, sl=stop_loss, tp=take_profit)

            elif entry_short:
                risk = 0.01 * self.equity
                entry_price = self.data.Close[-1]
                stop_loss = self.middle_bb[-1]
                risk_per_unit = stop_loss - entry_price

                if risk_per_unit > 0:
                    size = int(round(risk / risk_per_unit))
                    take_profit = entry_price - 1.5 * self.bb_width[-1]
                    print(
                        f"🌙✨🚀 SHORT SIGNAL! Price: {entry_price:.2f}, Size: {size}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}"
                    )
                    self.sell(size=size, sl=stop_loss, tp=take_profit)


bt = Backtest(data, VolSqueezeBreakout, cash=1_000_000, margin=1.0)
stats = bt.run()
print(stats)
print(stats._strategy)
