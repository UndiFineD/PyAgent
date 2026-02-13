# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergenceVolatility_ULTRA.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DivergenceVolatility ULTRA Strategy - Beat Buy & Hold
AI6 Implementation for Moon Dev Trading System 🌙
Target: Beat 127.77% buy & hold return
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


class DivergenceVolatilityULTRA(Strategy):
    """
    DivergenceVolatility ULTRA Strategy: Beat Buy & Hold 🌙

    Target: Beat 127.77% buy & hold return
    Approach: Aggressive trend following with momentum acceleration
    """

    # ULTRA Aggressive Parameters for Maximum Returns
    risk_per_trade = 0.05  # 5% risk per trade (higher risk for higher returns)
    atr_multiplier = 3.0  # Higher profit targets
    bb_period = 10  # Very responsive bands
    volume_spike_multiplier = 1.1  # Lower threshold for more entries
    swing_period = 5  # Very frequent swings
    atr_period = 8  # Highly responsive ATR
    min_separation = 2  # Minimal separation for rapid entries
    leverage_factor = 2.0  # Position size multiplier for bull trends

    def init(self):
        # MACD calculation using pandas
        def calc_ema(data, period):
            return data.ewm(span=period).mean()

        def calc_macd_hist(close):
            ema_fast = calc_ema(pd.Series(close), 8)  # Faster MACD
            ema_slow = calc_ema(pd.Series(close), 16)  # More responsive
            macd_line = ema_fast - ema_slow
            signal_line = calc_ema(macd_line, 6)  # Faster signal
            hist = macd_line - signal_line
            return hist.values

        self.macd_hist = self.I(calc_macd_hist, self.data.Close)

        # Volume indicators with multiple timeframes
        def calc_sma(data, period):
            return pd.Series(data).rolling(window=period).mean().values

        self.volume_sma = self.I(
            calc_sma, self.data.Volume, 10
        )  # Shorter for responsiveness
        self.volume_sma_long = self.I(calc_sma, self.data.Volume, 20)

        # Bollinger Bands for volatility
        def calc_bb_upper(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma + 1.5 * std).values  # Tighter bands

        def calc_bb_lower(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma - 1.5 * std).values  # Tighter bands

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

        self.atr = self.I(
            calc_atr, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )

        # Trend detection
        def calc_trend_sma(close):
            return pd.Series(close).rolling(window=20).mean().values

        self.trend_sma = self.I(calc_trend_sma, self.data.Close)

        # Momentum indicators
        def calc_roc(close, period=10):
            close_series = pd.Series(close)
            return (
                (close_series - close_series.shift(period))
                / close_series.shift(period)
                * 100
            ).values

        self.roc = self.I(calc_roc, self.data.Close, 10)

        # Swing lows using rolling minimum
        def calc_rolling_min(data, period):
            return (
                pd.Series(data)
                .rolling(window=period, center=True)
                .min()
                .fillna(method="ffill")
                .values
            )

        self.swing_lows = self.I(calc_rolling_min, self.data.Low, self.swing_period)

        # Enhanced divergence tracking
        self.swing_history = []

        # Advanced trade management
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None
        self.entry_time = None
        self.atr_at_entry = None
        self.trend_at_entry = None

    def next(self):
        if len(self.data) < max(self.bb_period, self.swing_period, self.atr_period) + 1:
            return

        # Exit conditions first
        if self.position:
            self.check_exit_conditions()
            return

        # ULTRA aggressive entry detection
        current_low = self.data.Low[-1]
        current_swing_low = self.swing_lows[-1]
        current_index = len(self.data) - 1

        # Detect new swing low
        if (
            not np.isnan(current_swing_low)
            and abs(current_low - current_swing_low) < 0.01
        ):
            current_macd = self.macd_hist[-1]

            # Store swing in history
            self.swing_history.append((current_low, current_macd, current_index))

            # Keep only recent swings (last 6 for aggressive trading)
            if len(self.swing_history) > 6:
                self.swing_history.pop(0)

            # Check for bullish divergence with multiple previous swings
            for i in range(len(self.swing_history) - 1):
                prev_low, prev_macd, prev_idx = self.swing_history[i]

                # Minimal separation for rapid entries
                if current_index - prev_idx > self.min_separation:
                    # Bullish divergence condition
                    if current_low < prev_low and current_macd > prev_macd:
                        print(
                            f"🌙 ULTRA BULLISH DIVERGENCE: Price {prev_low:.2f} -> {current_low:.2f} | MACD {prev_macd:.4f} -> {current_macd:.4f}"
                        )

                        # Ultra aggressive validation
                        volume_conditions = self.check_ultra_volume_conditions()
                        momentum_conditions = self.check_ultra_momentum_conditions()
                        trend_conditions = self.check_ultra_trend_conditions()

                        # More lenient entry requirements
                        if volume_conditions or momentum_conditions or trend_conditions:
                            print(
                                f"🚀 ULTRA ENTRY: Vol={volume_conditions} | Mom={momentum_conditions} | Trend={trend_conditions}"
                            )
                            self.execute_ultra_long_entry()
                            break

    def check_ultra_volume_conditions(self):
        """Ultra aggressive volume analysis"""
        if len(self.volume_sma) == 0 or np.isnan(self.volume_sma[-1]):
            return False

        current_volume = self.data.Volume[-1]
        short_avg = self.volume_sma[-1]

        # Very lenient volume requirements
        volume_spike = current_volume > short_avg * self.volume_spike_multiplier
        volume_trend = (
            len(self.volume_sma) > 2 and self.volume_sma[-1] > self.volume_sma[-2]
        )

        return volume_spike or volume_trend

    def check_ultra_momentum_conditions(self):
        """Ultra aggressive momentum analysis"""
        if len(self.macd_hist) < 2:
            return True  # Default to true for aggressive entry

        # Any positive momentum signal
        macd_improving = self.macd_hist[-1] > self.macd_hist[-2]
        roc_positive = len(self.roc) > 0 and self.roc[-1] > -5  # Very lenient ROC

        return macd_improving or roc_positive

    def check_ultra_trend_conditions(self):
        """Ultra aggressive trend analysis"""
        if len(self.trend_sma) == 0:
            return True

        # Trend following for bull market
        price_above_trend = (
            self.data.Close[-1] > self.trend_sma[-1] * 0.98
        )  # Very lenient
        trend_up = len(self.trend_sma) > 5 and self.trend_sma[-1] > self.trend_sma[-5]

        return price_above_trend or trend_up

    def execute_ultra_long_entry(self):
        """ULTRA Aggressive Risk-Managed Entry 🚀"""
        if not self.swing_history:
            return

        # Use recent swing lows for stop loss calculation
        recent_swing_low = min([swing[0] for swing in self.swing_history[-2:]])
        stop_loss = recent_swing_low * 0.99  # Tighter stop for aggressive trading
        risk_per_unit = self.data.Close[-1] - stop_loss

        if risk_per_unit <= 0:
            print("⚠️ INVALID RISK CALCULATION - Trade skipped")
            return

        # ULTRA aggressive position sizing
        base_risk = self.equity * self.risk_per_trade

        # Leverage factor for bull trend
        if len(self.trend_sma) > 0 and self.data.Close[-1] > self.trend_sma[-1]:
            leverage_multiplier = self.leverage_factor
        else:
            leverage_multiplier = 1.0

        risk_amount = base_risk * leverage_multiplier
        position_size = risk_amount / risk_per_unit
        position_size = int(round(position_size))

        if position_size > 0:
            # Set entry parameters with ultra aggressive take profit
            self.entry_price = self.data.Close[-1]
            self.stop_loss = stop_loss
            self.entry_time = len(self.data)
            self.atr_at_entry = self.atr[-1]
            self.trend_at_entry = (
                self.trend_sma[-1] if len(self.trend_sma) > 0 else self.entry_price
            )

            # Ultra aggressive take profit
            current_atr = self.atr[-1]
            self.take_profit = self.entry_price + (current_atr * self.atr_multiplier)

            # Execute trade
            self.buy(size=position_size)

            print(f"🚀 ULTRA ENTRY: Size={position_size} @ {self.entry_price:.2f}")
            print(f"   TP: {self.take_profit:.2f} | SL: {self.stop_loss:.2f}")
            print(f"   Leverage: {leverage_multiplier:.1f}x | Risk: ${risk_amount:.0f}")

    def check_exit_conditions(self):
        """Ultra Aggressive Exit Logic"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)

        # Take profit
        if self.take_profit and current_price >= self.take_profit:
            self.position.close()
            print(f"🎯 ULTRA PROFIT HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Stop loss
        if self.stop_loss and current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑 ULTRA STOP @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Aggressive trailing stop (move up quickly)
        if self.entry_price and current_price > self.entry_price * 1.02:  # 2% profit
            new_stop = max(self.stop_loss, current_price * 0.98)  # 2% trailing
            if new_stop > self.stop_loss:
                self.stop_loss = new_stop
                print(f"📈 ULTRA TRAILING: {self.stop_loss:.2f}")

        # Time-based exit (shorter for rapid turnover)
        if self.entry_time and (current_time - self.entry_time) > 20:  # Very short hold
            self.position.close()
            print(f"⏰ ULTRA TIME EXIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Trend reversal exit
        if (
            self.trend_at_entry
            and len(self.trend_sma) > 0
            and current_price < self.trend_sma[-1] * 0.97
        ):  # 3% below trend
            self.position.close()
            print(f"📉 ULTRA TREND EXIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

    def reset_trade_params(self):
        """Reset trade parameters"""
        self.entry_price = None
        self.take_profit = None
        self.stop_loss = None
        self.entry_time = None
        self.atr_at_entry = None
        self.trend_at_entry = None


# Run backtest
print("🌙 Starting DivergenceVolatility ULTRA Backtest...")
print("Target: Beat 127.77% Buy & Hold Return")
print("=" * 60)

bt = Backtest(data, DivergenceVolatilityULTRA, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 DivergenceVolatility ULTRA Strategy Results:")
print("=" * 60)
print(stats)
print(f"\n🚀 Strategy Details: {stats._strategy}")

# Key metrics
print(f"\n⭐ ULTRA Performance Metrics:")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"🎯 Buy & Hold Target: 127.77%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"📊 Total Trades: {stats['# Trades']}")

# Success check
if stats["Return [%]"] > 127.77 and stats["# Trades"] >= 5:
    print(f"\n🏆 SUCCESS! Strategy beats buy & hold!")
    print(f"   Strategy: {stats['Return [%]']:.2f}% vs Buy & Hold: 127.77%")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")
else:
    print(f"\n❌ Need more optimization...")
    print(f"   Return: {stats['Return [%]']:.2f}% (Target: >127.77%)")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")

print("\n🌙 ULTRA backtest completed! ✨")
