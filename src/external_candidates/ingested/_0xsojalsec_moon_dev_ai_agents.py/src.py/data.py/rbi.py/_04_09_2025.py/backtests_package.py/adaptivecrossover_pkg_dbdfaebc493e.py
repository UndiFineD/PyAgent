# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_09_2025\backtests_package\AdaptiveCrossover_PKG.py
# 🌙 MOON DEV BACKTESTING SCRIPT FOR ADAPTIVECROSSOVER STRATEGY 🚀

import pandas as pd
import talib
from backtesting import Backtest, Strategy

# =====================
# DATA PREPARATION 🌐
# =====================
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

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

# Convert datetime and set index ⏰
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# =====================
# STRATEGY IMPLEMENTATION 🚀
# =====================


class AdaptiveCrossover(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # 🌙 MOON INDICATORS ✨
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50, name="EMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200, name="EMA200")
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ADX",
        )
        self.swing_low = self.I(
            talib.MIN, self.data.Low, timeperiod=20, name="Swing Low"
        )

        print("🌙 MOON DEV: Indicators initialized! ✨")

    def next(self):
        # 🌙 CORE LOGIC 🧠
        price = self.data.Close[-1]

        # Long entry conditions 🌙
        if not self.position:
            # Bullish crossover replacement
            if (
                self.ema50[-2] < self.ema200[-2] and self.ema50[-1] > self.ema200[-1]
            ) and self.adx[-1] < 20:
                sl_price = self.swing_low[-1]
                risk_amount = self.equity * self.risk_per_trade
                risk_per_unit = price - sl_price

                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price)
                        print(
                            f"🌙✨ GOLDEN CROSS ALERT! Entry: {price:.2f} | Size: {position_size} | Risk: {risk_per_unit:.2f} 🚀"
                        )

        # Exit conditions 🌙
        else:
            # Bearish crossunder replacement
            if (
                self.ema50[-2] > self.ema200[-2] and self.ema50[-1] < self.ema200[-1]
            ) or self.adx[-1] > 40:
                self.position.close()
                print(
                    f"🚨🌙 EXIT SIGNAL! Price: {price:.2f} | ADX: {self.adx[-1]:.2f} | Equity: {self.equity:.2f} ✨"
                )


# =====================
# BACKTEST EXECUTION 📊
# =====================

bt = Backtest(data, AdaptiveCrossover, cash=1_000_000, exclusive_orders=True)

print("🌙🌙🌙 MOON DEV BACKTEST INITIATED 🚀🚀🚀")
stats = bt.run()
print("🌙🌙🌙 BACKTEST COMPLETE! MOON DEV STATS BELOW ✨✨✨")
print(stats)
print(stats._strategy)
