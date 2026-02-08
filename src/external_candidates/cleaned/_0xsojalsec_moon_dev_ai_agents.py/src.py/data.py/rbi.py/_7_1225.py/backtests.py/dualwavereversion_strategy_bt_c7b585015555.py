# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\DualWaveReversion_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DualWaveReversionStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DualWaveReversion strategy! 🚀")
        self.sma50 = self.I(talib.SMA, self.data.Close, 50)
        self.ema20 = self.I(talib.EMA, self.data.Close, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_i = None

    def next(self):
        if self.position:
            bars_since = self._i - self.entry_i
            if bars_since > 5 * 96:  # 5 days * 96 15m bars per day
                print("🌙 Moon Dev time-based exit triggered! Closing position. ✨")
                self.position.close()
            return

        # Check for EMA crossing below SMA
        if self.ema20[-1] < self.sma50[-1] and (len(self.ema20) < 2 or self.ema20[-2] >= self.sma50[-2]):
            print("🌙 Moon Dev detected EMA cross below SMA! Preparing entry. 🚀")
            entry_price = self.data.Close[-1]
            atr_value = self.atr[-1]
            stop_loss = entry_price - 0.01 * atr_value  # 1% of ATR as per description
            take_profit = entry_price + 0.03 * atr_value  # 3% of ATR
            risk_per_unit = entry_price - stop_loss
            if risk_per_unit <= 0:
                print("🌙 Moon Dev risk calculation invalid, skipping entry. ⚠️")
                return
            risk_amount = self.equity * 0.01  # 1% risk
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                self.entry_i = self._i
                print(
                    f"🌙 Moon Dev entered long position with size {position_size}! SL: {stop_loss}, TP: {take_profit} ✨"
                )
            else:
                print("🌙 Moon Dev position size too small, skipping. ⚠️")


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
    data, DualWaveReversionStrategy, cash=1000000, margin=0.5, commission=0.001
)  # 2x leverage, small commission
stats = bt.run()
print(stats)
print(stats._strategy)
