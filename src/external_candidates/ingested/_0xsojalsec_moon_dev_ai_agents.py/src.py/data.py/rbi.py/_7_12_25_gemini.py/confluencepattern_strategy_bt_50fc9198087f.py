# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\ConfluencePattern_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ConfluencePatternStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating ConfluencePattern strategy! 🚀")
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.macdsignal, self.macdhist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            return

        # Long Entry Conditions
        is_long_trend = (
            self.data.Close[-1] > self.ema50[-1]
            and self.data.Close[-1] > self.ema200[-1]
        )
        is_bullish_momentum = self.rsi[-1] > 50
        is_macd_buy = (
            self.macd[-1] > self.macdsignal[-1] and self.macd[-2] <= self.macdsignal[-2]
        )
        is_volume_confirm = self.data.Volume[-1] > self.volume_sma[-1]

        if is_long_trend and is_bullish_momentum and is_macd_buy and is_volume_confirm:
            print("🌙 Moon Dev bullish ConfluencePattern setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 3 * self.atr[-1]  # 1.5 R:R
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry Conditions
        is_short_trend = (
            self.data.Close[-1] < self.ema50[-1]
            and self.data.Close[-1] < self.ema200[-1]
        )
        is_bearish_momentum = self.rsi[-1] < 50
        is_macd_sell = (
            self.macd[-1] < self.macdsignal[-1] and self.macd[-2] >= self.macdsignal[-2]
        )

        if (
            is_short_trend
            and is_bearish_momentum
            and is_macd_sell
            and is_volume_confirm
        ):
            print("🌙 Moon Dev bearish ConfluencePattern setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 3 * self.atr[-1]  # 1.5 R:R
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


if __name__ == "__main__":
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
        data, ConfluencePatternStrategy, cash=1000000, margin=1, commission=0.001
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
