# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\BandwidthSurge_BTFinal.py
# Bandwidth‑Surge v8  –  high‑frequency breakout, 6‑dial optimiser
# ---------------------------------------------------------------
import math

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# ── 1) Load BTC‑USD 15 min data ──────────────────────────────────────
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[c for c in data.columns if "unnamed" in c])
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


# ── 2) Helpers ───────────────────────────────────────────────────────
def _tick(px: float) -> float:
    return max(0.10, px * 2e-4)


def long_targets(px, atr, atr_mul):
    d = max(atr_mul * abs(atr), 4 * _tick(px))
    return px - d * 0.67, px + d  # sl, tp


def short_targets(px, atr, atr_mul):
    d = max(atr_mul * abs(atr), 4 * _tick(px))
    return px + d * 0.67, px - d


# ── 3) Strategy class ────────────────────────────────────────────────
class BandwidthSurge(Strategy):
    # Six tunables – optimised below
    bb_len = 20
    nbdev = 2.0
    atr_len = 14
    atr_mul = 1.2
    exit_bars = 2
    risk_pct = 0.01

    def init(self):
        bb = self.I(
            lambda c, l, d: talib.BBANDS(c, timeperiod=l, nbdevup=d, nbdevdn=d),
            self.data.Close,
            self.bb_len,
            self.nbdev,
        )
        self.bb_u, self.bb_m, self.bb_l = bb
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_len,
        )

    def size_by_atr(self, atr_val):
        cash_risk = self.equity * self.risk_pct
        return int(max(1, math.floor(cash_risk / abs(atr_val))))

    def next(self):
        atr = self.atr[-1]
        if np.isnan(atr) or atr == 0:
            return

        c, p = self.data.Close[-1], self.data.Close[-2]

        # —— Entry: single‑bar band cross ————————————————
        if not self.position:
            sz = self.size_by_atr(atr)

            # long breakout
            if p <= self.bb_u[-2] and c > self.bb_u[-1]:
                sl, tp = long_targets(c, atr, self.atr_mul)
                self.buy(size=sz, limit=c, sl=sl, tp=tp)

            # short breakdown
            elif p >= self.bb_l[-2] and c < self.bb_l[-1]:
                sl, tp = short_targets(c, atr, self.atr_mul)
                self.sell(size=sz, limit=c, sl=sl, tp=tp)

        # —— Exit: n‑bar reversal ————————————————
        else:
            o = self.data.Open
            if self.position.is_long and all(
                self.data.Close[-i] < o[-i] for i in range(1, self.exit_bars + 1)
            ):
                self.position.close()
            elif self.position.is_short and all(
                self.data.Close[-i] > o[-i] for i in range(1, self.exit_bars + 1)
            ):
                self.position.close()


# ── 4) Back‑test + optimiser ─────────────────────────────────────────
bt = Backtest(data, BandwidthSurge, cash=1_000_000, commission=0.002)


def good(obj):
    # Pass-through during grid enumeration
    if "# Trades" not in obj:
        return True
    # Enforce: >=25 trades, Sharpe>0.8 OR Return>5%
    return obj["# Trades"] >= 25 and (
        obj["Sharpe Ratio"] > 0.8 or obj["Return [%]"] > 5
    )


opt = bt.optimize(
    bb_len=range(8, 28, 4),  # 8,12,16,20,24
    nbdev=[1.5, 2.0, 2.5],
    atr_len=range(6, 18, 4),  # 6,10,14
    atr_mul=[1.0, 1.2, 1.4],
    exit_bars=[1, 2, 3],
    risk_pct=[0.01, 0.02, 0.03],
    maximize="Sharpe Ratio",
    constraint=good,
    random_state=42,
    return_heatmap=False,
    max_tries=300,
)

print("\n— Best configuration found —")
print(
    f"bb_len={opt._strategy.bb_len}, nbdev={opt._strategy.nbdev}, "
    f"atr_len={opt._strategy.atr_len}, atr_mul={opt._strategy.atr_mul}, "
    f"exit_bars={opt._strategy.exit_bars}, risk_pct={opt._strategy.risk_pct}"
)
print(opt)
