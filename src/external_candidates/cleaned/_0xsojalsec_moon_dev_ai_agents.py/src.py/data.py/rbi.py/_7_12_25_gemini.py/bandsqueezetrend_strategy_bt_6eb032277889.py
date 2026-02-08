# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandSqueezeTrend_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandSqueezeTrendStrategy(Strategy):
    atr_period = 20
    atr_ma_period = 50

    def init(self):
        print("🌙 Moon Dev initiating BandSqueezeTrend strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.atr_ma = self.I(talib.SMA, self.atr, self.atr_ma_period)

    def next(self):
        # --- Exit Logic ---
        if self.position:
            # Additional exit if price closes below the middle band
            if self.data.Close[-1] < self.middle[-1]:
                print("🌙 Moon Dev price fell below middle band! Closing long position. ✨")
                self.position.close()
            return

        # --- Entry Logic (Long only) ---
        # Condition 1: Price breaks above the upper Bollinger Band
        is_breakout = self.data.Close[-1] > self.upper[-1] and self.data.Close[-2] <= self.upper[-2]

        # Condition 2: Volatility is not excessively high
        is_vol_stable = self.atr[-1] < (1.5 * self.atr_ma[-1])

        if is_breakout and is_vol_stable:
            print("🌙 Moon Dev bullish BandSqueezeTrend setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            current_atr = self.atr[-1]

            # The strategy doc has an unusual R:R of 3:1 (1.5 / 0.5)
            sl = entry_price - 0.5 * current_atr
            tp = entry_price + 1.5 * current_atr

            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
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

    bt = Backtest(data, BandSqueezeTrendStrategy, cash=1000000, margin=1, commission=0.001)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
