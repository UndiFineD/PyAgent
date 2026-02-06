# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_final\InverseMomentum_BTFinal_WORKING_-0.845397pct.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
raw_data = pd.read_csv(data_path)

# Clean column names
raw_data.columns = raw_data.columns.str.strip().str.lower()

# Drop unnamed columns
raw_data = raw_data.drop(
    columns=[col for col in raw_data.columns if "unnamed" in col.lower()]
)

# Rename columns properly (keep datetime lowercase for set_index)
raw_data = raw_data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Convert to datetime and set index
raw_data["datetime"] = pd.to_datetime(raw_data["datetime"])
raw_data = raw_data.set_index(raw_data["datetime"]).drop("datetime", axis=1)

# Resample to daily OHLCV
daily_data = (
    raw_data.resample("1D")
    .agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    .dropna()
)


class InverseMomentum(Strategy):
    fast_period = 3
    slow_period = 5
    vol_period = 10
    trend_period = 20
    risk_pct = 0.02
    stop_pct = 0.05

    def init(self):
        close = self.data.Close
        volume = self.data.Volume

        self.fast_sma = self.I(talib.SMA, close, timeperiod=self.fast_period)
        self.slow_sma = self.I(talib.SMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast SMA {self.fast_sma[-1]:.2f}, Slow SMA {self.slow_sma[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f}, "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} 🚀"
            )

        # Position sizing for risk management: fraction = risk_pct / stop_pct
        size = self.risk_pct / self.stop_pct

        if self.position:
            # Exit on bearish crossover
            if (
                self.slow_sma[-2] < self.fast_sma[-2]
                and self.slow_sma[-1] > self.fast_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev Exit: Bearish crossover detected! Closing position at {self.data.Close[-1]:.2f} ✨"
                )
        else:
            # Entry conditions: bullish crossover + volume + trend filter
            if (
                (
                    self.fast_sma[-2] < self.slow_sma[-2]
                    and self.fast_sma[-1] > self.slow_sma[-1]
                )
                and self.data.Volume[-1] > self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
            ):

                sl_price = self.data.Close[-1] * (1 - self.stop_pct)
                self.buy(size=size, sl=sl_price)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! Crossover confirmed with volume & trend. "
                    f"Entry: {self.data.Close[-1]:.2f}, Size: {size}, SL: {sl_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(
    daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True
)

stats = bt.run()
print(stats)
print(stats._strategy)
