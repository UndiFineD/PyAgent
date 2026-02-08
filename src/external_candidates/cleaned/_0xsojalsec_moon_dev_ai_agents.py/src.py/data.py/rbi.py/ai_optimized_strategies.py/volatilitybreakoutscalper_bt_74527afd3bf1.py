# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\VolatilityBreakoutScalper_BT.py
# 🌙 Moon Dev's Volatility Breakout Scalper Strategy 🌙
# AI-Optimized High-Frequency Scalping Strategy for Volatility Breakouts

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


class VolatilityBreakoutScalper(Strategy):
    """
    🌙 VOLATILITY BREAKOUT SCALPER STRATEGY 🌙

    High-frequency scalping strategy that captures volatility breakouts for quick profits.

    Strategy Logic:
    - Detects volatility contraction using Bollinger Band squeeze
    - Identifies breakout momentum using price action and volume
    - Uses multiple volatility indicators (ATR, BB width, price range)
    - Quick entries and exits for scalping profits
    - Aggressive trade frequency with tight risk management
    """

    # Optimized parameters for high-frequency scalping
    risk_per_trade = 0.01  # 1% risk per trade

    # Volatility detection parameters
    bb_period = 12  # Short period for responsive bands
    bb_std = 1.6  # Tighter bands for more breakouts
    atr_period = 8  # Short ATR for quick volatility detection
    squeeze_period = 8  # Period for squeeze detection

    # Breakout parameters
    breakout_multiplier = 1.1  # Minimum breakout threshold
    volume_multiplier = 1.2  # Volume confirmation threshold
    momentum_period = 4  # Short momentum period

    # Scalping parameters
    quick_profit_ratio = 1.5  # Quick profit target (1.5:1 R:R)
    scalp_profit_ratio = 1.0  # Ultra-quick scalp (1:1 R:R)
    max_hold_bars = 15  # Maximum hold time for scalping

    def init(self):
        # Bollinger Bands for volatility
        bb_data = ta.bbands(self.data.Close, length=self.bb_period, std=self.bb_std)
        self.bb_upper = self.I(lambda: bb_data[f"BBU_{self.bb_period}_{self.bb_std}"].values)
        self.bb_middle = self.I(lambda: bb_data[f"BBM_{self.bb_period}_{self.bb_std}"].values)
        self.bb_lower = self.I(lambda: bb_data[f"BBL_{self.bb_period}_{self.bb_std}"].values)
        self.bb_width = self.I(
            lambda: (
                bb_data[f"BBU_{self.bb_period}_{self.bb_std}"] - bb_data[f"BBL_{self.bb_period}_{self.bb_std}"]
            ).values
        )

        # ATR for volatility measurement
        self.atr = self.I(ta.atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)

        # Volume indicators
        self.volume_sma = self.I(ta.sma, self.data.Volume, 10)
        self.volume_ema = self.I(ta.ema, self.data.Volume, 8)

        # Price momentum indicators
        self.roc = self.I(ta.roc, self.data.Close, self.momentum_period)  # Rate of change
        self.rsi = self.I(ta.rsi, self.data.Close, 7)  # Short RSI for quick signals

        # Price range indicators
        self.true_range = self.I(lambda: ta.true_range(self.data.High, self.data.Low, self.data.Close).values)
        self.price_range = self.I(lambda: (self.data.High - self.data.Low).values)

        # Moving averages for trend bias
        self.ema_fast = self.I(ta.ema, self.data.Close, 5)
        self.ema_slow = self.I(ta.ema, self.data.Close, 13)

        # Volatility squeeze detection
        self.bb_width_sma = self.I(ta.sma, pd.Series(self.bb_width), self.squeeze_period)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None
        self.trade_type = None

        print("🌙✨ Volatility Breakout Scalper Initialized! Ready for high-frequency action! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.bb_period, self.atr_period, self.squeeze_period) + 1:
            return

        # Handle existing positions
        if self.position:
            self.manage_scalp_position()
            return

        # Check for scalping opportunities
        self.check_breakout_signals()

    def check_breakout_signals(self):
        """Detect volatility breakouts for scalping entries"""

        # Current market conditions
        current_close = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_volume = self.data.Volume[-1]

        # Volatility conditions
        bb_width_current = self.bb_width[-1]
        bb_width_avg = self.bb_width_sma[-1]
        atr_current = self.atr[-1]
        atr_avg = np.nanmean(self.atr[-10:]) if len(self.atr) >= 10 else atr_current

        # Squeeze detection (low volatility before breakout)
        bb_squeeze = bb_width_current < bb_width_avg * 0.8  # BB width contracting
        atr_low = atr_current < atr_avg * 0.9  # ATR below average
        range_contraction = np.mean(self.price_range[-3:]) < np.mean(self.price_range[-10:-3])

        volatility_squeeze = bb_squeeze or (atr_low and range_contraction)

        # Breakout conditions
        price_above_bb_upper = current_close > self.bb_upper[-1]
        price_below_bb_lower = current_close < self.bb_lower[-1]
        price_breaking_range = (
            current_high > max(self.data.High[-5:-1]) * self.breakout_multiplier
            or current_low < min(self.data.Low[-5:-1]) / self.breakout_multiplier
        )

        # Volume confirmation
        volume_surge = current_volume > self.volume_sma[-1] * self.volume_multiplier
        volume_increasing = current_volume > self.volume_ema[-1] * 1.1
        volume_confirmation = volume_surge or volume_increasing

        # Momentum confirmation
        momentum_strong = abs(self.roc[-1]) > 0.5  # Strong rate of change
        momentum_accelerating = abs(self.roc[-1]) > abs(self.roc[-2])

        # Trend bias
        trend_bullish = self.ema_fast[-1] > self.ema_slow[-1]
        trend_bearish = self.ema_fast[-1] < self.ema_slow[-1]

        # RSI not extreme (avoid exhaustion)
        rsi_not_extreme = 25 < self.rsi[-1] < 75

        # LONG BREAKOUT SCALP
        if price_above_bb_upper or (price_breaking_range and current_close > self.bb_middle[-1]):
            if (
                volume_confirmation
                and momentum_strong
                and rsi_not_extreme
                and (volatility_squeeze or momentum_accelerating)
            ):
                self.enter_long_scalp()

        # SHORT BREAKOUT SCALP
        elif price_below_bb_lower or (price_breaking_range and current_close < self.bb_middle[-1]):
            if (
                volume_confirmation
                and momentum_strong
                and rsi_not_extreme
                and (volatility_squeeze or momentum_accelerating)
            ):
                self.enter_short_scalp()

        # VOLATILITY EXPANSION SCALP (trade in direction of breakout)
        elif not volatility_squeeze and atr_current > atr_avg * 1.2:  # High volatility expansion
            if trend_bullish and current_close > self.bb_middle[-1] and volume_confirmation:
                self.enter_long_scalp()
            elif trend_bearish and current_close < self.bb_middle[-1] and volume_confirmation:
                self.enter_short_scalp()

    def enter_long_scalp(self):
        """Enter long scalping position"""
        entry_price = self.data.Close[-1]

        # Dynamic stop loss for scalping
        atr_stop = entry_price - (self.atr[-1] * 1.0)  # Tight ATR stop
        bb_stop = self.bb_lower[-1]
        recent_low = min(self.data.Low[-3:]) * 0.999

        stop_loss = max(atr_stop, bb_stop, recent_low)

        # Risk per share
        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Scalping take profit - quick and aggressive
            volatility_high = self.atr[-1] > np.nanmean(self.atr[-10:]) * 1.2

            if volatility_high:
                # Higher volatility = larger target
                take_profit = entry_price + (risk_per_share * self.quick_profit_ratio)
            else:
                # Lower volatility = quick scalp
                take_profit = entry_price + (risk_per_share * self.scalp_profit_ratio)

            # Adjust TP based on BB upper resistance
            bb_resistance = self.bb_upper[-1] * 1.002
            if take_profit > bb_resistance:
                take_profit = bb_resistance

            self.buy(size=position_size)

            # Store scalp parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)
            self.trade_type = "LONG_SCALP"

            print(f"🚀⚡ LONG BREAKOUT SCALP: Size={position_size} @ {entry_price:.2f}")
            print(f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Hold Max: {self.max_hold_bars} bars")

    def enter_short_scalp(self):
        """Enter short scalping position"""
        entry_price = self.data.Close[-1]

        # Dynamic stop loss for short scalping
        atr_stop = entry_price + (self.atr[-1] * 1.0)  # Tight ATR stop
        bb_stop = self.bb_upper[-1]
        recent_high = max(self.data.High[-3:]) * 1.001

        stop_loss = min(atr_stop, bb_stop, recent_high)

        # Risk per share
        risk_per_share = stop_loss - entry_price
        if risk_per_share <= 0:
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            # Scalping take profit
            volatility_high = self.atr[-1] > np.nanmean(self.atr[-10:]) * 1.2

            if volatility_high:
                take_profit = entry_price - (risk_per_share * self.quick_profit_ratio)
            else:
                take_profit = entry_price - (risk_per_share * self.scalp_profit_ratio)

            # Adjust TP based on BB lower support
            bb_support = self.bb_lower[-1] * 0.998
            if take_profit < bb_support:
                take_profit = bb_support

            self.sell(size=position_size)

            # Store scalp parameters
            self.entry_price = entry_price
            self.stop_loss = stop_loss
            self.take_profit = take_profit
            self.entry_time = len(self.data)
            self.trade_type = "SHORT_SCALP"

            print(f"📉⚡ SHORT BREAKOUT SCALP: Size={position_size} @ {entry_price:.2f}")
            print(f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Hold Max: {self.max_hold_bars} bars")

    def manage_scalp_position(self):
        """Aggressive scalping position management"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)
        bars_held = current_time - self.entry_time

        # Quick take profit for scalping
        if self.position.is_long and current_price >= self.take_profit:
            self.position.close()
            print(f"🎯⚡ LONG SCALP TP @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price <= self.take_profit:
            self.position.close()
            print(f"🎯⚡ SHORT SCALP TP @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Stop loss
        if self.position.is_long and current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑⚡ LONG SCALP SL @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return
        elif self.position.is_short and current_price >= self.stop_loss:
            self.position.close()
            print(f"🛑⚡ SHORT SCALP SL @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Maximum hold time for scalping (quick exits)
        if bars_held >= self.max_hold_bars:
            self.position.close()
            print(f"⏰⚡ SCALP TIME EXIT @ {current_price:.2f} ({bars_held} bars)")
            self.reset_trade_params()
            return

        # Momentum reversal exit (scalping requires quick momentum)
        momentum_weakening = abs(self.roc[-1]) < abs(self.roc[-2]) * 0.7

        if self.position.is_long:
            # Exit long if momentum weakens or RSI becomes overbought
            if (
                momentum_weakening or self.rsi[-1] > 70 or current_price < self.bb_middle[-1]
            ):  # Price back below middle BB
                self.position.close()
                print(f"🔄⚡ LONG MOMENTUM EXIT @ {current_price:.2f} ({bars_held} bars)")
                self.reset_trade_params()
                return

        elif self.position.is_short:
            # Exit short if momentum weakens or RSI becomes oversold
            if (
                momentum_weakening or self.rsi[-1] < 30 or current_price > self.bb_middle[-1]
            ):  # Price back above middle BB
                self.position.close()
                print(f"🔄⚡ SHORT MOMENTUM EXIT @ {current_price:.2f} ({bars_held} bars)")
                self.reset_trade_params()
                return

        # Aggressive trailing stop for profitable scalps
        profit_threshold = 0.003  # 0.3% profit threshold

        if self.position.is_long and current_price > self.entry_price * (1 + profit_threshold):
            # Trail stop aggressively
            new_stop = max(self.stop_loss, current_price * 0.997)  # 0.3% trailing
            if new_stop > self.stop_loss:
                self.stop_loss = new_stop

        elif self.position.is_short and current_price < self.entry_price * (1 - profit_threshold):
            # Trail stop aggressively
            new_stop = min(self.stop_loss, current_price * 1.003)  # 0.3% trailing
            if new_stop < self.stop_loss:
                self.stop_loss = new_stop

    def reset_trade_params(self):
        """Reset trade management parameters"""
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None
        self.trade_type = None


# Run Default Backtest
print("🌙 Starting Volatility Breakout Scalper Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, VolatilityBreakoutScalper, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 VOLATILITY BREAKOUT SCALPER - DEFAULT RESULTS")
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
    bb_period=range(10, 16, 2),
    bb_std=[1.4, 1.6, 1.8, 2.0],
    atr_period=range(6, 12, 2),
    breakout_multiplier=[1.05, 1.1, 1.15, 1.2],
    volume_multiplier=[1.1, 1.2, 1.3, 1.4],
    quick_profit_ratio=[1.2, 1.5, 1.8, 2.0],
    max_hold_bars=range(10, 20, 3),
    maximize="Sharpe Ratio",
    constraint=lambda p: p["# Trades"] > 100 and p["Return [%]"] > 0,
)

print("\n🌙 VOLATILITY BREAKOUT SCALPER - OPTIMIZED RESULTS")
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
    print("\n🏆 VOLATILITY BREAKOUT SCALPER STRATEGY: SUCCESS! 🏆")
else:
    print("\n⚠️ Strategy needs further optimization...")

print("\n🌙 Volatility Breakout Scalper backtest completed! ✨")
