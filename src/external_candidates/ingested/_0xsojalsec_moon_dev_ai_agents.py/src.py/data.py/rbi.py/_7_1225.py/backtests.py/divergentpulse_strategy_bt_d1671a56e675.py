# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\DivergentPulse_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DivergentPulseStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DivergentPulse strategy! 🚀")
        self.macd, self.signal, self.hist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.price_high = self.I(talib.MAX, self.data.High, 20)
        self.price_low = self.I(talib.MIN, self.data.Low, 20)
        self.macd_high = self.I(talib.MAX, self.hist, 20)
        self.macd_low = self.I(talib.MIN, self.hist, 20)
        self.rsi_high = self.I(talib.MAX, self.rsi, 20)
        self.rsi_low = self.I(talib.MIN, self.rsi, 20)
        self.current_day = None
        self.traded_today = False

    def next(self):
        current_day = self.data.index[-1].day
        if current_day != self.current_day:
            self.current_day = current_day
            self.traded_today = False

        if self.position or self.traded_today:
            return

        bullish_div_macd = (self.price_low[-1] < self.price_low[-2]) and (
            self.macd_low[-1] > self.macd_low[-2]
        )
        bullish_div_rsi = (self.price_low[-1] < self.price_low[-2]) and (
            self.rsi_low[-1] > self.rsi_low[-2]
        )
        if bullish_div_macd and bullish_div_rsi:
            print("🌙 Moon Dev bullish divergence! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + 3 * self.atr[-1]
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                self.traded_today = True
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        bearish_div_macd = (self.price_high[-1] > self.price_high[-2]) and (
            self.macd_high[-1] < self.macd_high[-2]
        )
        bearish_div_rsi = (self.price_high[-1] > self.price_high[-2]) and (
            self.rsi_high[-1] < self.rsi_high[-2]
        )
        if bearish_div_macd and bearish_div_rsi:
            print("🌙 Moon Dev bearish divergence! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 3 * self.atr[-1]
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                self.traded_today = True
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

bt = Backtest(data, DivergentPulseStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
