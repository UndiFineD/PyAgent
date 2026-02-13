# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\VolatilitySurgeBreakout_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
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


class VolatilitySurgeBreakout(Strategy):
    def init(self):
        self.atr_5m = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR_5m",
        )
        self.atr_daily = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=96,
            name="ATR_Daily",
        )

        def compute_bbands(close):
            upper, _, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return upper, lower

        self.bb_upper, self.bb_lower = self.I(
            compute_bbands, self.data.Close, name=["UpperBB", "LowerBB"]
        )

        self.equity = self._broker.starting_cash

    def next(self):
        self.equity = self._broker.equity

        if len(self.data.Close) < 3:
            return

        prev_atr_5m = self.atr_5m[-2]
        prev_atr_daily = self.atr_daily[-2]
        prev_close = self.data.Close[-2]
        prev_upper = self.bb_upper[-2]

        if (
            prev_atr_5m > prev_atr_daily * 1.5
            and prev_close > prev_upper
            and not self.position
        ):

            entry_price = self.data.Open[-1]
            sl = self.bb_lower[-2]
            risk_per_share = entry_price - sl

            if risk_per_share > 0:
                risk_amount = self.equity * 0.01
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    tp = entry_price + 2 * risk_per_share
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙✨ MOON DEV ENTRY ✨🌙\nSize: {position_size} @ {entry_price:.2f}\nSL: {sl:.2f} | TP: {tp:.2f} 🚀"
                    )

    def notify_trade(self, trade):
        if trade.is_closed:
            profit = trade.pl_pct * 100
            emoji = "🚀🌙 PROFIT MOON!" if profit > 0 else "💸 LUNAR ECLIPSE"
            print(f"{emoji}\nClosed: {profit:.2f}% | Equity: {self.equity:,.2f}")


bt = Backtest(data, VolatilitySurgeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
