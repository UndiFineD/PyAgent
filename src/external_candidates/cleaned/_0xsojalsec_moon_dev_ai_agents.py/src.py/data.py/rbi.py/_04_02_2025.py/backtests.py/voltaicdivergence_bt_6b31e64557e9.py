# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests\VoltaicDivergence_BT.py
# 🌙 Moon Dev's Voltaic Divergence Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Clean and prepare data 🌌
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date",
    }
)
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")


class VoltaicDivergence(Strategy):
    def init(self):
        # 🌗 Core Indicators
        self.obv = self.I(talib.OBV, self.data.Close, self.data.Volume, name="OBV")
        self.sma10 = self.I(talib.SMA, self.data.Close, 10, name="SMA10")
        self.atr14 = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14, name="ATR14")

        # 🌑 Swing Detection
        self.price_swing_high = self.I(talib.MAX, self.data.High, 20, name="PriceSwing")
        self.obv_swing_high = self.I(talib.MAX, self.obv, 20, name="OBVSwing")

        # 🌓 Volatility Analysis
        self.atr_sma20 = self.I(talib.SMA, self.atr14, 20, name="ATR_SMA20")
        self.entry_atr = None

    def next(self):
        # 🚀 Entry Logic
        if not self.position:
            # Divergence Check
            swing_checks = (
                len(self.price_swing_high) >= 3
                and len(self.obv_swing_high) >= 3
                and self.price_swing_high[-3] < self.price_swing_high[-2] < self.price_swing_high[-1]
                and self.obv_swing_high[-3] > self.obv_swing_high[-2] > self.obv_swing_high[-1]
            )

            # Volatility Contraction
            volatility_check = self.atr14[-1] < self.atr_sma20[-1]

            # Trend Alignment
            price_position = self.data.Close[-1] < self.sma10[-1]

            if swing_checks and volatility_check and price_position:
                # 🌕 Risk Management
                risk_amount = self.equity * 0.02
                atr_value = self.atr14[-1]
                position_size = int(round(risk_amount / atr_value))

                if position_size > 0:
                    self.sell(
                        size=position_size,
                        sl=self.data.Close[-1] + atr_value,
                        tag="🌙Short_Entry",
                    )
                    self.entry_atr = atr_value
                    print(
                        f"🌙🚀 BEARISH DIVERGENCE! Short {position_size} @ {self.data.Close[-1]} | SL: {self.data.Close[-1] + atr_value}"
                    )

        # 🌒 Exit Logic
        if self.position.is_short:
            # Volatility Expansion
            vol_exit = self.atr14[-1] >= 2 * self.entry_atr

            # Trend Reversal
            trend_exit = self.data.Close[-1] > self.sma10[-1]

            if vol_exit or trend_exit:
                self.position.close()
                reason = "2x ATR 🌪️" if vol_exit else "SMA Cross 📈"
                print(f"🌑✨ EXIT SIGNAL! {reason} | P/L: {self.position.pl}")


# 🌟 Run Backtest
bt = Backtest(data, VoltaicDivergence, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
