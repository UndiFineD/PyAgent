# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\backtests_final\VIXContraMomentum_BTFinal.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 MOON DEV DATA PREPARATION 🌙
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and prepare data
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


class VIXContraMomentum(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌙
    atr_period = 14
    swing_period = 20
    vix_threshold = 0.02  # 2% threshold for pattern confirmation ✨

    def init(self):
        # 🌙 MOON DEV INDICATORS 🌙
        self.swing_high = self.I(
            talib.MAX, self.data.Close, timeperiod=self.swing_period
        )
        self.swing_low = self.I(
            talib.MIN, self.data.Close, timeperiod=self.swing_period
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )

    def next(self):
        current_price = self.data.Close[-1]
        atr_value = self.atr[-1]
        equity = self.equity

        # 🌙✨ RISK MANAGEMENT CALCULATIONS 🚀
        risk_amount = equity * self.risk_percent
        if atr_value == 0:
            return  # Avoid division by zero

        if not self.position:
            # 🌙 V PATTERN LONG ENTRY 🌙
            if current_price <= self.swing_high[-1] * (1 - self.vix_threshold):
                position_size = int(round(risk_amount / atr_value))
                if position_size > 0:
                    sl = current_price - atr_value * 1.5
                    tp = current_price + atr_value * 3
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙✨🚀 MOON DEV LONG SIGNAL! Entry: {current_price:.2f} | Size: {position_size} | SL: {sl:.2f} | TP: {tp:.2f}"
                    )

            # 🌙 INVERTED V SHORT ENTRY 🌙
            elif current_price >= self.swing_low[-1] * (1 + self.vix_threshold):
                position_size = int(round(risk_amount / atr_value))
                if position_size > 0:
                    sl = current_price + atr_value * 1.5
                    tp = current_price - atr_value * 3
                    self.sell(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙✨🚀 MOON DEV SHORT SIGNAL! Entry: {current_price:.2f} | Size: {position_size} | SL: {sl:.2f} | TP: {tp:.2f}"
                    )

        else:
            # 🌙 MOON DEV TRAILING LOGIC ✨
            if self.position.is_long and (
                self.data.Close[-2] < self.swing_high[-2]
                and self.data.Close[-1] > self.swing_high[-1]
            ):
                self.position.close()
                print(f"🌙✨ MOON DEV LONG EXIT | Price: {current_price:.2f}")
            elif self.position.is_short and (
                self.swing_low[-2] > self.data.Close[-2]
                and self.swing_low[-1] < self.data.Close[-1]
            ):
                self.position.close()
                print(f"🌙✨ MOON DEV SHORT EXIT | Price: {current_price:.2f}")


# 🌙✨ BACKTEST EXECUTION 🚀
bt = Backtest(data, VIXContraMomentum, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙✨ MOON DEV FINAL STATS 🌙✨")
print(stats)
print("\n🌙✨ STRATEGY DETAILS 🌙✨")
