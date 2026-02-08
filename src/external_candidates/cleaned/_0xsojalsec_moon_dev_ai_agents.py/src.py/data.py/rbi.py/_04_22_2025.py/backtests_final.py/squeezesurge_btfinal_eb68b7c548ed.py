# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\SqueezeSurge_BTFinal.py
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class SqueezeSurge(Strategy):
    def init(self):
        # Bollinger Bands (20-day, 2σ)
        self.upper_band, self.mid_band, self.lower_band = self.I(
            lambda x: (
                pd.Series(x).rolling(20).mean() + 2 * pd.Series(x).rolling(20).std(),
                pd.Series(x).rolling(20).mean(),
                pd.Series(x).rolling(20).mean() - 2 * pd.Series(x).rolling(20).std(),
            ),
            self.data.Close,
        )

        # Volume 30-day average
        self.vol_avg = self.I(lambda x: pd.Series(x).rolling(30).mean(), self.data.Volume)

        # VWAP
        typical_price = (self.data.High + self.data.Low + self.data.Close) / 3
        vwap = (typical_price * self.data.Volume).cumsum() / self.data.Volume.cumsum()
        self.vwap = self.I(lambda x: x, vwap)

        # Stochastic RSI (14,3,3)
        rsi = pd.Series(self.data.Close).ewm(span=14).mean()
        stoch_rsi = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min()) * 100
        self.stoch_k = self.I(lambda x: stoch_rsi.rolling(3).mean(), self.data.Close)
        self.stoch_d = self.I(lambda x: self.stoch_k.rolling(3).mean(), self.data.Close)

    def next(self):
        # Position sizing (1% risk per trade)
        size = 0.01 * self.equity / self.data.Close[-1]
        size = round(size)  # Round to whole units

        # Long entry conditions
        long_entry = (
            (self.data.Close[-1] > self.upper_band[-1])
            and (self.data.Volume[-1] > 2 * self.vol_avg[-1])
            and (crossover(self.data.Close, self.vwap))
        )

        if long_entry and not self.position:
            self.buy(size=size)
            print(f"🌙 MOON DEV LONG ENTRY | Price: {self.data.Close[-1]} | Size: {size} units")
            # Set stop at mid band
            self.position.sl = self.mid_band[-1]

        # Short entry conditions
        short_entry = (
            (self.data.Close[-1] < self.lower_band[-1])
            and (self.data.Volume[-1] > 2 * self.vol_avg[-1])
            and (crossover(self.vwap, self.data.Close))
        )

        if short_entry and not self.position:
            self.sell(size=size)
            print(f"🌙 MOON DEV SHORT ENTRY | Price: {self.data.Close[-1]} | Size: {size} units")
            # Set stop at mid band
            self.position.sl = self.mid_band[-1]

        # Exit conditions
        if self.position.is_long:
            # Long exit conditions
            exit_cond = (self.stoch_k[-1] < 80 and self.stoch_k[-2] >= 80) or (
                self.data.Close[-1] < self.upper_band[-1]
            )
            if exit_cond:
                self.position.close()
                print(f"✅ MOON DEV LONG EXIT | Price: {self.data.Close[-1]} | StochRSI: {self.stoch_k[-1]}")

        elif self.position.is_short:
            # Short exit conditions
            exit_cond = (self.stoch_k[-1] > 20 and self.stoch_k[-2] <= 20) or (
                self.data.Close[-1] > self.lower_band[-1]
            )
            if exit_cond:
                self.position.close()
                print(f"✅ MOON DEV SHORT EXIT | Price: {self.data.Close[-1]} | StochRSI: {self.stoch_k[-1]}")


# Backtest setup
bt = Backtest(data, SqueezeSurge, commission=0.002, exclusive_orders=True)

# Run backtest
stats = bt.run()
print("🌙✨ MOON DEV BACKTEST COMPLETE ✨🌙")
print(stats)

# Plot results
bt.plot(filename="moon_dev_squeeze_surge")
