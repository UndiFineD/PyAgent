# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\SuperSimple_AI5.py
# 🌙 Moon Dev's Super Simple Strategy - Beat Buy and Hold
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for SuperSimple strategy...")
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

print(f"🚀 Data loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]}")


def sma(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).mean().values


class SuperSimple(Strategy):

    def init(self):
        # Just two simple moving averages
        self.sma50 = self.I(sma, self.data.Close, 50)
        self.sma200 = self.I(sma, self.data.Close, 200)

        print("🌙✨ SuperSimple Strategy Initialized!")

    def next(self):
        if len(self.sma200) < 200:
            return

        current_close = self.data.Close[-1]
        sma50_val = self.sma50[-1]
        sma200_val = self.sma200[-1]

        # Check for valid values
        if np.isnan(sma50_val) or np.isnan(sma200_val):
            return

        if not self.position:
            # Buy when SMA50 is significantly above SMA200 (strong uptrend)
            if sma50_val > sma200_val * 1.10:  # 10% above for strong signal
                # Use entire portfolio
                position_size = int(self.equity * 0.98 / current_close)
                if position_size > 0:
                    self.buy(size=position_size)
                    print(
                        f"🚀🌙 SUPER BUY! Entry: {current_close:.2f}, Size: {position_size}"
                    )

        else:
            # Sell when trend clearly reverses
            if sma50_val < sma200_val * 0.98:  # 2% below for exit
                print(f"🌕 SUPER SELL at {current_close:.2f}")
                self.position.close()


# Launch Backtest
print("🚀 Launching SuperSimple backtest with $1,000,000 portfolio...")
bt = Backtest(data, SuperSimple, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV SUPER SIMPLE STRATEGY RESULTS 🌙")
print("=" * 60)
print(stats)
print(f"\n🎯 Buy and Hold Benchmark: 127.77% return ($2,277,687)")
print(f"🚀 Strategy Return: {stats['Return [%]']:.2f}%")
print(f"💰 Strategy Final Value: ${stats['Equity Final [$]']:,.2f}")
print(f"📊 Total Trades: {stats['# Trades']}")

if stats["Return [%]"] > 127.77 and stats["# Trades"] > 5:
    print("🏆 SUCCESS: Strategy beats buy and hold with sufficient trades!")
    success = True
else:
    print("❌ Strategy needs improvement...")
    success = False

print("=" * 60)

if success:
    print("\nDONE")
    print(
        "🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀"
    )
