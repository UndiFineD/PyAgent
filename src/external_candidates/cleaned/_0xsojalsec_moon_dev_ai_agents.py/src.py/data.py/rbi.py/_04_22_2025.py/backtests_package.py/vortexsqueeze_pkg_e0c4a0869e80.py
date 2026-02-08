# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\VortexSqueeze_PKG.py
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class VortexSqueeze(Strategy):
    def init(self):
        # Calculate Vortex Indicator
        def calculate_vortex(high, low, close):
            vi = ta.vortex(high=high, low=low, close=close, length=14)
            return vi["VORTICPD_14"], vi["VORTICPM_14"]

        self.vi_plus, self.vi_minus = self.I(calculate_vortex, self.data.High, self.data.Low, self.data.Close)

        # 200-period SMA
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

        # Bollinger Band Width
        def calculate_bb_width(close):
            upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return (upper - lower) / middle

        self.bb_width = self.I(calculate_bb_width, self.data.Close)

        # BBW Percentile (1-year lookback)
        def calculate_percentile(bbw):
            return bbw.rolling(35040).apply(lambda x: (x < x[-1]).mean() * 100)

        self.bbw_percentile = self.I(calculate_percentile, self.bb_width)

    def next(self):
        if len(self.data) < 35040 or np.isnan(self.bbw_percentile[-1]):
            return

        # Long entry conditions
        if not self.position:
            if (
                self.data.Close[-1] > self.sma200[-1]
                and (self.vi_plus[-2] < self.vi_minus[-2] and self.vi_plus[-1] > self.vi_minus[-1])
                and self.bbw_percentile[-1] < 20
            ):
                # Risk management
                risk_pct = 0.01
                stop_pct = 0.02
                risk_amount = self.equity * risk_pct
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * (1 - stop_pct)
                risk_per_unit = entry_price - stop_loss

                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss)
                        print(f"🌙 MOON DEV LONG ENTRY 🌙 Size: {position_size} @ {entry_price:.2f} ✨")

        # Exit conditions
        elif self.position.is_long and (self.vi_minus[-2] < self.vi_plus[-2] and self.vi_minus[-1] > self.vi_plus[-1]):
            self.position.close()
            print(f"🚨 VORTEX REVERSAL EXIT 🚨 @ {self.data.Close[-1]:.2f}")


# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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
data["DateTime"] = pd.to_datetime(data["datetime"])
data = data.set_index("DateTime")[["Open", "High", "Low", "Close", "Volume"]]

# Execute backtest
bt = Backtest(data, VortexSqueeze, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
