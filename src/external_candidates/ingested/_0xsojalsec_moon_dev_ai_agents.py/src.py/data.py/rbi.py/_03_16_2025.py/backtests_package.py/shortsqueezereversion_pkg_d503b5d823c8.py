# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_package\ShortSqueezeReversion_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 MOON DEV DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and prepare data according to Moon Dev specs
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


class ShortSqueezeReversion(Strategy):
    def init(self):
        # 🌙✨ MOON DEV INDICATORS
        self.avg_daily_volume = self.I(
            talib.SMA, self.data.Volume, timeperiod=96
        )  # 15m -> daily
        self.short_interest_ratio = self.I(
            lambda si, vol: si / vol,
            self.data.df["short_interest"],  # Assumes column exists
            self.avg_daily_volume,
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=96)  # 1-day RSI
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        self.entry_bar = 0  # For time-based exit tracking

    def next(self):
        # 🌙 MOON DEV DEBUG PRINTS
        print(
            f"🌙 RSI: {self.rsi[-1]:.1f} | Short Ratio: {self.short_interest_ratio[-1]:.2f} | Vol: {self.data.Volume[-1]:.0f}"
        )

        if not self.position:
            # 🚀 ENTRY LOGIC
            three_green = all(
                self.data.Close[-i] > self.data.Open[-i] for i in range(2, 5)
            )
            vol_spike = self.data.Volume[-1] > 1.5 * self.vol_sma[-1]

            if (
                self.short_interest_ratio[-1] > 0.2
                and self.rsi[-1] < 30
                and (three_green or vol_spike)
            ):

                # 🌙 RISK MANAGEMENT
                risk_pct = 0.01  # 1% equity risk
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * 0.95  # 5% stop
                risk_per_share = entry_price - stop_loss

                position_size = int(round((self.equity * risk_pct) / risk_per_share))

                if position_size > 0:
                    # 🚀 ENTRY WITH MOON DEV FLAIR
                    take_profit = entry_price * 1.10  # 10% target
                    self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                    self.entry_bar = len(self.data)
                    print(
                        f"🚀🌕 MOON DEV LONG! Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_loss:.2f} | TP: {take_profit:.2f}"
                    )
        else:
            # 🌑 EXIT CONDITIONS
            if self.rsi[-1] >= 70:
                self.position.close()
                print(f"🌑🌙 MOON DEV EXIT! RSI 70 @ {self.data.Close[-1]:.2f}")

            # ⏰ Time-based exit (1 day = 96 bars)
            if len(self.data) - self.entry_bar >= 96:
                self.position.close()
                print(f"⏰🌕 TIME EXIT @ {self.data.Close[-1]:.2f}")


# 🌙 BACKTEST EXECUTION
bt = Backtest(data, ShortSqueezeReversion, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
