# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_17_2025\backtests\VolatilityReversion_BT.py
# 🌙 Moon Dev Backtest AI Implementation: VolatilityReversion Strategy 🚀

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🌌 DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# 🧹 Cleanse and align cosmic data streams
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


class VolatilityReversion(Strategy):
    risk_pct = 0.02  # 🌑 2% risk per trade

    def init(self):
        # 🌠 CALCULATE COSMIC INDICATORS
        # Log returns calculation
        close = self.data.Close
        log_ret = np.log(close) - np.log(close.shift(1))
        self.log_ret = self.I(lambda x: x, log_ret, name="LOG_RET")

        # Volatility measurements 🌪️
        self.hv_10 = self.I(talib.STDDEV, self.log_ret, timeperiod=10, nbdev=1, name="HV_10")
        self.hv_10_ma20 = self.I(talib.SMA, self.hv_10, timeperiod=20, name="HV_10_MA20")

        # RSI exit signals 🚦
        self.rsi_5 = self.I(talib.RSI, self.data.Close, timeperiod=5, name="RSI_5")

        # ATR for stop loss 🌗
        self.atr_10 = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=10,
            name="ATR_10",
        )

        print("🌙✨ Moon Dev Indicators Activated! Ready for Cosmic Reversion ✨")

    def next(self):
        # ⏳ Ensure sufficient cosmic alignment (30 periods needed)
        if len(self.data) < 30:
            return

        # 🌑 CURRENT STAR ALIGNMENTS
        entry_signal = crossover(self.hv_10_ma20, self.hv_10)
        exit_signal = crossover(self.rsi_5, 70)
        current_atr = self.atr_10[-1]

        # 🚀 ENTER THE COSMOS (Long Entry)
        if not self.position and entry_signal:
            if current_atr > 0 and not np.isnan(current_atr):
                equity = self._broker.equity
                risk_amount = equity * self.risk_pct
                stop_distance = 2 * current_atr

                position_size = risk_amount / stop_distance
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        sl=self.data.Close[-1] - stop_distance,
                        tag="🌙 Cosmic Reversion Entry",
                    )
                    print(
                        f"🌠🚀 MOON DEV ALERT: LONG {position_size} units at {self.data.Close[-1]:.2f} | SL: {self.data.Close[-1] - stop_distance:.2f} 🌌"
                    )

        # 💸 EXIT TO PRESERVE COSMIC BALANCE
        elif self.position and exit_signal:
            self.position.close()
            print(
                f"🌑💸 RSI OVERHEAT: Closing position at {self.data.Close[-1]:.2f} | Profit: {self.position.pl_pct:.2f}% 🌗"
            )


# 🚀 LAUNCH BACKTEST
bt = Backtest(data, VolatilityReversion, cash=1_000_000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("FINAL MOON DEV STRATEGY STATS:")
print(stats)
print(stats._strategy)
print("🌙✨ May your returns be as infinite as the cosmos! 🚀")
