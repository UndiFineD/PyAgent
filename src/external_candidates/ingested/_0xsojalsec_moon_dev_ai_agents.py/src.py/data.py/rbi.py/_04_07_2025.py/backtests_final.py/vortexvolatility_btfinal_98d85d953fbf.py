# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests_final\VortexVolatility_BTFinal.py
# 🌙 Moon Dev's Vortex Volatility Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🚀 Data Preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"])

# Clean and prepare data
data.columns = [col.strip().lower() for col in data.columns]
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
data.set_index("datetime", inplace=True)


class VortexVolatility(Strategy):
    risk_pct = 0.01  # 🌕 1% risk per trade
    stop_loss_pct = 0.10  # 🔻 10% stop loss
    vix_sma_period = 20
    vortex_period = 14
    entry_bar = None  # 📊 Track entry bar for time exit

    def init(self):
        # 🌗 Calculate indicators using TA-Lib
        self.vix_sma = self.I(
            talib.SMA, self.data.Close, timeperiod=self.vix_sma_period
        )
        vi_plus, vi_minus = talib.VORTEX(
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.vortex_period,
        )
        self.vi_plus = self.I(lambda: vi_plus, name="VI+")
        self.vi_minus = self.I(lambda: vi_minus, name="VI-")

    def next(self):
        # 🌑 Exit conditions first
        if self.position:
            # Time-based exit after 5 days (15m * 96 = 1 day)
            if len(self.data) - self.entry_bar >= 5 * 96:
                self.position.close()
                print(f"⏳ MOON DEV TIME EXIT | Price: {self.data.Close[-1]:.2f}")
                return

            # Regular exit conditions
            if self.data.Close[-1] < self.vix_sma[-1] and crossover(
                self.vi_plus, self.vi_minus
            ):
                self.position.close()
                print(f"🌑 MOON DEV STRATEGY EXIT | Price: {self.data.Close[-1]:.2f}")

        # 🚀 Entry conditions
        elif not self.position:
            if self.data.Close[-1] > self.vix_sma[-1] and crossover(
                self.vi_minus, self.vi_plus
            ):

                # 🌕 Risk management calculations
                equity = self.broker.get_value()
                risk_amount = equity * self.risk_pct
                entry_price = self.data.Close[-1]
                stop_loss_price = entry_price * (1 + self.stop_loss_pct)
                risk_per_unit = abs(stop_loss_price - entry_price)

                if risk_per_unit > 0:
                    position_size = int(round(risk_amount / risk_per_unit))
                    if position_size > 0:
                        self.sell(size=position_size, sl=stop_loss_price)
                        self.entry_bar = len(self.data) - 1
                        print(
                            f"🚀 MOON DEV SHORT ENTRY | Size: {position_size} | Entry: {entry_price:.2f} | SL: {stop_loss_price:.2f}"
                        )


# 🌖 Run backtest
bt = Backtest(
    data, VortexVolatility, cash=1_000_000, commission=0.002, exclusive_orders=True
)
stats = bt.run()

# 🌟 Print full statistics
print("\n" + "=" * 55 + " MOON DEV FINAL STATS " + "=" * 55)
print(stats)
print("=" * 130 + "\n")
