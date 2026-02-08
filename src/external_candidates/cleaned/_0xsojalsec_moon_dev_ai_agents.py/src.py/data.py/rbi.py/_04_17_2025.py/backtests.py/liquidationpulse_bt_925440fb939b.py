# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_17_2025\backtests\LiquidationPulse_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Map required columns
column_mapping = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
for orig, new in column_mapping.items():
    if orig in data.columns:
        data.rename(columns={orig: new}, inplace=True)


class LiquidationPulse(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    oi_lookback = 2  # Consecutive OI increases required
    cluster_period = 20  # Periods for cluster identification

    def init(self):
        # Precompute indicators using TA-Lib
        self.funding_rate = self.data.df["funding_rate"]
        self.open_interest = self.data.df["open_interest"]

        # Calculate OI changes using TSF as proxy for difference
        self.oi_diff = self.I(talib.TSF, self.open_interest, timeperiod=1)
        self.consecutive_oi_increases = self.I(
            talib.SUM,
            (self.oi_diff > self.oi_diff.shift(1)).astype(int),
            timeperiod=self.oi_lookback,
        )

        # Cluster identification
        self.low_cluster = self.I(talib.MIN, self.data.Low, timeperiod=self.cluster_period)
        self.high_cluster = self.I(talib.MAX, self.data.High, timeperiod=self.cluster_period)

        # Track initial risk for trailing stops
        self.initial_risk = None

    def next(self):
        price = self.data.Close[-1]

        if self.position:
            # Moon Dev Trailing Stop Logic 🌙
            if price >= self.position.entry_price + 1.5 * self.initial_risk:
                self.position.close()
                print(f"🌕 TRAILING STOP ACTIVATED: Reached 1.5R at {price}!")
                return

            # Check exit conditions
            if self.funding_rate[-1] >= 0:
                self.position.close()
                print(f"🌑 FUNDING RATE EXIT: Turned positive ({self.funding_rate[-1]:.6f})")
            elif self.oi_diff[-1] < self.oi_diff[-2]:
                self.position.close()
                print(f"🌒 OI DECLINE EXIT: Open interest decreased")
            elif price >= self.high_cluster[-1]:
                self.position.close()
                print(f"🌓 RESISTANCE EXIT: Reached high cluster {self.high_cluster[-1]:.2f}")
        else:
            # Entry conditions check
            entry_conditions = (
                self.funding_rate[-1] < 0,
                self.consecutive_oi_increases[-1] >= self.oi_lookback,
                price > self.low_cluster[-1],
            )

            if all(entry_conditions):
                # Moon Dev Risk Calculation 🌙
                sl_price = self.low_cluster[-1] * 0.995
                risk_per_share = price - sl_price
                risk_amount = self.equity * self.risk_pct
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    self.initial_risk = risk_per_share
                    print(
                        f"🚀🌙 LIQUIDATION PULSE TRIGGERED! "
                        f"Size: {position_size} @ {price:.2f} "
                        f"SL: {sl_price:.2f} "
                        f"Risk: {risk_per_share:.2f}"
                    )


# Initialize and run backtest
bt = Backtest(data, LiquidationPulse, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
