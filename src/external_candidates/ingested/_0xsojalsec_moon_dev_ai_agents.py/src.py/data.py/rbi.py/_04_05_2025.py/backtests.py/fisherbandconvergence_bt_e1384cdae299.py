# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\FisherBandConvergence_BT.py
# 🌙 Moon Dev's FisherBand Convergence Backtest 🌙
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


def calculate_fisher(high, low):
    fisher_df = ta.fisher(high=high, low=low, length=9)
    return fisher_df["FISHERT_9"]


class FisherBandConvergence(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # 🌀 Indicator Initialization
        self.fisher = self.I(calculate_fisher, self.data.High, self.data.Low)
        self.cmf = self.I(
            talib.CMF,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            20,
        )

        # 📊 Bollinger Bands Width Calculation
        def bb_width(close):
            upper, middle, lower = talib.BBANDS(
                close, timeperiod=20, nbdevup=2, nbdevdn=2
            )
            return (upper - lower) / middle

        self.bb_width = self.I(bb_width, self.data.Close)
        self.bb_min = self.I(talib.MIN, self.bb_width, 30)

        # 🛡️ ATR for Risk Management
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if len(self.data) < 30:  # Warmup period
            return

        # 🌙 Entry Conditions
        if not self.position:
            fisher_above = crossover(self.fisher, 0)
            cmf_valid = self.cmf[-1] > 0.1
            bb_contraction = self.bb_width[-1] <= self.bb_min[-1]

            if fisher_above and cmf_valid and bb_contraction:
                risk_amount = self.equity * self.risk_per_trade
                atr_value = self.atr[-1] or 1  # Avoid zero division
                entry_price = self.data.Close[-1]
                stop_loss = entry_price - 2 * atr_value

                position_size = int(round(risk_amount / (entry_price - stop_loss)))
                if position_size > 0:
                    print(
                        f"🌙✨🚀 MOON DEV BUY SIGNAL! Size: {position_size} @ {entry_price:.2f}"
                    )
                    self.buy(size=position_size, sl=stop_loss)

        # 🌙 Exit Condition
        else:
            if crossunder(self.fisher, 0):
                print(f"🌙✨💎 PROFIT TAKEN! Closing @ {self.data.Close[-1]:.2f}")
                self.position.close()


# 🧹 Data Cleaning Ritual
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# 🚀 Launch Backtest
bt = Backtest(data, FisherBandConvergence, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕 MOON DEV FINAL STATS 🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print(stats)
print(stats._strategy)
