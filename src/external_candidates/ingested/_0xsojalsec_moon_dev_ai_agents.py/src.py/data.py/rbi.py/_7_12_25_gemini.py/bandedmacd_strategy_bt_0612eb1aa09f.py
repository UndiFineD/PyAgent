# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandedMACD_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandedMACDStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandedMACD strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.macd, self.macdsignal, self.macdhist = self.I(
            talib.MACD, self.data.Close, 12, 26, 9
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # --- Exit Logic ---
        if self.position:
            # Exit if price is at upper band and a pullback starts
            is_overbought = self.data.Close[-1] >= self.upper[-1]
            is_pullback = self.data.Close[-1] < self.data.Close[-2]

            if is_overbought and is_pullback:
                print(
                    "🌙 Moon Dev overbought pullback detected! Closing long position. ✨"
                )
                self.position.close()
            return

        # --- Entry Logic (Long only) ---
        is_uptrend = self.data.Close[-1] > self.middle[-1]
        is_macd_cross_up = (
            self.macd[-1] > self.macdsignal[-1] and self.macd[-2] <= self.macdsignal[-2]
        )
        is_not_overbought = self.data.Close[-1] < self.upper[-1]

        if is_uptrend and is_macd_cross_up and is_not_overbought:
            print("🌙 Moon Dev bullish BandedMACD setup! Entering long. 🚀")
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

        # No short logic as per strategy description


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

    bt = Backtest(data, BandedMACDStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
