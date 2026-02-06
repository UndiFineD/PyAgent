# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\BandSqueezeTrend_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandSqueezeTrend(Strategy):
    def init(self):
        self.bbands_upper, self.bbands_middle, self.bbands_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20
        )
        self.atr_sma = self.I(talib.SMA, self.atr, timeperiod=20)

    def next(self):
        if (
            self.data.Close[-1] > self.bbands_upper[-1]
            and self.data.Close[-1] < self.atr_sma[-1]
        ):
            atr_value = self.atr[-1]
            sl = self.data.Close[-1] - 0.5 * atr_value
            tp = self.data.Close[-1] + 1.5 * atr_value
            position_size = int(
                1_000_000 / self.data.Close[-1]
            )  # Size based on $1,000,000 capital

            self.buy(size=position_size, sl=sl, tp=tp)
            print(
                f"🌙 🚀 Buy Signal: Close={self.data.Close[-1]:.2f}, SL={sl:.2f}, TP={tp:.2f}"
            )

        if self.position and self.data.Close[-1] < self.bbands_middle[-1]:
            self.position.close()
            print(
                f"🌙 ✨ Exit Signal: Close={self.data.Close[-1]:.2f}, Middle Band={self.bbands_middle[-1]:.2f}"
            )


# Load and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=True,
    index_col=0,
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.columns = ["Open", "High", "Low", "Close", "Volume"]

# Run backtest
bt = Backtest(data, BandSqueezeTrend, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
