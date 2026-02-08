# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_01_2025\backtests_package\VoltaicAccumulation_PKG.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean column names and drop unnamed columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Rename columns to proper case
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VoltaicAccumulation(Strategy):
    risk_pct = 0.01  # 1% risk per trade 🌙
    rrr = 3  # Risk-Reward Ratio 🚀

    def init(self):
        # Calculate 4H TWAP (SMA of typical price) ✨
        typical_price = (self.data.High + self.data.Low + self.data.Close) / 3
        self.twap = self.I(talib.SMA, typical_price, timeperiod=16)

        # Volatility-Adjusted Bollinger Bands (20, 2.5σ) 🌙
        self.bb_upper = self.I(talib.BBANDS, self.data.Close, 20, 2.5, 2.5, 0, which=0)
        self.bb_lower = self.I(talib.BBANDS, self.data.Close, 20, 2.5, 2.5, 0, which=2)

        # Chaikin Money Flow (20-period) 🕯️
        self.cmf = self.I(ta.cmf, self.data.High, self.data.Low, self.data.Close, self.data.Volume, 20)

        # Volume filter SMA
        self.vol_sma = self.I(talib.SMA, self.data.Volume, 20)

        print("🌙✨ Moon Dev Indicators Activated! TWAP | BBands(2.5σ) | CMF Online 🚀")

    def next(self):
        # Wait for sufficient data 🌙
        if len(self.data) < 20:
            return

        # Current values ✨
        price = self.data.Close[-1]
        twap_cross = (self.twap[-2] < self.bb_upper[-2]) and (
            self.twap[-1] > self.bb_upper[-1]
        )  # Bullish crossover replacement
        cmf_bullish = self.cmf[-1] > 0
        vol_ok = self.data.Volume[-1] > self.vol_sma[-1]

        # Entry Logic: TWAP Breakout + CMF Confirmation 🌙🚀
        if not self.position and twap_cross and cmf_bullish and vol_ok:
            sl = self.bb_lower[-1]
            risk_per_share = price - sl

            if risk_per_share <= 0:
                print("⚠️ Moon Dev Warning: Negative risk detected! Trade aborted 🌙")
                return

            risk_amount = self.equity * self.risk_pct
            position_size = int(round(risk_amount / risk_per_share))

            if position_size > 0:
                tp = price + (risk_per_share * self.rrr)
                self.buy(size=position_size, sl=sl, tp=tp)
                print(
                    f"🌙🚀 MOON DEV LONG! Size: {position_size} | Entry: {price:.2f} | SL: {sl:.2f} | TP: {tp:.2f} ✨"
                )


# Launch Backtest 🌙🚀
bt = Backtest(data, VoltaicAccumulation, cash=1_000_000, margin=1.0)
stats = bt.run()
print("\n" + "=" * 50)
print("🌙✨ MOON DEV BACKTEST RESULTS 🚀")
print("=" * 50)
print(stats)
print(stats._strategy)
