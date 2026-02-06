# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\BandedStochastic_BTFinal_v1.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandedStochastic(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    bb_period = 20
    bb_dev = 2
    stoch_k = 14
    stoch_d = 3
    stoch_smooth = 3

    def init(self):
        # Clean and prepare data
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # Calculate indicators
        upper_band, middle_band, lower_band = talib.BBANDS(
            close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_dev,
            nbdevdn=self.bb_dev,
            matype=0,
        )

        self.upper_band = self.I(lambda x: x, upper_band, name="Upper Band")
        self.lower_band = self.I(lambda x: x, lower_band, name="Lower Band")

        slowk, slowd = talib.STOCH(
            high,
            low,
            close,
            fastk_period=self.stoch_k,
            slowk_period=self.stoch_smooth,
            slowk_matype=0,
            slowd_period=self.stoch_d,
            slowd_matype=0,
        )

        self.slowk = self.I(lambda x: x, slowk, name="Stoch K")
        self.slowd = self.I(lambda x: x, slowd, name="Stoch D")

        self.avg_volume = self.I(talib.SMA, volume, timeperiod=20, name="Avg Volume")

    def next(self):
        price = self.data.Close[-1]
        upper = self.upper_band[-1]
        lower = self.lower_band[-1]
        slowk = self.slowk[-1]
        slowd = self.slowd[-1]
        volume = self.data.Volume[-1]
        avg_volume = self.avg_volume[-1]

        # Moon Dev themed debug prints 🌙
        if not self.position:
            if (
                price > upper
                and (
                    self.slowk[-2] < self.slowd[-2] and self.slowk[-1] > self.slowd[-1]
                )
                and slowk < 20
                and slowd < 20
                and volume > avg_volume
            ):

                # Calculate position size with 1% risk
                stop_loss = min(self.data.Low[-5:])  # Recent swing low
                risk_amount = self.equity * self.risk_per_trade
                risk_per_unit = price - stop_loss
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    print(
                        f"🌙 MOON DEV LONG SIGNAL! ✨ Price: {price:.2f}, Upper Band: {upper:.2f}, Stoch K: {slowk:.2f}, Stoch D: {slowd:.2f}"
                    )
                    self.buy(size=position_size, sl=stop_loss, tp=self.lower_band[-1])

            elif (
                price < lower
                and (
                    self.slowd[-2] < self.slowk[-2] and self.slowd[-1] > self.slowk[-1]
                )
                and slowk > 80
                and slowd > 80
                and volume > avg_volume
            ):

                # Calculate position size with 1% risk
                stop_loss = max(self.data.High[-5:])  # Recent swing high
                risk_amount = self.equity * self.risk_per_trade
                risk_per_unit = stop_loss - price
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    print(
                        f"🌙 MOON DEV SHORT SIGNAL! ✨ Price: {price:.2f}, Lower Band: {lower:.2f}, Stoch K: {slowk:.2f}, Stoch D: {slowd:.2f}"
                    )
                    self.sell(size=position_size, sl=stop_loss, tp=self.upper_band[-1])

        # Check for exit conditions
        if self.position:
            if self.position.is_long:
                if slowk > 90 or price <= self.lower_band[-1]:
                    print(
                        f"🌙 MOON DEV EXIT LONG! 🚀 Price: {price:.2f}, Stoch K: {slowk:.2f}"
                    )
                    self.position.close()
            else:
                if slowk < 10 or price >= self.upper_band[-1]:
                    print(
                        f"🌙 MOON DEV EXIT SHORT! 🚀 Price: {price:.2f}, Stoch K: {slowk:.2f}"
                    )
                    self.position.close()


# Load and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(
    columns=[col for col in data.columns if "unnamed" in col.lower()], errors="ignore"
)
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
data = data.dropna()

# Run backtest
bt = Backtest(data, BandedStochastic, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
