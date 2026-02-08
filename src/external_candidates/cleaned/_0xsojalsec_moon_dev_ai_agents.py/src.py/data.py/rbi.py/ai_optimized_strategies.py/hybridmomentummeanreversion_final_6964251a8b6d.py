# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\HybridMomentumMeanReversion_FINAL.py
# 🌙 Moon Dev's Hybrid Momentum Mean Reversion - FINAL OPTIMIZED VERSION 🌙
# Designed to achieve >100 trades with >2.0 Sharpe ratio

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
    df = df.drop(columns=[col for col in df.columns if "unnamed" in col.lower()], errors="ignore")

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


class HybridMomentumMeanReversionFinal(Strategy):
    """Final optimized hybrid strategy targeting >100 trades and >2.0 Sharpe"""

    # Optimized parameters based on successful strategies analysis
    risk_per_trade = 0.01  # 1% risk per trade

    # Ultra-responsive parameters for high frequency
    ema_fast = 3
    ema_slow = 8
    rsi_period = 7
    rsi_oversold = 45  # Relaxed for more entries
    rsi_overbought = 55  # Relaxed for more entries

    # Profit targets and risk management
    profit_target_ratio = 1.8  # Conservative profit target
    max_hold_bars = 12  # Quick exits for high turnover

    def init(self):
        def ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        def sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        def rsi(values, period=7):
            delta = pd.Series(values).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).values

        def atr(high, low, close, period=10):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            tr1 = h - l
            tr2 = abs(h - c.shift(1))
            tr3 = abs(l - c.shift(1))
            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            return tr.rolling(window=period).mean().values

        # Ultra-responsive indicators
        self.ema_fast_line = self.I(ema, self.data.Close, self.ema_fast)
        self.ema_slow_line = self.I(ema, self.data.Close, self.ema_slow)
        self.rsi = self.I(rsi, self.data.Close, self.rsi_period)
        self.atr = self.I(atr, self.data.High, self.data.Low, self.data.Close, 10)
        self.volume_sma = self.I(sma, self.data.Volume, 8)

        # Bollinger Bands for mean reversion
        self.bb_middle = self.I(sma, self.data.Close, 12)
        bb_std = self.I(lambda: pd.Series(self.data.Close).rolling(12).std().values)
        self.bb_upper = self.I(lambda: self.bb_middle + bb_std * 1.5)  # Tighter bands
        self.bb_lower = self.I(lambda: self.bb_middle - bb_std * 1.5)

        # Trade management
        self.entry_time = None
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None

        print("🌙✨ Hybrid Momentum Mean Reversion FINAL Initialized! ✨")

    def next(self):
        if len(self.data) < self.ema_slow + 1:
            return

        # Handle existing positions
        if self.position:
            self.manage_position()
            return

        # Entry logic - designed for high frequency
        current_close = self.data.Close[-1]

        # Momentum signals
        ema_bullish = self.ema_fast_line[-1] > self.ema_slow_line[-1]
        ema_rising = self.ema_fast_line[-1] > self.ema_fast_line[-2]

        # Mean reversion signals (relaxed)
        rsi_low = self.rsi[-1] < self.rsi_oversold
        rsi_high = self.rsi[-1] > self.rsi_overbought
        near_bb_lower = current_close < self.bb_middle[-1]
        near_bb_upper = current_close > self.bb_middle[-1]

        # Volume filter (very relaxed)
        volume_ok = self.data.Volume[-1] > self.volume_sma[-1] * 0.7

        # Price momentum (additional signal)
        price_momentum = (current_close - self.data.Close[-3]) / self.data.Close[-3]

        # LONG ENTRIES (multiple ways to enter)
        long_conditions = [
            ema_bullish and rsi_low,  # Momentum + oversold
            ema_rising and near_bb_lower,  # Rising trend + below middle
            price_momentum > 0.001 and self.rsi[-1] < 50,  # Price momentum + not overbought
            ema_bullish and current_close > self.bb_lower[-1] * 1.001,  # Above BB lower with trend
        ]

        # SHORT ENTRIES (multiple ways to enter)
        short_conditions = [
            not ema_bullish and rsi_high,  # Bearish momentum + overbought
            not ema_rising and near_bb_upper,  # Falling trend + above middle
            price_momentum < -0.001 and self.rsi[-1] > 50,  # Negative momentum + not oversold
            not ema_bullish and current_close < self.bb_upper[-1] * 0.999,  # Below BB upper with downtrend
        ]

        # Enter if any condition is met (high frequency approach)
        if any(long_conditions) and volume_ok:
            self.enter_long()
        elif any(short_conditions) and volume_ok:
            self.enter_short()

    def enter_long(self):
        """Optimized long entry with tight risk management"""
        entry_price = self.data.Close[-1]

        # Conservative stop loss
        atr_stop = entry_price - (self.atr[-1] * 1.2)  # Tight stop
        bb_stop = self.bb_lower[-1] * 0.998
        stop_loss = max(atr_stop, bb_stop)  # Use tighter stop

        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = int(risk_amount / risk_per_share)

        if position_size > 0:
            # Conservative take profit
            take_profit = entry_price + (risk_per_share * self.profit_target_ratio)

            self.buy(size=position_size)
            self.entry_time = len(self.data)
            self.entry_price = entry_price
            self.take_profit = take_profit
            self.stop_loss = stop_loss

    def enter_short(self):
        """Optimized short entry with tight risk management"""
        entry_price = self.data.Close[-1]

        # Conservative stop loss
        atr_stop = entry_price + (self.atr[-1] * 1.2)  # Tight stop
        bb_stop = self.bb_upper[-1] * 1.002
        stop_loss = min(atr_stop, bb_stop)  # Use tighter stop

        risk_per_share = stop_loss - entry_price
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = int(risk_amount / risk_per_share)

        if position_size > 0:
            # Conservative take profit
            take_profit = entry_price - (risk_per_share * self.profit_target_ratio)

            self.sell(size=position_size)
            self.entry_time = len(self.data)
            self.entry_price = entry_price
            self.take_profit = take_profit
            self.stop_loss = stop_loss

    def manage_position(self):
        """Optimized position management for profitability"""
        current_price = self.data.Close[-1]
        bars_held = len(self.data) - self.entry_time if self.entry_time else 0

        # Quick profit taking
        if self.position.is_long and current_price >= self.take_profit:
            self.position.close()
            self.reset_params()
            return
        elif self.position.is_short and current_price <= self.take_profit:
            self.position.close()
            self.reset_params()
            return

        # Stop loss
        if self.position.is_long and current_price <= self.stop_loss:
            self.position.close()
            self.reset_params()
            return
        elif self.position.is_short and current_price >= self.stop_loss:
            self.position.close()
            self.reset_params()
            return

        # Time exit for high turnover
        if bars_held >= self.max_hold_bars:
            self.position.close()
            self.reset_params()
            return

        # Trail stop when profitable
        if bars_held > 3:  # After a few bars
            if self.position.is_long and current_price > self.entry_price * 1.005:
                new_stop = max(self.stop_loss, current_price * 0.996)  # Trail with 0.4%
                if new_stop > self.stop_loss:
                    self.stop_loss = new_stop

            elif self.position.is_short and current_price < self.entry_price * 0.995:
                new_stop = min(self.stop_loss, current_price * 1.004)  # Trail with 0.4%
                if new_stop < self.stop_loss:
                    self.stop_loss = new_stop

    def reset_params(self):
        """Reset trade parameters"""
        self.entry_time = None
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None


# Test the strategy
print("🌙 Testing Hybrid Momentum Mean Reversion FINAL Strategy...")
print("=" * 70)

bt = Backtest(data, HybridMomentumMeanReversionFinal, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 HYBRID MOMENTUM MEAN REVERSION FINAL RESULTS")
print("=" * 70)
print(f"📊 Total Trades: {stats['# Trades']}")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")

# Check requirements
trade_requirement = stats["# Trades"] > 100
sharpe_requirement = stats["Sharpe Ratio"] > 2.0

print(f"\n✅ FINAL VALIDATION:")
print(f"📊 Trade Count (>100): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats['# Trades']} trades)")
print(f"📈 Sharpe Ratio (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats['Sharpe Ratio']:.2f})")

if trade_requirement and sharpe_requirement:
    print("\n🏆 HYBRID MOMENTUM MEAN REVERSION: FULL SUCCESS! 🏆")
    print("✅ Both requirements met - ready for production!")
elif trade_requirement:
    print(f"\n🎯 PARTIAL SUCCESS: Trade count achieved ({stats['# Trades']} trades)")
    print(f"⚠️ Sharpe ratio needs improvement: {stats['Sharpe Ratio']:.2f}")
else:
    print(f"\n⚠️ NEEDS OPTIMIZATION: {stats['# Trades']} trades, {stats['Sharpe Ratio']:.2f} Sharpe")

print("\n🌙 Hybrid Momentum Mean Reversion FINAL test completed! ✨")
