# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\VortexFisherDivergence_PKG.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
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
        "datetime": "DateTime",
    },
    inplace=True,
)
data["DateTime"] = pd.to_datetime(data["DateTime"])
data.set_index("DateTime", inplace=True)


def compute_fisher(high, low, length=9):
    fisher_df = ta.fisher(high=pd.Series(high), low=pd.Series(low), length=length)
    return fisher_df.iloc[:, 0].values


class VortexFisherDivergence(Strategy):
    def init(self):
        self.vi_plus, self.vi_minus = self.I(
            talib.VORTEX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            14,
            name=["VI+", "VI-"],
        )
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.fisher = self.I(compute_fisher, self.data.High, self.data.Low, 9)
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        if not self.position:
            vol_cond = self.data.Volume[-1] > self.volume_sma[-1]
            adx_cond = self.adx[-1] > 20

            # Bullish entry
            if (
                (self.fisher[-1] > 0 and self.fisher[-2] <= 0)
                and (self.vi_minus[-1] > self.vi_plus[-1])
                and vol_cond
                and adx_cond
            ):
                sl = self.swing_low[-1]
                risk = self.equity * 0.01
                size = int(round(risk / (self.data.Open[-1] - sl))) if self.data.Open[-1] > sl else 0
                if size > 0:
                    self.buy(size=size, sl=sl)
                    print(f"🚀 Moon Dev LONG: {self.data.Close[-1]} | Size: {size} | SL: {sl}")

            # Bearish entry
            elif (
                (self.fisher[-1] < 0 and self.fisher[-2] >= 0)
                and (self.vi_plus[-1] > self.vi_minus[-1])
                and vol_cond
                and adx_cond
            ):
                sl = self.swing_high[-1]
                risk = self.equity * 0.01
                size = int(round(risk / (sl - self.data.Open[-1]))) if sl > self.data.Open[-1] else 0
                if size > 0:
                    self.sell(size=size, sl=sl)
                    print(f"🌑 Moon Dev SHORT: {self.data.Close[-1]} | Size: {size} | SL: {sl}")
        else:
            current_adx = self.adx[-1]
            prev_adx = self.adx[-2] if len(self.adx) > 1 else current_adx

            if self.position.is_long:
                if current_adx < 25 or current_adx < prev_adx or (self.fisher[-1] < 0 and self.fisher[-2] >= 0):
                    self.position.close()
                    print(f"🌙 Moon Dev EXIT LONG: {self.data.Close[-1]}")
            elif self.position.is_short:
                if current_adx < 25 or current_adx < prev_adx or (self.fisher[-1] > 0 and self.fisher[-2] <= 0):
                    self.position.close()
                    print(f"🌙 Moon Dev EXIT SHORT: {self.data.Close[-1]}")


bt = Backtest(data, VortexFisherDivergence, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
