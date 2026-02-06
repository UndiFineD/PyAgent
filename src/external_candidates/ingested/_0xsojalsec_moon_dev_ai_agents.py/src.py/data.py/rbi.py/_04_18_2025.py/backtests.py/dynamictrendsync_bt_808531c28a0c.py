# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests\DynamicTrendSync_BT.py
# 🌙 MOON DEV BACKTESTING IMPLEMENTATION FOR DynamicTrendSync STRATEGY
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class DynamicTrendSync(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade

    def init(self):
        # 🌙 STRATEGY INDICATORS USING TA-LIB
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20)

        print(
            "🌙✨ Moon Dev Indicators Activated: EMA(50/200), ADX(14), RSI(14), SwingLow(20)"
        )

    def next(self):
        # Skip early bars without sufficient data
        if len(self.data.Close) < 200:
            return

        # 🌙 DEBUG PRINT CURRENT MARKET STATE
        print(
            f"🌕 Close: {self.data.Close[-1]:.2f} | EMA50: {self.ema50[-1]:.2f} ➔ EMA200: {self.ema200[-1]:.2f}"
        )
        print(
            f"📶 ADX: {self.adx[-1]:.2f} | RSI: {self.rsi[-1]:.2f} | SwingLow: {self.swing_low[-1]:.2f}"
        )

        # 💹 ENTRY LOGIC
        if not self.position:
            # Golden Cross + Strong Trend Confirmation
            if crossover(self.ema50, self.ema200) and self.adx[-1] > 25:
                # 🌙 RISK MANAGEMENT CALCULATIONS
                entry_price = self.data.Close[-1]
                stop_price = self.swing_low[-1]
                risk_per_share = entry_price - stop_price

                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_per_trade
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_price, tag="MoonDev_Long")
                        print(f"🚀🌙 MOON DEV ENTRY SIGNAL! Long {position_size} units")
                        print(
                            f"🎯 Entry: {entry_price:.2f} | Stop: {stop_price:.2f} | Risk: {risk_per_share:.2f}"
                        )

        # 🔴 EXIT LOGIC
        else:
            # RSI Exit Signal
            if self.rsi[-1] < 70 and self.rsi[-2] >= 70:
                self.position.close()
                print(f"🎯🌙 RSI EXIT SIGNAL! Closed at {self.data.Close[-1]:.2f}")

            # Death Cross Emergency Exit
            if crossover(self.ema200, self.ema50):
                self.position.close()
                print(f"🌑💥 DEATH CROSS EXIT! Closed at {self.data.Close[-1]:.2f}")


# 🌙 DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# 🧹 DATA CLEANING
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

# 🚀 BACKTEST EXECUTION
bt = Backtest(data, DynamicTrendSync, cash=1_000_000, commission=0.002)
stats = bt.run()

# 📊 RESULTS
print("\n🌙✨ MOON DEV BACKTEST COMPLETE! FULL STRATEGY STATS:")
print(stats)
print("\n🔍 STRATEGY DETAIL ANALYSIS:")
print(stats._strategy)
