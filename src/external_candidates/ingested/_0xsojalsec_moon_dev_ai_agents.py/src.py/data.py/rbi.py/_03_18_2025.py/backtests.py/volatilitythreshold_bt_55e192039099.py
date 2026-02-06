# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_18_2025\backtests\VolatilityThreshold_BT.py
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


# Moon Dev Data Preparation 🌙✨
def prepare_data(filepath):
    # Load and clean data
    data = pd.read_csv(filepath)

    # Clean column names
    data.columns = data.columns.str.strip().str.lower()

    # Drop unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

    # Proper column mapping
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

    # Convert datetime and set index
    data["DateTime"] = pd.to_datetime(data["datetime"])
    data.set_index("DateTime", inplace=True)

    return data


class VolatilityThreshold(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Moon Dev Indicators 🌙📈
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20
        )
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)

        # ATR percentile calculation using pandas rolling quantile
        def calculate_percentile(arr):
            return pd.Series(arr).rolling(100).quantile(0.10).values

        self.atr_percentile = self.I(calculate_percentile, self.atr)

        self.stop_loss_price = None
        self.entry_bar = None

    def next(self):
        # Moon Dev Entry Logic 🌙🚀
        if not self.position:
            # Check minimum data length
            if len(self.data) < 100:
                return

            current_atr = self.atr[-1]
            current_percentile = self.atr_percentile[-1]
            sma50_cross = (self.data.Close[-1] > self.sma50[-1]) and (
                self.data.Close[-2] <= self.sma50[-2]
            )

            if current_atr < current_percentile and sma50_cross:
                # Risk management calculations
                risk_amount = self.equity[-1] * self.risk_percent
                atr_value = current_atr
                stop_loss_price = self.data.Close[-1] - 2 * atr_value
                risk_per_share = self.data.Close[-1] - stop_loss_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size)
                        self.stop_loss_price = stop_loss_price
                        self.entry_bar = len(self.data)
                        print(
                            f"🚀🌙 MOON DEV ENTRY! Buy {position_size} @ {self.data.Close[-1]} | SL: {stop_loss_price:.2f} ✨"
                        )

        # Moon Dev Exit Logic 🌙🛑
        if self.position:
            # Stop loss check
            if self.data.Low[-1] < self.stop_loss_price:
                self.sell(size=self.position.size)
                print(
                    f"🌧️🌙 MOON DEV STOP LOSS! Sold @ {self.data.Close[-1]} | Loss: {self.position.pl:.2f} ✨"
                )

            # Time-based exit (5 days = 480 15min bars)
            elif (len(self.data) - self.entry_bar) >= 480:
                self.sell(size=self.position.size)
                print(
                    f"⏰🌙 MOON DEV TIME EXIT! Sold @ {self.data.Close[-1]} | Profit: {self.position.pl:.2f} ✨"
                )


# Moon Dev Backtest Execution 🌙📊
if __name__ == "__main__":
    data = prepare_data(
        "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
    )
    bt = Backtest(data, VolatilityThreshold, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Moon Dev Results 🌙📜
    print("\n" + "=" * 40 + " MOON DEV FINAL STATS " + "=" * 40)
    print(stats)
    print("\n" + "=" * 40 + " STRATEGY DETAILS " + "=" * 40)
    print(stats._strategy)
