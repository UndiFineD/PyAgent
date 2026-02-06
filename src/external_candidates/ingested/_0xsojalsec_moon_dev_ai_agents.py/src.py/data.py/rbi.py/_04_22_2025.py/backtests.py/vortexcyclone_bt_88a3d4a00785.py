# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests\VortexCyclone_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VortexCycloneStrategy(Strategy):
    risk_per_trade = 0.01
    dpo_period = 20
    vi_period = 14
    max_trade_duration = 10

    def init(self):
        self.vi_plus, self.vi_minus = self.I(
            talib.VORTEX, self.data.High, self.data.Low, self.data.Close, self.vi_period
        )
        self.dpo = self.I(self.calculate_dpo, self.data.Close, self.dpo_period)
        self.dpo_std = self.I(talib.STDDEV, self.dpo, 20, nbdev=1)

    def calculate_dpo(self, close, period):
        sma = talib.SMA(close, timeperiod=period)
        shift_amount = int(period / 2 + 1)
        return close - sma.shift(shift_amount)

    def next(self):
        if len(self.data) < 20:
            return

        lower_entry = -1.5 * self.dpo_std[-1]
        upper_entry = 1.5 * self.dpo_std[-1]
        upper_exit = 1.0 * self.dpo_std[-1]

        # Exit conditions
        for trade in self.trades:
            if trade.is_long:
                if crossover(self.vi_minus, self.vi_plus) or crossover(
                    self.dpo, upper_exit
                ):
                    trade.close()
                    print(f"🌙✨ LONG exit at {self.data.Close[-1]} (VI-/DPO exit)")
                elif len(self.data) - trade.entry_bar >= self.max_trade_duration:
                    trade.close()
                    print(f"🌙⏳ LONG exit (max duration)")
            else:
                if crossover(self.vi_plus, self.vi_minus) or crossover(
                    -self.dpo, upper_exit
                ):
                    trade.close()
                    print(f"🌙✨ SHORT exit at {self.data.Close[-1]} (VI+/DPO exit)")
                elif len(self.data) - trade.entry_bar >= self.max_trade_duration:
                    trade.close()
                    print(f"🌙⏳ SHORT exit (max duration)")

        # Entry conditions
        if not self.position:
            # Long entry checks
            vi_cross_up = crossover(self.vi_plus, self.vi_minus)
            dpo_cross_above = crossover(self.dpo, lower_entry)

            # Short entry checks
            vi_cross_down = crossover(self.vi_minus, self.vi_plus)
            dpo_cross_below = crossover(upper_entry, self.dpo)

            if vi_cross_up and dpo_cross_above:
                swing_low = min(self.data.Low[-5:])
                risk_amount = self.equity * self.risk_per_trade
                risk_per_unit = self.data.Close[-1] - swing_low
                if risk_per_unit > 0:
                    size = int(round(risk_amount / risk_per_unit))
                    self.buy(size=size, sl=swing_low)
                    print(f"🌪️🚀 LONG ENTRY {size} units at {self.data.Close[-1]}!")

            elif vi_cross_down and dpo_cross_below:
                swing_high = max(self.data.High[-5:])
                risk_amount = self.equity * self.risk_per_trade
                risk_per_unit = swing_high - self.data.Close[-1]
                if risk_per_unit > 0:
                    size = int(round(risk_amount / risk_per_unit))
                    self.sell(size=size, sl=swing_high)
                    print(f"🌪️💥 SHORT ENTRY {size} units at {self.data.Close[-1]}!")


# Data handling
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
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
).set_index("datetime")

bt = Backtest(data, VortexCycloneStrategy, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
