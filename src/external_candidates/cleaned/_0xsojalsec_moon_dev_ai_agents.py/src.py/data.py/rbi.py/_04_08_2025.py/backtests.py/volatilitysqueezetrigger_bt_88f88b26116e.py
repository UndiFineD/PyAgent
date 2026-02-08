# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests\VolatilitySqueezeTrigger_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolatilitySqueezeTrigger(Strategy):
    bb_period = 20
    bb_dev = 2
    hv_period = 10
    contraction_threshold = 0.7
    risk_pct = 0.01
    time_exit_bars = 5

    def init(self):
        # Bollinger Bands components
        self.sma = self.I(talib.SMA, self.data.Close, self.bb_period)
        self.std = self.I(talib.STDDEV, self.data.Close, self.bb_period)
        self.upper = self.I(lambda sma, std: sma + std * self.bb_dev, self.sma, self.std)
        self.lower = self.I(lambda sma, std: sma - std * self.bb_dev, self.sma, self.std)
        self.band_width = self.I(lambda u, l, m: (u - l) / m, self.upper, self.lower, self.sma)

        # Historical Volatility calculation
        def log_returns(close):
            returns = np.zeros_like(close)
            for i in range(1, len(close)):
                returns[i] = np.log(close[i] / close[i - 1])
            return returns

        self.hv = self.I(talib.STDDEV, self.I(log_returns, self.data.Close), self.hv_period)

        print("🌙 MOON DEV INIT: Strategy armed with Bollinger Bands & Volatility Squeeze Detector! ✨")

    def next(self):
        if len(self.data) < max(self.bb_period, self.hv_period) + 1:
            return

        current_close = self.data.Close[-1]
        bandwidth = self.band_width[-1]
        hv_value = self.hv[-1]
        in_squeeze = bandwidth < self.contraction_threshold * hv_value
        price_in_bands = self.lower[-1] < current_close < self.upper[-1]

        if not self.position and in_squeeze and price_in_bands:
            risk_amount = self.equity * self.risk_pct
            stop_distance = current_close - self.lower[-1]

            if stop_distance <= 0:
                print("🌙⚠️ MOON DEV ALERT: Invalid stop distance! Trade aborted.")
                return

            position_size = int(round(risk_amount / stop_distance))
            if position_size > 0:
                self.buy(size=position_size)
                print(f"🚀 MOON DEV LAUNCH: Long {position_size} units at {current_close:.2f}! ✨")
                print(f"   SL: {self.lower[-1]:.2f} | TP: {self.upper[-1]:.2f} | Risk: {self.risk_pct * 100}%")

        elif self.position:
            if current_close >= self.upper[-1]:
                self.position.close()
                print(f"🎯 MOON DEV BULLSEYE: Take profit at {current_close:.2f}! 💰")
            elif current_close <= self.lower[-1]:
                self.position.close()
                print(f"🌧️ MOON DEV STORM: Stop loss triggered at {current_close:.2f}! ☔")
            elif len(self.data) - self.position.entry_bar >= self.time_exit_bars:
                self.position.close()
                print(f"⌛ MOON DEV TIMEOUT: Position closed after {self.time_exit_bars} bars! ⏳")


# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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

# Execute backtest
bt = Backtest(data, VolatilitySqueezeTrigger, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
