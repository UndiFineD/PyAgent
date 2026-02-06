# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\VolConvergeBreakout_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data handling
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


class VolConvergeBreakout(Strategy):
    def init(self):
        # Bollinger Bands
        self.bb_upper = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BB_upper",
            output=0,
        )
        self.bb_middle = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BB_middle",
            output=1,
        )
        self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BB_lower",
            output=2,
        )

        # Keltner Channel components
        self.ema = self.I(talib.EMA, self.data.Close, 20, name="EMA_20")
        self.atr_kc = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            20,
            name="ATR_KC_20",
        )

        # OBV
        self.obv = self.I(talib.OBV, self.data.Close, self.data.Volume, name="OBV")

        # ATR for volatility
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 20, name="ATR_20"
        )

        # Volatility percentile storage
        self.atr_percentile = []
        self.kc_bandwidth = []

    def next(self):
        if len(self.data) < 50:
            return

        i = len(self.data) - 1

        # Volatility percentile calculation
        current_atr = self.atr[i]
        if i >= 50:
            recent_atr = self.atr[i - 49 : i + 1]
            percentile = (sum(recent_atr <= current_atr) / 50) * 100
            self.atr_percentile.append(percentile)
        else:
            self.atr_percentile.append(0)

        # Bollinger Band conditions
        bb_width = (self.bb_upper[i] - self.bb_lower[i]) / self.bb_middle[i]
        bb_width_sma = talib.SMA(bb_width, timeperiod=20)[-1] if i >= 20 else 0
        bb_cond = bb_width < bb_width_sma if bb_width_sma else False

        # Keltner Channel calculations
        kc_upper = self.ema[i] + 1.5 * self.atr_kc[i]
        kc_lower = self.ema[i] - 1.5 * self.atr_kc[i]
        current_kc_bandwidth = kc_upper - kc_lower
        self.kc_bandwidth.append(current_kc_bandwidth)
        kc_squeeze = (
            current_kc_bandwidth < talib.SMA(self.kc_bandwidth, timeperiod=20)[-1]
            if len(self.kc_bandwidth) >= 20
            else False
        )

        # OBV divergence check
        bullish_div = False
        if i >= 5:
            price_lows = self.data.Low[i - 4 : i + 1]
            obv_lows = self.obv[i - 4 : i + 1]
            if self.data.Low[i] == min(price_lows) and self.obv[i] == max(obv_lows):
                bullish_div = True

        # Long entry conditions
        if (
            self.atr_percentile[-1] <= 30
            and bb_cond
            and kc_squeeze
            and bullish_div
            and (self.data.Close[i] > self.bb_upper[i] or self.data.Close[i] > kc_upper)
        ):
            self.buy()
