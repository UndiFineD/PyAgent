# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\ClusterBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load data with Moon Dev precision 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.columns = ["datetime", "open", "high", "low", "close", "volume"]
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class ClusterBreakout(Strategy):
    def init(self):
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

    def next(self):
        volume_clusters = self.data.Volume.rolling(window=20).sum()
        cluster_high = self.data.High.rolling(window=20).max()
        cluster_low = self.data.Low.rolling(window=20).min()

        breakout_long = self.data.Close[-1] > cluster_high[-1] and self.data.Volume[-1] > volume_clusters[-1]
        breakout_short = self.data.Close[-1] < cluster_low[-1] and self.data.Volume[-1] > volume_clusters[-1]

        if self.data.Close[-2] < self.sma50[-2] and self.data.Close[-1] > self.sma50[-1]:
            if breakout_long and self.data.Close[-1] > self.sma50[-1]:
                sl = self.data.Close[-1] - self.atr[-1]
                tp = self.data.Close[-1] + 2 * self.atr[-1]
                risk_amount = 0.01 * self.equity
                position_size = int(round(risk_amount / (self.data.Close[-1] - sl)))
                if position_size > 0:
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌕 Moon Dev Alert: LONG position opened | Size: {position_size} units | Entry: {self.data.Close[-1]:.2f} | SL: {sl:.2f} | TP: {tp:.2f} 🚀"
                    )

        if self.sma50[-2] > self.data.Close[-2] and self.sma50[-1] < self.data.Close[-1]:
            if breakout_short and self.data.Close[-1] < self.sma50[-1]:
                sl = self.data.Close[-1] + self.atr[-1]
                tp = self.data.Close[-1] - 2 * self.atr[-1]
                risk_amount = 0.01 * self.equity
                position_size = int(round(risk_amount / (sl - self.data.Close[-1])))
                if position_size > 0:
                    self.sell(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌑 Moon Dev Alert: SHORT position opened | Size: {position_size} units | Entry: {self.data.Close[-1]:.2f} | SL: {sl:.2f} | TP: {tp:.2f} 🚀"
                    )


# Run backtest with lunar precision 🌙
bt = Backtest(data, ClusterBreakout, cash=1000000, commission=0.002)
stats = bt.run()
print("\n🌙✨ Moon Dev Backtest Complete ✨🌙")
print("=" * 40)
print(stats)
