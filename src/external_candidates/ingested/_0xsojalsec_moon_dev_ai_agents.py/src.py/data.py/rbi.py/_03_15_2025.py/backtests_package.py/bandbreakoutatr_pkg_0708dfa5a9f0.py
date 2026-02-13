# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\BandBreakoutATR_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandBreakoutATR(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Clean data and calculate indicators with TA-Lib
        close = self.data.Close
        high, low = self.data.High, self.data.Low

        # Calculate Bollinger Bands using TA-Lib
        upper, middle, lower = talib.BBANDS(
            close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

        # Add indicators with Moon Dev flavor ✨
        self.I(lambda: upper, name="BB_UPPER")
        self.I(lambda: middle, name="BB_MIDDLE")
        self.I(lambda: lower, name="BB_LOWER")
        self.I(talib.ATR, high, low, close, timeperiod=14, name="MOON_ATR")

    def next(self):
        # Moon Dev's trading logic core 🚀
        price = self.data.Close[-1]

        if not self.position:
            # Long entry on Upper Band crossover
            if (
                self.data.BB_UPPER[-2] < self.data.BB_MIDDLE[-2]
                and self.data.BB_UPPER[-1] > self.data.BB_MIDDLE[-1]
            ):

                atr = self.data.MOON_ATR[-1]
                sl_price = price - 0.1 * atr
                risk_per_share = price - sl_price

                if risk_per_share > 0:
                    equity_risk = self.equity * self.risk_percent
                    moon_size = int(round(equity_risk / risk_per_share))

                    if moon_size > 0:
                        self.buy(size=moon_size, sl=sl_price)
                        print(
                            f"🌕🚀 MOON DEV BLASTOFF! LONG {moon_size} @ {price:.2f} | ATR Shield: {sl_price:.2f}"
                        )
        else:
            # Exit on Lower Band crossunder
            if (
                self.data.BB_MIDDLE[-2] > self.data.BB_LOWER[-2]
                and self.data.BB_MIDDLE[-1] < self.data.BB_LOWER[-1]
            ):

                self.position.close()
                print(f"🌘✨ MOON PHASE SHIFT! Exiting @ {price:.2f}")


# Moon Dev's data preparation ritual 🌙
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Cleanse the data columns 🔥
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Align with celestial coordinates 🌌
data.rename(
    columns={
        "datetime": "DateTime",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

data["DateTime"] = pd.to_datetime(data["DateTime"])
data.set_index("DateTime", inplace=True)

# Launch the Moon Dev backtest protocol 🚀
bt = Backtest(data, BandBreakoutATR, cash=1_000_000, commission=0.002)
stats = bt.run()

# Reveal the cosmic truth ✨
print("\n🌙🌙🌙 MOON DEV BACKTEST RESULTS 🌙🌙🌙")
print(stats)
print("\n⚡ STRATEGY METRICS ⚡")
print(stats._strategy)
