# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_final\FlowReversal_BTFinal.py
# 🌙 Moon Dev's FlowReversal Backtest Implementation
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class FlowReversal(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # 🌟 Calculate indicators using TA-Lib and pandas_ta
        # MACD components
        self.macd, self.macd_signal, self.macd_hist = self.I(
            talib.MACD,
            self.data.Close,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
            name=["MACD", "MACD_signal", "MACD_hist"],
        )

        # 🎯 Swing high/low detection
        self.swing_high = self.I(talib.MAX, self.data.High, 20, name="SwingHigh")
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="SwingLow")

        # 🌊 Cumulative Delta Volume using pandas_ta
        self.cum_delta = self.I(lambda: ta.cdv(self.data.Close, self.data.Volume), name="CumulativeDelta")

        # 🌪️ ATR for volatility measurement
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # 🚨 Ensure enough data points for calculations
        if len(self.data) < 2:
            return

        i = len(self.data) - 1  # Current bar index

        # 🌈 MACD crossover conditions
        current_macd = self.macd[i]
        previous_macd = self.macd[i - 1]
        macd_bullish = current_macd > 0 and previous_macd <= 0
        macd_bearish = current_macd < 0 and previous_macd >= 0

        # 🌊 Order flow confirmation
        current_delta = self.cum_delta[i]
        previous_delta = self.cum_delta[i - 1]
        delta_bullish = current_delta > previous_delta
        delta_bearish = current_delta < previous_delta

        # 💰 Risk management calculations
        equity = self.equity
        price = self.data.Close[i]

        if not self.position:
            # 🚀 Long entry logic
            if macd_bullish and delta_bullish:
                sl = self.swing_low[i]
                risk_per_share = price - sl
                if risk_per_share > 0:
                    size = int(round((equity * self.risk_percent) / risk_per_share))
                    tp = price + 2 * risk_per_share  # 2:1 reward:risk
                    self.buy(size=size, sl=sl, tp=tp)
                    print(f"🌙✨🚀 BULLISH REVERSAL! Long {size} @ {price:.2f} | SL: {sl:.2f} TP: {tp:.2f}")

            # 🧨 Short entry logic
            elif macd_bearish and delta_bearish:
                sl = self.swing_high[i]
                risk_per_share = sl - price
                if risk_per_share > 0:
                    size = int(round((equity * self.risk_percent) / risk_per_share))
                    tp = price - 2 * risk_per_share  # 2:1 reward:risk
                    self.sell(size=size, sl=sl, tp=tp)
                    print(f"🌙✨🚀 BEARISH REVERSAL! Short {size} @ {price:.2f} | SL: {sl:.2f} TP: {tp:.2f}")
        else:
            # 💸 Exit logic for open positions
            if self.position.is_long and macd_bearish:
                self.position.close()
                print(f"🌙 MACD Bearish Cross! Closing long @ {price:.2f}")
            elif self.position.is_short and macd_bullish:
                self.position.close()
                print(f"🌙 MACD Bullish Cross! Closing short @ {price:.2f}")


# 🛠️ Data Preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
