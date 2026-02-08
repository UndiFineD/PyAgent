# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_16_2025\backtests_final\LiquidationFader_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class LiquidationFader(Strategy):
    atr_period = 14
    swing_window = 20
    atr_ma_period = 50
    risk_pct = 0.01

    def init(self):
        # Volatility indicators 🌊
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.atr_ma = self.I(talib.SMA, self.atr, self.atr_ma_period)

        # Liquidation levels ✨
        self.swing_high = self.I(talib.MAX, self.data.High, self.swing_window)
        self.swing_low = self.I(talib.MIN, self.data.Low, self.swing_window)

        # Trade tracking 🌙
        self.entry_bar = None
        self.trail_stop = None

    def next(self):
        if not self.position:
            # Wait for indicator maturity 🌱
            if len(self.data.Close) < max(self.atr_period, self.swing_window):
                return

            # Volatility filter check 🌪️
            if self.atr[-1] > self.atr_ma[-1]:
                entry_price = self.data.Close[-1]

                # Long setup 🌛
                if entry_price < (self.swing_low[-1] - 2 * self.atr[-1]):
                    risk_amount = self.equity * self.risk_pct
                    risk_per_unit = 1.5 * self.atr[-1]
                    size = int(round(risk_amount / risk_per_unit))
                    if size > 0:
                        self.buy(size=size)
                        print(f"🌙✨ MOON ALERT: LONG {size} units @ {entry_price:.2f} 🌛 ATR: {self.atr[-1]:.2f} 🚀")

                # Short setup 🌜
                elif entry_price > (self.swing_high[-1] + 2 * self.atr[-1]):
                    risk_amount = self.equity * self.risk_pct
                    risk_per_unit = 1.5 * self.atr[-1]
                    size = int(round(risk_amount / risk_per_unit))
                    if size > 0:
                        self.sell(size=size)
                        print(f"🌙✨ MOON ALERT: SHORT {size} units @ {entry_price:.2f} 🌛 ATR: {self.atr[-1]:.2f} 🚀")
        else:
            # Dynamic trailing stop management 🛑
            price = self.data.Close[-1]
            atr = self.atr[-1]

            if self.position.is_long:
                self.trail_stop = max(self.trail_stop or 0, price - 1.5 * atr)
                if self.data.Low[-1] <= self.trail_stop:
                    self.position.close()
                    print(f"🌙 STOPPED OUT LONG 💰 PNL: {self.position.pl:.2f} ✨")
            else:
                self.trail_stop = min(self.trail_stop or np.inf, price + 1.5 * atr)
                if self.data.High[-1] >= self.trail_stop:
                    self.position.close()
                    print(f"🌙 STOPPED OUT SHORT 💰 PNL: {self.position.pl:.2f} ✨")


# Launch backtest 🚀
bt = Backtest(data, LiquidationFader, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙✨ MOON DEV BACKTEST COMPLETE ✨🌙")
print("=" * 50)
print(stats)
print("\n🌙 STRATEGY DETAILS:")
print(stats._strategy)
