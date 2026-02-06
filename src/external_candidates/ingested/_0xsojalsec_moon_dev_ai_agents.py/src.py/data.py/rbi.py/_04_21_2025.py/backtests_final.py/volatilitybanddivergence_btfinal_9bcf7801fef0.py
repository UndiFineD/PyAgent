# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\VolatilityBandDivergence_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
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


class VolatilityBandDivergence(Strategy):
    risk_per_trade = 0.01

    def init(self):
        # Bollinger Bands
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name=["UpperBB", "MiddleBB", "LowerBB"],
        )

        # VWAP Calculation
        def calculate_vwap(h, l, c, v):
            tp = (h + l + c) / 3
            cum_tpv = (tp * v).cumsum()
            cum_vol = v.cumsum()
            return cum_tpv / cum_vol

        self.vwap = self.I(
            calculate_vwap,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            name="VWAP",
        )

        # VWAP StdDev
        self.vwap_std = self.I(talib.STDDEV, self.vwap, timeperiod=20, name="VWAP_STD")

        # BB Width
        self.bb_width = self.I(
            lambda u, l: u - l, self.upper, self.lower, name="BB_WIDTH"
        )
        self.bb_width_ma = self.I(
            talib.SMA, self.bb_width, timeperiod=20, name="BB_WIDTH_MA"
        )

        # ATR for sizing
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )

    def next(self):
        price = self.data.Close[-1]
        vwap_val = self.vwap[-1]
        std_val = self.vwap_std[-1]

        if not self.position:
            # Long entry logic
            if (
                self.bb_width[-1] > self.bb_width_ma[-1]
                and price < vwap_val - 2 * std_val
            ):
                sl = vwap_val - 3 * std_val
                risk_amount = self.risk_per_trade * self.equity
                size = int(round(risk_amount / abs(price - sl)))
                if size > 0:
                    self.buy(size=size, sl=sl)
                    print(
                        f"🌙🚀 LONG ENTRY @ {price:.2f} | Size: {size} | SL: {sl:.2f}"
                    )

            # Short entry logic
            elif (
                self.bb_width[-1] > self.bb_width_ma[-1]
                and price > vwap_val + 2 * std_val
            ):
                sl = vwap_val + 3 * std_val
                risk_amount = self.risk_per_trade * self.equity
                size = int(round(risk_amount / abs(sl - price)))
                if size > 0:
                    self.sell(size=size, sl=sl)
                    print(
                        f"🌙🚀 SHORT ENTRY @ {price:.2f} | Size: {size} | SL: {sl:.2f}"
                    )
        else:
            # Exit conditions
            if self.position.is_long:
                if (
                    self.bb_width[-1] < self.bb_width_ma[-1]
                    or price >= vwap_val - std_val
                ):
                    self.position.close()
                    print(
                        f"🌙✨ LONG EXIT @ {price:.2f} | Profit: {self.position.pl:.2f}"
                    )

            elif self.position.is_short:
                if (
                    self.bb_width[-1] < self.bb_width_ma[-1]
                    or price <= vwap_val + std_val
                ):
                    self.position.close()
                    print(
                        f"🌙✨ SHORT EXIT @ {price:.2f} | Profit: {self.position.pl:.2f}"
                    )
