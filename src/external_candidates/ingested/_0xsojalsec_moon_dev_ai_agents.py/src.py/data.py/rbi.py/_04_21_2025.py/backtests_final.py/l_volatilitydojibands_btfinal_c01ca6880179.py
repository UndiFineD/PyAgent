# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\L-VolatilityDojiBands_BTFinal.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data[["open", "high", "low", "close", "volume"]]
data.columns = ["Open", "High", "Low", "Close", "Volume"]


class VolatilityDojiBands(Strategy):
    def init(self):
        # Heikin-Ashi calculation
        ha_close = (
            self.data.Open + self.data.High + self.data.Low + self.data.Close
        ) / 4
        ha_open = np.zeros_like(ha_close)
        ha_open[0] = (self.data.Open[0] + self.data.Close[0]) / 2
        for i in range(1, len(ha_open)):
            ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2
        ha_high = np.maximum.reduce([self.data.High, ha_open, ha_close])
        ha_low = np.minimum.reduce([self.data.Low, ha_open, ha_close])

        self.ha_close_ind = self.I(lambda: ha_close, name="HA_Close")
        self.ha_open_ind = self.I(lambda: ha_open, name="HA_Open")

        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            name=["BB_Upper", "BB_Middle", "BB_Lower"],
        )
        bb_width = (self.bb_upper - self.bb_lower) / self.bb_middle
        self.bb_width_ind = self.I(lambda: bb_width, name="BB_Width")

        # BB Width Percentile
        bb_percentile = []
        for i in range(len(self.data)):
            window = bb_width[max(0, i - 100) : i + 1]
            bb_percentile.append((bb_width[i] <= window).mean() * 100)
        self.bb_percentile_ind = self.I(
            lambda: np.array(bb_percentile), name="BB_Percentile"
        )

        # Keltner Channels
        self.ema20 = self.I(talib.EMA, self.data.Close, timeperiod=20, name="EMA20")
        self.atr20 = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=20,
            name="ATR20",
        )
        self.keltner_upper = self.I(
            lambda: self.ema20 + 1.5 * self.atr20, name="Keltner_Upper"
        )
        self.keltner_lower = self.I(
            lambda: self.ema20 - 1.5 * self.atr20, name="Keltner_Lower"
        )

        # Volume MA
        self.vol_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20, name="Vol_MA")

    def next(self):
        if len(self.data) < 100:
            return

        # Check 3 consecutive dojis
        doji_streak = all(
            [
                abs(self.ha_close_ind[-i] - self.ha_open_ind[-i])
                < 0.1 * (self.data.High[-i] - self.data.Low[-i])
                for i in range(1, 4)
            ]
        )

        # Entry conditions
        if doji_streak and self.bb_percentile_ind[-1] <= 1 and not self.position:
            if self.data.Volume[-1] > 2 * self.vol_ma[-1]:
                risk_amount = self.equity * 0.01
                bb_width = self.bb_upper[-1] - self.bb_lower[-1]
                stop_loss = 1.5 * bb_width
                position_size = int(round(risk_amount / stop_loss))

                if position_size > 0:
                    self.buy(size=position_size)
                    print(
                        f"🌙 MOON DEV LONG ENTRY: {self.data.Close[-1]:.2f} | Size: {position_size} ✨"
                    )
                    self.sl = self.data.Close[-1] - stop_loss
