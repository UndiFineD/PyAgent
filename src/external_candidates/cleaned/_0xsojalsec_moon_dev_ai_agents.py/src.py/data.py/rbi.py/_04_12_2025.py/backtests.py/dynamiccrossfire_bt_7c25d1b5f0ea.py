# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_12_2025\backtests\DynamicCrossfire_BT.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and prepare data
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


class DynamicCrossfire(Strategy):
    ema_period_fast = 50
    ema_period_slow = 200
    adx_period = 14
    rsi_period = 14
    risk_pct = 0.01
    swing_period = 20

    def init(self):
        # Core Indicators 🌙
        self.ema_fast = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_fast, name="EMA50")
        self.ema_slow = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_slow, name="EMA200")
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period, name="SWING_LOW")

        self.entry_signal = False
        print("🌙✨ Moon Dev Backtest Engine Initialized! Ready for Launch 🚀")

    def next(self):
        current_bar = len(self.data) - 1

        # Exit Conditions 🌙
        if self.position:
            # RSI Exit
            if crossover(70, self.rsi):
                self.position.close()
                print(f"🌙✨ RSI EXIT | Price: {self.data.Close[-1]} | RSI: {self.rsi[-1]:.1f}")

            # EMA Death Cross Exit
            if crossover(self.ema_slow, self.ema_fast):
                self.position.close()
                print(f"🌙☠️ DEATH CROSS EXIT | Price: {self.data.Close[-1]}")

        # Entry Conditions 🚀
        else:
            # EMA Golden Cross Check
            ema_cross = crossover(self.ema_fast, self.ema_slow)

            # ADX Strength Check
            adx_rising = self.adx[-1] > self.adx[-2] and self.adx[-1] > 25

            if ema_cross and adx_rising:
                self.entry_signal = True
                print(f"🌙🔥 SIGNAL CONFIRMED | EMA Cross: ✅ | ADX Strength: {self.adx[-1]:.1f} ✅")

            # Execute Entry on Next Candle
            if self.entry_signal:
                # Risk Management Calculations 🌙
                entry_price = self.data.Open[-1]
                stop_price = self.swing_low[-2]  # Previous swing low
                risk_per_unit = entry_price - stop_price

                if risk_per_unit > 0:
                    position_size = (self.equity * self.risk_pct) / risk_per_unit
                    position_size = int(round(position_size))

                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_price)
                        print(f"🚀🌙 ENTRY | Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_price:.2f}")

                self.entry_signal = False


# Launch Backtest 🌙🚀
bt = Backtest(data, DynamicCrossfire, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print("\n🌕🌕🌕 MOON DEV FINAL STATS 🌕🌕🌕")
print(stats)
print(stats._strategy)
