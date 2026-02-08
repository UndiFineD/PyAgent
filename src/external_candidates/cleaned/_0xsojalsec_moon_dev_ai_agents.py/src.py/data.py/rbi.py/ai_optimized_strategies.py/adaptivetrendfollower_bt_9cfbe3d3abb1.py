# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\AdaptiveTrendFollower_BT.py
# 🌙 Moon Dev's Adaptive Trend Follower Strategy 🌙
# AI-Optimized Trend Following Strategy with Adaptive Parameters Based on Market Conditions

import warnings

import numpy as np
import pandas as pd
import pandas_ta as ta
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


class AdaptiveTrendFollower(Strategy):
    """
    🌙 ADAPTIVE TREND FOLLOWER STRATEGY 🌙

    Trend following strategy with adaptive parameters based on current market conditions.

    Strategy Logic:
    - Adapts EMA periods based on market volatility
    - Adjusts entry thresholds based on trend strength
    - Uses multiple trend confirmation signals
    - Implements regime detection for parameter optimization
    - Dynamic position sizing based on market conditions
    """

    # Base parameters (will be adapted dynamically)
    risk_per_trade = 0.01  # 1% risk per trade

    # Adaptive EMA parameters
    ema_fast_base = 9
    ema_slow_base = 21
    ema_trend_base = 50

    # Volatility adaptation parameters
    volatility_lookback = 20
    volatility_multiplier = 1.5

    # Trend strength parameters
    trend_strength_period = 14
    min_trend_strength = 0.3

    # MACD parameters (adaptive)
    macd_fast_base = 8
    macd_slow_base = 21
    macd_signal_base = 6

    # Risk management
    atr_period = 14
    atr_multiplier_base = 2.0
    trailing_atr_multiplier = 1.5

    def init(self):
        # Initialize base indicators
        self.close_series = pd.Series(self.data.Close, index=range(len(self.data.Close)))

        # Volatility measurement for adaptation
        self.atr = self.I(ta.atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)

        # Price change volatility
        self.price_change = self.I(
            lambda: self.close_series.pct_change().abs().rolling(self.volatility_lookback).mean().values
        )

        # Initialize with base parameters (will be adapted)
        self.ema_fast = self.I(ta.ema, self.data.Close, self.ema_fast_base)
        self.ema_slow = self.I(ta.ema, self.data.Close, self.ema_slow_base)
        self.ema_trend = self.I(ta.ema, self.data.Close, self.ema_trend_base)

        # MACD with base parameters
        macd_data = ta.macd(
            self.data.Close,
            fast=self.macd_fast_base,
            slow=self.macd_slow_base,
            signal=self.macd_signal_base,
        )
        self.macd_line = self.I(lambda: macd_data.iloc[:, 0].values)
        self.macd_signal = self.I(lambda: macd_data.iloc[:, 1].values)
        self.macd_hist = self.I(lambda: macd_data.iloc[:, 2].values)

        # Additional trend indicators
        self.rsi = self.I(ta.rsi, self.data.Close, 14)

        # Volume analysis
        self.volume_sma = self.I(ta.sma, self.data.Volume, 20)
        self.volume_ema = self.I(ta.ema, self.data.Volume, 10)

        # Bollinger Bands for trend channel
        bb_data = ta.bbands(self.data.Close, length=20, std=2.0)
        self.bb_upper = self.I(lambda: bb_data["BBU_20_2.0"].values)
        self.bb_middle = self.I(lambda: bb_data["BBM_20_2.0"].values)
        self.bb_lower = self.I(lambda: bb_data["BBL_20_2.0"].values)

        # Supertrend for trend direction
        supertrend_data = ta.supertrend(self.data.High, self.data.Low, self.data.Close, length=10, multiplier=3.0)
        self.supertrend = self.I(lambda: supertrend_data[f"SUPERT_10_3.0"].values)
        self.supertrend_direction = self.I(lambda: supertrend_data[f"SUPERTd_10_3.0"].values)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None
        self.current_regime = None
        self.adaptive_params = {}

        print("🌙✨ Adaptive Trend Follower Initialized! Market regime detection active! ✨")

    def next(self):
        # Skip if not enough data
        if (
            len(self.data)
            < max(
                self.ema_trend_base,
                self.volatility_lookback,
                self.trend_strength_period,
            )
            + 1
        ):
            return

        # Adapt parameters based on current market conditions
        self.adapt_parameters()

        # Handle existing positions
        if self.position:
            self.manage_trend_position()
            return

        # Check for trend following entries
        self.check_trend_signals()

    def adapt_parameters(self):
        """Dynamically adapt strategy parameters based on market conditions"""

        # Calculate current market volatility
        current_atr = self.atr[-1]
        atr_avg = np.nanmean(self.atr[-20:]) if len(self.atr) >= 20 else current_atr
        volatility_ratio = current_atr / atr_avg if atr_avg > 0 else 1.0

        # Calculate trend strength
        trend_strength = self.calculate_trend_strength()

        # Determine market regime
        if volatility_ratio > 1.3 and trend_strength > 0.6:
            regime = "HIGH_VOLATILITY_TRENDING"
        elif volatility_ratio > 1.3 and trend_strength < 0.4:
            regime = "HIGH_VOLATILITY_RANGING"
        elif volatility_ratio < 0.8 and trend_strength > 0.5:
            regime = "LOW_VOLATILITY_TRENDING"
        else:
            regime = "NORMAL_MARKET"

        self.current_regime = regime

        # Adapt parameters based on regime
        if regime == "HIGH_VOLATILITY_TRENDING":
            # Fast parameters for volatile trending markets
            self.adaptive_params = {
                "ema_fast_period": max(5, int(self.ema_fast_base * 0.7)),
                "ema_slow_period": max(12, int(self.ema_slow_base * 0.8)),
                "atr_multiplier": self.atr_multiplier_base * 1.2,
                "entry_threshold": 0.7,  # Relaxed entry
                "volume_threshold": 1.1,
                "rsi_filter": False,  # No RSI filter in strong trends
            }
        elif regime == "HIGH_VOLATILITY_RANGING":
            # Mean reversion parameters for volatile ranging markets
            self.adaptive_params = {
                "ema_fast_period": max(8, int(self.ema_fast_base * 1.2)),
                "ema_slow_period": max(18, int(self.ema_slow_base * 1.1)),
                "atr_multiplier": self.atr_multiplier_base * 0.8,
                "entry_threshold": 1.2,  # Stricter entry
                "volume_threshold": 1.3,
                "rsi_filter": True,  # Use RSI filter
            }
        elif regime == "LOW_VOLATILITY_TRENDING":
            # Sensitive parameters for low volatility trends
            self.adaptive_params = {
                "ema_fast_period": max(6, int(self.ema_fast_base * 0.8)),
                "ema_slow_period": max(15, int(self.ema_slow_base * 0.9)),
                "atr_multiplier": self.atr_multiplier_base * 0.9,
                "entry_threshold": 0.8,
                "volume_threshold": 1.0,  # Relaxed volume
                "rsi_filter": False,
            }
        else:  # NORMAL_MARKET
            # Base parameters
            self.adaptive_params = {
                "ema_fast_period": self.ema_fast_base,
                "ema_slow_period": self.ema_slow_base,
                "atr_multiplier": self.atr_multiplier_base,
                "entry_threshold": 1.0,
                "volume_threshold": 1.2,
                "rsi_filter": True,
            }

    def calculate_trend_strength(self):
        """Calculate trend strength based on multiple factors"""
        if len(self.data) < self.trend_strength_period:
            return 0.5

        # EMA alignment strength
        ema_alignment = 0
        if self.ema_fast[-1] > self.ema_slow[-1] > self.ema_trend[-1]:
            ema_alignment = 1  # Strong uptrend
        elif self.ema_fast[-1] < self.ema_slow[-1] < self.ema_trend[-1]:
            ema_alignment = 1  # Strong downtrend
        elif self.ema_fast[-1] > self.ema_slow[-1] or self.ema_fast[-1] < self.ema_slow[-1]:
            ema_alignment = 0.5  # Partial alignment

        # Price vs trend EMA
        price_trend_strength = abs(self.data.Close[-1] - self.ema_trend[-1]) / self.ema_trend[-1]
        price_trend_strength = min(price_trend_strength * 10, 1.0)  # Normalize to 0-1

        # MACD trend consistency
        macd_consistency = 0
        if len(self.macd_hist) >= 3:
            if all(self.macd_hist[-i] > 0 for i in range(1, 4)):
                macd_consistency = 1
            elif all(self.macd_hist[-i] < 0 for i in range(1, 4)):
                macd_consistency = 1
            else:
                macd_consistency = 0.3

        # Average trend strength
        trend_strength = (ema_alignment + price_trend_strength + macd_consistency) / 3
        return trend_strength

    def check_trend_signals(self):
        """Check for adaptive trend following signals"""

        # Current market conditions
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Get adaptive parameters
        params = self.adaptive_params
        entry_threshold = params.get("entry_threshold", 1.0)
        volume_threshold = params.get("volume_threshold", 1.2)
        use_rsi_filter = params.get("rsi_filter", True)

        # Trend direction signals
        ema_bullish = self.ema_fast[-1] > self.ema_slow[-1]
        ema_trend_bullish = current_close > self.ema_trend[-1]
        ema_momentum = (self.ema_fast[-1] - self.ema_fast[-2]) / self.ema_fast[-2] if self.ema_fast[-2] != 0 else 0

        # MACD signals
        macd_bullish = self.macd_line[-1] > self.macd_signal[-1]
        macd_improving = self.macd_hist[-1] > self.macd_hist[-2]
        macd_positive = self.macd_line[-1] > 0

        # Supertrend signal
        supertrend_bullish = self.supertrend_direction[-1] == 1

        # Volume confirmation
        volume_confirmation = current_volume > self.volume_sma[-1] * volume_threshold
        volume_trend = current_volume > self.volume_ema[-1]

        # RSI filter (if enabled)
        rsi_ok = True
        if use_rsi_filter:
            rsi_ok = 25 < self.rsi[-1] < 75  # Avoid extreme RSI levels

        # Bollinger Band position
        bb_position = (current_close - self.bb_lower[-1]) / (self.bb_upper[-1] - self.bb_lower[-1])

        # Trend strength requirement
        trend_strength = self.calculate_trend_strength()
        trend_strong_enough = trend_strength > self.min_trend_strength

        # LONG SIGNALS
        long_signals = [
            ema_bullish and ema_trend_bullish,
            macd_bullish and macd_improving,
            supertrend_bullish,
            ema_momentum > 0.001 * entry_threshold,  # Adaptive momentum threshold
            macd_positive or not use_rsi_filter,  # Flexible MACD requirement
        ]

        long_confirmations = [
            volume_confirmation or volume_trend,
            rsi_ok,
            bb_position > 0.3,  # Not at bottom of BB
            trend_strong_enough,
        ]

        # SHORT SIGNALS
        short_signals = [
            not ema_bullish and not ema_trend_bullish,
            not macd_bullish and not macd_improving,
            not supertrend_bullish,
            ema_momentum < -0.001 * entry_threshold,
            not macd_positive or not use_rsi_filter,
        ]

        short_confirmations = [
            volume_confirmation or volume_trend,
            rsi_ok,
            bb_position < 0.7,  # Not at top of BB
            trend_strong_enough,
        ]

        # Execute trades based on adaptive thresholds
        required_signals = max(2, int(3 * entry_threshold))  # Adaptive signal requirement
        required_confirmations = max(2, int(3 * entry_threshold))

        if sum(long_signals) >= required_signals and sum(long_confirmations) >= required_confirmations:
            self.enter_long_trend()

        elif sum(short_signals) >= required_signals and sum(short_confirmations) >= required_confirmations:
            self.enter_short_trend()

    def enter_long_trend(self):
        """Enter long trend following position"""
        entry_price = self.data.Close[-1]

        # Adaptive stop loss
        atr_multiplier = self.adaptive_params.get("atr_multiplier", self.atr_multiplier_base)

        atr_stop = entry_price - (self.atr[-1] * atr_multiplier)
        supertrend_stop = self.supertrend[-1] if self.supertrend_direction[-1] == 1 else atr_stop
        ema_stop = self.ema_slow[-1] * 0.98

        stop_loss = max(atr_stop, supertrend_stop, ema_stop)

        # Risk per share
        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Adaptive take profit
            trend_strength = self.calculate_trend_strength()
            reward_ratio = 2.0 + trend_strength  # Higher R:R for stronger trends

            take_profit = entry_price + (risk_per_share * reward_ratio)

            # Adjust based on BB upper
            bb_target = self.bb_upper[-1] * 0.99
            if trend_strength < 0.5:  # Weak trend
                take_profit = min(take_profit, bb_target)

            self.buy(size=position_size)

            # Store trade parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)

            print(f"🚀📈 LONG TREND ({self.current_regime}): Size={position_size} @ {entry_price:.2f}")
            print(
                f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Trend Strength: {self.calculate_trend_strength():.2f}"
            )

    def enter_short_trend(self):
        """Enter short trend following position"""
        entry_price = self.data.Close[-1]

        # Adaptive stop loss
        atr_multiplier = self.adaptive_params.get("atr_multiplier", self.atr_multiplier_base)

        atr_stop = entry_price + (self.atr[-1] * atr_multiplier)
        supertrend_stop = self.supertrend[-1] if self.supertrend_direction[-1] == -1 else atr_stop
        ema_stop = self.ema_slow[-1] * 1.02

        stop_loss = min(atr_stop, supertrend_stop, ema_stop)

        # Risk per share
        risk_per_share = stop_loss - entry_price
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Adaptive take profit
            trend_strength = self.calculate_trend_strength()
            reward_ratio = 2.0 + trend_strength

            take_profit = entry_price - (risk_per_share * reward_ratio)

            # Adjust based on BB lower
            bb_target = self.bb_lower[-1] * 1.01
            if trend_strength < 0.5:
                take_profit = max(take_profit, bb_target)

            self.sell(size=position_size)

            # Store trade parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)

            print(f"📉📈 SHORT TREND ({self.current_regime}): Size={position_size} @ {entry_price:.2f}")
            print(
                f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Trend Strength: {self.calculate_trend_strength():.2f}"
            )

    def manage_trend_position(self):
        """Manage trend following positions with adaptive exit rules"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)
        bars_held = current_time - self.entry_time

        # Take profit
        if self.position.is_long and current_price >= self.take_profit:
            self.position.close()
            print(f"🎯📈 LONG TREND TP @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price <= self.take_profit:
            self.position.close()
            print(f"🎯📉 SHORT TREND TP @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Stop loss
        if self.position.is_long and current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑📈 LONG TREND SL @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price >= self.stop_loss:
            self.position.close()
            print(f"🛑📉 SHORT TREND SL @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Adaptive maximum hold time based on regime
        max_hold = 50  # Base hold time
        if self.current_regime == "HIGH_VOLATILITY_TRENDING":
            max_hold = 30  # Shorter for volatile trends
        elif self.current_regime == "LOW_VOLATILITY_TRENDING":
            max_hold = 80  # Longer for stable trends

        if bars_held >= max_hold:
            self.position.close()
            print(f"⏰📈 TREND TIME EXIT @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Trend reversal exit
        trend_strength = self.calculate_trend_strength()

        if self.position.is_long:
            # Exit long if trend weakens significantly
            if (
                trend_strength < 0.2
                or self.supertrend_direction[-1] == -1
                or (self.ema_fast[-1] < self.ema_slow[-1] and bars_held > 5)
            ):
                self.position.close()
                print(f"🔄📈 LONG TREND REVERSAL @ {current_price:.2f} ({bars_held} bars)")
                self.reset_trade_params()
                return

        elif self.position.is_short:
            # Exit short if trend weakens significantly
            if (
                trend_strength < 0.2
                or self.supertrend_direction[-1] == 1
                or (self.ema_fast[-1] > self.ema_slow[-1] and bars_held > 5)
            ):
                self.position.close()
                print(f"🔄📉 SHORT TREND REVERSAL @ {current_price:.2f} ({bars_held} bars)")
                self.reset_trade_params()
                return

        # Adaptive trailing stop
        if bars_held > 10:  # Only after position is established
            atr_trail_multiplier = self.adaptive_params.get("atr_multiplier", self.atr_multiplier_base) * 0.75

            if self.position.is_long:
                new_stop = current_price - (self.atr[-1] * atr_trail_multiplier)
                if new_stop > self.stop_loss:
                    self.stop_loss = new_stop

            elif self.position.is_short:
                new_stop = current_price + (self.atr[-1] * atr_trail_multiplier)
                if new_stop < self.stop_loss:
                    self.stop_loss = new_stop

    def reset_trade_params(self):
        """Reset trade management parameters"""
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None


# Run Default Backtest
print("🌙 Starting Adaptive Trend Follower Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, AdaptiveTrendFollower, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 ADAPTIVE TREND FOLLOWER - DEFAULT RESULTS")
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
    ema_fast_base=range(6, 12, 2),
    ema_slow_base=range(18, 26, 2),
    ema_trend_base=range(40, 60, 5),
    volatility_multiplier=[1.2, 1.5, 1.8, 2.0],
    min_trend_strength=[0.2, 0.3, 0.4, 0.5],
    atr_multiplier_base=[1.5, 2.0, 2.5, 3.0],
    maximize="Sharpe Ratio",
    constraint=lambda p: p["# Trades"] > 100 and p["Return [%]"] > 0,
)

print("\n🌙 ADAPTIVE TREND FOLLOWER - OPTIMIZED RESULTS")
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
    print("\n🏆 ADAPTIVE TREND FOLLOWER STRATEGY: SUCCESS! 🏆")
else:
    print("\n⚠️ Strategy needs further optimization...")

print("\n🌙 Adaptive Trend Follower backtest completed! ✨")
