# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\VolSpikeReversion_BTFinal.py
#!/usr/bin/env python3
# src/data/rbi/04_21_2025/backtests_final/VolSpikeReversion_BTFinal.py
"""
VolSpikeReversion back‑test
---------------------------
* Uses BTC 15‑minute candles only.
* Re‑creates synthetic ‘vol‑surface’ columns so the original strategy logic remains intact:
    • vix_front  – 30‑bar realised volatility (annualised).
    • vix_second – 60‑bar realised volatility (annualised).
    • vvix       – “vol‑of‑vol”: 30‑bar stdev of daily ∆vol.
    • vix_volume / spx_volume – raw trade volume.
    • spx_close  – BTC close (proxy).
"""

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# ──────────────────────────────
# 1.  LOAD & FEATURE ENGINEER
# ──────────────────────────────
DATA_FILE = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)

data = pd.read_csv(DATA_FILE, parse_dates=["datetime"])
data.columns = (
    data.columns.str.strip().str.lower().str.replace("unnamed.*", "", regex=True)
)

# Keep only relevant columns and give Backtesting.py‑friendly names
data = data[["datetime", "open", "high", "low", "close", "volume"]]
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
data.set_index("datetime", inplace=True)

# --- Synthetic VIX / SPX helpers ----------------------------------------------
#  ‣ intraday log‑returns
ret = np.log(data["Close"]).diff()

#  ‣ realised vol (annualised) : √N * σ
data["vix_front"] = ret.rolling(30).std() * np.sqrt(30)
data["vix_second"] = ret.rolling(60).std() * np.sqrt(60)

#  ‣ vol‑of‑vol (VVIX proxy) : rolling stdev of ∆vix_front
data["vvix"] = data["vix_front"].diff().rolling(30).std() * np.sqrt(30)

#  ‣ re‑use BTC volume / price as stand‑ins for VIX & SPX series
data["vix_volume"] = data["Volume"]
data["spx_volume"] = data["Volume"]
data["spx_close"] = data["Close"]

# Clean up NaNs so first few rows don’t break the sim
data.fillna(method="bfill", inplace=True)


# ──────────────────────────────
# 2.  STRATEGY
# ──────────────────────────────
class VolSpikeReversion(Strategy):
    bb_window = 20
    sma_window = 20
    risk_pct = 0.02  # 2 % equity per trade
    vol_mult_entry = 1.20  # 20 % volume spike
    vol_mult_exit = 1.10  # hold until volume calms
    max_hold_days = 5

    def init(self):
        # Bollinger upper band on vvix
        def bb_upper(series):
            upper, *_ = talib.BBANDS(
                series,
                timeperiod=self.bb_window,
                nbdevup=2,
                nbdevdn=2,
                matype=0,
            )
            return upper

        self.vvix_upper = self.I(bb_upper, self.data.vvix)
        self.vvix_sma = self.I(talib.SMA, self.data.vvix, timeperiod=self.sma_window)
        self.vix_vol_avg = self.I(
            talib.SMA, self.data.vix_volume, timeperiod=self.sma_window
        )
        self.spx_vol_avg = self.I(
            talib.SMA, self.data.spx_volume, timeperiod=self.sma_window
        )
        self.spx_low = self.I(
            talib.MIN, self.data.spx_close, timeperiod=self.sma_window
        )

        self.entry_bar = None  # track trade duration

    def next(self):
        price = self.data.Close[-1]
        bar = len(self.data) - 1

        # ─── ENTRY ────────────────────────────────────────────────────────────
        if not self.position:
            term_backwardation = self.data.vix_front[-1] > self.data.vix_second[-1]
            vvix_breakout = self.data.vvix[-1] > self.vvix_upper[-1]
            vol_spike = (
                self.data.vix_volume[-1] > self.vol_mult_entry * self.vix_vol_avg[-1]
            )
            spx_safe = self.data.spx_close[-1] > self.spx_low[-1]

            if term_backwardation and vvix_breakout and vol_spike and spx_safe:
                risk_dollars = self.equity * self.risk_pct
                size = int(risk_dollars / price)

                if size > 0:
                    self.sell(size=size)
                    self.entry_bar = bar
                    print(f"🌙 MOON DEV SHORT ENTRY | Bar {bar} | Size {size}")

        # ─── EXIT ─────────────────────────────────────────────────────────────
        else:
            bars_in_trade = bar - self.entry_bar
            days_in_trade = bars_in_trade / (24 * 4)  # 15‑min bars → 4 per hour

            vvix_below_sma = self.data.vvix[-1] < self.vvix_sma[-1]
            term_contango = self.data.vix_front[-1] < self.data.vix_second[-1]
            vol_cooling = (
                self.data.vix_volume[-1] > self.vol_mult_exit * self.vix_vol_avg[-1]
            )

            vvix_5d_high = self.data.vvix[-1] == self.data.vvix[-5 * 24 * 4 :].max()
            time_exit = days_in_trade >= self.max_hold_days

            if (
                (vvix_below_sma and term_contango and vol_cooling)
                or vvix_5d_high
                or time_exit
            ):
                self.position.close()
                print(f"🌙 MOON DEV EXIT | Bar {bar} | Reason: Signal/Stop")


# ──────────────────────────────
# 3.  BACK‑TEST
# ──────────────────────────────
bt = Backtest(
    data,
    VolSpikeReversion,
    cash=1_000_000,
    commission=0.002,
)

stats = bt.run()
print(stats)
print("Best‑run parameters:", stats._strategy)
