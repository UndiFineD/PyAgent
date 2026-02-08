# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\ChikouVolatility_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ChikouVolatilityStrategy(Strategy):
    chikou_period = 26

    def init(self):
        print("🌙 Moon Dev initiating ChikouVolatility strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # The data needs to be long enough for Chikou Span comparison
        if len(self.data) < self.chikou_period + 1:
            print("Not enough data for Chikou Span yet.")

    def next(self):
        # Ensure we have enough data for the lookback
        if len(self.data.Close) <= self.chikou_period:
            return

        # --- Exit Logic ---
        if self.position:
            if self.position.is_long and self.data.Close[-1] >= self.upper[-1]:
                print("🌙 Moon Dev long hit upper band! Closing position. ✨")
                self.position.close()
            elif self.position.is_short and self.data.Close[-1] <= self.lower[-1]:
                print("🌙 Moon Dev short hit lower band! Closing position. ✨")
                self.position.close()
            return

        # --- Entry Logic ---
        # Bullish Entry
        is_bullish_trend = self.data.Close[-1] > self.data.High[-1 - self.chikou_period]
        was_oversold = self.data.Close[-2] < self.lower[-2]
        is_recovering = self.data.Close[-1] > self.lower[-1]

        if is_bullish_trend and was_oversold and is_recovering:
            print("🌙 Moon Dev bullish ChikouVolatility setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Bearish Entry
        is_bearish_trend = self.data.Close[-1] < self.data.Low[-1 - self.chikou_period]
        was_overbought = self.data.Close[-2] > self.upper[-2]
        is_reversing = self.data.Close[-1] < self.upper[-1]

        if is_bearish_trend and was_overbought and is_reversing:
            print("🌙 Moon Dev bearish ChikouVolatility setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


if __name__ == "__main__":
    data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
    # Make sure data is long enough for the strategy to run
    # data = data.iloc[ChikouVolatilityStrategy.chikou_period:] # This is not needed, backtesting.py handles warmup
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

    bt = Backtest(data, ChikouVolatilityStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
