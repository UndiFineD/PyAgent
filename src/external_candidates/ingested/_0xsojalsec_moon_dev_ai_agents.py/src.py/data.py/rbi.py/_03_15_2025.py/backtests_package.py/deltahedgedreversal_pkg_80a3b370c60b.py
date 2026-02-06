# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\DeltaHedgedReversal_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and format columns 🌙
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


class DeltaHedgedReversal(Strategy):
    rsi_period = 14
    overbought_level = 70
    exit_level = 55
    swing_window = 20
    risk_pct = 0.01

    def init(self):
        # 🌙 Moon-powered Indicators ✨
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.swing_high = self.I(
            talib.MAX, self.data.High, timeperiod=self.swing_window
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

    def next(self):
        price = self.data.Close[-1]
        equity = self.equity

        # 🌙 Moon Dev Trading Logic 🚀
        if not self.position:
            if self.rsi[-1] > self.overbought_level:
                # Calculate risk parameters
                sl = self.swing_high[-1]
                risk_per_unit = sl - price

                if risk_per_unit > 0:
                    position_size = int(round((equity * self.risk_pct) / risk_per_unit))
                    if position_size > 0:
                        tp = price - (2 * risk_per_unit)
                        self.sell(size=position_size, sl=sl, tp=tp)
                        print(
                            f"🌙✨ SHORT SIGNAL! Selling {position_size} units at {price:.2f}"
                        )
                        print(
                            f"   🛡️ SL: {sl:.2f} | 🎯 TP: {tp:.2f} | 📈 RSI: {self.rsi[-1]:.2f}"
                        )

        else:
            if self.rsi[-1] < self.exit_level:
                self.position.close()
                print(f"🌙💫 EXIT SIGNAL! Closing position at {price:.2f}")
                print(
                    f"   📉 RSI dropped to {self.rsi[-1]:.2f} | 💰 Equity: {equity:,.2f}"
                )


# 🌙 Launch Moon Dev Backtest 🚀
bt = Backtest(data, DeltaHedgedReversal, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌟 Print Moon-charged Results 💫
print("\n" + "=" * 50)
print("🌙 MOON DEV FINAL STATS 🌙")
print("=" * 50)
print(stats)
print(stats._strategy)
print("\n🌙 Backtest completed! May the Moon's wisdom guide your trades! 🌙")
