# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_11_2025\backtests\BandEngulfReversal_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class BandEngulfReversal(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators using TA-Lib with self.I()
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            name=["BB_upper", "BB_middle", "BB_lower"],
        )
        self.volume_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=20, name="Volume_SMA"
        )
        self.engulfing = self.I(
            talib.CDLENGULFING,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
            name="Engulfing",
        )

        # Swing low using TA-Lib MIN
        self.swing_low = self.I(
            talib.MIN, self.data.Low, timeperiod=20, name="Swing_Low"
        )

    def next(self):
        # Skip initial bars without indicator data
        if len(self.data) < 20:
            return

        # Entry Conditions 🌙
        if not self.position:
            # Check if price touched lower BB in previous candle
            prev_touched_bb = self.data.Low[-2] <= self.bb_lower[-2]

            # Check bullish engulfing pattern
            engulf_signal = self.engulfing[-1] == 100

            # Volume check
            volume_ok = self.data.Volume[-1] > self.volume_sma[-1]

            # Bollinger Band width check (avoid squeeze)
            bb_width = (self.bb_upper[-1] - self.bb_lower[-1]) / self.bb_middle[-1]
            volatility_ok = bb_width > 0.05

            if prev_touched_bb and engulf_signal and volume_ok and volatility_ok:
                # Calculate risk parameters 🚀
                entry_price = self.data.Open[-1]
                stop_loss = min(self.swing_low[-1], self.data.Low[-1])
                risk = entry_price - stop_loss

                if risk <= 0:
                    return

                # Position sizing calculation
                risk_amount = self.equity * self.risk_percent
                position_size = risk_amount / risk
                position_size = int(round(position_size))

                if position_size > 0:
                    # Execute trade with OCO orders ✨
                    take_profit1 = self.bb_upper[-1]
                    take_profit2 = entry_price + 2 * risk

                    self.buy(
                        size=position_size,
                        sl=stop_loss,
                        tp=max(take_profit1, take_profit2),
                        exectype=bt.Order.Market,  # Market order at next open
                    )

                    print(f"🌙✨ MOON DEV ALERT: LONG {position_size} units")
                    print(f"🎯 Entry: {entry_price:.2f} | SL: {stop_loss:.2f}")
                    print(f"🚀 TP1: {take_profit1:.2f} | TP2: {take_profit2:.2f}")

        # Exit logic - Let backtesting.py handle OCO exits via tp/sl


# DATA PREPARATION 🌍
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data[["open", "high", "low", "close", "volume"]]
data.columns = ["Open", "High", "Low", "Close", "Volume"]

# Run backtest 💻
bt = Backtest(data, BandEngulfReversal, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
