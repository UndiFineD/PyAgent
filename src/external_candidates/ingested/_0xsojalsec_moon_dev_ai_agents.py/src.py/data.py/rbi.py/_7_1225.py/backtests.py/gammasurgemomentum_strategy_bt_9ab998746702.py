# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\GammaSurgeMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class GammaSurgeMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating GammaSurgeMomentum strategy! 🚀")
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20)
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_i = None

    def next(self):
        if self.position:
            bars_since = self._i - self.entry_i
            if bars_since > 288:  # 3 days
                print("🌙 Moon Dev time exit! Closing position. ✨")
                self.position.close()
            elif (entry_price * 1.1) <= self.data.Close[-1]:
                print("🌙 Moon Dev 10% target reached! Closing position. ✨")
                self.position.close()
            return

        if self.data.Volume[-1] > 2 * self.avg_volume[-1] and crossover(
            self.macd, self.signal
        ):
            print("🌙 Moon Dev detected gamma surge! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price * 1.1
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                self.entry_i = self._i
                print(
                    f"🌙 Moon Dev entered long with size {position_size}! SL: {sl}, TP: {tp} ✨"
                )


data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
print("🌙 Moon Dev loading BTC-USD data... 🚀")
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
print("🌙 Moon Dev data cleaning complete! ✨")

bt = Backtest(
    data, GammaSurgeMomentumStrategy, cash=1000000, margin=2, commission=0.001
)  # 2x leverage as per strategy
stats = bt.run()
print(stats)
print(stats._strategy)
