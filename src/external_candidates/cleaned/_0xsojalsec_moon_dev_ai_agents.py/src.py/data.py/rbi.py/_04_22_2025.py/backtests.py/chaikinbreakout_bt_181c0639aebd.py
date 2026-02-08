# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests\ChaikinBreakout_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime").sort_index()


class ChaikinBreakout(Strategy):
    risk_pct = 0.01
    stop_loss = 0.02
    cmf_period = 20
    swing_window = 20
    exit_sma = 5

    def init(self):
        self.high_20 = self.I(talib.MAX, self.data.High, timeperiod=self.swing_window)
        self.low_20 = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_window)
        self.sma_5 = self.I(talib.SMA, self.data.Close, timeperiod=self.exit_sma)
        self.cmf = self.I(
            self._calc_cmf,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
        )

    def _calc_cmf(self, H, L, C, V):
        return ta.cmf(H, L, C, V, length=self.cmf_period)

    def next(self):
        if len(self.data) < max(self.swing_window, self.cmf_period, self.exit_sma) + 3:
            return

        cmf_values = self.cmf[-3:]
        has_cmf_confirmation = all(v > 0 for v in cmf_values) or all(v < 0 for v in cmf_values)

        if not self.position:
            # Long entry
            if self.data.High[-1] > self.high_20[-2] and all(v > 0 for v in cmf_values):
                equity_risk = self.equity * self.risk_pct
                risk_per_unit = self.data.Close[-1] * self.stop_loss
                units = int(round(equity_risk / risk_per_unit))
                if units > 0:
                    self.buy(size=units, sl=self.data.Close[-1] * (1 - self.stop_loss))
                    print(f"🌙🚀 BULLISH BREAKOUT! Long {units} units at {self.data.Close[-1]:.2f}")

            # Short entry
            elif self.data.Low[-1] < self.low_20[-2] and all(v < 0 for v in cmf_values):
                equity_risk = self.equity * self.risk_pct
                risk_per_unit = self.data.Close[-1] * self.stop_loss
                units = int(round(equity_risk / risk_per_unit))
                if units > 0:
                    self.sell(size=units, sl=self.data.Close[-1] * (1 + self.stop_loss))
                    print(f"🌙✨ BEARISH BREAKOUT! Short {units} units at {self.data.Close[-1]:.2f}")

        else:
            # Exit logic
            if self.position.is_long and crossover(self.sma_5, self.data.Close):
                self.position.close()
                print(f"🌙💎 CLOSING LONG at {self.data.Close[-1]:.2f} (SMA5 reversal)")
            elif self.position.is_short and crossover(self.data.Close, self.sma_5):
                self.position.close()
                print(f"🌙💎 CLOSING SHORT at {self.data.Close[-1]:.2f} (SMA5 reversal)")


bt = Backtest(data, ChaikinBreakout, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
