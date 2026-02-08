# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\UltimateStrategy_AI5.py
# 🌙 Moon Dev's Ultimate Strategy - Beat Buy and Hold
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for UltimateStrategy...")
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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


def rsi(series, period=14):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return (100 - (100 / (1 + rs))).values


class UltimateStrategy(Strategy):
    def init(self):
        # Long term trend and momentum
        self.sma20 = self.I(sma, self.data.Close, 20)
        self.sma200 = self.I(sma, self.data.Close, 200)
        self.rsi = self.I(rsi, self.data.Close, 14)
        self.volume_ma = self.I(sma, self.data.Volume, 30)

        # Track entry price manually
        self.entry_price = None

        print("🌙✨ UltimateStrategy Initialized!")

    def next(self):
        if len(self.sma200) < 200:
            return

        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Get indicator values
        sma20_val = self.sma20[-1]
        sma200_val = self.sma200[-1]
        rsi_val = self.rsi[-1]
        volume_ma_val = self.volume_ma[-1]

        # Check for valid values
        if np.isnan(sma20_val) or np.isnan(sma200_val) or np.isnan(rsi_val) or np.isnan(volume_ma_val):
            return

        # Major trend signal
        major_uptrend = sma20_val > sma200_val * 1.02  # SMA20 at least 2% above SMA200
        momentum_oversold = 25 < rsi_val < 40  # Oversold but not extreme
        volume_spike = current_volume > volume_ma_val * 2.0  # High volume confirmation

        if not self.position:
            # Enter on major trend + momentum + volume
            if major_uptrend and momentum_oversold and volume_spike:
                # Use most of portfolio for maximum impact
                cash_available = self.equity * 0.95
                position_size = int(cash_available / current_close)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_price = current_close
                    print(f"🚀🌙 ULTIMATE BUY! Entry: {current_close:.2f}, Size: {position_size}")
                    print(f"RSI: {rsi_val:.1f}, Volume: {current_volume / volume_ma_val:.1f}x")

        else:
            # Exit conditions
            trend_reversal = sma20_val < sma200_val  # Trend breaks
            take_profit = current_close > self.entry_price * 1.25  # 25% profit
            stop_loss = current_close < self.entry_price * 0.90  # 10% stop loss
            overbought = rsi_val > 80

            if trend_reversal or take_profit or stop_loss or overbought:
                profit_pct = ((current_close - self.entry_price) / self.entry_price * 100) if self.entry_price else 0
                print(f"🌕 EXIT at {current_close:.2f}, P&L: {profit_pct:.2f}%")
                self.position.close()
                self.entry_price = None


# Launch Backtest
print("🚀 Launching UltimateStrategy backtest with $1,000,000 portfolio...")
bt = Backtest(data, UltimateStrategy, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV ULTIMATE STRATEGY RESULTS 🌙")
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
    print("🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀")
