# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\BandStochFusion_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandStochFusionStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandStochFusion strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.slowk, self.slowd = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # Exit logic
        if self.position:
            if self.position.is_long and self.data.Close[-1] >= self.middle[-1]:
                print("🌙 Moon Dev long position hit middle band! Closing. ✨")
                self.position.close()
            elif self.position.is_short and self.data.Close[-1] <= self.middle[-1]:
                print("🌙 Moon Dev short position hit middle band! Closing. ✨")
                self.position.close()
            return

        # Entry logic
        # Long Entry: Reversal from oversold at lower band
        is_oversold = self.slowk[-1] < 20 and self.slowd[-1] < 20
        is_price_low = self.data.Close[-1] < self.lower[-1]
        is_bullish_cross = (
            self.slowk[-1] > self.slowd[-1] and self.slowk[-2] <= self.slowd[-2]
        )

        if is_oversold and is_price_low and is_bullish_cross:
            print("🌙 Moon Dev bullish BandStochFusion setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            # No TP, exit is based on hitting middle band
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry: Reversal from overbought at upper band
        is_overbought = self.slowk[-1] > 80 and self.slowd[-1] > 80
        is_price_high = self.data.Close[-1] > self.upper[-1]
        is_bearish_cross = (
            self.slowk[-1] < self.slowd[-1] and self.slowk[-2] >= self.slowd[-2]
        )

        if is_overbought and is_price_high and is_bearish_cross:
            print("🌙 Moon Dev bearish BandStochFusion setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            # No TP, exit is based on hitting middle band
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
        data, BandStochFusionStrategy, cash=1000000, margin=1, commission=0.001
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
