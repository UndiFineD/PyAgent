# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_16_2025\backtests\VolatilitySurge_BT.py
# 🌙 Moon Dev's VolatilitySurge Backtest Script 🌙
import pandas as pd
import pandas_ta as pd_ta
import talib
from backtesting import Backtest, Strategy


class VolatilitySurge(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # ✨ Calculate indicators with TA-Lib/pandas_ta using self.I() ✨
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr_ma = self.I(talib.SMA, self.atr, 20)
        self.vwap = self.I(pd_ta.vwap, self.data.High, self.data.Low, self.data.Close, self.data.Volume)

    def next(self):
        # 🌙 Check minimum data length
        if len(self.data) < 20:
            return

        # 🚀 Get indicator values
        current_close = self.data.Close[-1]
        current_atr = self.atr[-1]
        previous_atr = self.atr[-2]
        current_atr_ma = self.atr_ma[-1]
        previous_atr_ma = self.atr_ma[-2]

        # 💡 Entry Conditions
        atr_cross = (current_atr > current_atr_ma) and (previous_atr <= previous_atr_ma)
        price_above_vwap = current_close > self.vwap[-1]

        # 🌙 Entry Logic
        if not self.position and atr_cross and price_above_vwap:
            # 🛡️ Risk Management Calculations
            stop_loss = current_close - 2 * current_atr
            risk_amount = self.equity * self.risk_percent
            risk_per_unit = current_close - stop_loss

            if risk_per_unit > 0:
                position_size = int(round(risk_amount / risk_per_unit))
                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss)
                    print(
                        f"🌙 MOON DEV BUY SIGNAL 🌙 | Entry: {current_close:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | ATR: {current_atr:.2f} ✨"
                    )

        # 🔄 Update Trailing Stop
        if self.position:
            new_sl = self.data.Close[-1] - 2 * self.atr[-1]
            if new_sl > self.position.sl:
                self.position.sl = new_sl
                print(
                    f"🚀 TRAILING STOP UPDATED 🚀 | New SL: {new_sl:.2f} | Price: {self.data.Close[-1]:.2f} | ATR: {self.atr[-1]:.2f}"
                )


# 📂 Data Preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# 🧹 Clean and format data
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

# 🚀 Run Backtest
bt = Backtest(data, VolatilitySurge, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌙 Print Full Statistics
print("\n" + "=" * 50)
print("🌕 MOON DEV BACKTEST RESULTS 🌕")
print("=" * 50 + "\n")
print(stats)
print("\n" + "=" * 50)
print("🔍 STRATEGY ANALYSIS 🔍")
print("=" * 50 + "\n")
print(stats._strategy)
