# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\DynamicTrendSync_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class DynamicTrendSync(Strategy):
    risk_percent = 0.01
    adx_threshold = 25
    rsi_exit_levels = (70, 30)
    swing_period = 5
    time_stop = 10

    def init(self):
        # Indicators
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)

        self.entry_bar = 0

    def next(self):
        if not self.position:
            # Entry conditions
            ema_cross = (self.ema50[-2] < self.ema200[-2]) and (
                self.ema50[-1] > self.ema200[-1]
            )
            adx_strong = (self.adx[-1] > self.adx_threshold) and (
                self.adx[-1] > self.adx[-2]
            )

            if ema_cross and adx_strong:
                entry_price = self.data.Open[-1]
                sl_price = self.swing_low[-1]
                risk_per_share = entry_price - sl_price

                if risk_per_share <= 0:
                    return

                equity = self.equity()
                position_size = (equity * self.risk_percent) / risk_per_share
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙✨ MOON DEV ENTRY ✨🚀\nLong {position_size} @ {entry_price:.2f}\nSL: {sl_price:.2f} | Risk: {risk_per_share:.2f}"
                    )

        else:
            # Exit conditions
            current_rsi = self.rsi[-1]
            time_in_trade = len(self.data) - self.entry_bar

            # RSI exit
            if (
                current_rsi > self.rsi_exit_levels[0]
                or current_rsi < self.rsi_exit_levels[1]
            ):
                self.position.close()
                print(
                    f"🚨🌙 RSI EXIT at {self.data.Close[-1]:.2f} | RSI: {current_rsi:.2f}"
                )

            # Death cross exit
            elif (self.ema200[-2] < self.ema50[-2]) and (
                self.ema200[-1] > self.ema50[-1]
            ):
                self.position.close()
                print(f"☠️🌙 DEATH CROSS EXIT at {self.data.Close[-1]:.2f}")

            # Time stop
            elif time_in_trade >= self.time_stop:
                self.position.close()
                print(f"⏳🌙 TIME STOP EXIT after {self.time_stop} bars")


bt = Backtest(data, DynamicTrendSync, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
