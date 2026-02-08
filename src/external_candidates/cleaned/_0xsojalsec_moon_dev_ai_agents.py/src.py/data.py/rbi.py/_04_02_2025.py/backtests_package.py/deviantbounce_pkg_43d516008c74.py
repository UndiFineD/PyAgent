# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests_package\DeviantBounce_PKG.py
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 MOON DEV DATA PREPARATION ✨
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Cleanse and prepare data with Moon Dev magic
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Cosmic column alignment 🌌
column_mapping = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data.rename(columns=column_mapping, inplace=True)

# Validate cosmic data integrity
required_columns = ["Open", "High", "Low", "Close", "Volume"]
assert all(col in data.columns for col in required_columns), "🚨 Missing celestial columns!"


class DeviantBounce(Strategy):
    def init(self):
        # 🌗 Moon Phase Indicators
        self.upper_bb, self.middle_bb, self.lower_bb = self.I(self._compute_bbands, self.data.Close)
        self.funding_avg, self.funding_std, self.funding_lower = self.I(
            self._compute_funding_bands, self.data["funding_rate"]
        )

        print("🌙✨ Lunar indicators initialized! Ready for cosmic alignment...")

    def _compute_bbands(self, close):
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        return upper, middle, lower

    def _compute_funding_bands(self, funding_rate):
        avg = talib.SMA(funding_rate, timeperiod=2880)  # 30 days in 15m intervals
        std = talib.STDDEV(funding_rate, timeperiod=2880)
        lower_band = avg - 2 * std
        return avg, std, lower_band

    def next(self):
        price = self.data.Close[-1]

        # 🌑 New Moon Entry Signals
        if not self.position:
            funding_condition = self.data["funding_rate"][-1] < self.funding_lower[-1]
            price_condition = price < self.lower_bb[-1]

            if funding_condition and price_condition:
                # 🌕 Full Moon Position Sizing
                risk_pct = 1  # 1% of cosmic capital
                risk_amount = self.equity * risk_pct / 100
                sl_price = price * 0.98  # 2% stop loss
                risk_per_share = price - sl_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    self.buy(size=position_size)
                    print(f"🌕🚀 MOONSHOT! Long {position_size} @ {price:.2f}")
                    print(f"   🌙 Funding Rate: {self.data['funding_rate'][-1]:.6f}")
                    print(f"   📉 Lower Band: {self.lower_bb[-1]:.2f}")

        # 🌕 Full Moon Exit Strategy
        else:
            entry_price = self.position.entry_price
            middle_bb = self.middle_bb[-1]
            take_profit = entry_price * 1.02

            # Check both exit conditions
            if self.data.High[-1] >= middle_bb or self.data.High[-1] >= take_profit:
                self.position.close()
                print(f"🌗🌠 Cosmic Exit @ {self.data.Close[-1]:.2f}")
                print(f"   🌕 Profit: {(self.data.Close[-1] / entry_price - 1) * 100:.2f}%")


# 🌟 Launch Lunar Backtest
bt = Backtest(data, DeviantBounce, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌙✨ Cosmic Performance Report
print("\n" + "=" * 50)
print("🌙✨ MOON DEV FINAL REPORT 🚀🌕")
print("=" * 50)
print(stats)
print(stats._strategy)
print("🌌 Cosmic journey complete! Until next moon phase...")
