# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests\VoltaicBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


class VoltaicBreakout(Strategy):
    n1 = 20
    n2 = 2

    def init(self):
        self.keltner_middle = self.I(talib.EMA, self.data.Close, timeperiod=self.n1)
        self.keltner_upper = self.keltner_middle + 2 * self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.n1,
        )
        self.keltner_lower = self.keltner_middle - 2 * self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.n1,
        )

        self.bb_middle = self.I(talib.SMA, self.data.Close, timeperiod=self.n1)
        self.bb_std = self.I(talib.STDDEV, self.data.Close, timeperiod=self.n1)
        self.bb_upper = self.bb_middle + self.n2 * self.bb_std
        self.bb_lower = self.bb_middle - self.n2 * self.bb_std

        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_previous = self.rsi.shift(1)

        self.low_previous = self.data.Low.shift(1)

    def next(self):
        if not self.position:
            if (
                self.data.Low[-1] < self.low_previous
                and self.rsi[-1] > self.rsi_previous
            ):
                if crossover(self.data.Close, self.keltner_upper):
                    if self.bb_upper[-1] > self.bb_upper[-2]:
                        risk_amount = self.equity * 0.01
                        risk = self.data.Close - self.keltner_lower
                        position_size = risk_amount / risk
                        self.buy(size=int(round(position_size)))
                        print(
                            f"🌙 VoltaicBreakout Entry Signal! Bought {position_size:.2f} units. 🚀"
                        )
        else:
            if crossover(self.keltner_middle, self.data.Close):
                self.sell()
                print("✨ VoltaicBreakout Exit Signal! Closed position. 💰")

            if self.bb_upper[-1] < self.bb_upper[-2]:
                self.sell()
                print("🚨 Emergency Exit! Volatility collapsed. Position closed. 🛡️")


# Load data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.columns = [col.capitalize() for col in data.columns]
data = data.set_index("Datetime")
data.index = pd.to_datetime(data.index)

# Run backtest
bt = Backtest(data, VoltaicBreakout, cash=1_000_000)
stats = bt.run()

print(stats)
print(stats._strategy)
