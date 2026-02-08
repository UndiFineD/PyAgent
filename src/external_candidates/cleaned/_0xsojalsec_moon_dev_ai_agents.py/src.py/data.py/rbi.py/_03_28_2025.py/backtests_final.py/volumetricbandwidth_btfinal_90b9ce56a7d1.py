# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests_final\VolumetricBandwidth_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data with Moon Dev precision 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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


class VolumetricBandwidth(Strategy):
    def init(self):
        # Calculate Volume-Weighted MACD components with lunar precision 🌙
        vw_price = self.data.Close * self.data.Volume
        self.ema12 = self.I(talib.EMA, vw_price, timeperiod=12)
        self.ema26 = self.I(talib.EMA, vw_price, timeperiod=26)
        self.vw_macd = self.I(lambda: self.ema12 - self.ema26, name="VW_MACD")
        self.vw_signal = self.I(talib.EMA, self.vw_macd, timeperiod=50, name="Signal")

        # Calculate Bollinger Band components with cosmic accuracy ✨
        self.middle_band = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.std_dev = self.I(talib.STDDEV, self.data.Close, timeperiod=20)

        # Swing low detection for stop loss 🛡️
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20, name="Swing_Low")

        print("🌙 VolumetricBandwidth initialized! Moon Dev engines ready for launch! 🚀")

    def next(self):
        # Calculate dynamic Bollinger Bandwidth with stellar precision 📉
        if len(self.middle_band) < 20 or len(self.vw_signal) < 50:
            return  # Warmup period

        middle = self.middle_band[-1]
        std = self.std_dev[-1]
        bandwidth = (4 * std / middle) * 100  # Simplified bandwidth calculation

        # Moon Dev trading logic - unchanged strategy core 🌗
        if not self.position:
            # Long entry conditions 🌕
            if (self.vw_macd[-2] < self.vw_signal[-2] and self.vw_macd[-1] > self.vw_signal[-1]) and bandwidth < 1:
                risk_amount = 0.01 * self.equity
                entry_price = self.data.Close[-1]
                stop_loss = self.swing_low[-1]

                if stop_loss >= entry_price:
                    print(f"🌙 ABORT MISSION! Invalid SL {stop_loss:.2f} ≥ entry {entry_price:.2f}")
                    return

                position_size = int(round(risk_amount / (entry_price - stop_loss)))
                if position_size > 0:  # Ensure valid position size
                    self.buy(size=position_size, sl=stop_loss)
                    print(f"🚀 LIFTOFF! Long {position_size} units @ {entry_price:.2f} | SL: {stop_loss:.2f} 🌕")
        else:
            # Exit conditions 🌑
            time_in_trade = len(self.data) - self.trades[0].entry_bar
            if (
                (self.vw_signal[-2] < self.vw_macd[-2] and self.vw_signal[-1] > self.vw_macd[-1])
                or bandwidth > 3
                or time_in_trade >= 5
            ):
                self.position.close()
                print(
                    f"🌑 EXIT SIGNAL! {'Timeout' if time_in_trade >= 5 else 'Signal/Bandwidth'} | Price: {self.data.Close[-1]:.2f} 🌘"
                )


# Launch backtest with cosmic parameters 🚀
bt = Backtest(data, VolumetricBandwidth, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n=== MOON DEV FINAL STATS ===")
print(stats)
print(stats._strategy)
