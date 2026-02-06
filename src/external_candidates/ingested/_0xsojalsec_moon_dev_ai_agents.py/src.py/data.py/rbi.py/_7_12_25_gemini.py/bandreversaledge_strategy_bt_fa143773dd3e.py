# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandReversalEdge_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandReversalEdgeStrategy(Strategy):
    time_limit = 3  # 3-bar time limit for the trade

    def init(self):
        print("🌙 Moon Dev initiating BandReversalEdge strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.entry_bar = None

    def next(self):
        # --- Time-based Exit Logic ---
        if self.position:
            # Exit if time limit is reached
            if self.position.is_long and (self.i - self.entry_bar >= self.time_limit):
                print("🌙 Moon Dev time limit reached! Closing long position. ✨")
                self.position.close()
            # Exit if profit target (upper band) is hit
            elif self.position.is_long and self.data.Close[-1] >= self.upper[-1]:
                print("🌙 Moon Dev profit target hit! Closing long position. ✨")
                self.position.close()
            return

        # --- Entry Logic (Long only) ---
        is_oversold = self.data.Close[-1] < self.lower[-1]

        if is_oversold:
            print("🌙 Moon Dev bullish BandReversalEdge setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 0.5 * self.atr[-1]

            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl)
                self.entry_bar = self.i  # Record entry bar index
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

    bt = Backtest(
        data, BandReversalEdgeStrategy, cash=1000000, margin=1, commission=0.001
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
