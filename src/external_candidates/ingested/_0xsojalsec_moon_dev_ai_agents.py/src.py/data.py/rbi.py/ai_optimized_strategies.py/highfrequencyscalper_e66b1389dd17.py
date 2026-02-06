# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\HighFrequencyScalper.py
# 🌙 Moon Dev's High Frequency Scalper - Targeting 100+ Trades 🌙
# Ultra-aggressive scalping strategy designed for high trade count

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


class HighFrequencyScalper(Strategy):
    """Ultra high frequency scalping strategy"""

    risk_per_trade = 0.005  # Lower risk for more trades

    # Ultra-short periods for high frequency
    ema_period = 3
    rsi_period = 5
    volume_period = 5
    max_hold_bars = 5  # Very short holds

    def init(self):
        def ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        def rsi(values, period=5):
            delta = pd.Series(values).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).values

        # Ultra-responsive indicators
        self.ema = self.I(ema, self.data.Close, self.ema_period)
        self.rsi = self.I(rsi, self.data.Close, self.rsi_period)
        self.volume_sma = self.I(sma, self.data.Volume, self.volume_period)

        # Price change indicator
        self.price_change = self.I(
            lambda: pd.Series(self.data.Close).pct_change().values
        )

        # Trade management
        self.entry_time = None
        self.entry_price = None

        print("🌙⚡ High Frequency Scalper Initialized! ⚡")

    def next(self):
        if len(self.data) < self.ema_period + 1:
            return

        # Handle existing positions - very quick exits
        if self.position:
            current_bars_held = (
                len(self.data) - self.entry_time if self.entry_time else 0
            )
            current_price = self.data.Close[-1]

            # Quick profit taking (even tiny profits)
            if (
                self.position.is_long and current_price > self.entry_price * 1.001
            ):  # 0.1% profit
                self.position.close()
                self.entry_time = None
                self.entry_price = None
                return
            elif (
                self.position.is_short and current_price < self.entry_price * 0.999
            ):  # 0.1% profit
                self.position.close()
                self.entry_time = None
                self.entry_price = None
                return

            # Force exit after max hold period
            if current_bars_held >= self.max_hold_bars:
                self.position.close()
                self.entry_time = None
                self.entry_price = None
            return

        # Ultra-aggressive entry conditions
        current_close = self.data.Close[-1]
        current_rsi = self.rsi[-1]
        price_momentum = self.price_change[-1]

        # Very relaxed volume filter
        volume_ok = (
            self.data.Volume[-1] > self.volume_sma[-1] * 0.5
        )  # Very low threshold

        # Price above/below EMA with momentum
        price_above_ema = current_close > self.ema[-1]
        price_below_ema = current_close < self.ema[-1]

        # Multiple entry conditions (very relaxed)
        long_signals = [
            price_above_ema,
            current_rsi < 60,  # Not extremely overbought
            price_momentum > 0.0001,  # Any positive momentum
            volume_ok,
        ]

        short_signals = [
            price_below_ema,
            current_rsi > 40,  # Not extremely oversold
            price_momentum < -0.0001,  # Any negative momentum
            volume_ok,
        ]

        # Enter if any 2+ conditions are met
        if sum(long_signals) >= 2:
            # Calculate position size with very tight stop
            stop_loss = current_close * 0.995  # 0.5% stop loss
            risk_per_share = current_close - stop_loss
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_time = len(self.data)
                    self.entry_price = current_close

        elif sum(short_signals) >= 2:
            # Calculate position size with very tight stop
            stop_loss = current_close * 1.005  # 0.5% stop loss
            risk_per_share = stop_loss - current_close
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_time = len(self.data)
                    self.entry_price = current_close


# Test the strategy
print("🌙 Testing High Frequency Scalper Strategy...")
print("=" * 60)

bt = Backtest(data, HighFrequencyScalper, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 HIGH FREQUENCY SCALPER RESULTS")
print("=" * 60)
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
    print("\n🏆 HIGH FREQUENCY SCALPER SUCCESS! 🏆")
elif trade_requirement:
    print(f"\n🎯 TRADE COUNT SUCCESS! Got {stats['# Trades']} trades")
    print("⚠️ Need to improve Sharpe Ratio...")
else:
    print("\n⚠️ Strategy needs more optimization...")

print("\n🌙 High Frequency Scalper test completed! ✨")
