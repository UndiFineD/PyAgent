# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests\ContrarianGapfill_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=True, index_col=0)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Ensure proper column mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class ContrarianGapfill(Strategy):
    gap_threshold = 0.04  # 4% gap down
    rsi_oversold = 30
    volume_multiplier = 1.5
    sl_pct = 0.05  # 5% stop loss
    tp_pct = 0.15  # 15% take profit
    risk_pct = 0.01  # 1% portfolio risk per trade
    vol_period = 20
    rsi_period = 14

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.volume_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=self.vol_period
        )
        self.gap_level = None
        print(
            "🌙 Moon Dev ContrarianGapfill Strategy Initialized! Scanning for gaps... ✨"
        )

    def next(self):
        if len(self.data) < max(self.rsi_period, self.vol_period) + 1:
            return

        # If in position, check for gap fill exit
        if self.position:
            if self.data.Close[-1] >= self.gap_level:
                self.position.close()
                print(
                    f"🌕 Moon Dev Exit: Gap filled at {self.data.Close[-1]:.2f}! Profits secured. 🚀"
                )
            # Additional trailing logic can be added here if needed, but SL/TP handles basics

        # Entry logic if no position
        else:
            prev_close = self.data.Close[-2]
            curr_open = self.data.Open[-1]
            gap_pct = (prev_close - curr_open) / prev_close

            if (
                gap_pct > self.gap_threshold
                and self.rsi[-1] < self.rsi_oversold
                and self.data.Volume[-1] > self.volume_sma[-1] * self.volume_multiplier
            ):

                self.gap_level = prev_close
                entry = self.data.Close[-1]
                equity = self._broker.getvalue()
                risk_amount = self.risk_pct * equity
                risk_per_unit = entry * self.sl_pct
                size = risk_amount / risk_per_unit
                size = int(round(size))

                if size > 0:
                    self.buy(size=size, sl=1 - self.sl_pct, tp=1 + self.tp_pct)
                    print(
                        f"🚀 Moon Dev Entry Alert: {gap_pct*100:.1f}% gap down on BTC! RSI: {self.rsi[-1]:.1f}, Volume spike detected. Buying {size} units at {entry:.2f} 🌙✨"
                    )


# Run backtest
bt = Backtest(
    data, ContrarianGapfill, cash=1000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
print(stats._strategy)
