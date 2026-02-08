# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergenceVolatility_AI6.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DivergenceVolatility Strategy Backtest
AI6 Implementation for Moon Dev Trading System 🌙
"""

import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

warnings.filterwarnings("ignore")

# Load and prepare data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class DivergenceVolatility(Strategy):
    """
    DivergenceVolatility Strategy: Moon Dev Implementation 🌙 (Optimized)

    Entry Logic:
    - Enhanced divergence detection with multiple timeframes
    - Dynamic volume spike threshold based on market conditions
    - Adaptive volatility filtering using multiple indicators
    - Multiple entry confirmation signals

    Exit Logic:
    - Dynamic take profit based on market volatility
    - Trailing stops with multiple confirmation levels
    - Time-based and momentum-based exits
    """

    # Optimized Parameters for Better Performance
    risk_per_trade = 0.01  # 1% risk per trade
    atr_multiplier = 1.8  # Reduced for quicker profits
    bb_period = 15  # Reduced for more responsive bands
    volume_spike_multiplier = 1.3  # Reduced threshold for more entries
    swing_period = 8  # Reduced for more frequent swings
    atr_period = 10  # Reduced for more responsive ATR
    min_separation = 3  # Minimum bars between divergences

    def init(self):
        # MACD calculation using pandas
        def calc_ema(data, period):
            return data.ewm(span=period).mean()

        def calc_macd_hist(close):
            ema_fast = calc_ema(pd.Series(close), 12)
            ema_slow = calc_ema(pd.Series(close), 26)
            macd_line = ema_fast - ema_slow
            signal_line = calc_ema(macd_line, 9)
            hist = macd_line - signal_line
            return hist.values

        self.macd_hist = self.I(calc_macd_hist, self.data.Close)

        # Volume indicators with multiple timeframes
        def calc_sma(data, period):
            return pd.Series(data).rolling(window=period).mean().values

        self.volume_sma = self.I(calc_sma, self.data.Volume, 15)  # Shorter period for responsiveness
        self.volume_sma_long = self.I(calc_sma, self.data.Volume, 30)  # Longer period for context

        # Bollinger Bands for volatility
        def calc_bb_upper(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma + 2 * std).values

        def calc_bb_lower(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma - 2 * std).values

        self.bb_upper = self.I(calc_bb_upper, self.data.Close)
        self.bb_lower = self.I(calc_bb_lower, self.data.Close)
        self.bb_middle = self.I(calc_sma, self.data.Close, self.bb_period)

        # ATR for volatility
        def calc_atr(high, low, close, period=14):
            high_series = pd.Series(high)
            low_series = pd.Series(low)
            close_series = pd.Series(close)

            tr1 = high_series - low_series
            tr2 = abs(high_series - close_series.shift(1))
            tr3 = abs(low_series - close_series.shift(1))

            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            atr = tr.rolling(window=period).mean()
            return atr.values

        self.atr = self.I(calc_atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)

        # Swing lows using rolling minimum
        def calc_rolling_min(data, period):
            return pd.Series(data).rolling(window=period, center=True).min().fillna(method="ffill").values

        self.swing_lows = self.I(calc_rolling_min, self.data.Low, self.swing_period)

        # Enhanced divergence tracking
        self.swing_history = []  # Store multiple swing points for better analysis

        # Advanced trade management
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None
        self.entry_time = None
        self.atr_at_entry = None

    def next(self):
        if len(self.data) < max(self.bb_period, self.swing_period, self.atr_period) + 1:
            return

        # Exit conditions first
        if self.position:
            self.check_exit_conditions()
            return

        # Enhanced divergence detection system
        current_low = self.data.Low[-1]
        current_swing_low = self.swing_lows[-1]
        current_index = len(self.data) - 1

        # Detect new swing low
        if not np.isnan(current_swing_low) and abs(current_low - current_swing_low) < 0.01:
            current_macd = self.macd_hist[-1]

            # Store swing in history
            self.swing_history.append((current_low, current_macd, current_index))

            # Keep only recent swings (last 8 for better analysis)
            if len(self.swing_history) > 8:
                self.swing_history.pop(0)

            # Check for bullish divergence with multiple previous swings
            for i in range(len(self.swing_history) - 1):
                prev_low, prev_macd, prev_idx = self.swing_history[i]

                # Ensure minimum separation
                if current_index - prev_idx > self.min_separation:
                    # Bullish divergence condition
                    if current_low < prev_low and current_macd > prev_macd:
                        print(
                            f"🌙 BULLISH DIVERGENCE: Price {prev_low:.2f} -> {current_low:.2f} | MACD {prev_macd:.4f} -> {current_macd:.4f}"
                        )

                        # Enhanced validation with multiple conditions
                        volume_conditions = self.check_volume_conditions()
                        volatility_conditions = self.check_volatility_conditions()
                        momentum_conditions = self.check_momentum_conditions()

                        if volume_conditions and volatility_conditions and momentum_conditions:
                            print(
                                f"✅ ALL CONDITIONS MET: Volume={volume_conditions} | Vol={volatility_conditions} | Mom={momentum_conditions}"
                            )
                            self.execute_long_entry()
                            break  # Only take first valid divergence

    def check_volume_conditions(self):
        """Enhanced volume analysis"""
        if len(self.volume_sma) == 0 or np.isnan(self.volume_sma[-1]):
            return False

        current_volume = self.data.Volume[-1]
        short_avg = self.volume_sma[-1]
        long_avg = (
            self.volume_sma_long[-1]
            if len(self.volume_sma_long) > 0 and not np.isnan(self.volume_sma_long[-1])
            else short_avg
        )

        # Dynamic volume threshold based on recent volatility
        dynamic_multiplier = self.volume_spike_multiplier
        if len(self.atr) > 10:
            recent_atr = np.nanmean(self.atr[-10:])
            atr_avg = np.nanmean(self.atr[-30:]) if len(self.atr) > 30 else recent_atr
            if recent_atr > atr_avg * 1.2:  # High volatility period
                dynamic_multiplier *= 0.8  # Lower volume requirement

        # Multiple volume conditions (any can pass)
        volume_spike = current_volume > short_avg * dynamic_multiplier
        relative_volume = current_volume > long_avg * 1.1
        volume_trend = len(self.volume_sma) > 2 and self.volume_sma[-1] > self.volume_sma[-3]

        return volume_spike or relative_volume or volume_trend

    def check_volatility_conditions(self):
        """Enhanced volatility analysis"""
        if len(self.atr) < 10:
            return False

        current_atr = self.atr[-1]
        atr_avg = np.nanmean(self.atr[-15:])
        bb_width = self.bb_upper[-1] - self.bb_lower[-1]
        bb_width_avg = np.nanmean([self.bb_upper[i] - self.bb_lower[i] for i in range(-10, 0) if i < 0])

        # Multiple volatility conditions (any can pass)
        atr_above_avg = current_atr > atr_avg * 0.8  # Relaxed threshold
        bb_expansion = bb_width > bb_width_avg * 0.9  # Relaxed threshold
        atr_trend = len(self.atr) > 3 and self.atr[-1] > self.atr[-3]  # ATR increasing

        return atr_above_avg or bb_expansion or atr_trend

    def check_momentum_conditions(self):
        """Enhanced momentum analysis"""
        if len(self.macd_hist) < 3:
            return False

        # MACD momentum
        macd_improving = self.macd_hist[-1] > self.macd_hist[-2]
        macd_positive = self.macd_hist[-1] > 0

        # Price momentum
        price_above_bb_mid = self.data.Close[-1] > self.bb_middle[-1]
        price_trend = len(self.data.Close) > 3 and self.data.Close[-1] > self.data.Close[-3]

        # Any momentum condition can pass
        return macd_improving or macd_positive or price_above_bb_mid or price_trend

    def execute_long_entry(self):
        """Moon Dev Enhanced Risk-Managed Entry 🚀"""
        if not self.swing_history:
            return

        # Use recent swing lows for stop loss calculation
        recent_swing_low = min([swing[0] for swing in self.swing_history[-3:]])
        stop_loss = recent_swing_low * 0.995
        risk_per_unit = self.data.Close[-1] - stop_loss

        if risk_per_unit <= 0:
            print("⚠️ INVALID RISK CALCULATION - Trade skipped")
            return

        # Position sizing
        risk_amount = self.equity * self.risk_per_trade
        position_size = risk_amount / risk_per_unit
        position_size = int(round(position_size))

        if position_size > 0:
            # Set entry parameters with dynamic take profit
            self.entry_price = self.data.Close[-1]
            self.stop_loss = stop_loss
            self.entry_time = len(self.data)
            self.atr_at_entry = self.atr[-1]

            # Dynamic take profit based on volatility
            current_atr = self.atr[-1]
            atr_avg = np.nanmean(self.atr[-10:]) if len(self.atr) > 10 else current_atr

            if current_atr > atr_avg * 1.3:  # High volatility
                multiplier = self.atr_multiplier * 1.2  # Larger target
            elif current_atr < atr_avg * 0.8:  # Low volatility
                multiplier = self.atr_multiplier * 0.8  # Smaller target
            else:
                multiplier = self.atr_multiplier

            self.take_profit = self.entry_price + (current_atr * multiplier)

            # Execute trade
            self.buy(size=position_size)

            print(f"🚀 ENHANCED ENTRY: Size={position_size} @ {self.entry_price:.2f}")
            print(f"   TP: {self.take_profit:.2f} | SL: {self.stop_loss:.2f}")
            print(f"   ATR: {current_atr:.1f} (Avg: {atr_avg:.1f}) | Multiplier: {multiplier:.1f}")

    def check_exit_conditions(self):
        """Enhanced Exit Logic Implementation"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)

        # Take profit
        if self.take_profit and current_price >= self.take_profit:
            self.position.close()
            print(f"🎯 TAKE PROFIT HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Stop loss
        if self.stop_loss and current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑 STOP LOSS HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Dynamic trailing stop
        if self.entry_price and current_price > self.entry_price * 1.01:  # 1% profit
            new_stop = max(self.stop_loss, current_price * 0.99)  # 1% trailing
            if new_stop > self.stop_loss:
                self.stop_loss = new_stop
                print(f"📈 TRAILING STOP: {self.stop_loss:.2f}")

        # Time-based exit (40 bars for quicker turnover)
        if self.entry_time and (current_time - self.entry_time) > 40:
            self.position.close()
            print(f"⏰ TIME EXIT @ {current_price:.2f} (40 bars)")
            self.reset_trade_params()
            return

        # MACD reversal exit
        if (
            len(self.macd_hist) > 3
            and self.macd_hist[-1] < self.macd_hist[-2] < self.macd_hist[-3]
            and self.entry_price
            and current_price > self.entry_price
        ):  # Only if profitable
            self.position.close()
            print(f"🔄 MACD REVERSAL EXIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # ATR contraction exit (early exit when volatility drops)
        if (
            self.atr_at_entry
            and len(self.atr) > 5
            and self.atr[-1] < self.atr_at_entry * 0.6
            and current_price > self.entry_price
        ):  # Only if profitable
            self.position.close()
            print(f"🌊 ATR CONTRACTION EXIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Bollinger Band squeeze exit
        if current_price < self.bb_lower[-1]:
            self.position.close()
            print(f"📉 BB LOWER EXIT @ {current_price:.2f}")
            self.reset_trade_params()

    def reset_trade_params(self):
        """Reset trade parameters"""
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None
        self.entry_time = None
        self.atr_at_entry = None


# Run backtest
print("🌙 Starting DivergenceVolatility Backtest...")
print("=" * 50)

bt = Backtest(data, DivergenceVolatility, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 DivergenceVolatility Strategy Results:")
print("=" * 50)
print(stats)
print(f"\n🚀 Strategy Details: {stats._strategy}")

# Key metrics
print(f"\n⭐ Key Performance Metrics:")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"📊 Total Trades: {stats['# Trades']}")

print(f"\n🔥 Strategy Analysis:")
print(f"   📊 Trade Frequency: {stats['# Trades']} trades over {stats['Duration']}")
print(f"   💰 Average Trade: {(stats['Return [%]'] / max(stats['# Trades'], 1)):.2f}% per trade")
print(f"   📈 Best Trade: {stats.get('Best Trade [%]', 'N/A')}")
print(f"   📉 Worst Trade: {stats.get('Worst Trade [%]', 'N/A')}")

print("\n🌙 DivergenceVolatility backtest completed successfully! ✨")
