# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\DynamicBreakoutX_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class DynamicBreakoutX(Strategy):
    donchian_period = 20
    adx_period = 14
    atr_period = 14
    risk_per_trade = 0.01

    def init(self):
        self.donchian_high = self.I(talib.MAX, self.data.High, timeperiod=self.donchian_period)
        self.donchian_low = self.I(talib.MIN, self.data.Low, timeperiod=self.donchian_period)
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )
        self.trailing_high = None
        self.trailing_low = None

    def next(self):
        if not self.position:
            if self.data.Close[-1] > self.donchian_high[-1] and self.adx[-1] > 25 and self.adx[-1] > self.adx[-2]:
                risk_amount = self.equity * self.risk_per_trade
                atr_value = self.atr[-1]
                if atr_value != 0:
                    position_size = int(round(risk_amount / (3 * atr_value)))
                    if position_size > 0:
                        self.buy(size=position_size)
                        self.trailing_high = self.data.High[-1]
                        print(
                            f"🚀🌙 LONG ENTRY @ {self.data.Close[-1]:.2f} | Size: {position_size} | Moon Power Activated!"
                        )

            elif self.data.Close[-1] < self.donchian_low[-1] and self.adx[-1] > 25 and self.adx[-1] > self.adx[-2]:
                risk_amount = self.equity * self.risk_per_trade
                atr_value = self.atr[-1]
                if atr_value != 0:
                    position_size = int(round(risk_amount / (3 * atr_value)))
                    if position_size > 0:
                        self.sell(size=position_size)
                        self.trailing_low = self.data.Low[-1]
                        print(
                            f"📉🌙 SHORT ENTRY @ {self.data.Close[-1]:.2f} | Size: {position_size} | Dark Side Engaged!"
                        )

        elif self.position.is_long:
            self.trailing_high = max(self.trailing_high, self.data.High[-1])
            stop_price = self.trailing_high - 3 * self.atr[-1]
            if self.data.Low[-1] <= stop_price:
                self.position.close()
                print(f"✨🚀 EXIT LONG @ {self.data.Close[-1]:.2f} | Cosmic Profits Captured!")

        elif self.position.is_short:
            self.trailing_low = min(self.trailing_low, self.data.Low[-1])
            stop_price = self.trailing_low + 3 * self.atr[-1]
            if self.data.High[-1] >= stop_price:
                self.position.close()
                print(f"✨📉 EXIT SHORT @ {self.data.Close[-1]:.2f} | Stellar Losses Avoided!")


data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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

bt = Backtest(data, DynamicBreakoutX, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
