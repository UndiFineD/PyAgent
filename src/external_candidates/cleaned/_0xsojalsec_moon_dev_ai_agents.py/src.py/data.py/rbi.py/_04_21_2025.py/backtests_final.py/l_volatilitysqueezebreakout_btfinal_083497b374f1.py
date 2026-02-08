# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\L-VolatilitySqueezeBreakout_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolatilitySqueezeBreakout(Strategy):
    def init(self):
        # Calculate indicators
        self.middle_band = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.std_dev = self.I(talib.STDDEV, self.data.Close, timeperiod=20)
        self.upper_band = self.I(lambda: self.middle_band + 2 * self.std_dev)
        self.lower_band = self.I(lambda: self.middle_band - 2 * self.std_dev)
        self.bb_width = self.I(lambda: (self.upper_band - self.lower_band) / self.middle_band)
        self.bb_width_ma = self.I(talib.SMA, self.bb_width, timeperiod=10)
        self.volume_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        print("🌙 MOON STRATEGY INITIALIZED! Indicators ready for launch 🚀")

    def next(self):
        if len(self.data) < 20:
            return

        entry_conditions = {}

        # Long entry conditions
        entry_conditions["long"] = (
            self.bb_width[-1] < self.bb_width_ma[-1]
            and self.data.Volume[-1] > 1.5 * self.volume_ma[-1]
            and self.data.Close[-1] > self.upper_band[-1]
        )

        # Short entry conditions
        entry_conditions["short"] = (
            self.bb_width[-1] < self.bb_width_ma[-1]
            and self.data.Volume[-1] > 1.5 * self.volume_ma[-1]
            and self.data.Close[-1] < self.lower_band[-1]
        )

        # Risk management calculations
        atr_value = self.atr[-1]
        risk_percent = 0.01
        risk_amount = self.equity * risk_percent

        # Execute trades
        if not self.position:
            if entry_conditions["long"]:
                position_size = int(round(risk_amount / atr_value))
                if position_size > 0:
                    sl = self.data.Close[-1] - atr_value
                    tp = self.data.Close[-1] + 2 * atr_value
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙 LONG LAUNCH! 🚀 Price: {self.data.Close[-1]:.2f} | Size: {position_size} | SL: {sl:.2f} | TP: {tp:.2f}"
                    )

            elif entry_conditions["short"]:
                position_size = int(round(risk_amount / atr_value))
                if position_size > 0:
                    sl = self.data.Close[-1] + atr_value
                    tp = self.data.Close[-1] - 2 * atr_value
                    self.sell(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙 SHORT IGNITION! 🌠 Price: {self.data.Close[-1]:.2f} | Size: {position_size} | SL: {sl:.2f} | TP: {tp:.2f}"
                    )

        # Time-based exit
        if self.position and self.position.duration >= 5:
            self.position.close()
            print(
                f"🌙 TIME PORTAL CLOSING! ⏳ Bar duration: {self.position.duration} | Price: {self.data.Close[-1]:.2f}"
            )


# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)
data = data[["open", "high", "low", "close", "volume"]]
data.columns = ["Open", "High", "Low", "Close", "Volume"]
