# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_10_2025\backtests_final\VolClusterFlip_BTFinal.py
# 🌙 Moon Dev's VolClusterFlip Backtest Implementation �✨
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare lunar data 🌕
try:
    data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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
except Exception as e:
    print(f"🌑 LUNAR DATA ERROR: {str(e)}")
    raise


class VolClusterFlip(Strategy):
    risk_pct = 0.02  # 🌑 2% risk per trade (fixed as fraction)
    atr_period = 14
    rsi_period = 14

    def init(self):
        # Core Lunar Indicators 🌙
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.volume_ma = self.I(talib.SMA, self.data.Volume, 30)

        # Liquidity Zones ✨
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        price = self.data.Close[-1]

        # 🌕 Moon Dev Entry Logic Cluster
        if (
            not self.position
            and price >= self.swing_high[-1]
            and self.data.Volume[-1] > self.volume_ma[-1]
            and self.rsi[-1] > 60
        ):
            # Lunar Risk Management Calculations 🌑
            atr_value = self.atr[-1] or 1  # Prevent zero division
            risk_amount = self.equity * self.risk_pct
            position_size = int(round(risk_amount / atr_value))

            if position_size > 0:  # Ensure valid position size
                # ✨ Moon-sized Entry!
                self.buy(size=position_size)
                print(f"🚀 MOON DEV ENTRY: {position_size} units at {price:.2f}")
                print(f"   📈 RSI: {self.rsi[-1]:.2f} | 📊 Volume: {self.data.Volume[-1]:.2f}")
            else:
                print("🌑 WARNING: Invalid position size calculated")

        # 🌑 Exit Logic Constellation
        if self.position:
            entry_price = self.position.entry_price
            atr_value = self.atr[-1] or 1
            take_profit = entry_price + 1.5 * atr_value
            stop_loss = entry_price - atr_value

            if price >= take_profit or price <= stop_loss:
                self.position.close()
                print(f"🌕 MOON DEV EXIT: Closed at {price:.2f}")
                print(f"   🎯 Profit: {(price / entry_price - 1) * 100:.2f}%")


# Launch Lunar Backtest 🌙🚀
try:
    bt = Backtest(data, VolClusterFlip, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print Full Moon Stats 🌕✨
    print("\n" + "🌙" * 10 + " MOON DEV FINAL STATS " + "🌙" * 10)
    print(stats)
    print("\n🌑 Backtest Complete - To the Moon! 🚀")
except Exception as e:
    print(f"🌑 LUNAR BACKTEST FAILURE: {str(e)}")
    raise
