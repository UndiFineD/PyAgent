# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_package\VolatilityDivergence_PKG.py
import numpy as np
import pandas as pd
import talib as TA
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VolatilityDivergence(Strategy):
    def init(self):
        # Bollinger Bands with width calculation
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            TA.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.bb_width = self.I(lambda u, l: u - l, self.bb_upper, self.bb_lower)
        self.bb_width_max = self.I(TA.MAX, self.bb_width, timeperiod=20)

        # Chaikin Money Flow
        def calc_cmf(h, l, c, v, period):
            mfm = ((2 * c - h - l) / (h - l + 1e-9)) * v
            cmf = TA.SMA(mfm, period) / TA.SMA(v, period)
            return cmf

        self.cmf = self.I(
            calc_cmf,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            20,
        )

        # Keltner Channel
        self.ema = self.I(TA.EMA, self.data.Close, 20)
        self.atr = self.I(TA.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.keltner_upper = self.I(lambda e, a: e + 1.5 * a, self.ema, self.atr)
        self.keltner_lower = self.I(lambda e, a: e - 1.5 * a, self.ema, self.atr)

        print("🌙 Moon Dev Strategy Activated! Ready for stellar trades! 🚀✨")

    def next(self):
        if self.position:
            entry = self.position.entry_price
            risk = self.position.sl - entry
            current_profit = entry - self.data.Close[-1]

            if current_profit >= 2 * abs(risk):
                self.position.update(sl=entry)
                print(f"🌕 Trailing SL to breakeven! {entry}")
            return

        if len(self.data) < 40:
            return

        # Bollinger contraction check
        bb_contraction = self.bb_width[-1] < self.bb_width_max[-2]

        # CMF divergence check
        lookback = 5
        price_highs = self.data.High[-lookback - 1 : -1]
        cmf_values = self.cmf[-lookback - 1 : -1]
        div_condition = (self.data.High[-1] > max(price_highs)) and (
            self.cmf[-1] < max(cmf_values)
        )

        # Entry conditions
        if (
            bb_contraction
            and div_condition
            and (self.data.Close[-1] < self.bb_lower[-1])
        ):
            risk_amount = self.equity * 0.01
            entry_price = self.data.Close[-1]
            sl_price = self.keltner_upper[-1]
            tp_price = self.keltner_lower[-1]

            risk_per_unit = sl_price - entry_price
            if risk_per_unit <= 0:
                return

            position_size = int(round(risk_amount / risk_per_unit))
            if position_size == 0:
                return

            self.sell(size=position_size, sl=sl_price, tp=tp_price)
            print(
                f"🌑 SHORT ENTRY! Size: {position_size} ✨ Entry: {entry_price:.2f} | SL: {sl_price:.2f} | TP: {tp_price:.2f}"
            )


bt = Backtest(data, VolatilityDivergence, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
