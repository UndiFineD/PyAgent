# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_package\LiquidationRebound_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
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


class LiquidationRebound(Strategy):
    risk_percent = 0.01
    atr_period = 14
    oi_window = 16  # 4h in 15m intervals
    cascade_low = None

    def init(self):
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.oi = self.I(lambda x: x, self.data.df["open_interest"])
        self.funding = self.I(lambda x: x, self.data.df["funding_rate"])
        self.oi_pct = self.I(lambda x: x.pct_change(self.oi_window), self.oi)
        self.max_price = self.I(talib.MAX, self.data.High, timeperiod=self.oi_window)

    def next(self):
        if self.position:
            # Moon Dev exit checks
            if self.funding[-1] > -0.0001 and self.funding[-2] > -0.0001:
                self.position.close()
                print(f"🌙 MOON DEV: Funding normalized @ {self.data.Close[-1]} ✨")
                return
            if self.data.Close[-1] >= self.position.entry_price + 2 * self.atr[-1]:
                self.position.close()
                print(f"🌙 MOON DEV: Target hit @ {self.data.Close[-1]} 🎯")
                return
            if self.data.Close[-1] <= self.cascade_low:
                self.position.close()
                print(f"🌙 MOON DEV: STOPPED OUT @ {self.data.Close[-1]} 🚨")
                return
            if len(self.data) - self.position.entry_bar >= 192:
                self.position.close()
                print(f"🌙 MOON DEV: Time exit @ {self.data.Close[-1]} ⏳")
                return
        else:
            # Liquidation detection
            if (
                self.oi_pct[-1] <= -0.15
                and self.funding[-1] < -0.0005
                and (self.max_price[-1] - self.data.Close[-1]) > 3 * self.atr[-1]
            ):

                self.cascade_low = min(self.data.Low[-self.oi_window :])
                print(f"🌙 MOON DEV: CASCADE DETECTED! Low: {self.cascade_low} 📉")

                # Entry logic
                hl = [self.data.Low[-i] > self.data.Low[-i - 1] for i in range(1, 4)]
                vol_trend = self.data.Volume[-3:].values
                if (
                    all(hl)
                    and self.data.Close[-1] > self.cascade_low + 1.5 * self.atr[-1]
                    and vol_trend[0] < vol_trend[1] < vol_trend[2]
                ):

                    risk_amount = self.risk_percent * self.equity
                    stop_loss = self.data.Close[-1] - self.cascade_low
                    position_size = int(round(risk_amount / stop_loss))
                    self.buy(size=position_size)
                    print(
                        f"🌙 MOON DEV: LONG ENTRY @ {self.data.Close[-1]} 🚀 Size: {position_size}"
                    )


bt = Backtest(data, LiquidationRebound, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
