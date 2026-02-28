# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergenceAnchor_AI6.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DivergenceAnchor Strategy Backtest
AI6 Implementation for Moon Dev Trading System 🌙
"""

import warnings

import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

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


class DivergenceAnchor(Strategy):
    """
    DivergenceAnchor Strategy: Moon Dev Implementation 🌙 (Optimized for More Trades)

    Entry Logic:
    - Detect both bearish AND bullish divergences
    - Reduced swing period for more frequent signals
    - Multiple divergence timeframes for better coverage
    - Enhanced entry conditions with momentum confirmation

    Exit Logic:
    - Adaptive take profit (1.5:1 to 3:1 risk/reward ratio)
    - Trailing stop with MACD reversal
    - Time-based exit for stale positions
    """

    # Optimized Parameters for More Trades
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    swing_period = 10  # Reduced from 20 for more frequent swings
    risk_percent = 0.01
    rr_ratio = 1.5  # Reduced from 2.0 for easier profit taking
    min_separation = 5  # Reduced from 10 for more opportunities

    def init(self):
        # MACD calculation using pandas
        def calc_ema(data, period):
            return data.ewm(span=period).mean()

        def calc_macd(close):
            ema_fast = calc_ema(pd.Series(close), self.macd_fast)
            ema_slow = calc_ema(pd.Series(close), self.macd_slow)
            macd_line = ema_fast - ema_slow
            return macd_line.values

        def calc_macd_hist(close):
            ema_fast = calc_ema(pd.Series(close), self.macd_fast)
            ema_slow = calc_ema(pd.Series(close), self.macd_slow)
            macd_line = ema_fast - ema_slow
            signal_line = calc_ema(macd_line, self.macd_signal)
            hist = macd_line - signal_line
            return hist.values

        self.macd_line = self.I(calc_macd, self.data.Close)
        self.macd_hist = self.I(calc_macd_hist, self.data.Close)

        # Swing high/low indicators
        def calc_rolling_max(data, period):
            return (
                pd.Series(data)
                .rolling(window=period, center=True)
                .max()
                .fillna(method="ffill")
                .values
            )

        def calc_rolling_min(data, period):
            return (
                pd.Series(data)
                .rolling(window=period, center=True)
                .min()
                .fillna(method="ffill")
                .values
            )

        self.swing_high = self.I(calc_rolling_max, self.data.High, self.swing_period)
        self.swing_low = self.I(calc_rolling_min, self.data.Low, self.swing_period)

        # Track peaks for divergence detection
        self.peaks = []  # Stores (price_high, macd_value, index) tuples
        self.valleys = (
            []
        )  # Stores (price_low, macd_value, index) tuples for bullish divergence
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None

    def next(self):
        if len(self.data) < self.swing_period + 1:
            return

        # Moon Dev Enhanced Divergence Detection System 🌙
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_swing_high = self.swing_high[-1]
        current_swing_low = self.swing_low[-1]
        current_index = len(self.data) - 1

        # Detect new swing high formation (for bearish divergence)
        if (
            not np.isnan(current_swing_high)
            and abs(current_high - current_swing_high) < 0.01
        ):
            # Store the peak
            self.peaks.append((current_high, self.macd_line[-1], current_index))

            # Keep only last 4 peaks for more opportunities
            if len(self.peaks) > 4:
                self.peaks.pop(0)

            # Check for bearish divergence with relaxed separation
            if len(self.peaks) >= 2:
                last_high, last_macd, last_idx = self.peaks[-2]
                curr_high, curr_macd, curr_idx = self.peaks[-1]

                # Ensure minimum separation between peaks
                if curr_idx - last_idx > self.min_separation:
                    # Bearish divergence condition
                    if (curr_high > last_high) and (curr_macd < last_macd):
                        print(
                            f"🌙 BEARISH DIVERGENCE: Price {last_high:.2f} -> {curr_high:.2f} | MACD {last_macd:.4f} -> {curr_macd:.4f}"
                        )
                        self.check_entry_conditions("bearish")

        # Detect new swing low formation (for bullish divergence)
        if (
            not np.isnan(current_swing_low)
            and abs(current_low - current_swing_low) < 0.01
        ):
            # Store the valley
            self.valleys.append((current_low, self.macd_line[-1], current_index))

            # Keep only last 4 valleys
            if len(self.valleys) > 4:
                self.valleys.pop(0)

            # Check for bullish divergence
            if len(self.valleys) >= 2:
                last_low, last_macd, last_idx = self.valleys[-2]
                curr_low, curr_macd, curr_idx = self.valleys[-1]

                # Ensure minimum separation
                if curr_idx - last_idx > self.min_separation:
                    # Bullish divergence condition
                    if (curr_low < last_low) and (curr_macd > last_macd):
                        print(
                            f"🌙 BULLISH DIVERGENCE: Price {last_low:.2f} -> {curr_low:.2f} | MACD {last_macd:.4f} -> {curr_macd:.4f}"
                        )
                        self.check_entry_conditions("bullish")

        # Exit conditions
        if self.position:
            self.check_exit_conditions()

    def check_entry_conditions(self, divergence_type):
        """Moon Dev Enhanced Entry Logic 🌙"""
        if self.position:  # Already in position
            return

        current_low = self.data.Low[-1]
        current_high = self.data.High[-1]
        current_close = self.data.Close[-1]
        support_level = self.swing_low[-1]
        resistance_level = self.swing_high[-1]

        # More flexible entry conditions based on divergence type
        if divergence_type == "bullish":
            # Bullish divergence - enter long on any confirmation
            if not np.isnan(support_level):
                # More aggressive entry - just need to be near or above support
                if current_close >= support_level * 0.995:  # Within 0.5% of support
                    print(f"✨ BULLISH ENTRY CONFIRMED @ {current_close:.2f}")
                    self.execute_long_entry(support_level, "bullish")

        elif divergence_type == "bearish":
            # Bearish divergence - still enter long but wait for better confirmation
            if not np.isnan(support_level):
                # Counter-trend long entry on bearish divergence (contrarian approach)
                if current_low <= support_level * 1.002:  # Within 0.2% of support
                    print(
                        f"🌙 CONTRARIAN ENTRY @ {current_close:.2f} (Bearish divergence reversal)"
                    )
                    self.execute_long_entry(support_level, "bearish")

    def execute_long_entry(self, support, divergence_type):
        """Moon Dev Risk-Managed Entry 🚀"""
        # Calculate stop loss 0.5% below support
        stop_loss = support * 0.995
        risk_per_unit = self.data.Close[-1] - stop_loss

        if risk_per_unit <= 0:
            print("⚠️ INVALID RISK CALCULATION - Trade skipped")
            return

        # Position sizing based on risk
        risk_amount = self.equity * self.risk_percent
        position_size = risk_amount / risk_per_unit
        position_size = int(round(position_size))

        if position_size > 0:
            # Set entry parameters
            self.entry_price = self.data.Close[-1]
            self.stop_loss = stop_loss
            self.entry_time = len(self.data)

            # Adaptive take profit based on divergence type
            if divergence_type == "bullish":
                self.take_profit = self.entry_price + (
                    risk_per_unit * 2.0
                )  # Higher TP for bullish
            else:
                self.take_profit = self.entry_price + (
                    risk_per_unit * self.rr_ratio
                )  # Standard TP

            # Execute trade
            self.buy(size=position_size)

            print(
                f"🚀 {divergence_type.upper()} ENTRY: Size={position_size} @ {self.entry_price:.2f}"
            )
            print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")
            print(f"   Risk: ${risk_amount:.2f} | Type: {divergence_type}")

    def check_exit_conditions(self):
        """Enhanced Exit Logic Implementation"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)

        # Stop loss
        if current_price <= self.stop_loss:
            self.position.close()
            print(f"🛑 STOP LOSS HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Take profit
        if current_price >= self.take_profit:
            self.position.close()
            print(f"🎯 TAKE PROFIT HIT @ {current_price:.2f}")
            self.reset_trade_params()
            return

        # Trailing stop - move stop loss up if profitable
        if self.entry_price and current_price > self.entry_price * 1.005:  # 0.5% profit
            new_stop = max(self.stop_loss, current_price * 0.995)  # 0.5% trailing
            if new_stop > self.stop_loss:
                self.stop_loss = new_stop
                print(f"📈 TRAILING STOP UPDATED: {self.stop_loss:.2f}")

        # Time-based exit (stale positions after 100 bars)
        if self.entry_time and (current_time - self.entry_time) > 100:
            self.position.close()
            print(f"⏰ TIME EXIT @ {current_price:.2f} (Stale position)")
            self.reset_trade_params()
            return

        # MACD reversal exit (less strict)
        if (
            len(self.macd_hist) > 2
            and self.macd_hist[-1] > self.macd_hist[-2] > self.macd_hist[-3]
            and current_price > self.entry_price
        ):  # Only exit if profitable
            self.position.close()
            print(f"🔄 MACD MOMENTUM EXIT @ {current_price:.2f}")
            self.reset_trade_params()

    def reset_trade_params(self):
        """Reset trade parameters"""
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None


# Run backtest
print("🌙 Starting DivergenceAnchor Backtest...")
print("=" * 50)

bt = Backtest(data, DivergenceAnchor, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 DivergenceAnchor Strategy Results:")
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
print(
    f"   💰 Average Trade: {(stats['Return [%]'] / max(stats['# Trades'], 1)):.2f}% per trade"
)
print(f"   📈 Best Trade: {stats.get('Best Trade [%]', 'N/A')}")
print(f"   📉 Worst Trade: {stats.get('Worst Trade [%]', 'N/A')}")

print("\n🌙 DivergenceAnchor backtest completed successfully! ✨")
