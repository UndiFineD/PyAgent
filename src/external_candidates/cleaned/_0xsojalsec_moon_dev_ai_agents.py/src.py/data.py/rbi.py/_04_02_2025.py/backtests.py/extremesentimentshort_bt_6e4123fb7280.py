# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests\ExtremeSentimentShort_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and prepare columns 🌙
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

assert "funding_rate" in data.columns, "🌙 CRITICAL: Missing funding_rate column!"
assert "long_short_ratio" in data.columns, "🌙 CRITICAL: Missing long_short_ratio column!"


class ExtremeSentimentShort(Strategy):
    risk_pct = 0.01  # 1% per trade 🚀
    fr_period = 2880  # 30 days in 15m intervals (30*24*4)
    ls_percentile = 90
    bb_length = 20
    bb_dev = 2
    max_bars = 96  # 24 hours in 15m

    def init(self):
        # Funding Rate Indicators 🌙
        self.fr_ma = self.I(talib.SMA, self.data.funding_rate, self.fr_period)
        self.fr_std = self.I(talib.STDDEV, self.data.funding_rate, self.fr_period)
        self.fr_threshold = self.I(lambda ma, std: ma + 2 * std, self.fr_ma, self.fr_std)

        # Long/Short Ratio Analysis ✨
        self.ls_pct = self.I(
            ta.percentile,
            self.data.long_short_ratio,
            self.fr_period,
            self.ls_percentile,
        )

        # Bollinger Bands Setup 🎯
        self.lower_bb = self.I(talib.BBANDS, self.data.Close, self.bb_length, self.bb_dev, self.bb_dev)[2]

        self.entry_bar = 0  # Track position duration

    def next(self):
        # Wait for indicators to warm up 🌙
        if len(self.data) < self.fr_period:
            return

        # Get current values ✨
        current_fr = self.data.funding_rate[-1]
        fr_threshold = self.fr_threshold[-1]
        current_ls = self.data.long_short_ratio[-1]
        ls_pct = self.ls_pct[-1]

        # Moon Dev Debug Console 🖥️
        print(f"🌙 Funding Rate: {current_fr:.6f} | Threshold: {fr_threshold:.6f}")
        print(f"✨ L/S Ratio: {current_ls:.2f} | 90th%: {ls_pct:.2f}")

        # Entry Logic 🚀
        if not self.position:
            if current_fr > fr_threshold and current_ls >= ls_pct:
                print(f"🚀🚀🚀 MOON DEV SHORT ACTIVATED! Selling at {self.data.Close[-1]:.2f} 🚀🚀🚀")
                self.sell(size=self.risk_pct)
                self.entry_bar = len(self.data)

        # Exit Logic 💰
        if self.position:
            # Bollinger Band Exit 🎯
            if self.data.Low[-1] <= self.lower_bb[-1]:
                print(f"🌙✨ PROFIT TAKEN! Closing at {self.data.Close[-1]:.2f}")
                self.position.close()

            # Time-based Exit ⏳
            elif len(self.data) - self.entry_bar >= self.max_bars:
                print(f"🌙⏰ 24H AUTO-CLOSE! Exiting at {self.data.Close[-1]:.2f}")
                self.position.close()


# Run backtest with 1M capital 🌙
bt = Backtest(data, ExtremeSentimentShort, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
