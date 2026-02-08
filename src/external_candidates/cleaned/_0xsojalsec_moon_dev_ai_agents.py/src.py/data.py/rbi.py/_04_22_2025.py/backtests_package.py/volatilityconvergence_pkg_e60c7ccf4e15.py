# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_package\VolatilityConvergence_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data Handling
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
    }
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VolatilityConvergence(Strategy):
    def init(self):
        # Calculate VWAP
        def calculate_vwap(h, l, c, v):
            tp = (h + l + c) / 3
            cum_tp = (tp * v).cumsum()
            cum_vol = v.cumsum()
            return cum_tp / cum_vol

        self.vwap = self.I(
            calculate_vwap,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
        )

        # Bollinger Bands
        self.bb_upper = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BB_Upper",
            index=0,
        )
        self.bb_middle = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BB_Lower",
            index=2,
        )

        # Bandwidth Calculation
        def calc_bandwidth(u, m, l):
            return (u - l) / m

        self.bandwidth = self.I(calc_bandwidth, self.bb_upper, self.bb_middle, self.bb_lower)

        # Daily ATR
        def daily_atr(h, l, c):
            daily_h = h.resample("D").max()
            daily_l = l.resample("D").min()
            daily_c = c.resample("D").last()
            atr = talib.ATR(daily_h, daily_l, daily_c, timeperiod=14)
            return atr.reindex(h.index).ffill()

        self.daily_atr = self.I(daily_atr, self.data.High, self.data.Low, self.data.Close)

    def next(self):
        if len(self.data) < 100:
            return

        # Bandwidth Percentile Calculation
        current_bw = self.bandwidth[-1]
        bw_window = self.bandwidth[-100:]
        percentile = (sum(bw < current_bw for bw in bw_window) / 100) * 100

        # Entry Conditions
        if (percentile <= 10) and (self.data.Close[-1] > self.vwap[-1]) and not self.position:
            atr = self.daily_atr[-1]
            if atr <= 0:
                return

            risk_amount = self.equity * 0.01
            risk_per_share = atr
            position_size = int(round(risk_amount / risk_per_share))

            if position_size > 0:
                tp = self.data.Close[-1] + 2 * atr
                sl = self.data.Close[-1] - atr
                self.buy(size=position_size, sl=sl, tp=tp)
                print(
                    f"🌙✨ MOON DEV LONG! Entry: {self.data.Close[-1]:.2f}, Size: {position_size}, TP: {tp:.2f}, SL: {sl:.2f} 🚀"
                )


bt = Backtest(data, VolatilityConvergence, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
