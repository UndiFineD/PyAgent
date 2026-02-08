# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_18_2025\backtests\ReversalMomentum_BT.py
# 🌙 MOON DEV BACKTESTING IMPLEMENTATION FOR REVERSALMOMENTUM STRATEGY 🚀

import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class ReversalMomentum(Strategy):
    ema_short = 50
    ema_long = 200
    adx_period = 14
    adx_entry_threshold = 20
    adx_exit_threshold = 40
    risk_per_trade = 0.01  # 1% risk per trade
    swing_period = 20  # Swing low period for stop loss

    def init(self):
        # 🌙 CALCULATE INDICATORS USING TALIB WITH SELF.I() WRAPPER ✨
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_short)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_long)
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)

    def next(self):
        # 🌑 MOON DEV TRADE LOGIC: ENTRY/EXIT CONDITIONS ✨
        price = self.data.Close[-1]

        if not self.position:
            # 🌙 LONG ENTRY CONDITIONS 🌟
            ema50_cross = crossover(self.ema50, self.ema200)
            adx_below = self.adx[-1] < self.adx_entry_threshold

            if ema50_cross and adx_below:
                # 🌙 RISK MANAGEMENT CALCULATIONS 🛡️
                sl_price = self.swing_low[-1]
                risk_per_share = price - sl_price

                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_per_trade
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price)
                        print(f"🌙✨ MOON DEV ENTRY: LONG {position_size} units at {price:.2f} | SL: {sl_price:.2f} 🚀")

        else:
            # 🌑 EXIT CONDITIONS 🌗
            current_adx = self.adx[-1]
            ema50_below = crossover(self.ema200, self.ema50)

            if current_adx >= self.adx_exit_threshold or ema50_below:
                self.position.close()
                print(f"🌙💫 MOON DEV EXIT: ADX {current_adx:.1f} | Price {price:.2f} 🌑")


# 🌙 DATA PREPARATION MAGIC ✨
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# 🧹 CLEANSE DATA COLUMNS 🌪️
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# 🗺️ PROPER COLUMN MAPPING 🗺️
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# ⏰ SET DATETIME INDEX ⏳
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")

# 🚀 LAUNCH MOON DEV BACKTEST 🌕
bt = Backtest(data, ReversalMomentum, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 📊 PRINT FULL MOON STATISTICS 🌕
print("\n🌙✨ MOON DEV FINAL BACKTEST STATISTICS 🚀")
print(stats)
print("\n🌙🔧 STRATEGY-SPECIFIC METRICS ⚙️")
print(stats._strategy)
