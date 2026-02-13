# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\final_working_strategies.py
# 🌙 Moon Dev's Final Working AI-Optimized Strategies 🌙
# Three strategies designed to meet both >100 trades and >2.0 Sharpe requirements

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


class HybridMomentumMeanReversion(Strategy):
    """Strategy 1: Momentum + Mean Reversion with tight risk management"""

    risk_per_trade = 0.008  # Slightly lower risk for better Sharpe

    def init(self):
        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        def ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        def rsi(values, period=9):
            delta = pd.Series(values).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).values

        # Short-term responsive indicators
        self.sma_fast = self.I(sma, self.data.Close, 5)
        self.sma_slow = self.I(sma, self.data.Close, 15)
        self.rsi = self.I(rsi, self.data.Close, 9)
        self.volume_sma = self.I(sma, self.data.Volume, 10)

        # Price change momentum
        self.returns = self.I(lambda: pd.Series(self.data.Close).pct_change(3).values)

        self.entry_time = None

    def next(self):
        if len(self.data) < 20:
            return

        # Force exit after 8 bars for high turnover
        if self.position:
            bars_held = len(self.data) - self.entry_time if self.entry_time else 0
            if bars_held >= 8:
                self.position.close()
                self.entry_time = None
            return

        # Simple but effective conditions
        current_close = self.data.Close[-1]

        # Trend following with mean reversion timing
        trend_up = self.sma_fast[-1] > self.sma_slow[-1]
        trend_down = self.sma_fast[-1] < self.sma_slow[-1]

        # RSI for entry timing (relaxed)
        rsi_low = self.rsi[-1] < 45
        rsi_high = self.rsi[-1] > 55

        # Volume confirmation (very relaxed)
        volume_ok = self.data.Volume[-1] > self.volume_sma[-1] * 0.8

        # Momentum confirmation
        momentum_positive = self.returns[-1] > 0.002  # 0.2% over 3 bars
        momentum_negative = self.returns[-1] < -0.002

        # Entry logic (multiple paths)
        if (trend_up and rsi_low and volume_ok) or (
            momentum_positive and self.rsi[-1] < 50
        ):
            # Conservative position sizing
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.02)
            )  # 2% risk per share
            if position_size > 0:
                self.buy(size=position_size)
                self.entry_time = len(self.data)

        elif (trend_down and rsi_high and volume_ok) or (
            momentum_negative and self.rsi[-1] > 50
        ):
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.02)
            )
            if position_size > 0:
                self.sell(size=position_size)
                self.entry_time = len(self.data)


class VolatilityBreakoutScalper(Strategy):
    """Strategy 2: Quick volatility breakout scalping"""

    risk_per_trade = 0.008

    def init(self):
        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # Bollinger Bands for breakouts
        self.bb_middle = self.I(sma, self.data.Close, 10)
        bb_std = self.I(lambda: pd.Series(self.data.Close).rolling(10).std().values)
        self.bb_upper = self.I(lambda: self.bb_middle + bb_std * 1.5)
        self.bb_lower = self.I(lambda: self.bb_middle - bb_std * 1.5)

        # Volume
        self.volume_sma = self.I(sma, self.data.Volume, 8)

        # Price velocity
        self.velocity = self.I(lambda: pd.Series(self.data.Close).diff(2).values)

        self.entry_time = None

    def next(self):
        if len(self.data) < 15:
            return

        # Very quick exits for scalping
        if self.position:
            bars_held = len(self.data) - self.entry_time if self.entry_time else 0
            if bars_held >= 5:  # Very quick exits
                self.position.close()
                self.entry_time = None
            return

        current_close = self.data.Close[-1]

        # Breakout conditions
        breaking_upper = current_close > self.bb_upper[-1]
        breaking_lower = current_close < self.bb_lower[-1]

        # Volume surge
        volume_surge = self.data.Volume[-1] > self.volume_sma[-1] * 1.3

        # Price momentum
        strong_velocity = (
            abs(self.velocity[-1]) > current_close * 0.003
        )  # 0.3% movement

        if breaking_upper and (volume_surge or strong_velocity):
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.015)
            )  # 1.5% risk
            if position_size > 0:
                self.buy(size=position_size)
                self.entry_time = len(self.data)

        elif breaking_lower and (volume_surge or strong_velocity):
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.015)
            )
            if position_size > 0:
                self.sell(size=position_size)
                self.entry_time = len(self.data)


class AdaptiveTrendFollower(Strategy):
    """Strategy 3: Adaptive trend following with regime detection"""

    risk_per_trade = 0.01

    def init(self):
        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        def ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        # Multi-timeframe trend detection
        self.ema_short = self.I(ema, self.data.Close, 8)
        self.ema_medium = self.I(ema, self.data.Close, 21)
        self.ema_long = self.I(ema, self.data.Close, 55)

        # Volatility measurement
        self.volatility = self.I(
            lambda: pd.Series(self.data.Close).rolling(10).std().values
        )
        self.vol_avg = self.I(sma, self.volatility, 20)

        # Volume
        self.volume_sma = self.I(sma, self.data.Volume, 15)

        self.entry_time = None

    def next(self):
        if len(self.data) < 60:
            return

        # Adaptive hold time based on trend strength
        if self.position:
            bars_held = len(self.data) - self.entry_time if self.entry_time else 0

            # Stronger trends = longer holds, weaker trends = quick exits
            trend_strength = (
                abs(self.ema_short[-1] - self.ema_long[-1]) / self.ema_long[-1]
            )
            max_hold = max(
                6, min(20, int(trend_strength * 500))
            )  # 6-20 bars based on strength

            if bars_held >= max_hold:
                self.position.close()
                self.entry_time = None
            return

        # Trend alignment
        strong_uptrend = self.ema_short[-1] > self.ema_medium[-1] > self.ema_long[-1]
        strong_downtrend = self.ema_short[-1] < self.ema_medium[-1] < self.ema_long[-1]

        # Volatility regime
        current_vol = self.volatility[-1]
        avg_vol = self.vol_avg[-1]
        high_vol_regime = current_vol > avg_vol * 1.2

        # Volume confirmation
        volume_ok = self.data.Volume[-1] > self.volume_sma[-1] * 0.9

        # Momentum confirmation
        price_momentum = (self.data.Close[-1] - self.data.Close[-5]) / self.data.Close[
            -5
        ]

        current_close = self.data.Close[-1]

        # Entry conditions adapted to volatility regime
        if high_vol_regime:
            # In high volatility, be more selective
            momentum_threshold = 0.005  # 0.5%
        else:
            # In low volatility, be more aggressive
            momentum_threshold = 0.002  # 0.2%

        if strong_uptrend and price_momentum > momentum_threshold and volume_ok:
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.025)
            )  # 2.5% risk
            if position_size > 0:
                self.buy(size=position_size)
                self.entry_time = len(self.data)

        elif strong_downtrend and price_momentum < -momentum_threshold and volume_ok:
            position_size = int(
                self.equity * self.risk_per_trade / (current_close * 0.025)
            )
            if position_size > 0:
                self.sell(size=position_size)
                self.entry_time = len(self.data)


def test_strategy(strategy_class, strategy_name):
    """Test a strategy and return results"""
    print(f"\n🌙 Testing {strategy_name}...")
    print("=" * 60)

    bt = Backtest(data, strategy_class, cash=1000000, commission=0.002)
    stats = bt.run()

    print(f"📊 Total Trades: {stats['# Trades']}")
    print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
    print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")

    # Check requirements
    trade_req = stats["# Trades"] > 100
    sharpe_req = stats["Sharpe Ratio"] > 2.0

    print(f"\n✅ VALIDATION:")
    print(
        f"📊 Trades (>100): {'✅ PASS' if trade_req else '❌ FAIL'} ({stats['# Trades']})"
    )
    print(
        f"📈 Sharpe (>2.0): {'✅ PASS' if sharpe_req else '❌ FAIL'} ({stats['Sharpe Ratio']:.2f})"
    )

    if trade_req and sharpe_req:
        print(f"🏆 {strategy_name}: FULL SUCCESS! 🏆")
    elif trade_req:
        print(f"🎯 {strategy_name}: Trade count achieved, Sharpe needs work")
    else:
        print(f"⚠️ {strategy_name}: Needs optimization")

    return {
        "name": strategy_name,
        "trades": stats["# Trades"],
        "return": stats["Return [%]"],
        "sharpe": stats["Sharpe Ratio"],
        "drawdown": stats["Max. Drawdown [%]"],
        "win_rate": stats["Win Rate [%]"],
        "success": trade_req and sharpe_req,
    }


# Test all three strategies
print("🌙" + "=" * 70 + "🌙")
print("                  FINAL AI-OPTIMIZED STRATEGIES TEST")
print("🌙" + "=" * 70 + "🌙")

strategies = [
    (HybridMomentumMeanReversion, "Hybrid Momentum Mean Reversion"),
    (VolatilityBreakoutScalper, "Volatility Breakout Scalper"),
    (AdaptiveTrendFollower, "Adaptive Trend Follower"),
]

results = []
for strategy_class, name in strategies:
    result = test_strategy(strategy_class, name)
    results.append(result)

# Summary
print(f"\n🌙 FINAL SUMMARY REPORT")
print("=" * 70)

successful = [r for r in results if r["success"]]
print(f"✅ Successful Strategies: {len(successful)}/3")

if successful:
    print(f"\n🏆 SUCCESS STORIES:")
    for r in successful:
        print(f"   ✅ {r['name']}: {r['trades']} trades, {r['sharpe']:.2f} Sharpe")

print(f"\n📊 DETAILED RESULTS:")
for r in results:
    status = "✅ SUCCESS" if r["success"] else "❌ NEEDS WORK"
    print(f"{r['name']}: {r['trades']} trades, {r['sharpe']:.2f} Sharpe - {status}")

print(f"\n🌙 All strategies tested successfully! ✨")
