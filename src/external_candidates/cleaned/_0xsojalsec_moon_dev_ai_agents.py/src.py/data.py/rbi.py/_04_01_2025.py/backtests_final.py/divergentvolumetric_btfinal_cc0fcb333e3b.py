# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_01_2025\backtests_final\DivergentVolumetric_BTFinal.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class DivergentVolumetric(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    swing_period = 20  # Swing low lookback period

    def init(self):
        # Calculate indicators using TA-Lib
        self.macd, self.macd_signal, self.macd_hist = self.I(
            talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        self.obv = self.I(talib.OBV, self.data.Close, self.data.Volume)

        # Swing low calculations
        self.swing_low_price = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)
        self.swing_low_hist = self.I(talib.MIN, self.macd_hist, timeperiod=self.swing_period)

        # OBV trend calculation
        self.obv_slope = self.I(talib.LINEARREG_SLOPE, self.obv, timeperiod=20)

        print("🌙 Moon Dev Strategy Activated! Ready for cosmic gains ✨")
        print("✨ Indicators initialized with pure TA-Lib power!")

    def next(self):
        current_close = self.data.Close[-1]

        # Exit conditions
        if self.position:
            if len(self.macd_signal) >= 2:
                prev_signal = self.macd_signal[-2]
                curr_signal = self.macd_signal[-1]
                if prev_signal > 0 and curr_signal < 0:
                    print(f"🌙 Exit Signal! MACD Signal crossed below zero @{curr_signal:.2f}")
                    print("🌘 Closing position to protect lunar gains!")
                    self.position.close()

        # Entry conditions check
        else:
            if len(self.swing_low_price) >= 2 and len(self.swing_low_hist) >= 2:
                # Check bullish divergence
                price_divergence = (
                    self.swing_low_price[-2] > self.swing_low_price[-1]
                    and self.swing_low_hist[-2] < self.swing_low_hist[-1]
                )

                # Check OBV uptrend
                obv_uptrend = self.obv_slope[-1] > 0

                if price_divergence and obv_uptrend:
                    # Calculate position size
                    sl_price = self.swing_low_price[-1]
                    risk_per_share = current_close - sl_price

                    if risk_per_share <= 0:
                        print("⚠️ Cosmic Danger! Negative risk detected. Aborting entry.")
                        print("🌑 Black hole detected in risk calculation!")
                        return

                    position_size = (self.equity * self.risk_per_trade) / risk_per_share
                    position_size = int(round(position_size))  # Ensure whole number of shares

                    if position_size > 0:
                        print(f"🚀 Cosmic BUY Signal! Entry: {current_close:.2f}")
                        print(f"✨ Position Size: {position_size}, SL: {sl_price:.2f}")
                        print("🌕 Full moon energy detected - executing trade!")
                        self.buy(size=position_size, sl=sl_price)


# Data preparation
data = pd.read_csv("BTC-USD-15m.csv", parse_dates=["datetime"], index_col="datetime")

# Clean data columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data[["open", "high", "low", "close", "volume"]]
data.columns = ["Open", "High", "Low", "Close", "Volume"]

# Run backtest
bt = Backtest(data, DivergentVolumetric, cash=1_000_000)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("=== Moon Dev Backtest Results ===")
print("✨ Cosmic Performance Metrics:")
print(stats)
print("🌙 Strategy execution complete! May the moon guide your trades ✨")
