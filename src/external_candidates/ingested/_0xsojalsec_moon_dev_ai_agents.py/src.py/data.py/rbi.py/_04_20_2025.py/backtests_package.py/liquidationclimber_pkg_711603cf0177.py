# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\LiquidationClimber_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class LiquidationClimber(Strategy):
    risk_per_trade = 0.01
    max_drawdown = 0.15
    max_positions = 3

    def init(self):
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.atr_sma = self.I(talib.SMA, self.atr, timeperiod=30)
        self.liq = self.data.df["liquidation"]
        self.liq_mean = self.I(talib.SMA, self.liq, timeperiod=30)
        self.liq_std = self.I(talib.STDDEV, self.liq, timeperiod=30)

    def next(self):
        if self.equity < self._broker.initial_cash * (1 - self.max_drawdown):
            print("🌧️ Moon Dev Alert: Max drawdown limit reached! Ceasing trading.")
            return

        current_atr = self.atr[-1]
        atr_sma = self.atr_sma[-1]
        liq = self.liq[-1]
        liq_mean = self.liq_mean[-1]
        liq_std = self.liq_std[-1]

        # Emergency exit condition
        if self.position and liq < (liq_mean - liq_std):
            print(f"🚨 Moon Dev Emergency Exit: Liquidation dropped below 1σ!")
            self.position.close()

        # Exit conditions
        if self.position:
            if self.atr[-2] < self.atr_sma[-2] and self.atr[-1] > self.atr_sma[-1]:
                print(f"🌪️ Moon Dev Exit: Volatility expansion detected!")
                self.position.close()
                return
            if (
                self.data.Close[-1] >= self.take_profit
                or self.data.Close[-1] <= self.stop_loss
            ):
                self.position.close()

        # Entry conditions
        if len(self.trades) < self.max_positions and not self.position:
            if current_atr < atr_sma and liq > (liq_mean + 2 * liq_std):
                if self.data.Close[-1] > self.data.Close[-2]:
                    risk_amount = self.equity * self.risk_per_trade
                    sl = self.data.Close[-1] - current_atr
                    position_size = int(round(risk_amount / (current_atr)))
                    self.buy(size=position_size)
                    self.stop_loss = sl
                    self.take_profit = self.data.Close[-1] + 2 * current_atr
                    print(
                        f"🚀 Moon Dev Long Entry: {position_size} shares @ {self.data.Close[-1]}"
                    )
                elif self.data.Close[-1] < self.data.Close[-2]:
                    risk_amount = self.equity * self.risk_per_trade
                    sl = self.data.Close[-1] + current_atr
                    position_size = int(round(risk_amount / (current_atr)))
                    self.sell(size=position_size)
                    self.stop_loss = sl
                    self.take_profit = self.data.Close[-1] - 2 * current_atr
                    print(
                        f"🌒 Moon Dev Short Entry: {position_size} shares @ {self.data.Close[-1]}"
                    )


bt = Backtest(data, LiquidationClimber, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
