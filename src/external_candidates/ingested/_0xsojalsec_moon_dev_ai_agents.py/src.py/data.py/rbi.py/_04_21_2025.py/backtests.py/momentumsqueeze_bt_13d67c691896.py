# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests\MomentumSqueeze_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from pandas_ta import fisher

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
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


class MomentumSqueeze(Strategy):
    fisher_period = 10
    signal_period = 9
    bb_period = 20
    risk_pct = 0.01
    stop_loss_pct = 0.02

    def init(self):
        # Fisher Transform with Signal Line
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        fisher_result = fisher(
            high=high, low=low, length=self.fisher_period, signal=self.signal_period
        )
        self.fisher = self.I(
            lambda: fisher_result[f"FISHERT_{self.fisher_period}_{self.signal_period}"],
            name="Fisher",
        )
        self.signal = self.I(
            lambda: fisher_result[
                f"FISHERTs_{self.signal_period}_{self.signal_period}"
            ],
            name="Signal",
        )

        # Bollinger Bands and Bandwidth
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name=["BB_Upper", "BB_Middle", "BB_Lower"],
        )
        self.bb_width = self.I(
            lambda: (self.bb_upper - self.bb_lower) / self.bb_middle, name="BB_Width"
        )

    def next(self):
        if len(self.data) < 50:  # Warmup period
            return

        # Entry Logic 🌙
        if not self.position:
            # Fisher crossover + Volume uptrend + BB squeeze
            if (
                crossover(self.fisher, self.signal)
                and self.data.Volume[-3] < self.data.Volume[-2] < self.data.Volume[-1]
                and self.bb_width[-1] < self.bb_width[-2]
            ):

                # Risk management 🛡️
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * (1 - self.stop_loss_pct)
                risk_amount = self.equity * self.risk_pct
                position_size = int(round(risk_amount / (entry_price - stop_loss)))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss)
                    print(
                        f"🌙✨ MOON DEV LONG ENTRY ✨🌙 | Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_loss:.2f}"
                    )

        # Exit Logic 🚀
        else:
            if (
                crossover(self.signal, self.fisher)
                or self.bb_width[-1] > self.bb_width[-2] * 1.5
            ):
                self.position.close()
                print(
                    f"🌙💎 MOON DEV EXIT 💎🌙 | Price: {self.data.Close[-1]:.2f} | Profit: {self.position.pl:.2f}"
                )


# Execute backtest 🌌
bt = Backtest(data, MomentumSqueeze, cash=1_000_000, trade_on_close=True)
stats = bt.run()
print(stats)
print(stats._strategy)
