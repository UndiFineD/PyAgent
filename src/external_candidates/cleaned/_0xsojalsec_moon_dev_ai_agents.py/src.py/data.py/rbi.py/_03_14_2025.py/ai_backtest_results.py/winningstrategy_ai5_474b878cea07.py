# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\WinningStrategy_AI5.py
# 🌙 Moon Dev's Winning Strategy - Beat Buy and Hold with Few Trades
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for WinningStrategy...")
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


def rolling_max(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).max().values


def rolling_min(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).min().values


class WinningStrategy(Strategy):
    def init(self):
        # Strategic indicators for major moves
        self.sma10 = self.I(sma, self.data.Close, 10)
        self.sma100 = self.I(sma, self.data.Close, 100)  # Longer term trend
        self.rsi = self.I(rsi, self.data.Close, 14)
        self.high_50 = self.I(rolling_max, self.data.High, 50)
        self.low_50 = self.I(rolling_min, self.data.Low, 50)
        self.volume_ma = self.I(sma, self.data.Volume, 50)

        print("🌙✨ WinningStrategy Initialized!")

    def next(self):
        if len(self.sma100) < 100:
            return

        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Get indicator values
        sma10_val = self.sma10[-1]
        sma100_val = self.sma100[-1]
        rsi_val = self.rsi[-1]
        high_50_val = self.high_50[-1]
        low_50_val = self.low_50[-1]
        volume_ma_val = self.volume_ma[-1]

        # Check for valid values
        if (
            np.isnan(sma10_val)
            or np.isnan(sma100_val)
            or np.isnan(rsi_val)
            or np.isnan(high_50_val)
            or np.isnan(low_50_val)
            or np.isnan(volume_ma_val)
        ):
            return

        # Powerful momentum conditions
        strong_uptrend = sma10_val > sma100_val * 1.05  # SMA10 significantly above SMA100
        oversold_bounce = rsi_val < 35 and rsi_val > 25  # Oversold but not extreme
        volume_confirmation = current_volume > volume_ma_val * 1.5  # Strong volume
        near_support = current_close < low_50_val * 1.02  # Near 50-period low

        if not self.position:
            # Buy on strong setups only
            if strong_uptrend and oversold_bounce and volume_confirmation:
                # Use significant position size for fewer but bigger wins
                cash_available = self.equity * 0.90  # Use 90% of equity
                position_size = int(cash_available / current_close)
                if position_size > 0:
                    self.buy(size=position_size)
                    print(f"🚀🌙 MAJOR BUY SIGNAL! Entry: {current_close:.2f}, Size: {position_size}")
                    print(f"RSI: {rsi_val:.1f}, Volume: {current_volume / volume_ma_val:.1f}x")

        else:
            # Exit on trend reversal or profit taking
            if (
                sma10_val < sma100_val  # Trend reversal
                or rsi_val > 75  # Overbought
                or current_close > self.position.entry_price * 1.30
            ):  # 30% profit
                print(f"🌕 STRATEGIC EXIT at {current_close:.2f}")
                print(f"P&L: {((current_close - self.position.entry_price) / self.position.entry_price * 100):.2f}%")
                self.position.close()


# Launch Backtest
print("🚀 Launching WinningStrategy backtest with $1,000,000 portfolio...")
bt = Backtest(data, WinningStrategy, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV WINNING STRATEGY RESULTS 🌙")
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
