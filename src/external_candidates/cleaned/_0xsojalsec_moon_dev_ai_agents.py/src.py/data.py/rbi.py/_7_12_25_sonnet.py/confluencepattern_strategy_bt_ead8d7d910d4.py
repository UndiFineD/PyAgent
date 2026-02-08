# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\ConfluencePattern_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ConfluencePatternStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating ConfluencePattern strategy! 🚀")
        self.ema_50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema_200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.signal, self.hist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)

    def next(self):
        if self.position:
            # Exit on indicator reversal
            if (self.position.is_long and (self.rsi[-1] > 70 or crossover(self.signal, self.macd))) or (
                self.position.is_short and (self.rsi[-1] < 30 or crossover(self.macd, self.signal))
            ):
                print("🌙 Moon Dev indicator reversal! Closing position. ✨")
                self.position.close()
            return

        # Bullish confluence
        trend_up = self.data.Close[-1] > self.ema_50[-1] and self.ema_50[-1] > self.ema_200[-1]
        rsi_oversold = self.rsi[-1] < 30
        macd_bullish = crossover(self.macd, self.signal)
        volume_confirm = self.data.Volume[-1] > self.data.Volume[-2]

        if trend_up and rsi_oversold and macd_bullish and volume_confirm:
            print("🌙 Moon Dev bullish confluence detected! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Bearish confluence
        trend_down = self.data.Close[-1] < self.ema_50[-1] and self.ema_50[-1] < self.ema_200[-1]
        rsi_overbought = self.rsi[-1] > 70
        macd_bearish = crossover(self.signal, self.macd)

        if trend_down and rsi_overbought and macd_bearish and volume_confirm:
            print("🌙 Moon Dev bearish confluence detected! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 2 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


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

bt = Backtest(data, ConfluencePatternStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
