# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests_final\VolatilitySqueeze_BTFinal.py
# 🌙 Moon Dev's Volatility Squeeze Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Clean data and prepare for backtesting
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Data cleansing rituals ✨
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


class VolatilitySqueeze(Strategy):
    min_history = 8640  # 3 months of 15m data 🌗
    risk_percent = 0.01  # 1% risk per trade 💰

    def init(self):
        # Celestial indicator calculations 🌌
        self.bb_upper = self.I(
            lambda c: talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[0],
            self.data.Close,
            name="BB Upper",
        )
        self.bb_lower = self.I(
            lambda c: talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[2],
            self.data.Close,
            name="BB Lower",
        )
        self.bb_width = self.I(lambda u, l: (u - l).round(2), self.bb_upper, self.bb_lower, name="BB Width")
        self.bb_width_sma = self.I(talib.SMA, self.bb_width, timeperiod=20, name="BB Width SMA 20")
        self.bb_width_history = []

    def next(self):
        # Update cosmic records 🌠
        if len(self.data) < 20:  # Wait for BBANDS calculation
            return

        current_width = self.bb_width[-1]
        self.bb_width_history.append(current_width)

        if len(self.bb_width_history) < self.min_history:
            return  # Wait for sufficient history 🌗

        # Calculate lunar percentile phase 🌓
        historical_percentile = (
            sum(1 for x in self.bb_width_history if x <= current_width) / len(self.bb_width_history)
        ) * 100

        # Moon Dev Entry Protocol 🌙🚀
        if not self.position and historical_percentile <= 10:
            entry_price = self.data.Close[-1]
            stop_price = self.bb_lower[-1]
            risk_per_unit = entry_price - stop_price

            if risk_per_unit > 0:
                equity = self.equity
                risk_amount = equity * self.risk_percent
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_price)
                    print(
                        f"🌙✨ MOON DEV ALERT: Squeeze Detected! "
                        f"Size: {position_size:,} @ {entry_price:.2f} | "
                        f"Stop: {stop_price:.2f} 🚀"
                    )

        # Stellar Exit Protocol 💫🌌
        if self.position:
            width_sma = self.bb_width_sma[-1]
            if current_width > width_sma:
                self.position.close()
                print(
                    f"🌙💥 COSMIC EXIT: Width {current_width:.2f} > SMA {width_sma:.2f} | "
                    f"Profit: ${self.position.pl:.2f} 🌠"
                )


# Launch backtest rocket 🚀🌙
bt = Backtest(data, VolatilitySqueeze, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙=== MOON DEV BACKTEST RESULTS ===🌙")
print(stats)
print("\n🌌=== STRATEGY DETAILS ===🌌")
print(stats._strategy)
