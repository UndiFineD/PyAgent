# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\LiquidityBreakout_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class LiquidityBreakout(Strategy):
    risk_percent = 0.01
    bbw_threshold = 0.5
    volatility_exit = 1.5

    def init(self):
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

        def calculate_bbw(close):
            upper, middle, lower = talib.BBANDS(close, 20, 2, 2)
            return (upper - lower) / middle

        self.bbw = self.I(calculate_bbw, self.data.Close)

    def next(self):
        price = self.data.Close[-1]
        equity = self.equity

        if not self.position:
            # Long entry logic
            long_trigger = (
                price > self.swing_high[-1]
                and (price - self.swing_high[-1]) / self.swing_high[-1] <= 0.02
                and self.bbw[-1] < self.bbw_threshold
            )

            if long_trigger:
                sl = self.swing_low[-1]
                risk_per_share = price - sl
                if risk_per_share > 0:
                    size = int(round((equity * self.risk_percent) / risk_per_share))
                    tp = price + 2 * (price - sl)
                    self.buy(size=size, sl=sl, tp=tp)
                    print(
                        f"🌙 LONG LAUNCH 🚀 | Price: {price:.2f} | Size: {size} | Moon Target: {tp:.2f}"
                    )

            # Short entry logic
            short_trigger = (
                price < self.swing_low[-1]
                and (self.swing_low[-1] - price) / self.swing_low[-1] <= 0.02
                and self.bbw[-1] < self.bbw_threshold
            )

            if short_trigger:
                sl = self.swing_high[-1]
                risk_per_share = sl - price
                if risk_per_share > 0:
                    size = int(round((equity * self.risk_percent) / risk_per_share))
                    tp = price - 2 * (sl - price)
                    self.sell(size=size, sl=sl, tp=tp)
                    print(
                        f"🌑 SHORT IGNITION 🌘 | Price: {price:.2f} | Size: {size} | Black Hole Target: {tp:.2f}"
                    )
        else:
            # Volatility-based exit
            if self.bbw[-1] > self.volatility_exit:
                self.position.close()
                print(
                    f"🌪️ VOLATILITY EJECTION 🌪️ | Price: {price:.2f} | Equity: {equity:.2f}"
                )


bt = Backtest(data, LiquidityBreakout, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
