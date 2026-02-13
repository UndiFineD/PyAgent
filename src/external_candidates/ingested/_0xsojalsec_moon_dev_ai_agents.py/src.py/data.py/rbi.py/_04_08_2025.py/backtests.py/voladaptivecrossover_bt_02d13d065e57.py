# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests\VolAdaptiveCrossover_BT.py
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and format data 🌙
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class VolAdaptiveCrossover(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌕

    def init(self):
        # Trend indicators 🚀
        self.ema50 = self.I(talib.EMA, self.data.Close, 50, name="EMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, 200, name="EMA200")

        # Volatility framework 🌊
        self.hv20 = self.I(ta.hv, self.data.Close, length=20, log=True, name="HV20")
        self.percentile_window = 252 * 96  # 1 year of 15m bars

        # Percentile calculations 📊
        window = self.percentile_window
        self.hv20_p20 = self.I(
            lambda x: x.rolling(window).quantile(0.2), self.hv20, name="HV20_20P"
        )
        self.hv20_p50 = self.I(
            lambda x: x.rolling(window).quantile(0.5), self.hv20, name="HV20_50P"
        )

    def next(self):
        # Wait for indicators to warm up ⏳
        if len(self.data) < max(200, self.percentile_window):
            return

        # Current values extraction 🌙
        price = self.data.Close[-1]
        ema50 = self.ema50[-1]
        ema200 = self.ema200[-1]
        hv20 = self.hv20[-1]
        hv20_p20 = self.hv20_p20[-1]
        hv20_p50 = self.hv20_p50[-1]

        # Moon Dev status print 🌑
        print(
            (
                f"🌙 EMA50/200: {ema50:.2f}/{ema200:.2f} | "
                f"HV20: {hv20:.4f} (20th% {hv20_p20:.4f}, 50th% {hv20_p50:.4f})"
            )
        )

        # Entry logic 🚀
        if not self.position:
            if ema50 > ema200 and hv20 < hv20_p20:
                size = int(round((self.equity * self.risk_percent) / price))
                if size > 0:
                    self.buy(size=size)
                    print(
                        (
                            f"🚀🌕 MOON DEV LONG SIGNAL 🚀🌕\n"
                            f"Entry Price: {price:.2f} | "
                            f"Position Size: {size} shares ✨\n"
                            f"Equity: {self.equity:.2f} | "
                            f"Risk: {self.risk_percent*100}% 🌙"
                        )
                    )

        # Exit logic 🌑
        else:
            if hv20 > hv20_p50 or ema50 < ema200:
                self.position.close()
                print(
                    (
                        f"🌑✨ MOON DEV EXIT SIGNAL 🌑✨\n"
                        f"Exit Price: {price:.2f} | "
                        f"Position Value: {self.position.size * price:.2f} ✨\n"
                        f"Equity: {self.equity:.2f} 🌙"
                    )
                )


# Launch backtest 🚀
bt = Backtest(data, VolAdaptiveCrossover, cash=1_000_000, trade_on_close=True)
stats = bt.run()
print(stats)
print(stats._strategy)
