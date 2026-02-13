# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\ReversalRetracement_PKG.py
# 🌙 Moon Dev's ReversalRetracement Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data 🌙
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class ReversalRetracement(Strategy):
    rsi_period = 14
    swing_window = 20
    volume_sma_period = 20
    risk_pct = 0.01  # 1% risk per trade

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.swing_high = self.I(talib.MAX, self.data.High, self.swing_window)
        self.swing_low = self.I(talib.MIN, self.data.Low, self.swing_window)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, self.volume_sma_period)

        # Trade tracking variables 🚀
        self.entry_swing_high = None
        self.entry_swing_low = None
        self.initial_risk = None
        self.trailing_high = None

    def next(self):
        current_idx = len(self.data) - 1

        # Entry Logic 🌙✨
        if not self.position:
            # Check 3 consecutive RSI lower lows
            rsi_condition = (
                current_idx >= 3
                and self.rsi[current_idx]
                < self.rsi[current_idx - 1]
                < self.rsi[current_idx - 2]
            )

            # Check uptrend in price
            price_condition = (
                current_idx >= 1
                and self.swing_high[current_idx] > self.swing_high[current_idx - 1]
                and self.swing_low[current_idx] > self.swing_low[current_idx - 1]
            )

            # Volume confirmation
            volume_condition = (
                self.data.Volume[current_idx] > self.volume_sma[current_idx]
            )

            if rsi_condition and price_condition and volume_condition:
                swing_high_val = self.swing_high[current_idx]
                swing_low_val = self.swing_low[current_idx]
                price_diff = swing_high_val - swing_low_val

                if price_diff > 0:
                    entry_price = swing_high_val - price_diff * 0.38
                    stop_loss = swing_high_val - price_diff * 0.5

                    if (
                        self.data.Low[current_idx]
                        <= entry_price
                        <= self.data.High[current_idx]
                    ):
                        risk_amount = self.equity * self.risk_pct
                        risk_per_share = entry_price - stop_loss

                        if risk_per_share > 0:
                            size = int(round(risk_amount / risk_per_share))
                            if size > 0:
                                self.buy(
                                    size=size,
                                    limit=entry_price,
                                    sl=stop_loss,
                                    tag="MoonDevEntry",
                                )
                                print(
                                    f"🌙✨🚀 MOON DEV LONG SIGNAL | Entry: {entry_price:.2f} | Size: {size} | SL: {stop_loss:.2f}"
                                )

                                # Store trade parameters 🌙
                                self.entry_swing_high = swing_high_val
                                self.entry_swing_low = swing_low_val
                                self.initial_risk = risk_per_share
                                self.trailing_high = entry_price

        # Exit Logic 🌙🛑
        if self.position:
            # Calculate Fibonacci levels from entry swing points
            price_diff = self.entry_swing_high - self.entry_swing_low
            tp_price = self.entry_swing_high - price_diff * 0.26

            # Take profit condition
            if self.data.Low[current_idx] <= tp_price:
                self.position.close()
                print(f"🌙✨🎯 MOON DEV TP HIT | Price: {tp_price:.2f}")

            # RSI exit
            if self.rsi[current_idx] > 70:
                self.position.close()
                print(f"🌙✨📉 MOON DEV RSI EXIT")
