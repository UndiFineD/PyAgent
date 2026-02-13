# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\DeltaSentiment_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class DeltaSentimentStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating DeltaSentiment strategy! 🚀")
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # Using volume RSI as proxy for VIX sentiment
        self.sentiment_proxy = self.I(talib.RSI, self.data.Volume, 20)
        self.liquidity_proxy = self.I(talib.SMA, self.data.Volume, 20)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

    def next(self):
        if self.position:
            # Exit on sentiment reversal or liquidity deterioration
            if self.position.is_long:
                if (
                    self.sentiment_proxy[-1] > 70
                    or self.data.Volume[-1] < 0.5 * self.liquidity_proxy[-1]
                ):
                    print("🌙 Moon Dev sentiment/liquidity reversal! Closing long. ✨")
                    self.position.close()
            elif self.position.is_short:
                if (
                    self.sentiment_proxy[-1] < 30
                    or self.data.Volume[-1] < 0.5 * self.liquidity_proxy[-1]
                ):
                    print("🌙 Moon Dev sentiment/liquidity reversal! Closing short. ✨")
                    self.position.close()
            return

        # High liquidity check
        high_liquidity = self.data.Volume[-1] > 1.2 * self.liquidity_proxy[-1]

        # Long entry: high liquidity + bullish sentiment (narrowing spread proxy)
        bullish_sentiment = (
            self.sentiment_proxy[-1] < self.sentiment_proxy[-2]
            and self.sentiment_proxy[-1] < 50
        )

        if high_liquidity and bullish_sentiment:
            print("🌙 Moon Dev bullish DeltaSentiment setup! Entering long. 🚀")
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

        # Short entry: high liquidity + bearish sentiment (widening spread proxy)
        bearish_sentiment = (
            self.sentiment_proxy[-1] > self.sentiment_proxy[-2]
            and self.sentiment_proxy[-1] > 50
        )

        if high_liquidity and bearish_sentiment:
            print("🌙 Moon Dev bearish DeltaSentiment setup! Entering short. 🚀")
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
        data, DeltaSentimentStrategy, cash=1000000, margin=1, commission=0.001
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
