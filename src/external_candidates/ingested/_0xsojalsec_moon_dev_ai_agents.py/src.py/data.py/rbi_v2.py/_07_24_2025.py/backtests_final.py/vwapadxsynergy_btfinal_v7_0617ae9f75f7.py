# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\VwapAdxSynergy_BTFinal_v7.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VwapAdxSynergy(Strategy):
    risk_per_trade = 0.01
    adx_period = 14
    tp_multiplier = 2
    sl_multiplier = 1

    def init(self):
        # Clean and prepare data
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # Calculate indicators
        self.vwap = self.I(
            lambda x: talib.SMA(x, timeperiod=len(x)), close * volume
        ) / self.I(lambda x: talib.SMA(x, timeperiod=len(x)), volume)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.plus_di = self.I(
            talib.PLUS_DI, high, low, close, timeperiod=self.adx_period
        )
        self.minus_di = self.I(
            talib.MINUS_DI, high, low, close, timeperiod=self.adx_period
        )

    def next(self):
        price = self.data.Close[-1]
        vwap = self.vwap[-1]
        adx = self.adx[-1]
        plus_di = self.plus_di[-1]
        minus_di = self.minus_di[-1]

        # Moon Dev debug prints 🌙
        print(
            f"🌙 Moon Dev Debug | Price: {price:.2f} | VWAP: {vwap:.2f} | ADX: {adx:.2f} | +DI: {plus_di:.2f} | -DI: {minus_di:.2f}"
        )

        if not self.position:
            # Long entry conditions
            if (
                price > vwap
                and adx > 25
                and plus_di > minus_di
                and self.data.Close[-2] <= self.vwap[-2]
                and self.data.Close[-1] > vwap
            ):

                sl = min(self.data.Low[-3:])  # Swing low stop
                risk_amount = self.equity * self.risk_per_trade
                risk_per_share = price - sl
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    print(
                        f"🚀 Moon Dev LONG Signal | Entry: {price:.2f} | SL: {sl:.2f} | Size: {position_size}"
                    )
                    self.buy(
                        size=position_size,
                        sl=sl,
                        tp=price + (price - sl) * self.tp_multiplier,
                    )

            # Short entry conditions
            elif (
                price < vwap
                and adx > 25
                and minus_di > plus_di
                and self.data.Close[-2] >= self.vwap[-2]
                and self.data.Close[-1] < vwap
            ):

                sl = max(self.data.High[-3:])  # Swing high stop
                risk_amount = self.equity * self.risk_per_trade
                risk_per_share = sl - price
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    print(
                        f"🌑 Moon Dev SHORT Signal | Entry: {price:.2f} | SL: {sl:.2f} | Size: {position_size}"
                    )
                    self.sell(
                        size=position_size,
                        sl=sl,
                        tp=price - (sl - price) * self.tp_multiplier,
                    )

        else:
            # Exit conditions for long
            if self.position.is_long and (
                adx < 25
                or (self.minus_di[-1] < self.plus_di[-1] and minus_di > plus_di)
            ):
                print(f"✨ Moon Dev Closing LONG | ADX weakening or -DI crossing +DI")
                self.position.close()

            # Exit conditions for short
            elif self.position.is_short and (
                adx < 25
                or (self.plus_di[-1] < self.minus_di[-1] and plus_di > minus_di)
            ):
                print(f"✨ Moon Dev Closing SHORT | ADX weakening or +DI crossing -DI")
                self.position.close()


# Data preparation
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
data["Datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("Datetime")

# Run backtest
bt = Backtest(data, VwapAdxSynergy, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
