# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\10_20_2025\backtests_final\MidpointCrossover_BTFinal_WORKING.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path)
data["Datetime"] = pd.to_datetime(data["datetime"])
data = data.drop("datetime", axis=1)
data.set_index("Datetime", inplace=True)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.columns = [col.capitalize() for col in data.columns]


class MidpointCrossover(Strategy):
    bbmp_period = 50
    sma_period = 200
    stddev_mult = 2.0
    risk_per_trade = 0.01

    def init(self):
        self.bbmp = self.I(talib.SMA, self.data.Close, timeperiod=self.bbmp_period)
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period)
        self.stddev = self.I(
            lambda x: pd.Series(x).rolling(self.bbmp_period).std(), self.data.Close
        )
        self.trail_stop = None

    def next(self):
        if len(self.data) < self.sma_period:
            return

        # Entry logic: BBMP crosses above SMA200
        if (
            not self.position
            and self.bbmp[-1] > self.sma200[-1]
            and self.bbmp[-2] <= self.sma200[-2]
        ):
            entry_price = self.data.Close[-1]
            initial_stop = self.bbmp[-1] - self.stddev_mult * self.stddev[-1]
            if entry_price > initial_stop:
                risk_per_unit = entry_price - initial_stop
                risk_amount = self.risk_per_trade * self.equity
                position_size = risk_amount / risk_per_unit
                size = int(round(position_size))
                if size > 0:
                    self.buy(size=size)
                    self.trail_stop = initial_stop
                    print(
                        f"🌙 Moon Dev Long Entry! Price: {entry_price:.2f}, Size: {size}, Initial Stop: {initial_stop:.2f} 🚀"
                    )
            else:
                print(
                    f"🌙 Invalid entry: Entry {entry_price:.2f} <= Stop {initial_stop:.2f} ⚠️"
                )

        # Exit logic if in position
        elif self.position:
            # Signal exit: BBMP crosses below SMA200
            if self.bbmp[-1] < self.sma200[-1] and self.bbmp[-2] >= self.sma200[-2]:
                self.position.close()
                print(
                    f"🌙 Moon Dev Signal Exit! Price: {self.data.Close[-1]:.2f}, BBMP: {self.bbmp[-1]:.2f}, SMA200: {self.sma200[-1]:.2f} 📉"
                )
                self.trail_stop = None
            else:
                # Update trailing stop
                potential_stop = self.bbmp[-1] - self.stddev_mult * self.stddev[-1]
                if potential_stop > self.trail_stop:
                    old_stop = self.trail_stop
                    self.trail_stop = potential_stop
                    print(
                        f"🌙 Trail Stop Updated from {old_stop:.2f} to {self.trail_stop:.2f} ✨"
                    )
                # Check trailing stop hit
                if self.data.Close[-1] < self.trail_stop:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Trail Stop Hit! Price: {self.data.Close[-1]:.2f}, Stop: {self.trail_stop:.2f} 🛑"
                    )
                    self.trail_stop = None


bt = Backtest(
    data, MidpointCrossover, cash=10000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
print(stats._strategy)
