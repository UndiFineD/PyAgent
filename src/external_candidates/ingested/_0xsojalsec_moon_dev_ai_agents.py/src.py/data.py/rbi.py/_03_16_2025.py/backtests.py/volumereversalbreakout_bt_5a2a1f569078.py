# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests\VolumeReversalBreakout_BT.py
# 🌙 Moon Dev Backtest Implementation for VolumeReversalBreakout Strategy

import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# ========== DATA PREPARATION ==========
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns 🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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


# ========== STRATEGY IMPLEMENTATION ==========
class VolumeReversalBreakout(Strategy):
    risk_pct = 0.01  # 🌑 1% risk per trade

    def init(self):
        # 🚀 Moon Dev Indicators 🌙
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.bullish_engulf = self.I(
            talib.CDLENGULFING,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.hammer = self.I(
            talib.CDLHAMMER,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=5)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=5)

    def next(self):
        # 🌙 Current market conditions
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        if not self.position:
            # 🚀 Reversal Pattern Detection
            reversal_condition = (
                (self.bullish_engulf[-1] == 100 or self.hammer[-1] == 100)
                and (current_volume >= 1.5 * self.volume_sma[-1])
                and not pd.isna(self.volume_sma[-1])
            )

            if reversal_condition:
                self.reversal_high = current_high
                self.reversal_low = current_low
                print(
                    f"🌙✨ MOON DEV ALERT: Bullish reversal at {self.data.index[-1]} | "
                    f"High: {self.reversal_high:.2f} | Volume: {current_volume:.2f} (1.5x SMA) 🚀"
                )

            # 🚀 Breakout Entry Logic
            if hasattr(self, "reversal_high"):
                if (
                    current_close > self.reversal_high
                    and current_volume > self.volume_sma[-1]
                ):

                    # 🌑 Risk Management Calculations
                    equity = self.equity
                    risk_amount = equity * self.risk_pct
                    risk_per_share = current_close - self.reversal_low

                    if risk_per_share > 0:
                        position_size = int(round(risk_amount / risk_per_share))
                        tp_price = current_close + 1.5 * risk_per_share

                        # 🚀 Execute Trade
                        self.buy(size=position_size, sl=self.reversal_low, tp=tp_price)
                        print(
                            f"🚀🌕 MOON DEV ENTRY: Long {position_size} shares at {current_close:.2f} | "
                            f"SL: {self.reversal_low:.2f} | TP: {tp_price:.2f} ✨"
                        )
                        del self.reversal_high  # Reset for next signal

        else:
            # 🌑 Exit Condition: Volume Drop
            if current_volume < 0.8 * self.volume_sma[-1]:
                self.position.close()
                print(
                    f"🌑📉 MOON DEV EXIT: Volume drop at {self.data.index[-1]} | "
                    f"Price: {current_close:.2f} ✨"
                )


# ========== BACKTEST EXECUTION ==========
bt = Backtest(data, VolumeReversalBreakout, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🌙 Print Full Statistics
print(stats)
print(stats._strategy)
