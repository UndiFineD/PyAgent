# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\HybridMomentumMeanReversion_Simple.py
# 🌙 Moon Dev's Hybrid Momentum Mean Reversion Strategy - Simple Version 🌙
# AI-Optimized Strategy with High Trade Frequency

import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

warnings.filterwarnings("ignore")

# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def load_btc_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.drop(
        columns=[col for col in df.columns if "unnamed" in col.lower()], errors="ignore"
    )

    column_mapping = {
        "datetime": "datetime",
        "timestamp": "datetime",
        "date": "datetime",
        "time": "datetime",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }

    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime")

    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    df = df[required_cols].dropna()
    df = df[df > 0]
    return df


data = load_btc_data(data_path)


class HybridMomentumMeanReversionSimple(Strategy):
    """Simple high-frequency hybrid strategy"""

    risk_per_trade = 0.01

    # Aggressive parameters for high trade count
    ema_fast = 5
    ema_slow = 13
    rsi_period = 7
    rsi_oversold = 40  # Relaxed
    rsi_overbought = 60  # Relaxed

    def init(self):
        def ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        def rsi(values, period=14):
            delta = pd.Series(values).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).values

        def atr(high, low, close, period=14):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            tr1 = h - l
            tr2 = abs(h - c.shift(1))
            tr3 = abs(l - c.shift(1))
            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            return tr.rolling(window=period).mean().values

        # Indicators
        self.ema_fast_line = self.I(ema, self.data.Close, self.ema_fast)
        self.ema_slow_line = self.I(ema, self.data.Close, self.ema_slow)
        self.rsi = self.I(rsi, self.data.Close, self.rsi_period)
        self.atr = self.I(atr, self.data.High, self.data.Low, self.data.Close, 10)
        self.volume_sma = self.I(sma, self.data.Volume, 10)

        # Trade management
        self.entry_time = None

        print("🌙✨ Simple Hybrid Strategy Initialized! ✨")

    def next(self):
        if len(self.data) < self.ema_slow + 1:
            return

        # Handle existing positions - quick exits for high frequency
        if self.position:
            if (
                self.entry_time and len(self.data) - self.entry_time > 10
            ):  # Very short hold time
                self.position.close()
                self.entry_time = None
            return

        # Current values
        current_close = self.data.Close[-1]

        # Simple momentum + mean reversion logic
        ema_bullish = self.ema_fast_line[-1] > self.ema_slow_line[-1]
        rsi_oversold = self.rsi[-1] < self.rsi_oversold
        rsi_overbought = self.rsi[-1] > self.rsi_overbought
        volume_ok = (
            self.data.Volume[-1] > self.volume_sma[-1] * 0.8
        )  # Relaxed volume filter

        # Entry logic - either momentum OR mean reversion (relaxed)
        if (ema_bullish and rsi_oversold and volume_ok) or (
            ema_bullish and volume_ok and self.rsi[-1] < 50
        ):
            # Long entry
            stop_loss = current_close - (self.atr[-1] * 1.5)
            risk_per_share = current_close - stop_loss
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_time = len(self.data)

        elif (not ema_bullish and rsi_overbought and volume_ok) or (
            not ema_bullish and volume_ok and self.rsi[-1] > 50
        ):
            # Short entry
            stop_loss = current_close + (self.atr[-1] * 1.5)
            risk_per_share = stop_loss - current_close
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_time = len(self.data)


# Test the strategy
print("🌙 Testing Simple Hybrid Momentum Mean Reversion Strategy...")
print("=" * 70)

bt = Backtest(data, HybridMomentumMeanReversionSimple, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 SIMPLE HYBRID STRATEGY RESULTS")
print("=" * 70)
print(f"📊 Total Trades: {stats['# Trades']}")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")

# Check requirements
trade_requirement = stats["# Trades"] > 100
sharpe_requirement = stats["Sharpe Ratio"] > 2.0

print(f"\n✅ REQUIREMENTS CHECK:")
print(
    f"📊 Trade Count (>100): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 STRATEGY SUCCESS! 🏆")
else:
    print("\n⚠️ Strategy needs optimization...")

print(
    f"\nFull stats available if needed - strategy generated {stats['# Trades']} trades"
)
