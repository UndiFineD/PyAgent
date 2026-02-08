# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\VolgaDivergence_BTFinal_WORKING.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolgaDivergence(Strategy):
    def init(self):
        self.upper_kc = self.I(talib.MAX, self.data.High, timeperiod=20) + 2 * self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20
        )
        self.lower_kc = self.I(talib.MIN, self.data.Low, timeperiod=20) - 2 * self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20
        )
        self.upper_bb = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[0]
        self.lower_bb = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[2]
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)

    def next(self):
        if not self.position:
            if (
                self.data.Close[-1] > self.upper_kc[-1]
                and self.rsi[-1] < self.rsi[-2]
                and self.upper_bb[-1] > self.upper_bb[-2]
            ):
                risk = self.data.Close[-1] - self.lower_kc[-1]
                position_size = int(round(1000000 * 0.01 / risk))
                self.buy(size=position_size)
                print(f"🌙 Opening a position of {position_size} shares to the moon! 🚀")
        else:
            if self.data.Close[-1] < self.upper_kc[-1]:
                self.position.close()
                print("🌙 Closing position, taking profits! 💰")


# Load data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=True,
)

# Clean data
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

# Run backtest
bt = Backtest(data, VolgaDivergence, cash=1000000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
