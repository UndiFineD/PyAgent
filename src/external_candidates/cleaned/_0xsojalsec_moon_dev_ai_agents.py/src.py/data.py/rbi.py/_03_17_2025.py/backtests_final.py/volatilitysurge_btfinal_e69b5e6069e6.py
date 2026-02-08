# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_17_2025\backtests_final\VolatilitySurge_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Column mapping
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

# Convert index to datetime
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VolatilitySurge(Strategy):
    def init(self):
        # Calculate indicators with proper period conversions
        close_prices = self.data.Close

        # 10-day Historical Volatility (960 periods)
        returns = np.log(close_prices / close_prices.shift(1)).fillna(0)
        self.hv = self.I(talib.STDDEV, returns, 960, nbdev=1) * np.sqrt(96 * 252)

        # 20-day Volume Z-Score (1920 periods)
        self.vol_ma = self.I(talib.MA, self.data.Volume, 1920)
        self.vol_std = self.I(talib.STDDEV, self.data.Volume, 1920, nbdev=1)
        self.volume_z = self.I(
            lambda v, m, s: (v - m) / (s + 1e-9),
            self.data.Volume,
            self.vol_ma,
            self.vol_std,
        )

        # 14-day ATR (1344 periods)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 1344)

        print("🌙 Moon Dev Indicators Initialized! ✨")
        print(f"📉 10D HV Window: 960 | 📊 Volume Z Window: 1920 | 🚀 ATR Period: 1344")

    def next(self):
        if not self.position:
            # Get current indicator values
            hv = self.hv[-1]
            vz = self.volume_z[-1]
            atr = self.atr[-1]

            # Entry conditions
            if hv < 0.2 and vz > 2 and atr > 0:
                # Risk management calculations
                risk_amount = self.equity * 0.01
                position_size = int(round(risk_amount / atr))

                # Ensure position size is valid
                if position_size <= 0:
                    print("🌑 Invalid position size calculated. Skipping trade.")
                    return

                # Moon-themed debug
                print(f"\n🚀 MOONSHOT ALERT! 🌕")
                print(f"📉 HV: {hv:.2%} | 📊 Volume Z: {vz:.2f}")
                print(f"💰 Entry: {self.data.Close[-1]:.2f}")
                print(f"✨ ATR: {atr:.2f} | 📦 Size: {position_size} units")

                # Entry order with SL/TP
                self.buy(
                    size=position_size,
                    sl=self.data.Close[-1] - atr,
                    tp=self.data.Close[-1] + 2 * atr,
                )
        else:
            # Moon-themed exit tracking
            if self.position.pl_pct >= 0.5:
                print(f"🌕 PROFIT UNIVERSE REACHED! Closing: {self.data.Close[-1]:.2f}")
                self.position.close()
            elif self.position.pl_pct <= -0.1:
                print(f"🌑 BLACK HOLE STOPPED OUT! Closing: {self.data.Close[-1]:.2f}")
                self.position.close()


# Execute backtest
bt = Backtest(data, VolatilitySurge, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full statistics
print("\n🌙🌙🌙 MOON DEV BACKTEST RESULTS 🌙🌙🌙")
print(stats)
print(stats._strategy)
