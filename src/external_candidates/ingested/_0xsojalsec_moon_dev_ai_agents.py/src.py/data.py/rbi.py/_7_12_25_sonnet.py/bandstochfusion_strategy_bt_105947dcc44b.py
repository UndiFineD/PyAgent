# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_sonnet\BandStochFusion_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandStochFusionStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandStochFusion strategy! 🚀")
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(
            talib.BBANDS, self.data.Close, 20, 2, 2
        )
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH, self.data.High, self.data.Low, self.data.Close, 14, 3, 3
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if self.position:
            # Exit conditions
            if self.position.is_long:
                if self.data.Close[-1] >= self.middle_bb[-1] or self.stoch_k[-1] > 80:
                    print("🌙 Moon Dev long exit trigger! Closing position. ✨")
                    self.position.close()
            elif self.position.is_short:
                if self.data.Close[-1] <= self.middle_bb[-1] or self.stoch_k[-1] < 20:
                    print("🌙 Moon Dev short exit trigger! Closing position. ✨")
                    self.position.close()
            return

        # Long entry: Price touches lower BB, Stoch oversold, then bullish crossover
        price_at_lower_bb = self.data.Close[-1] <= self.lower_bb[-1]
        stoch_oversold = self.stoch_k[-1] < 20
        stoch_bullish_cross = crossover(self.stoch_k, self.stoch_d)

        if price_at_lower_bb and stoch_oversold and stoch_bullish_cross:
            print("🌙 Moon Dev bullish BandStoch fusion! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.lower_bb[-1] - 0.5 * self.atr[-1]
            tp = self.upper_bb[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short entry: Price touches upper BB, Stoch overbought, then bearish crossover
        price_at_upper_bb = self.data.Close[-1] >= self.upper_bb[-1]
        stoch_overbought = self.stoch_k[-1] > 80
        stoch_bearish_cross = crossover(self.stoch_d, self.stoch_k)

        if price_at_upper_bb and stoch_overbought and stoch_bearish_cross:
            print("🌙 Moon Dev bearish BandStoch fusion! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = self.upper_bb[-1] + 0.5 * self.atr[-1]
            tp = self.lower_bb[-1]
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

bt = Backtest(data, BandStochFusionStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
