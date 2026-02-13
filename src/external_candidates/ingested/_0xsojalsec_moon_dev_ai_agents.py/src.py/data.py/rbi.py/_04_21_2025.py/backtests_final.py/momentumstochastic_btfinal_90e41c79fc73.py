# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\MomentumStochastic_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class MomentumStochastic(Strategy):
    def init(self):
        h, l, c = self.data.High, self.data.Low, self.data.Close

        # Calculate indicators
        self.adx = self.I(talib.ADX, h, l, c, timeperiod=14)
        self.atr = self.I(talib.ATR, h, l, c, timeperiod=14)
        stoch_k, stoch_d = talib.STOCH(
            h,
            l,
            c,
            fastk_period=14,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )
        self.stoch_k = self.I(lambda: stoch_k, name="%K")
        self.stoch_d = self.I(lambda: stoch_d, name="%D")

        self.trail_high = None
        self.trail_low = None

    def next(self):
        if len(self.data) < 14:
            return

        adx_val = self.adx[-1]
        atr_val = self.atr[-1]
        k, d = self.stoch_k[-1], self.stoch_d[-1]
        prev_k, prev_d = self.stoch_k[-2], self.stoch_d[-2]

        # Entry logic
        if not self.position:
            risk = self.equity * 0.01
            if k > d and prev_k <= prev_d and adx_val > 25:
                size = int(round(risk / atr_val))
                if size > 0:
                    self.buy(size=size)
                    self.trail_high = self.data.High[-1]
                    print(
                        f"🌙🚀 LONG! | Price: {self.data.Close[-1]:.2f} | Size: {size} | ATR: {atr_val:.2f}"
                    )

            elif k < d and prev_k >= prev_d and adx_val > 25:
                size = int(round(risk / atr_val))
                if size > 0:
                    self.sell(size=size)
                    self.trail_low = self.data.Low[-1]
                    print(
                        f"🌙🚀 SHORT! | Price: {self.data.Close[-1]:.2f} | Size: {size} | ATR: {atr_val:.2f}"
                    )

        # Trailing stop logic
        if self.position.is_long:
            self.trail_high = max(self.trail_high, self.data.High[-1])
            stop = self.trail_high - 2 * atr_val
            if self.data.Low[-1] <= stop:
                self.position.close()
                print(
                    f"🚨🌙 EXIT LONG | Price: {self.data.Close[-1]:.2f} | Profit: {self.position.pl:.2f}"
                )

        elif self.position.is_short:
            self.trail_low = min(self.trail_low, self.data.Low[-1])
            stop = self.trail_low + 2 * atr_val
            if self.data.High[-1] >= stop:
                self.position.close()
                print(
                    f"🚨🌙 EXIT SHORT | Price: {self.data.Close[-1]:.2f} | Profit: {self.position.pl:.2f}"
                )

        # ADX exit
        if self.position and adx_val < 20:
            self.position.close()
            print(f"🌙📉 ADX EXIT | Current ADX: {adx_val:.2f}")


bt = Backtest(data, MomentumStochastic, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
