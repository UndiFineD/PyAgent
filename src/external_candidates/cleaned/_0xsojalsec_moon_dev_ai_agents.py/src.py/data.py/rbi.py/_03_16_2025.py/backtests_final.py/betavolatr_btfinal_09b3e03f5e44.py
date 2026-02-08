# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_final\BetaVolATR_BTFinal.py
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BetaVolATR(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade 🌙

    def init(self):
        # Clean and prepare data columns
        self.data.columns = [col.strip().lower() for col in self.data.columns]
        self.data = self.data.drop(columns=[col for col in self.data.columns if "unnamed" in col])

        # Core indicators ✨
        self.high_3d = self.I(talib.MAX, self.data.High, timeperiod=288)  # 3-day high (288x15m)
        self.low_3d = self.I(talib.MIN, self.data.Low, timeperiod=288)  # 3-day low

        # Volume analysis 🌊
        long_volume = self.I(
            lambda close, open: (close > open) * self.data.Volume,
            self.data.Close,
            self.data.Open,
        )
        self.sum_long_vol = self.I(talib.SUM, long_volume, 288)
        self.sum_total_vol = self.I(talib.SUM, self.data.Volume, 288)

        # Volatility metrics 🌪️
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.ema_atr = self.I(talib.EMA, self.atr, 20)

    def next(self):
        current_bar = len(self.data) - 1

        # Entry logic 🚀
        if not self.position:
            new_high = self.data.High[-1] == self.high_3d[-1]
            vol_ratio = self.sum_long_vol[-1] / self.sum_total_vol[-1] if self.sum_total_vol[-1] > 0 else 0

            if new_high and vol_ratio >= 0.8 and self.ema_atr[-1] > 0:
                risk_amount = self.equity * self.risk_per_trade
                stop_distance = 1.5 * self.ema_atr[-1]
                position_size = int(round(risk_amount / stop_distance))

                if position_size > 0:
                    stop_price = self.data.Close[-1] - stop_distance
                    self.buy(size=position_size, sl=stop_price, tag="🌙 BetaVolATR Entry")
                    print(
                        f"🚀 MOON DEV ALERT: Long {position_size} units at {self.data.Close[-1]:.2f} | SL: {stop_price:.2f} ✨"
                    )

        # Exit logic 💸
        elif self.position:
            entry_bar = self.position.entry_bar
            bars_held = current_bar - entry_bar

            # Momentum reversal exit
            if self.data.Close[-1] < self.low_3d[-1]:
                self.position.close()
                print(f"🌙 MOON DEV EXIT: Momentum reversal at {self.data.Close[-1]:.2f} 🌗")

            # Time-based exit (5 days = 480x15m)
            elif bars_held >= 480:
                self.position.close()
                print(f"🕒 MOON DEV EXIT: Time exit after 5 days at {self.data.Close[-1]:.2f} ⏳")


# Data preparation 🌐
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
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

# Run backtest ⚡
bt = Backtest(data, BetaVolATR, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
