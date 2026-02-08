# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_30_2025\backtests\LiquidityClusterTrail_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean data columns
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


class LiquidityClusterTrail(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    atr_period = 14
    swing_period = 20
    volatility_threshold = 100  # Adjust based on asset
    trail_multiplier = 2

    def init(self):
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=self.swing_period)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.highest_high = None

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            # Volatility check
            if self.atr[-1] < self.volatility_threshold:
                # Liquidity cluster detection
                if price <= self.swing_low[-1] * 1.01:
                    risk_amount = self.equity * self.risk_percent
                    stop_price = self.swing_low[-1]
                    risk_distance = price - stop_price

                    if risk_distance > 0:
                        size = int(round(risk_amount / risk_distance))
                        if size > 0:
                            self.buy(size=size, sl=stop_price)
                            self.highest_high = self.data.High[-1]
                            print(f"🌙✨ MOON DEV LONG ENTRY ✨")
                            print(f"Size: {size} | Entry: {price} | SL: {stop_price} 🚀")
        else:
            # Update trailing stop
            self.highest_high = max(self.highest_high, self.data.High[-1])
            trail_stop = self.highest_high - self.atr[-1] * self.trail_multiplier

            # Exit conditions
            if self.data.Close[-1] < trail_stop:
                self.position.close()
                print(f"🌙💥 TRAILING STOP EXIT @ {self.data.Close[-1]} 🔴")
            elif self.data.Close[-1] >= self.swing_high[-1]:
                self.position.close()
                print(f"🌙🎯 LIQUIDITY CLUSTER EXIT @ {self.data.Close[-1]} 🟢")


# Run backtest
bt = Backtest(data, LiquidityClusterTrail, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
