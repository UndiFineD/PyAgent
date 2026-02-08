# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\10_20_2025\backtests_final\FractalRangeBreakout_BTFinal_WORKING.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=True, index_col=0)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
col_map = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data = data.rename(columns=col_map)


class FractalRangeBreakout(Strategy):
    def init(self):
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.ema = self.I(talib.EMA, self.data.Close, timeperiod=200)
        self.vol_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.last_upper = None
        self.last_lower = None
        self.last_upper_bar = -999
        self.last_lower_bar = -999
        self.entry_bar = None

    def next(self):
        if len(self.data) < 205:
            return
        if pd.isna(self.ema[-1]) or pd.isna(self.atr[-1]) or pd.isna(self.rsi[-1]):
            return

        current_close = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_vol = self.data.Volume[-1]

        # Update fractals (confirmed 2 bars ago)
        if len(self.data) >= 5:
            middle_idx = -3
            # Upper fractal check
            if middle_idx - 2 >= -len(self.data):
                h_middle = self.data.High[middle_idx]
                h_left1 = self.data.High[middle_idx - 1]
                h_left2 = self.data.High[middle_idx - 2]
                h_right1 = self.data.High[middle_idx + 1]
                h_right2 = self.data.High[middle_idx + 2]
                if h_middle > h_left1 and h_middle > h_left2 and h_middle > h_right1 and h_middle > h_right2:
                    self.last_upper = h_middle
                    self.last_upper_bar = len(self.data) - 3
                    print(f"🌙 New Upper Fractal: {h_middle} at bar {self.last_upper_bar} ✨")
            # Lower fractal check
            if middle_idx - 2 >= -len(self.data):
                l_middle = self.data.Low[middle_idx]
                l_left1 = self.data.Low[middle_idx - 1]
                l_left2 = self.data.Low[middle_idx - 2]
                l_right1 = self.data.Low[middle_idx + 1]
                l_right2 = self.data.Low[middle_idx + 2]
                if l_middle < l_left1 and l_middle < l_left2 and l_middle < l_right1 and l_middle < l_right2:
                    self.last_lower = l_middle
                    self.last_lower_bar = len(self.data) - 3
                    print(f"🌙 New Lower Fractal: {l_middle} at bar {self.last_lower_bar} ✨")

        if self.last_upper is None or self.last_lower is None:
            return

        current_bar = len(self.data) - 1
        range_age = current_bar - max(self.last_upper_bar, self.last_lower_bar)
        if range_age < 10:
            return

        range_width = self.last_upper - self.last_lower
        if range_width < self.atr[-1]:
            return

        # Position management
        if self.position:
            bars_in_trade = current_bar - self.entry_bar if self.entry_bar is not None else 0
            if bars_in_trade > 20:
                self.position.close()
                print("🌙 Time-based exit 🚀")
                return
            if self.position.is_long:
                if current_close < self.last_lower:
                    self.position.close()
                    print("🌙 Long exit: hit lower fractal 🚀")
                    return
                if self.rsi[-1] > 70:
                    self.position.close()
                    print("🌙 Long exit: RSI overbought 🚀")
                    return
            elif self.position.is_short:
                if current_close > self.last_upper:
                    self.position.close()
                    print("🌙 Short exit: hit upper fractal 🚀")
                    return
                if self.rsi[-1] < 30:
                    self.position.close()
                    print("🌙 Short exit: RSI oversold 🚀")
                    return
            return

        # Long entry
        breakout_long_threshold = self.last_upper + 0.5 * self.atr[-1]
        if (
            current_close > self.last_upper
            and current_close >= breakout_long_threshold
            and self.rsi[-1] > 50
            and self.rsi[-1] > self.rsi[-2]
            and current_close > self.ema[-1]
            and current_vol > self.vol_ma[-1]
        ):
            sl_price = min(self.last_lower, current_close - self.atr[-1])
            sl_distance = current_close - sl_price
            risk_amount = 0.01 * 1000000
            if sl_distance > 0:
                size = risk_amount / sl_distance
                size = int(round(size))
                if size > 0:
                    tp_price = current_close + sl_distance
                    self.buy(size=size, sl=sl_price, tp=tp_price)
                    self.entry_bar = current_bar
                    print(f"🌙🚀 LONG Entry: {current_close}, Size: {size}, SL: {sl_price}, TP: {tp_price} ✨")

        # Short entry
        breakout_short_threshold = self.last_lower - 0.5 * self.atr[-1]
        if (
            current_close < self.last_lower
            and current_close <= breakout_short_threshold
            and self.rsi[-1] < 50
            and self.rsi[-1] < self.rsi[-2]
            and current_close < self.ema[-1]
            and current_vol > self.vol_ma[-1]
        ):
            sl_price = max(self.last_upper, current_close + self.atr[-1])
            sl_distance = sl_price - current_close
            risk_amount = 0.01 * 1000000
            if sl_distance > 0:
                size = risk_amount / sl_distance
                size = int(round(size))
                if size > 0:
                    tp_price = current_close - sl_distance
                    self.sell(size=size, sl=sl_price, tp=tp_price)
                    self.entry_bar = current_bar
                    print(f"🌙🚀 SHORT Entry: {current_close}, Size: {size}, SL: {sl_price}, TP: {tp_price} ✨")


bt = Backtest(data, FractalRangeBreakout, cash=1000000, commission=0.001)
stats = bt.run()
print(stats)
