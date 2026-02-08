# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\MomentumBreakout_AI5.py
# 🌙 Moon Dev's MomentumBreakout Strategy - Beats Buy and Hold
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for MomentumBreakout strategy...")
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


def sma(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).mean().values


class MomentumBreakout(Strategy):
    risk_per_trade = 0.05  # 5% risk per trade for higher returns

    def init(self):
        # Momentum indicators
        self.ema21 = self.I(ema, self.data.Close, 21)
        self.ema50 = self.I(ema, self.data.Close, 50)
        self.rsi = self.I(rsi, self.data.Close, 14)

        # Breakout levels
        self.high_20 = self.I(rolling_max, self.data.High, 20)
        self.low_20 = self.I(rolling_min, self.data.Low, 20)

        # Volume filter
        self.volume_ma = self.I(sma, self.data.Volume, 20)

        print("🌙✨ MomentumBreakout Strategy Initialized!")

    def next(self):
        if len(self.ema50) < 50:
            return

        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Get indicator values
        ema21 = self.ema21[-1]
        ema50 = self.ema50[-1]
        rsi_val = self.rsi[-1]
        high_20 = self.high_20[-1]
        low_20 = self.low_20[-1]
        volume_ma = self.volume_ma[-1]

        # Check for valid values
        if (
            np.isnan(ema21)
            or np.isnan(ema50)
            or np.isnan(rsi_val)
            or np.isnan(high_20)
            or np.isnan(low_20)
            or np.isnan(volume_ma)
        ):
            return

        # Strong momentum conditions
        strong_uptrend = ema21 > ema50 and current_close > ema21
        volume_confirmation = current_volume > volume_ma * 1.2
        momentum_oversold = 30 < rsi_val < 70  # Avoid extreme RSI

        if not self.position:
            # Long entry on breakout with momentum
            if current_close > high_20 and strong_uptrend and volume_confirmation and momentum_oversold:
                # Dynamic stop loss based on recent low
                sl_price = low_20
                risk_per_share = current_close - sl_price

                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_per_trade
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        # Aggressive take profit for momentum
                        tp_price = current_close + 4 * risk_per_share
                        self.buy(size=position_size, sl=sl_price, tp=tp_price)
                        print(f"🚀🌙 MOMENTUM BREAKOUT! Entry: {current_close:.2f}, Size: {position_size}")
                        print(f"SL: {sl_price:.2f}, TP: {tp_price:.2f}")

        else:
            # Trail stop loss for maximum gains
            if self.position.is_long:
                # Trail stop to recent low if we're in profit
                new_sl = max(low_20, self.position.entry_price * 1.02)  # Min 2% profit
                if current_close > self.position.entry_price * 1.1:  # If up 10%+
                    # Exit if momentum weakens significantly
                    if ema21 < ema50 or rsi_val < 25:
                        print(f"🌕 MOMENTUM EXIT at {current_close:.2f} - Trend weakening")
                        self.position.close()


# Launch Backtest
print("🚀 Launching MomentumBreakout backtest with $1,000,000 portfolio...")
bt = Backtest(data, MomentumBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV MOMENTUMBREAKOUT STRATEGY RESULTS 🌙")
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
