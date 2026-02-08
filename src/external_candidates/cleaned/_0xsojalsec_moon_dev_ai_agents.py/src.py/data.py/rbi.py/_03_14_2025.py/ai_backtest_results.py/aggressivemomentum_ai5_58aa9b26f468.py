# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\AggressiveMomentum_AI5.py
# 🌙 Moon Dev's Aggressive Momentum Strategy - Beat Buy and Hold
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for AggressiveMomentum strategy...")
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


def ema(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.ewm(span=period).mean().values


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


class AggressiveMomentum(Strategy):
    risk_per_trade = 0.20  # 20% risk per trade for maximum leverage

    def init(self):
        # Simple but powerful momentum indicators
        self.ema10 = self.I(ema, self.data.Close, 10)
        self.ema30 = self.I(ema, self.data.Close, 30)
        self.rsi = self.I(rsi, self.data.Close, 14)
        self.volume_ma = self.I(sma, self.data.Volume, 10)

        print("🌙✨ AggressiveMomentum Strategy Initialized!")

    def next(self):
        if len(self.ema30) < 30:
            return

        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Get indicator values
        ema10 = self.ema10[-1]
        ema30 = self.ema30[-1]
        rsi_val = self.rsi[-1]
        volume_ma = self.volume_ma[-1]

        # Check for valid values
        if np.isnan(ema10) or np.isnan(ema30) or np.isnan(rsi_val) or np.isnan(volume_ma):
            return

        # Calculate momentum
        price_momentum = (current_close - self.data.Close[-10]) / self.data.Close[-10]
        volume_surge = current_volume > volume_ma * 1.1

        if not self.position:
            # Long entry on strong upward momentum
            if ema10 > ema30 and price_momentum > 0.02 and rsi_val > 50 and volume_surge:
                # Wide stop loss for momentum trades
                sl_price = current_close * 0.92  # 8% stop loss
                risk_per_share = current_close - sl_price

                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_per_trade
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        # Let winners run - wide take profit
                        tp_price = current_close * 1.25  # 25% take profit
                        self.buy(size=position_size, sl=sl_price, tp=tp_price)
                        print(f"🚀🌙 AGGRESSIVE MOMENTUM! Entry: {current_close:.2f}, Size: {position_size}")

        else:
            # Exit on momentum reversal
            if self.position.is_long:
                if ema10 < ema30 or rsi_val < 40:
                    print(f"🌕 MOMENTUM REVERSAL EXIT at {current_close:.2f}")
                    self.position.close()


# Launch Backtest
print("🚀 Launching AggressiveMomentum backtest with $1,000,000 portfolio...")
bt = Backtest(data, AggressiveMomentum, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV AGGRESSIVE MOMENTUM STRATEGY RESULTS 🌙")
print("=" * 60)
print(stats)
print(f"\n🎯 Buy and Hold Benchmark: 127.77% return ($2,277,687)")
print(f"🚀 Strategy Return: {stats['Return [%]']:.2f}%")
print(f"💰 Strategy Final Value: ${stats['Equity Final [$]']:,.2f}")
print(f"📊 Total Trades: {stats['# Trades']}")

if stats["Return [%]"] > 127.77 and stats["# Trades"] > 5:
    print("🏆 SUCCESS: Strategy beats buy and hold with sufficient trades!")
else:
    print("❌ Strategy needs improvement...")

print("=" * 60)
