# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\HybridMomentumMeanReversion_BT.py
# 🌙 Moon Dev's Hybrid Momentum Mean Reversion Strategy 🌙
# AI-Optimized Strategy for High Trade Count and Superior Risk-Adjusted Returns

import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

warnings.filterwarnings("ignore")

# 🌙 Data Loading with Adaptive Header Detection
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def load_btc_data(file_path):
    """Load and prepare BTC data with adaptive header detection"""
    try:
        # Try reading with header first
        df = pd.read_csv(file_path)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Remove unnamed columns
        df = df.drop(
            columns=[col for col in df.columns if "unnamed" in col.lower()],
            errors="ignore",
        )

        # Standardize column names
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

        # Convert datetime and set as index
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")

        # Ensure OHLCV columns exist
        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Required column {col} not found")

        # Clean data
        df = df[required_cols].dropna()
        df = df[df > 0]  # Remove zero/negative values

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        raise


# Load the data
data = load_btc_data(data_path)


class HybridMomentumMeanReversion(Strategy):
    """
    🌙 HYBRID MOMENTUM MEAN REVERSION STRATEGY 🌙

    Combines momentum trend detection with mean reversion entries for optimal trade frequency.

    Strategy Logic:
    - Uses momentum indicators (EMA, MACD) to identify trend direction
    - Employs mean reversion signals (RSI, Bollinger Bands) for precise entry timing
    - High frequency trading approach with 1% risk management
    - Multiple exit conditions for risk control and profit optimization
    """

    # Optimized parameters for high trade frequency and good risk-adjusted returns
    risk_per_trade = 0.01  # 1% risk per trade

    # Momentum parameters (shorter periods for more signals)
    ema_fast = 8
    ema_slow = 21
    macd_fast = 8
    macd_slow = 21
    macd_signal = 6

    # Mean reversion parameters
    rsi_period = 9  # Shorter RSI for more signals
    rsi_oversold = 35  # Relaxed thresholds
    rsi_overbought = 65
    bb_period = 15  # Shorter BB period
    bb_std = 1.8  # Slightly tighter bands

    # Volume and volatility filters
    volume_period = 10
    atr_period = 12
    atr_multiplier = 1.5

    def init(self):
        # Custom indicator functions
        def ema(values, period):
            """Exponential Moving Average"""
            return pd.Series(values).ewm(span=period).mean().values

        def sma(values, period):
            """Simple Moving Average"""
            return pd.Series(values).rolling(window=period).mean().values

        def rsi(values, period=14):
            """Relative Strength Index"""
            delta = pd.Series(values).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).values

        def atr(high, low, close, period=14):
            """Average True Range"""
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            tr1 = h - l
            tr2 = abs(h - c.shift(1))
            tr3 = abs(l - c.shift(1))
            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            return tr.rolling(window=period).mean().values

        def macd(values, fast=12, slow=26, signal=9):
            """MACD Histogram"""
            close = pd.Series(values)
            ema_fast = close.ewm(span=fast).mean()
            ema_slow = close.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            return histogram.values

        def stoch_k(high, low, close, k_period=14):
            """Stochastic %K"""
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            lowest_low = l.rolling(window=k_period).min()
            highest_high = h.rolling(window=k_period).max()
            k_percent = 100 * ((c - lowest_low) / (highest_high - lowest_low))
            return k_percent.values

        def bollinger_bands(values, period=20, std_dev=2):
            """Bollinger Bands"""
            close = pd.Series(values)
            sma = close.rolling(window=period).mean()
            std = close.rolling(window=period).std()
            upper = sma + (std * std_dev)
            lower = sma - (std * std_dev)
            return upper.values, sma.values, lower.values

        # Momentum Indicators
        self.ema_fast_line = self.I(ema, self.data.Close, self.ema_fast)
        self.ema_slow_line = self.I(ema, self.data.Close, self.ema_slow)

        # MACD
        self.macd_hist = self.I(macd, self.data.Close, self.macd_fast, self.macd_slow, self.macd_signal)

        # Mean Reversion Indicators
        self.rsi = self.I(rsi, self.data.Close, self.rsi_period)

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = bollinger_bands(self.data.Close, self.bb_period, self.bb_std)
        self.bb_upper = self.I(lambda: bb_upper)
        self.bb_middle = self.I(lambda: bb_middle)
        self.bb_lower = self.I(lambda: bb_lower)

        # Volume and Volatility
        self.volume_sma = self.I(sma, self.data.Volume, self.volume_period)
        self.atr = self.I(atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)

        # Stochastic for additional mean reversion signal
        stoch_k_values = stoch_k(self.data.High, self.data.Low, self.data.Close, 9)
        self.stoch_k = self.I(lambda: stoch_k_values)
        self.stoch_d = self.I(sma, stoch_k_values, 3)  # %D is 3-period SMA of %K

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None

        print("🌙✨ Hybrid Momentum Mean Reversion Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.ema_slow, self.bb_period, self.rsi_period) + 1:
            return

        # Handle existing positions
        if self.position:
            self.manage_position()
            return

        # Check for new entry signals
        self.check_entry_signals()

    def check_entry_signals(self):
        """Check for hybrid momentum + mean reversion entry signals"""

        # Current values
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Momentum conditions
        ema_bullish = self.ema_fast_line[-1] > self.ema_slow_line[-1]
        ema_trend_strong = self.ema_fast_line[-1] > self.ema_fast_line[-2]  # EMA rising
        macd_bullish = self.macd_hist[-1] > 0  # MACD histogram above zero
        macd_improving = self.macd_hist[-1] > self.macd_hist[-2]

        # Mean reversion conditions (oversold in uptrend)
        rsi_oversold = self.rsi[-1] < self.rsi_oversold
        rsi_recovering = self.rsi[-1] > self.rsi[-2]  # RSI starting to recover
        bb_oversold = current_close < self.bb_lower[-1]
        bb_bounce = current_close > self.data.Low[-1]  # Price bouncing from low
        stoch_oversold = self.stoch_k[-1] < 25
        stoch_recovering = self.stoch_k[-1] > self.stoch_d[-1]  # K crossing above D

        # Volume confirmation
        volume_above_avg = current_volume > self.volume_sma[-1] * 0.8  # Relaxed volume filter

        # Volatility filter
        current_atr = self.atr[-1]
        atr_suitable = current_atr > np.nanmean(self.atr[-10:]) * 0.7  # Ensure some volatility

        # Hybrid entry conditions (momentum trend + mean reversion entry)
        # Long entries: Bullish momentum trend + oversold mean reversion signal
        momentum_bullish = (ema_bullish and ema_trend_strong) or (macd_bullish and macd_improving)
        mean_reversion_long = (
            (rsi_oversold and rsi_recovering) or (bb_oversold and bb_bounce) or (stoch_oversold and stoch_recovering)
        )

        # Short entries: Bearish momentum trend + overbought mean reversion signal
        momentum_bearish = (not ema_bullish and not ema_trend_strong) or (not macd_bullish and not macd_improving)
        rsi_overbought = self.rsi[-1] > self.rsi_overbought
        rsi_declining = self.rsi[-1] < self.rsi[-2]
        bb_overbought = current_close > self.bb_upper[-1]
        bb_rejection = current_close < self.data.High[-1]
        stoch_overbought = self.stoch_k[-1] > 75
        stoch_declining = self.stoch_k[-1] < self.stoch_d[-1]
        mean_reversion_short = (
            (rsi_overbought and rsi_declining)
            or (bb_overbought and bb_rejection)
            or (stoch_overbought and stoch_declining)
        )

        # Execute trades
        if momentum_bullish and mean_reversion_long and volume_above_avg and atr_suitable:
            self.enter_long()
        elif momentum_bearish and mean_reversion_short and volume_above_avg and atr_suitable:
            self.enter_short()

    def enter_long(self):
        """Enter long position with risk management"""
        entry_price = self.data.Close[-1]

        # Dynamic stop loss: Use ATR or recent swing low
        atr_stop = entry_price - (self.atr[-1] * self.atr_multiplier)
        bb_stop = self.bb_lower[-1] * 0.995  # Slightly below BB lower
        swing_low = min(self.data.Low[-5:]) * 0.999  # Recent 5-bar low

        stop_loss = max(atr_stop, bb_stop, swing_low)  # Use the highest (closest) stop

        # Risk per share
        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Take profit: Dynamic based on ATR and R:R ratio
            reward_ratio = 2.0  # 2:1 reward to risk
            take_profit = entry_price + (risk_per_share * reward_ratio)

            # Adjust TP based on BB upper
            bb_target = self.bb_upper[-1]
            if bb_target < take_profit:
                take_profit = bb_target * 0.999  # Take profit near BB upper

            self.buy(size=position_size)

            # Store trade parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)

            print(f"🚀 LONG ENTRY: Size={position_size} @ {entry_price:.2f}")
            print(f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | R:R: {reward_ratio:.1f}")

    def enter_short(self):
        """Enter short position with risk management"""
        entry_price = self.data.Close[-1]

        # Dynamic stop loss for short
        atr_stop = entry_price + (self.atr[-1] * self.atr_multiplier)
        bb_stop = self.bb_upper[-1] * 1.005  # Slightly above BB upper
        swing_high = max(self.data.High[-5:]) * 1.001  # Recent 5-bar high

        stop_loss = min(atr_stop, bb_stop, swing_high)  # Use the lowest (closest) stop

        # Risk per share
        risk_per_share = stop_loss - entry_price
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Take profit
            reward_ratio = 2.0
            take_profit = entry_price - (risk_per_share * reward_ratio)

            # Adjust TP based on BB lower
            bb_target = self.bb_lower[-1]
            if bb_target > take_profit:
                take_profit = bb_target * 1.001

            self.sell(size=position_size)

            # Store trade parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)

            print(f"📉 SHORT ENTRY: Size={position_size} @ {entry_price:.2f}")
            print(f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | R:R: {reward_ratio:.1f}")

    def manage_position(self):
        """Manage existing positions with multiple exit conditions"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)

        # Take profit
        if self.position.is_long and current_price >= self.take_profit:
            self.position.close()
            print(f"🎯 LONG TP HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price <= self.take_profit:
            self.position.close()
            print(f"🎯 SHORT TP HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Stop loss
        if self.position.is_long and current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑 LONG SL HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price >= self.stop_loss:
            self.position.close()
            print(f"🛑 SHORT SL HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Time-based exit (25 bars for quick turnover)
        if current_time - self.entry_time > 25:
            self.position.close()
            print(f"⏰ TIME EXIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Momentum reversal exit
        if self.position.is_long:
            # Exit long if momentum turns bearish
            if (
                self.ema_fast_line[-1] < self.ema_slow_line[-1]
                or self.macd_hist[-1] < self.macd_hist[-2] < self.macd_hist[-3]
                or self.rsi[-1] > self.rsi_overbought
            ):
                self.position.close()
                print(f"🔄 LONG MOMENTUM EXIT @ {current_price:.2f}")
                self.reset_trade_params()
                return

        elif self.position.is_short:
            # Exit short if momentum turns bullish
            if (
                self.ema_fast_line[-1] > self.ema_slow_line[-1]
                or self.macd_hist[-1] > self.macd_hist[-2] > self.macd_hist[-3]
                or self.rsi[-1] < self.rsi_oversold
            ):
                self.position.close()
                print(f"🔄 SHORT MOMENTUM EXIT @ {current_price:.2f}")
                self.reset_trade_params()
                return

        # Trailing stop (only when profitable)
        if self.position.is_long and current_price > self.entry_price * 1.005:  # 0.5% profit
            new_stop = max(self.stop_loss, current_price * 0.995)  # 0.5% trailing
            if new_stop > self.stop_loss:
                self.stop_loss = new_stop

        elif self.position.is_short and current_price < self.entry_price * 0.995:  # 0.5% profit
            new_stop = min(self.stop_loss, current_price * 1.005)  # 0.5% trailing
            if new_stop < self.stop_loss:
                self.stop_loss = new_stop

    def reset_trade_params(self):
        """Reset trade management parameters"""
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None


# Run Default Backtest
print("🌙 Starting Hybrid Momentum Mean Reversion Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, HybridMomentumMeanReversion, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 HYBRID MOMENTUM MEAN REVERSION - DEFAULT RESULTS")
print("=" * 80)
print(stats)

print(f"\n⭐ KEY METRICS:")
print(f"📊 Total Trades: {stats['# Trades']}")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")

# Run Optimization
print(f"\n🔄 Running Parameter Optimization...")
print("=" * 80)

stats_opt = bt.optimize(
    ema_fast=range(5, 12, 2),
    ema_slow=range(18, 25, 2),
    rsi_period=range(7, 12, 2),
    rsi_oversold=range(30, 40, 3),
    rsi_overbought=range(65, 75, 3),
    bb_period=range(12, 18, 2),
    atr_multiplier=[1.2, 1.5, 1.8, 2.0],
    maximize="Sharpe Ratio",
    constraint=lambda p: p["# Trades"] > 100 and p["Return [%]"] > 0,
)

print("\n🌙 HYBRID MOMENTUM MEAN REVERSION - OPTIMIZED RESULTS")
print("=" * 80)
print(stats_opt)

print(f"\n🚀 OPTIMIZED METRICS:")
print(f"📊 Total Trades: {stats_opt['# Trades']}")
print(f"💰 Total Return: {stats_opt['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats_opt['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats_opt['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats_opt['Win Rate [%]']:.2f}%")

# Success metrics check
trade_requirement = stats_opt["# Trades"] > 100
sharpe_requirement = stats_opt["Sharpe Ratio"] > 2.0

print(f"\n✅ STRATEGY VALIDATION:")
print(
    f"📊 Trade Count Requirement (>100): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats_opt['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio Requirement (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats_opt['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 HYBRID MOMENTUM MEAN REVERSION STRATEGY: SUCCESS! 🏆")
else:
    print("\n⚠️ Strategy needs further optimization...")

print("\n🌙 Hybrid Momentum Mean Reversion backtest completed! ✨")
