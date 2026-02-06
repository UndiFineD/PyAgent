# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_30_2025\backtests\ChaikinSqueeze_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Data preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"])

# Clean and format columns
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
).set_index("datetime")


class ChaikinSqueeze(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators with TA-Lib
        self.cmf = self.I(
            talib.CMF,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            20,
            name="CMF",
        )
        self.cmf_roc = self.I(talib.ROC, self.cmf, 3, name="CMF_ROC")

        # Bollinger Bands components
        self.bb_upper = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2, 0)[0],
            self.data.Close,
            name="BB_UP",
        )
        self.bb_lower = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2, 0)[2],
            self.data.Close,
            name="BB_LOW",
        )
        self.bb_width = self.I(lambda: self.bb_upper - self.bb_lower, name="BB_WIDTH")
        self.min_width = self.I(talib.MIN, self.bb_width, 20, name="MIN_WIDTH")

        # VWAP and volume indicators
        self.vwap = self.I(
            ta.vwap,
            high=self.data.High,
            low=self.data.Low,
            close=self.data.Close,
            volume=self.data.Volume,
            name="VWAP",
        )
        self.vol_sma = self.I(talib.SMA, self.data.Volume, 10, name="VOL_SMA")

        # Swing high/low for stops
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="SWING_LOW")

    def next(self):
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        if not self.position:
            # Entry conditions
            squeeze = self.bb_width[-1] < self.min_width[-1] * 1.05
            cmf_boost = self.cmf_roc[-1] > 0.05
            vwap_break = (
                current_close > self.vwap[-1] and self.data.Close[-2] <= self.vwap[-2]
            )
            vol_spike = current_volume > self.vol_sma[-1]

            if all([squeeze, cmf_boost, vwap_break, vol_spike]):
                # Risk management calculations
                sl_price = self.swing_low[-1]
                risk_amount = self.equity * self.risk_percent
                risk_per_unit = current_close - sl_price

                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.buy(
                            size=position_size,
                            sl=sl_price,
                            tp=current_close + 2 * risk_per_unit,
                            tag="🌙 BULLISH SQUEEZE BREAKOUT",
                        )
                        print(
                            f"🚀 MOON DEV ENTRY: {current_close:.2f} | Size: {position_size} | Risk: {risk_per_unit:.2f}"
                        )
        else:
            # Exit on CMF momentum reversal
            if self.cmf_roc[-1] < 0:
                self.position.close()
                print(f"🌑 MOON DEV EXIT: CMF Reversal at {current_close:.2f}")


# Run backtest with 1M capital
bt = Backtest(data, ChaikinSqueeze, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full performance stats
print("\n🌕🌖🌗🌘 MOON DEV BACKTEST RESULTS 🌑🌒🌓🌔")
print(stats)
print(stats._strategy)
