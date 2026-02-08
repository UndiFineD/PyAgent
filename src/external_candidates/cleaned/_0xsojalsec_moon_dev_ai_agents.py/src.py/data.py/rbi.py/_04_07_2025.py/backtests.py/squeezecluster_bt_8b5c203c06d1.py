# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests\SqueezeCluster_BT.py
# moon_dev_backtest.py 🌙🚀
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# =====================
# MOON DEV DATA PREP ✨
# =====================
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Cleanse data with Moon Dev magic ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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


# ========================
# SQUEEZE CLUSTER STRAT 🌙
# ========================
class SqueezeCluster(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌕

    def init(self):
        # === BOLLINGER SQUEEZE DETECTOR ===
        def bbw_calculator(close):
            upper, middle, lower = talib.BBANDS(close, 20, 2, 2)
            return (upper - lower) / middle

        self.bbw = self.I(bbw_calculator, self.data.Close)
        self.bbw_avg = self.I(talib.SMA, self.bbw, 20)

        # === LIQUIDATION CLUSTER FINDER ===
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

        # === VOLATILITY MEASURES ===
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        # === MOON DEV SPECIAL SAUCE 🌶️ ===
        def volatility_percentile(series):
            return ta.quantile(series, length=30, q=0.9)

        self.bbw_percentile = self.I(volatility_percentile, self.bbw)

        print("🌙✨ Moon Dev Systems Armed - Ready for Launch! 🚀")

    def next(self):
        # === MOON DEV TRADE LOGIC ===
        price = self.data.Close[-1]
        atr = self.atr[-1]

        # Entry Conditions
        squeeze_active = self.bbw[-1] < self.bbw_avg[-1]
        long_trigger = price <= self.swing_low[-1] + atr
        short_trigger = price >= self.swing_high[-1] - atr

        # Position Sizing Alchemy 🔮
        position_size = int(round((self.equity * self.risk_percent) / (1.5 * atr)))

        # === EXECUTE ORDERS ===
        if not self.position:
            if squeeze_active and long_trigger:
                sl = price - 1.5 * atr
                self.buy(size=position_size, sl=sl)
                print(f"🌙🚀 LIFT OFF! Long {position_size} @ {price:.2f} | SL: {sl:.2f}")

            elif squeeze_active and short_trigger:
                sl = price + 1.5 * atr
                self.sell(size=position_size, sl=sl)
                print(f"🌙🌒 COMET DIVE! Short {position_size} @ {price:.2f} | SL: {sl:.2f}")

        # === EXIT CONDITIONS ===
        else:
            if self.bbw[-1] > self.bbw_percentile[-1]:
                self.position.close()
                print(f"🌪️💨 VOLATILITY STORM! Closing @ {price:.2f}")


# ======================
# LAUNCH BACKTEST 🚀
# ======================
bt = Backtest(data, SqueezeCluster, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n=== MOON DEV FINAL REPORT ===")
print(stats)
print(stats._strategy)
print("🌙🔭 Mission Complete! Time to analyze the stars 📈")
