# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_06_2025\backtests\VolumetricSqueeze_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Data cleaning
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VolumetricSqueeze(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    bb_period = 20
    bb_dev = 2
    atr_period = 14

    def init(self):
        # Volume anomaly detection
        def vol_percentile(series, window=100, percentile=90):
            vals = np.full(len(series), np.nan)
            for i in range(window, len(series)):
                vals[i] = np.percentile(series[i - window : i], percentile)
            return vals

        self.vol_pct = self.I(vol_percentile, self.data.Volume, name="VOL_90PCT")

        # Bollinger Bands
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_dev,
            nbdevdn=self.bb_dev,
            matype=0,
        )

        # Volatility metrics
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
            name="ATR",
        )

        self.entry_price = None
        self.trail_stop = None

    def next(self):
        price = self.data.Close[-1]

        # Exit logic
        if self.position:
            # Update trailing stop
            self.trail_stop = max(self.trail_stop, price - 1.5 * self.atr[-1])

            # Check exits
            if price <= self.trail_stop:
                print(f"🌙✨ Moon Exit: Trailing Stop @ {self.trail_stop:.2f}")
                self.position.close()
            elif price <= (self.entry_price - 2.5 * self.atr[-1]):
                print(f"🚨🌙 Emergency Stop!")
                self.position.close()

        # Entry logic
        else:
            if len(self.data) < 100:  # Ensure enough history
                return

            # Volume spike condition
            vol_cond = self.data.Volume[-1] > self.vol_pct[-1]

            # Bollinger Bandwidth calculation
            if self.middle[-1] != 0:
                bb_width = (self.upper[-1] - self.lower[-1]) / self.middle[-1]
            else:
                bb_width = np.inf

            if vol_cond and bb_width < 0.005:
                # Calculate position size
                risk_per_share = 2.5 * self.atr[-1]
                risk_amount = self.risk_pct * self.equity
                size = int(round(risk_amount / risk_per_share))

                if size > 0:
                    print(f"🚀🌙 MOON DEAL: Entry @ {price:.2f} Size {size}")
                    self.buy(size=size)
                    self.entry_price = price
                    self.trail_stop = price - 1.5 * self.atr[-1]


# Run backtest
bt = Backtest(data, VolumetricSqueeze, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
