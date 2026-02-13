# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\VolatilitySqueezeLiquidation_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder

# Clean and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean column names and handle data
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


class VolatilitySqueezeLiquidation(Strategy):
    bb_period = 20
    bb_dev = 2
    lookback_percentile = 100
    entry_percentile = 20
    exit_percentile = 50
    funding_threshold = 0.0001
    risk_pct = 0.01

    def init(self):
        # Calculate Bollinger Bands
        close = self.data.Close
        self.upper, self.middle, self.lower = talib.BBANDS(
            close, self.bb_period, self.bb_dev, self.bb_dev
        )

        # Add BB indicators
        self.I(lambda: self.upper, name="BB_upper")
        self.I(lambda: self.middle, name="BB_middle")
        self.I(lambda: self.lower, name="BB_lower")

        # Calculate BB Width and percentiles
        bb_width = (self.upper - self.lower) / self.middle
        self.entry_threshold = bb_width.rolling(self.lookback_percentile).apply(
            lambda x: np.percentile(x.dropna(), self.entry_percentile)
        )
        self.exit_threshold = bb_width.rolling(self.lookback_percentile).apply(
            lambda x: np.percentile(x.dropna(), self.exit_percentile)
        )

        # Add indicators
        self.I(lambda: bb_width, name="BB_width")
        self.I(lambda: self.entry_threshold, name="Entry_Threshold")
        self.I(lambda: self.exit_threshold, name="Exit_Threshold")

        # Funding rate series
        self.funding_rates = self.data["Funding_Rate"]

    def next(self):
        price = self.data.Close[-1]

        if self.position:
            # Moon Dev exit checks
            current_width = (self.upper[-1] - self.lower[-1]) / self.middle[-1]
            if current_width > self.exit_threshold[-1]:
                self.position.close()
                print(
                    f"🌙✨ Closing position! Volatility expanded to {current_width:.4f}"
                )

        else:
            # Calculate current conditions
            current_width = (self.upper[-1] - self.lower[-1]) / self.middle[-1]
            in_squeeze = current_width < self.entry_threshold[-1]
            high_funding = self.funding_rates[-1] > self.funding_threshold

            # Long entry logic
            if in_squeeze and high_funding and price > self.upper[-1]:
                sl = self.middle[-1]
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (price - sl)))
                self.buy(size=position_size, sl=sl, tp=price + 2 * (price - sl))
                print(f"🌕🚀 LONG! Size: {position_size} | Entry: {price:.2f}")

            # Short entry logic
            elif in_squeeze and high_funding and price < self.lower[-1]:
                sl = self.middle[-1]
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (sl - price)))
                self.sell(size=position_size, sl=sl, tp=price - 2 * (sl - price))
                print(f"🌑🚀 SHORT! Size: {position_size} | Entry: {price:.2f}")


# Run backtest with Moon Dev parameters
bt = Backtest(data, VolatilitySqueezeLiquidation, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
