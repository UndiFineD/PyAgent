# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests\VolatilityBreakout_BT.py
# 🌙 Moon Dev's Volatility Breakout Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolatilityBreakout(Strategy):
    # Strategy parameters
    atr_period_short = 288  # 3 days in 15m periods (3*24*4=288)
    atr_period_long = 1920  # 20 days in 15m periods (20*24*4=1920)
    keltner_multiplier = 2
    risk_pct = 0.01  # 1% risk per trade

    def init(self):
        # 🌗 Calculate core indicators using TA-Lib
        self.atr_short = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period_short,
            name="ATR3",
        )
        self.atr_long = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period_long,
            name="ATR20",
        )
        self.ema20 = self.I(
            talib.EMA, self.data.Close, timeperiod=self.atr_period_long, name="EMA20"
        )

        # 🌖 Calculate Keltner Channel bands
        self.upper_band = self.I(
            lambda: self.ema20 + self.keltner_multiplier * self.atr_long,
            name="Upper Keltner",
        )

        # 🌘 Volatility ratio indicator
        self.vol_ratio = self.I(
            lambda: self.atr_short / self.atr_long, name="Volatility Ratio"
        )

    def next(self):
        # 🌑 Moon Dev's Cosmic Checks
        if not self.position:
            # 🌒 Entry constellation alignment
            if self.vol_ratio[-1] < 0.5 and crossover(self.data.Close, self.upper_band):

                # 🌓 Calculate cosmic position size
                risk_amount = self.equity * self.risk_pct
                atr_value = self.atr_long[-1]

                if atr_value == 0:
                    print("🚨 Zero ATR detected - Aborting launch sequence")
                    return

                position_size = int(round(risk_amount / atr_value))

                if position_size > 0:
                    # 🚀 Lunar Launch!
                    self.buy(size=position_size)
                    self.entry_atr = atr_value
                    self.trail_high = self.data.High[-1]
                    print(
                        f"🌕 MOON SHOT! Long {position_size} units @ {self.data.Close[-1]:.2f}"
                    )

        else:
            # 🌔 Update trailing star map
            self.trail_high = max(self.trail_high, self.data.High[-1])

            # 🌖 Calculate double ATR trailing stop
            current_atr = self.atr_long[-1]
            trail_stop = self.trail_high - 2 * current_atr
            hard_stop = self.position.entry_price - self.entry_atr

            # 🌗 Use highest stop level
            stop_level = max(trail_stop, hard_stop)

            # 🌘 Check for exit conditions
            if self.data.Low[-1] < stop_level:
                self.position.close()
                print(
                    f"🌑 MOON LANDING! Exit @ {self.data.Close[-1]:.2f} | Profit: {self.position.pl_pct:.2f}%"
                )


# 🌟 Data Loading & Preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# 🪐 Clean cosmic data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# 🌌 Align with celestial coordinate system
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

# 🌠 Launch Backtest
bt = Backtest(data, VolatilityBreakout, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🌍 Print Galactic Results
print("\n🌙✨ MOON DEV FINAL STATS ✨🌙")
print(stats)
print(stats._strategy)
