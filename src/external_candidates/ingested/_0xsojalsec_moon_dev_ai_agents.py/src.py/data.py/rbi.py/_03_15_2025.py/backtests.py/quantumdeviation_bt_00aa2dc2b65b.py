# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\QuantumDeviation_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class QuantumDeviation(Strategy):
    def init(self):
        # Calculate indicators using TA-Lib
        self.sma20 = self.I(talib.SMA, self.data.Close, 20)
        self.spread = self.I(talib.SUB, self.data.Close, self.sma20)
        self.mean_spread = self.I(talib.SMA, self.spread, 100)
        self.std_spread = self.I(talib.STDDEV, self.spread, 100, 1)

        # Track spread values for signal calculations
        self.spread_values = self.I(lambda: np.zeros_like(self.data.Close), plot=False)

    def next(self):
        if (
            len(self.spread) < 100
            or len(self.mean_spread) < 1
            or len(self.std_spread) < 1
        ):
            return

        current_spread = self.spread[-1]
        current_mean = self.mean_spread[-1]
        current_std = self.std_spread[-1]
        upper_band = current_mean + 2 * current_std
        lower_band = current_mean - 2 * current_std

        # Moon Dev themed risk management 🌙
        risk_pct = 0.01  # 1% risk per trade
        price_risk = 3 * current_std
        position_size = (
            int(round((self.equity * risk_pct) / price_risk)) if price_risk > 0 else 0
        )

        # Entry logic with cosmic signals 🌌
        if not self.position:
            if current_spread > upper_band and position_size > 0:
                self.sell(
                    size=position_size,
                    tag={"entry_spread": current_spread, "std_spread": current_std},
                )
                print(
                    f"🚀 MOON DEV SHORT: Price={self.data.Close[-1]:.2f} | Spread={current_spread:.2f}σ | Size={position_size}"
                )

            elif current_spread < lower_band and position_size > 0:
                self.buy(
                    size=position_size,
                    tag={"entry_spread": current_spread, "std_spread": current_std},
                )
                print(
                    f"🌙 MOON DEV LONG: Price={self.data.Close[-1]:.2f} | Spread={current_spread:.2f}σ | Size={position_size}"
                )

        # Exit logic with quantum precision ⚛️
        else:
            pos = self.position
            entry_spread = pos.tag["entry_spread"]
            entry_std = pos.tag["std_spread"]

            if pos.is_long:
                tp = entry_spread + 1.5 * entry_std
                sl = entry_spread - 3 * entry_std
                if current_spread >= tp or current_spread <= sl:
                    pos.close()
                    print(
                        f"✨ LONG CLOSE: Profit={pos.pl:.2f} | Exit Spread={current_spread:.2f}σ"
                    )

            elif pos.is_short:
                tp = entry_spread - 1.5 * entry_std
                sl = entry_spread + 3 * entry_std
                if current_spread <= tp or current_spread >= sl:
                    pos.close()
                    print(
                        f"✨ SHORT CLOSE: Profit={pos.pl:.2f} | Exit Spread={current_spread:.2f}σ"
                    )


# Data preparation with cosmic cleaning 🌠
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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

# Launch backtest 🚀
bt = Backtest(data, QuantumDeviation, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
