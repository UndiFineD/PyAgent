# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_18_2025\backtests\DivergentRay_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


def calculate_bull_power(close, period):
    close_array = np.asarray(close)
    ema = talib.EMA(close_array, timeperiod=period)
    return close_array - ema


class DivergentRay(Strategy):
    risk_percent = 0.01
    adx_period = 14
    swing_high_window = 20
    bull_power_ema = 13
    volume_lookback = 5
    bull_sma_period = 5

    def init(self):
        self.bull_power = self.I(calculate_bull_power, self.data.Close, self.bull_power_ema)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, self.adx_period)
        self.price_highs = self.I(talib.MAX, self.data.High, self.swing_high_window)
        self.bull_highs = self.I(talib.MAX, self.bull_power, self.swing_high_window)
        self.bull_sma = self.I(talib.SMA, self.bull_power, self.bull_sma_period)

        print("🌙✨ Moon Dev Strategy Activated! Ready to hunt bearish divergences 🚀")

    def next(self):
        if len(self.data) < max(self.swing_high_window, self.volume_lookback) + 1:
            return

        current_idx = len(self.data) - 1
        prev_idx = current_idx - self.volume_lookback

        price_divergence = (self.price_highs[current_idx] > self.price_highs[prev_idx]) and (
            self.bull_highs[current_idx] < self.bull_highs[prev_idx]
        )
        volume_declining = self.data.Volume[current_idx] < self.data.Volume[prev_idx]
        strong_trend = self.adx[current_idx] > 25

        if not self.position and price_divergence and volume_declining and strong_trend:
            stop_loss = self.price_highs[current_idx]
            risk_distance = stop_loss - self.data.Close[-1]

            if risk_distance <= 0:
                print("🌙⚠️ Invalid risk distance, trade skipped")
                return

            position_size = int(round((self.equity * self.risk_percent) / risk_distance))
            if position_size > 0:
                self.sell(size=position_size, sl=stop_loss)
                print(f"🌙🚀 BEARISH DIVERGENCE DETECTED! Short {position_size} units at {self.data.Close[-1]:.2f} 🌌")
                print(f"   SL: {stop_loss:.2f} | ADX: {self.adx[-1]:.2f} 📉")

        elif self.position:
            bull_cross = crossover(self.bull_power[-2:], self.bull_sma[-2:])
            trend_weak = self.adx[-1] < 25

            if bull_cross or trend_weak:
                self.position.close()
                reason = "Bull Power breakout 🌤️" if bull_cross else "Trend weakening 📉"
                print(f"🌙✨ Closing position: {reason} at {self.data.Close[-1]:.2f} 🏁")


# Data preprocessing
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# Run backtest
bt = Backtest(data, DivergentRay, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙📊 FINAL STRATEGY STATS 🌙")
print(stats)
print(stats._strategy)
