# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_27_2025\backtests\VolatilityReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and prepare data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class VolatilityReversal(Strategy):
    risk_pct = 0.01  # 1% risk per trade

    def init(self):
        # 🌙 Moon Dev Indicators 🌙
        self.ema50 = self.I(talib.EMA, self.data.Close, 50, name="EMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, 200, name="EMA200")
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14, name="ADX")
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="SWING_LOW")

        print("🌙✨ Moon Dev Indicators Initialized! ✨")

    def next(self):
        # Skip early bars where indicators aren't ready
        if len(self.data) < 200:
            return

        # 🚀 Entry Logic: Golden Cross + Low Volatility 🌙
        if not self.position:
            if crossover(self.ema50, self.ema200):
                current_adx = self.adx[-1]
                if current_adx < 20:
                    entry_price = self.data.Close[-1]
                    sl_price = self.swing_low[-1]

                    risk_per_share = entry_price - sl_price
                    if risk_per_share <= 0:
                        print(f"🌙🚫 Invalid Risk: {risk_per_share:.2f}. Trade skipped.")
                        return

                    position_size = int(round((self.risk_pct * self.equity) / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price)
                        print(
                            f"🚀🌙 MOON ROCKET LAUNCH! 🚀 | Entry: {entry_price:.2f} | Size: {position_size} | SL: {sl_price:.2f} | ADX: {current_adx:.2f}"
                        )

        # ✨ Exit Logic: High Volatility or Death Cross 🌙
        else:
            current_adx = self.adx[-1]
            if current_adx > 30:
                self.position.close()
                print(f"🌙💫 MOON LANDING! 💫 | Exit: {self.data.Close[-1]:.2f} | ADX: {current_adx:.2f}")

            elif crossover(self.ema200, self.ema50):
                self.position.close()
                print(f"🌙☄️ METEOR SHOWER EXIT! ☄️ | Price: {self.data.Close[-1]:.2f} | EMA50/200 Cross")


# 🌙✨ Launch Moon Dev Backtest! 🚀
bt = Backtest(data, VolatilityReversal, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

print("\n🌙✨✨✨ MOON DEV FINAL STATS ✨✨✨🌙")
print(stats)
print(stats._strategy)
