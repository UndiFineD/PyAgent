# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests\DonchianADXSurge_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class DonchianADXSurge(Strategy):
    risk_per_trade = 0.01
    adx_threshold = 25
    donchian_period = 20
    adx_period = 5

    def init(self):
        self.donchian_high = self.I(
            talib.MAX, self.data.High, timeperiod=self.donchian_period
        )
        self.donchian_low = self.I(
            talib.MIN, self.data.Low, timeperiod=self.donchian_period
        )
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, self.adx_period
        )

    def next(self):
        if len(self.data) < self.donchian_period + 1:
            return

        current_idx = len(self.data) - 1
        prev_idx = current_idx - 1

        if not self.position:
            prev_close = self.data.Close[-2]
            prev_donchian_high = self.donchian_high[-2]
            prev_donchian_low = self.donchian_low[-2]
            prev_adx = self.adx[-2]

            if prev_close > prev_donchian_high and prev_adx > self.adx_threshold:
                entry_price = self.data.Open[-1]
                stop_loss = self.data.Low[-2]
                risk_distance = entry_price - stop_loss

                if risk_distance <= 0:
                    return

                risk_amount = self.equity * self.risk_per_trade
                position_size = int(round(risk_amount / risk_distance))
                take_profit = entry_price + 2 * risk_distance

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                    print(
                        f"🌙 MOON DEV LONG SIGNAL 🚀 | Entry: {entry_price:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Equity: {self.equity:.2f} ✨"
                    )

            elif prev_close < prev_donchian_low and prev_adx > self.adx_threshold:
                entry_price = self.data.Open[-1]
                stop_loss = self.data.High[-2]
                risk_distance = stop_loss - entry_price

                if risk_distance <= 0:
                    return

                risk_amount = self.equity * self.risk_per_trade
                position_size = int(round(risk_amount / risk_distance))
                take_profit = entry_price - 2 * risk_distance

                if position_size > 0:
                    self.sell(size=position_size, sl=stop_loss, tp=take_profit)
                    print(
                        f"🌙 MOON DEV SHORT SIGNAL 🌪 | Entry: {entry_price:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Equity: {self.equity:.2f} ✨"
                    )


bt = Backtest(data, DonchianADXSurge, cash=1_000_000, margin=1.0)
stats = bt.run()
print(stats)
print(stats._strategy)
