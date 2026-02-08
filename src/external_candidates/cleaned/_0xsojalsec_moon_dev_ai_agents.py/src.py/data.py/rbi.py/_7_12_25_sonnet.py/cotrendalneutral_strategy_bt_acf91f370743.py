# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\CoTrendalNeutral_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class CoTrendalNeutralStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating CoTrendalNeutral strategy! 🚀")
        self.sma_50 = self.I(talib.SMA, self.data.Close, 50)
        self.sma_200 = self.I(talib.SMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # Using RSI as proxy for VIX-like sentiment indicator
        self.vix_proxy = self.I(talib.RSI, self.data.Volume, 20)

    def next(self):
        if self.position:
            # Exit conditions based on sentiment reversal
            if (self.position.is_long and self.vix_proxy[-1] > 70) or (
                self.position.is_short and self.vix_proxy[-1] < 30
            ):
                print("🌙 Moon Dev sentiment reversal! Closing position. ✨")
                self.position.close()
            return

        # Long entry: upward trend with decreasing volatility (VIX proxy)
        trend_up = self.data.Close[-1] > self.sma_50[-1] and self.sma_50[-1] > self.sma_200[-1]
        vix_declining = self.vix_proxy[-1] < self.vix_proxy[-2] and self.vix_proxy[-1] < 50

        if trend_up and vix_declining:
            print("🌙 Moon Dev co-trendal bullish setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 6 * self.atr[-1]  # 3:1 risk reward
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short entry: downward trend with increasing volatility (VIX proxy)
        trend_down = self.data.Close[-1] < self.sma_50[-1] and self.sma_50[-1] < self.sma_200[-1]
        vix_rising = self.vix_proxy[-1] > self.vix_proxy[-2] and self.vix_proxy[-1] > 50

        if trend_down and vix_rising:
            print("🌙 Moon Dev co-trendal bearish setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 6 * self.atr[-1]  # 3:1 risk reward
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

bt = Backtest(data, CoTrendalNeutralStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
