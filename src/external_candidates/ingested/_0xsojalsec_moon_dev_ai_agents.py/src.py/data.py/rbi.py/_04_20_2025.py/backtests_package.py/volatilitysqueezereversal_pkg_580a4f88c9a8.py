# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\VolatilitySqueezeReversal_PKG.py
import numpy as np
import pandas as pd
import pandas_ta
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class VolatilitySqueezeReversal(Strategy):
    def init(self):
        # Bollinger Bands
        def upper_bb(close):
            upper, _, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return upper

        self.upper_band = self.I(upper_bb, self.data.Close)

        def lower_bb(close):
            _, _, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return lower

        self.lower_band = self.I(lower_bb, self.data.Close)

        # BB Width
        def bb_width(close):
            upper, middle, lower = talib.BBANDS(
                close, timeperiod=20, nbdevup=2, nbdevdn=2
            )
            return (upper - lower) / middle

        self.bb_width = self.I(bb_width, self.data.Close)

        # Hurst Exponent
        def hurst(close):
            return pandas_ta.hurst(close, length=100)

        self.hurst = self.I(hurst, self.data.Close)

        # ATR
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        self.trailing_stop = None
        self.highest_price = None

    def next(self):
        if len(self.data) < 100:
            return

        if not self.position:
            # Entry conditions
            current_width = self.bb_width[-1]
            historical_width = self.bb_width[: len(self.data) - 1]
            if len(historical_width) == 0:
                return
            perc_20 = np.percentile(historical_width, 20)
            bb_squeeze = current_width < perc_20

            funding = self.data.df["funding_rate"].iloc[-1]
            mean_funding = np.mean(self.data.df["funding_rate"].iloc[: len(self.data)])
            std_funding = np.std(self.data.df["funding_rate"].iloc[: len(self.data)])
            funding_ok = funding < -0.001 and funding < (mean_funding - 2 * std_funding)

            price_break = self.data.Close[-1] > self.upper_band[-1]

            if bb_squeeze and funding_ok and price_break:
                atr = self.atr[-1]
                stop_loss = self.data.Close[-1] - 1.5 * atr
                risk_amount = 0.01 * self.equity
                size = risk_amount / (self.data.Close[-1] - stop_loss)
                size = int(round(size))
                if size > 0:
                    self.buy(size=size)
                    print(
                        f"🌙🚀 MOON ENTRY: Long {size} units at {self.data.Close[-1]} ✨"
                    )
                    self.trailing_stop = stop_loss
                    self.highest_price = self.data.Close[-1]
        else:
            # Update trailing stop
            self.highest_price = max(self.highest_price, self.data.High[-1])
            self.trailing_stop = self.highest_price - 1.5 * self.atr[-1]

            # Hurst exit
            current_hurst = self.hurst[-1]
            hurst_window = self.hurst[-100:]
            min_h = np.min(hurst_window)
            max_h = np.max(hurst_window)
            norm_hurst = (
                (current_hurst - min_h) / (max_h - min_h) if max_h != min_h else 0
            )
            if norm_hurst > 0.7:
                self.position.close()
                print(
                    f"🌙🎯 HURST EXIT: Norm Hurst {norm_hurst:.2f} at {self.data.Close[-1]} ✨"
                )
