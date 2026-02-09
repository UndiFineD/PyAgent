# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_package\RangeBoundPutter_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Resample to daily timeframe
daily_data = (
    data.resample("D")
    .agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )
    .dropna()
)
daily_data.columns = ["Open", "High", "Low", "Close", "Volume"]


class RangeBoundPutter(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    sl_pct = 0.02  # 2% stop loss
    tp_pct = 0.02  # 2% take profit

    def init(self):
        # Calculate daily range percentage using self.I()
        def range_pct(high, low, close):
            return (high - low) / close * 100

        self.range_indicator = self.I(
            range_pct, self.data.High, self.data.Low, self.data.Close, name="RangePct"
        )

        # Add moon-themed indicators
        self.moon_signal = self.I(
            lambda close: np.full_like(close, 10),
            self.data.Close,
            name="MoonThreshold🌙",
        )

    def next(self):
        current_range = self.range_indicator[-1]

        if not self.position and current_range < 10:
            # Calculate position size with proper risk management
            entry_price = self.data.Close[-1]
            sl_price = entry_price * (1 - self.sl_pct)
            tp_price = entry_price * (1 + self.tp_pct)

            risk_amount = self.equity * self.risk_percent
            risk_per_share = entry_price - sl_price
            position_size = risk_amount / risk_per_share

            # Enforce integer position size
            position_size = int(round(position_size))

            if position_size > 0:
                self.buy(
                    size=position_size,
                    sl=sl_price,
                    tp=tp_price,
                    tag=f"🌕 Moon Entry: ${entry_price:.2f}",
                )

                print(
                    f"\n🚀🌙✨ MOON DEV ALERT ✨🌙🚀"
                    f"\nEntry Price: {entry_price:.2f}"
                    f"\nPosition Size: {position_size}"
                    f"\nRisk: {self.risk_percent*100}% of ${self.equity:,.2f}"
                    f"\nMoon Trail: SL {sl_price:.2f} | TP {tp_price:.2f}"
                )


# Run backtest with lunar precision 🌕
bt = Backtest(daily_data, RangeBoundPutter, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full moon stats 🌕📊
print("\n🌙🌙🌙 FULL MOON STATS 🌙🌙🌙")
print(stats)
print(stats._strategy)
