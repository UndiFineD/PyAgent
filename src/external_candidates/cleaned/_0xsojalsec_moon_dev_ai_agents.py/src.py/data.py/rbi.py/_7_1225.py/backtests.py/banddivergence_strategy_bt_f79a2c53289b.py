# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_1225\backtests\BandDivergence_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandDivergenceStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating BandDivergence strategy! 🚀")
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.width = self.I(lambda u, l: u - l, self.upper, self.lower)
        self.macd, self.signal, self.hist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if self.position:
            if self.position.is_long:
                if (
                    (len(self.macd) >= 2 and self.macd[-1] < 0 and self.macd[-2] > 0)
                    or self.data.Close[-1] < self.swing_low[-1]
                    or (len(self.middle) >= 2 and self.middle[-1] <= self.middle[-2])
                ):
                    print("🌙 Moon Dev exit condition met for long! Closing position. ✨")
                    self.position.close()
            elif self.position.is_short:
                if (
                    (len(self.macd) >= 2 and self.macd[-1] > 0 and self.macd[-2] < 0)
                    or self.data.Close[-1] > self.swing_high[-1]
                    or (len(self.middle) >= 2 and self.middle[-1] >= self.middle[-2])
                ):
                    print("🌙 Moon Dev exit condition met for short! Closing position. ✨")
                    self.position.close()
            return

        # Long entry
        uptrend = (
            len(self.swing_high) >= 2
            and self.swing_high[-1] > self.swing_high[-2]
            and self.swing_low[-1] > self.swing_low[-2]
        )
        middle_higher = len(self.middle) >= 2 and self.middle[-1] > self.middle[-2]
        macd_above = self.macd[-1] > 0
        if uptrend and middle_higher and macd_above:
            print("🌙 Moon Dev long entry signal detected! 🚀")
            entry_price = self.data.Close[-1]
            sl = self.swing_low[-1] - 1.5 * self.atr[-1]
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                print("🌙 Moon Dev invalid risk for long, skipping. ⚠️")
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price + 2 * risk_per_unit  # 2:1 RR
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! SL: {sl}, TP: {tp} ✨")
            else:
                print("🌙 Moon Dev position size too small for long. ⚠️")

        # Short entry
        downtrend = (
            len(self.swing_high) >= 2
            and self.swing_high[-1] < self.swing_high[-2]
            and self.swing_low[-1] < self.swing_low[-2]
        )
        width_tight = len(self.width) >= 2 and self.width[-1] < self.width[-2]
        macd_below = self.macd[-1] < 0
        if downtrend and width_tight and macd_below:
            print("🌙 Moon Dev short entry signal detected! 🚀")
            entry_price = self.data.Close[-1]
            sl = self.swing_high[-1] + 1.5 * self.atr[-1]
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                print("🌙 Moon Dev invalid risk for short, skipping. ⚠️")
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            tp = entry_price - 2 * risk_per_unit
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! SL: {sl}, TP: {tp} ✨")
            else:
                print("🌙 Moon Dev position size too small for short. ⚠️")


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

bt = Backtest(data, BandDivergenceStrategy, cash=1000000, margin=1, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
