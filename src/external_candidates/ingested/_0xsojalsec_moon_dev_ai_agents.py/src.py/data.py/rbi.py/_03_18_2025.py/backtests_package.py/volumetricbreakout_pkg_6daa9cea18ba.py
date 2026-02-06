# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_18_2025\backtests_package\VolumetricBreakout_PKG.py
# Moon Dev's Volumetric Breakout Backtest 🌙🚀
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare moon data 🌑
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class VolumetricBreakout(Strategy):
    risk_pct = 0.01  # 1% risk per trade 🌕
    bb_period = 20
    rsi_period = 14

    def init(self):
        # Moon-powered indicators 🌙✨
        self.bb_upper = self.I(
            lambda x: talib.BBANDS(x, self.bb_period, 2, 2)[0], self.data.Close
        )
        self.bb_middle = self.I(talib.SMA, self.data.Close, self.bb_period)
        self.volume_avg = self.I(talib.SMA, self.data.Volume, 20)
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        print("🌙 Lunar Indicators Activated:")
        print(f"   BB({self.bb_period}), RSI({self.rsi_period}), Volume(20)")

    def next(self):
        # Wait for full moon (enough data) 🌕
        if len(self.data) < 20:
            return

        # Current cosmic readings 🌌
        price = self.data.Close[-1]
        prev_price = self.data.Close[-2]
        bb_upper = self.bb_upper[-1]
        prev_bb_upper = self.bb_upper[-2]
        volume = self.data.Volume[-1]
        avg_volume = self.volume_avg[-1]
        rsi = self.rsi[-1]

        # Entry: When stars align 🌠
        if (
            not self.position
            and price > bb_upper
            and prev_price <= prev_bb_upper
            and volume > 2 * avg_volume
            and rsi > 50
        ):

            # Calculate moon rocket fuel 🚀
            sl_price = price - self.atr[-1]
            risk_amount = self.risk_pct * self.equity
            position_size = int(round(risk_amount / (price - sl_price)))

            if position_size > 0:
                self.buy(size=position_size, sl=sl_price)
                print(f"🌙✨ LIFTOFF @ {price:.2f}")
                print(f"   Size: {position_size}, SL: {sl_price:.2f}")
                print(f"   Volume: {volume:.2f} (2x {avg_volume:.2f})")
                print(f"   RSI: {rsi:.2f}\n")

        # Exit: When gravity calls 🌍
        if self.position:
            # Bearish crossover detection without backtesting.lib
            if (self.rsi[-2] < 70 and self.rsi[-1] > 70) or self.data.Close[
                -1
            ] < self.bb_middle[-1]:

                self.position.close()
                print(f"🌑 Re-entry @ {price:.2f}")
                print(f"   Profit: {self.position.pl_usd:.2f}\n")


# Launch sequence 🚀
bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# Moon mission report 📊
print("🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print(stats)
print(stats._strategy)
print("Moon Dev Mission Complete! 🌙🚀")
