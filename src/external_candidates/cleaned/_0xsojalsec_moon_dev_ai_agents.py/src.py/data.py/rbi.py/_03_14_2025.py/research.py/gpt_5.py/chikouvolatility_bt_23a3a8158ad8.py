# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\ChikouVolatility_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ChikouVolatility(Strategy):
    def init(self):
        self.chikou_span = self.I(talib.SMA, self.data.Close.shift(26), timeperiod=1)
        self.upper_band, self.middle_band, self.lower_band = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

    def next(self):
        price = self.data.Close[-1]
        chikou_span_value = self.chikou_span[-1]
        upper_band_value = self.upper_band[-1]
        lower_band_value = self.lower_band[-1]

        # Bullish Entry
        if (
            chikou_span_value > self.data.Close[-26]
            and price < lower_band_value
            and self.data.Close[-2] < lower_band_value
            and self.data.Close[-1] > lower_band_value
        ):
            sl = lower_band_value
            tp = upper_band_value
            size = 0.02  # Fixed 2% of equity
            print("🌙 🚀 Enter Bullish Position | Size: 2% of equity | SL: {:.2f} | TP: {:.2f} 🌙 🚀".format(sl, tp))
            self.buy(size=size, sl=sl, tp=tp)

        # Bearish Entry
        elif (
            chikou_span_value < self.data.Close[-26]
            and price > upper_band_value
            and self.data.Close[-2] > upper_band_value
            and self.data.Close[-1] < upper_band_value
        ):
            sl = upper_band_value
            tp = lower_band_value
            size = 0.02  # Fixed 2% of equity
            print("🌙 🚀 Enter Bearish Position | Size: 2% of equity | SL: {:.2f} | TP: {:.2f} 🌙 🚀".format(sl, tp))
            self.sell(size=size, sl=sl, tp=tp)


# Load data
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

# Run backtest
bt = Backtest(data, ChikouVolatility, cash=1000000, commission=0.002)
stats = bt.run()
print("🌙 ✨ Backtest Complete! Moon Dev Stats: 🌙 ✨")
print(stats)
