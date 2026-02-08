# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests\VolumetricBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data handling
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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


class VolumetricBreakout(Strategy):
    def init(self):
        self.donchian_upper = self.I(talib.MAX, self.data.High, 20)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, 20)

        def MACD_hist(close, fast, slow, signal):
            macd, _, hist = talib.MACD(close, fast, slow, signal)
            return hist

        self.macd_hist = self.I(MACD_hist, self.data.Close, 12, 26, 9)

        self.volume_sma = self.I(talib.SMA, self.data.Volume, 10)

    def next(self):
        if not self.position:
            if (
                self.data.Close[-1] > self.donchian_upper[-1]
                and self.macd_hist[-1] > 0
                and self.data.Volume[-1] >= 1.5 * self.volume_sma[-1]
            ):
                risk_amount = self.equity * 0.01
                entry_price = self.data.Close[-1]
                sl_price = self.donchian_lower[-1]
                risk_per_share = entry_price - sl_price

                if risk_per_share <= 0:
                    print("🌑 Invalid risk calculation. Moon aborting entry!")
                    return

                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    print(f"🚀🌙 MOON ENTRY! Price: {entry_price}, Size: {position_size}, Cosmic SL: {sl_price}")

        else:
            current_close = self.data.Close[-1]
            exit_conditions = [
                (current_close < self.donchian_lower[-1], "🌑 Below Donchian Lower"),
                (self.macd_hist[-1] < 0, "✨ MACD Hist Negative"),
            ]

            for condition, reason in exit_conditions:
                if condition:
                    self.position.close()
                    print(f"🌙🌠 {reason} at {current_close}. Returning to lunar base!")


bt = Backtest(data, VolumetricBreakout, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
