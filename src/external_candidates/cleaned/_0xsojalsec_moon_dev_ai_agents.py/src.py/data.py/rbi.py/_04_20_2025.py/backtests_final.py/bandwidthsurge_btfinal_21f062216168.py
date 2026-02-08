# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\BandwidthSurge_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation and cleaning
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


class BandwidthSurge(Strategy):
    def init(self):
        # Bollinger Bands indicators
        self.upper = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[0]
        self.middle = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[1]
        self.lower = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[2]

        # Bollinger Bandwidth calculation
        self.bbw = self.I(lambda u, l, m: (u - l) / m, self.upper, self.lower, self.middle)
        self.bbw_low = self.I(talib.MIN, self.bbw, timeperiod=20)

        # Volume indicators
        self.volume_ma50 = self.I(talib.SMA, self.data.Volume, timeperiod=50)

    def next(self):
        if len(self.data) < 50 or not (self.bbw[-1] and self.volume_ma50[-1]):
            return

        # Entry conditions
        if not self.position:
            if self.bbw[-1] <= self.bbw_low[-1] and self.data.Volume[-1] >= 3 * self.volume_ma50[-1]:
                if self.data.Close[-1] > self.upper[-1]:
                    # Long entry with risk management
                    risk_amount = self.equity * 0.01
                    risk_per_share = self.data.Close[-1] - self.middle[-1]
                    if risk_per_share > 0:
                        size = int(round(risk_amount / risk_per_share))
                        self.buy(size=size, sl=self.middle[-1])
                        print(f"🌙 MOON DEV LONG SIGNAL! ✨ Entry: {self.data.Close[-1]:.2f}, Size: {size} 🚀")

                elif self.data.Close[-1] < self.lower[-1]:
                    # Short entry with risk management
                    risk_amount = self.equity * 0.01
                    risk_per_share = self.middle[-1] - self.data.Close[-1]
                    if risk_per_share > 0:
                        size = int(round(risk_amount / risk_per_share))
                        self.sell(size=size, sl=self.middle[-1])
                        print(f"🌙 MOON DEV SHORT SIGNAL! ✨ Entry: {self.data.Close[-1]:.2f}, Size: {size} 🚀")

        # Exit conditions
        if self.position.is_long and self.data.Low[-1] <= self.lower[-1]:
            self.position.close()
            print(f"🌙 MOON DEV LONG EXIT! ✨ Profit: {self.position.pl:.2f} 💰")

        if self.position.is_short and self.data.High[-1] >= self.upper[-1]:
            self.position.close()
            print(f"🌙 MOON DEV SHORT EXIT! ✨ Profit: {self.position.pl:.2f} 💰")


# Backtest execution
bt = Backtest(data, BandwidthSurge, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
