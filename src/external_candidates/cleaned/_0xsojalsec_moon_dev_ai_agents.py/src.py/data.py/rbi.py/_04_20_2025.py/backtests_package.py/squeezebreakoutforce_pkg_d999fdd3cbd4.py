# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\SqueezeBreakoutForce_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class SqueezeBreakoutForce(Strategy):
    def init(self):
        # Bollinger Bands
        self.bb_upper = self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close)
        self.bb_lower = self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close)

        # Keltner Channel
        typical_price = self.I(
            lambda h, l, c: (h + l + c) / 3,
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.kc_mid = self.I(talib.EMA, typical_price, 20)
        kc_atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.kc_upper = self.I(lambda mid, atr: mid + 1.5 * atr, self.kc_mid, kc_atr)
        self.kc_lower = self.I(lambda mid, atr: mid - 1.5 * atr, self.kc_mid, kc_atr)

        # Elder Force Index
        def calc_force_index(close, vol):
            fi = np.zeros_like(close)
            fi[1:] = (close[1:] - close[:-1]) * vol[1:]
            return fi

        force_index = self.I(calc_force_index, self.data.Close, self.data.Volume)
        self.efi_13 = self.I(talib.EMA, force_index, 13)
        self.efi_50 = self.I(talib.EMA, force_index, 50)

        # ATR for trailing stop
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]

        if not self.position:
            # Entry conditions
            squeeze = (self.bb_upper[-1] < self.kc_upper[-1]) and (self.bb_lower[-1] > self.kc_lower[-1])
            efi_cross = (self.efi_13[-2] < self.efi_50[-2]) and (self.efi_13[-1] > self.efi_50[-1])
            breakout = price > self.bb_upper[-1]

            if squeeze and efi_cross and breakout:
                # Risk management
                risk = 0.01 * self.equity
                stop = price - atr_val
                size = int(round(risk / (price - stop)))

                if size > 0:
                    print(f"🌙✨ MOON DEATH STAR ACTIVATED! Buying {size} units at {price:.2f} 🚀")
                    self.buy(size=size, sl=stop)
                    self.entry_bar = len(self.data)
                    self.trail_high = self.data.High[-1]
        else:
            # Update trailing high
            self.trail_high = max(self.trail_high, self.data.High[-1])
            trail_stop = self.trail_high - 2 * atr_val

            # Exit conditions
            if self.data.Close[-1] < trail_stop:
                print(f"🌙🚨 COSMIC STOP TRIGGERED! Selling at {self.data.Close[-1]:.2f} ✨")
                self.position.close()
            elif len(self.data) >= self.entry_bar + 5:
                print(f"⏳ QUANTUM TIMEWARP EXIT! Holding period expired 🌌")
                self.position.close()


bt = Backtest(data, SqueezeBreakoutForce, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
