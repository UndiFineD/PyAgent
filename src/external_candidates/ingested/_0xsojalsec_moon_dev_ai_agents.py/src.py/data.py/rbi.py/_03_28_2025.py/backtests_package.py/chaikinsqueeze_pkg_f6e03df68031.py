# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests_package\ChaikinSqueeze_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ChaikinSqueeze(Strategy):
    risk_pct = 0.01  # 1% of equity per trade

    def init(self):
        # 🌙 Calculate Chaikin Money Flow (21-period) using pure TA-Lib
        self.cmf = self.I(
            talib.ADOSC,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            fastperiod=3,
            slowperiod=10,
        )  # Using ADOSC as CMF alternative

        # 🌀 Calculate Bollinger Bands (20-period, 2 StdDev) with direct TA-Lib
        self.upper_band, self.middle_band, self.lower_band = self.I(
            lambda c: talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0),
            self.data.Close,
        )

        # 📏 Calculate Bollinger Bandwidth and SMA filter with array operations
        self.bandwidth = self.I(
            lambda u, l, m: (np.array(u) - np.array(l)) / np.array(m),
            self.upper_band,
            self.lower_band,
            self.middle_band,
        )
        self.sma_bandwidth = self.I(talib.SMA, self.bandwidth, timeperiod=10)

        print(
            "🌕✨ Moon Dev Indicators Activated with Pure TA-Lib Power! Ready for launch... 🚀"
        )

    def next(self):
        # Wait for sufficient data 🌙
        if len(self.data) < 30:
            return

        # Entry Logic 🌙✨ (using array indexing for crossovers)
        if not self.position:
            # CMF crossover check (previous 2 periods)
            cmf_cross = self.cmf[-3] < 0 and self.cmf[-2] > 0

            # Squeeze check (previous period)
            squeeze_condition = self.bandwidth[-2] <= 0.5 * self.sma_bandwidth[-2]

            if cmf_cross and squeeze_condition:
                # 🚀 Calculate position size with moon math
                entry_price = self.data.Open[-1]
                position_size = int(round((self.risk_pct * self.equity) / entry_price))
                if position_size > 0:
                    self.buy(size=position_size)
                    print(
                        f"🌙✨ BUY SIGNAL! Size: {position_size} @ {entry_price} | Equity: {self.equity:,.2f} 🌌"
                    )

        # Exit Logic 🌘 (using direct array comparisons)
        if self.position:
            # Take profit at upper band 🎯
            if self.data.High[-1] >= self.upper_band[-1]:
                self.sell()
                print(
                    f"🎯 PROFIT TAKEN @ {self.upper_band[-1]:.2f} | PNL: {self.position.pl:.2f} 🌕"
                )

            # Stop loss on CMF cross below zero 🛑
            if self.cmf[-2] > 0 and self.cmf[-1] < 0:
                self.sell()
                print(
                    f"🛑 CMF STOP TRIGGERED! Exiting @ {self.data.Close[-1]:.2f} | PNL: {self.position.pl:.2f} 🌘"
                )


# Data preparation 🌙
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Format columns for backtesting.py requirements 🌙
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

# Launch backtest 🚀
bt = Backtest(data, ChaikinSqueeze, cash=1_000_000, commission=0.002)
stats = bt.run()
print("🌙✨ MOON DEV BACKTEST COMPLETE! ✨🌙")
print(stats)
print(stats._strategy)
