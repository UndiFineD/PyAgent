# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\VolatilityMomentum_BT.py
# 🌙 Moon Dev's Volatility Momentum Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Clean and prepare the cosmic data 📡
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Cosmic data cleansing ritual 🌌
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


class VolatilityMomentum(Strategy):
    risk_pct = 0.01  # 🌕 1% of stardust per trade
    take_profit = 1.05  # 🚀 5% above EMA
    stop_loss_pct = 0.97  # 🛡️ 3% stardust protection

    def init(self):
        # 🌠 Cosmic indicator alignment
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14, name="ATR")
        self.min_atr = self.I(talib.MIN, self.atr, 20, name="MIN_ATR")
        self.ema10 = self.I(talib.EMA, self.data.Close, 10, name="EMA_10")

    def next(self):
        current_bar = len(self.data) - 1

        # 🌙 Moon Dev Debug Console
        if current_bar % 100 == 0:
            print(f"\n🌌 Bar {current_bar}")
            print(f"   Close: {self.data.Close[-1]:.2f} | EMA10: {self.ema10[-1]:.2f}")
            print(f"   ATR: {self.atr[-1]:.2f} | 20-period MIN ATR: {self.min_atr[-1]:.2f}")

        if not self.position:
            # 🌠 Entry Conditions: Low Volatility + Momentum Cross
            if self.atr[-1] <= self.min_atr[-1] and crossover(self.data.Close, self.ema10):
                # 🧮 Stardust Risk Calculation
                risk_amount = self.equity * self.risk_pct
                entry_price = self.data.Close[-1]
                stop_price = entry_price * self.stop_loss_pct
                risk_per_share = entry_price - stop_price

                if risk_per_share <= 0:
                    print("🪐 Negative risk detected! Aborting launch.")
                    return

                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    print(f"\n🚀 LAUNCH DETECTED! Buying {position_size} shares")
                    print(f"   Entry: {entry_price:.2f} | Stop: {stop_price:.2f}")
                    self.buy(size=position_size, sl=stop_price)

        else:
            # 🌠 Exit Conditions: Profit Harvest or Cosmic Protection
            entry_price = self.position.entry_price
            current_ema = self.ema10[-1]

            # Take Profit Condition
            if self.data.Close[-1] >= current_ema * self.take_profit:
                print(f"\n✨ PROFIT HARVEST! Closing at {self.data.Close[-1]:.2f}")
                self.position.close()

            # Stop Loss Condition
            elif self.data.Low[-1] <= entry_price * self.stop_loss_pct:
                print(f"\n🌧️ COSMIC PROTECTION ACTIVATED! Closing at {self.data.Low[-1]:.2f}")
                self.position.close()


# 🚀 Launch Backtest
bt = Backtest(data, VolatilityMomentum, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Display Cosmic Performance
print("\n" + "=" * 55)
print("🌙 MOON DEV FINAL MISSION REPORT 🌙")
print("=" * 55)
print(stats)
print(stats._strategy)
print("✨ Mission Complete! Until next stellar strategy! 🚀")
