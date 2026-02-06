# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_package\BandwidthSurge_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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


class BandwidthSurge(Strategy):
    def init(self):
        # Bollinger Bands components
        self.bb_upper = self.I(
            lambda c: talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2)[0],
            self.data.Close,
        )
        self.bb_lower = self.I(
            lambda c: talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2)[2],
            self.data.Close,
        )
        self.bb_mid = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.bb_width = self.I(
            lambda u, l, m: (u - l) / m, self.bb_upper, self.bb_lower, self.bb_mid
        )
        self.bb_low = self.I(talib.MIN, self.bb_width, timeperiod=17280)

        # Volume and ATR indicators
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=1920)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

    def next(self):
        if not self.position:
            if (
                self.bb_width[-1] <= self.bb_low[-1]
                and self.data.Volume[-1] > self.vol_sma[-1]
            ):
                atr = self.atr[-1]
                risk_amount = self.equity * 0.01
                position_size = int(round(risk_amount / atr))

                if position_size > 0:
                    if self.data.Close[-1] > self.bb_upper[-1]:
                        self.buy(
                            size=position_size,
                            sl=self.data.Close[-1] - atr,
                            tp=self.data.Close[-1] + 1.5 * atr,
                        )
                        print(
                            f"🚀 Moon Dev LONG: {self.data.Close[-1]:.2f} | Size: {position_size} | ATR: {atr:.2f} 🌙"
                        )

                    elif self.data.Close[-1] < self.bb_lower[-1]:
                        self.sell(
                            size=position_size,
                            sl=self.data.Close[-1] + atr,
                            tp=self.data.Close[-1] - 1.5 * atr,
                        )
                        print(
                            f"🌑 Moon Dev SHORT: {self.data.Close[-1]:.2f} | Size: {position_size} | ATR: {atr:.2f} 🌘"
                        )

        else:
            if self.position.is_long:
                if (
                    self.data.Close[-1] < self.data.Open[-1]
                    and self.data.Close[-2] < self.data.Open[-2]
                ):
                    self.position.close()
                    print("🌧️🌧️ Moon Dev EXIT LONG: Double Bearish Close 🌧️🌧️")

            elif self.position.is_short:
                if (
                    self.data.Close[-1] > self.data.Open[-1]
                    and self.data.Close[-2] > self.data.Open[-2]
                ):
                    self.position.close()
                    print("🌞🌞 Moon Dev EXIT SHORT: Double Bullish Close 🌞🌞")


bt = Backtest(data, BandwidthSurge, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
