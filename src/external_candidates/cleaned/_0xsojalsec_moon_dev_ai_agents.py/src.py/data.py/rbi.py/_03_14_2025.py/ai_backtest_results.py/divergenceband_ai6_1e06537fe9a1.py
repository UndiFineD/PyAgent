# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergenceBand_AI6.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DivergenceBand Strategy Backtest
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


class DivergenceBand(Strategy):
    """
    DivergenceBand Strategy: Moon Dev Implementation 🌙 (Optimized for More Trades)

    Entry Logic:
    - Detect bullish divergence (price lower low, MACD higher low)
    - Relaxed RSI condition (<40 instead of <30)
    - Multiple entry triggers: BB cross, RSI confirmation, momentum
    - Reduced volatility requirements for more opportunities

    Exit Logic:
    - Adaptive trailing stops
    - Multiple exit signals for better trade management
    - Time-based exits for stale positions
    """

    # Optimized Parameters for More Trades
    risk_percent = 0.01
    bb_period = 15  # Reduced from 20 for more responsive bands
    bb_std = 1.8  # Reduced from 2.0 for tighter bands
    rsi_period = 10  # Reduced from 14 for more responsive RSI
    swing_period = 3  # Reduced from 5 for more frequent swings
    rsi_oversold = 40  # Relaxed from 30 for more entries
    bb_width_threshold = 0.7  # Relaxed volatility requirement

    def init(self):
        # MACD calculation
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

        # RSI calculation
        def calc_rsi(close, period=14):
            close_series = pd.Series(close)
            delta = close_series.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.values

        self.rsi = self.I(calc_rsi, self.data.Close, self.rsi_period)

        # Bollinger Bands
        def calc_sma(data, period):
            return pd.Series(data).rolling(window=period).mean().values

        self.middle_band = self.I(calc_sma, self.data.Close, self.bb_period)

        def calc_bb_upper(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma + self.bb_std * std).values

        def calc_bb_lower(close):
            sma = pd.Series(close).rolling(window=self.bb_period).mean()
            std = pd.Series(close).rolling(window=self.bb_period).std()
            return (sma - self.bb_std * std).values

        self.upper_band = self.I(calc_bb_upper, self.data.Close)
        self.lower_band = self.I(calc_bb_lower, self.data.Close)

        # Swing highs/lows
        def calc_rolling_max(data, period):
            return pd.Series(data).rolling(window=period, center=True).max().fillna(method="ffill").values

        def calc_rolling_min(data, period):
            return pd.Series(data).rolling(window=period, center=True).min().fillna(method="ffill").values

        self.swing_high = self.I(calc_rolling_max, self.data.High, self.swing_period)
        self.swing_low = self.I(calc_rolling_min, self.data.Low, self.swing_period)

        # Track previous swings for divergence
        self.swings = []  # Store multiple swing points for better divergence detection

        # Volatility filter
        def calc_bb_width(upper, lower):
            return upper - lower

        self.bb_width = self.I(calc_bb_width, self.upper_band, self.lower_band)
        self.bb_width_ma = self.I(calc_sma, self.bb_width, 15)  # Reduced period

        # Trade management
        self.entry_time = None
        self.entry_price = None

    def next(self):
        if len(self.data) < max(self.bb_period, self.rsi_period, self.swing_period) + 1:
            return

        # Exit conditions first
        if self.position:
            self.check_exit_conditions()
            return

        # Enhanced entry detection system
        current_low = self.data.Low[-1]
        current_swing_low = self.swing_low[-1]
        current_index = len(self.data) - 1

        # Detect new swing low
        if not np.isnan(current_swing_low) and abs(current_low - current_swing_low) < 0.01:
            current_macd = self.macd_hist[-1]

            # Store swing point
            self.swings.append((current_low, current_macd, current_index))

            # Keep only last 5 swings for more opportunities
            if len(self.swings) > 5:
                self.swings.pop(0)

            # Check for bullish divergence with multiple previous swings
            for i in range(len(self.swings) - 1):
                prev_low, prev_macd, prev_idx = self.swings[i]

                # Ensure minimum separation (reduced from 10 to 3)
                if current_index - prev_idx > 3:
                    # Bullish divergence condition
                    if current_low < prev_low and current_macd > prev_macd:
                        print(
                            f"🌙 BULLISH DIVERGENCE: Price {prev_low:.2f} -> {current_low:.2f} | MACD {prev_macd:.4f} -> {current_macd:.4f}"
                        )

                        # Multiple entry triggers (any one can trigger entry)
                        rsi_condition = self.rsi[-1] < self.rsi_oversold
                        bb_cross = self.data.Close[-1] > self.middle_band[-1]
                        momentum_up = len(self.macd_hist) > 1 and self.macd_hist[-1] > self.macd_hist[-2]
                        volatility_ok = (
                            not np.isnan(self.bb_width_ma[-1])
                            and self.bb_width[-1] > self.bb_width_ma[-1] * self.bb_width_threshold
                        )

                        # More flexible entry conditions
                        if (rsi_condition or bb_cross or momentum_up) and volatility_ok:
                            print(
                                f"✅ ENTRY CONDITIONS: RSI={rsi_condition} | BB_Cross={bb_cross} | Momentum={momentum_up} | Vol={volatility_ok}"
                            )
                            self.execute_long_entry()
                            break  # Only take one entry per swing

    def execute_long_entry(self):
        """Moon Dev Risk-Managed Entry 🚀"""
        # Use most recent swing low for stop loss
        if not self.swings:
            return

        recent_swing_low = min([swing[0] for swing in self.swings[-3:]])  # Use lowest of last 3 swings
        stop_loss = recent_swing_low * 0.995
        risk_per_unit = self.data.Close[-1] - stop_loss

        if risk_per_unit <= 0:
            print("⚠️ INVALID RISK CALCULATION - Trade skipped")
            return

        # Position sizing
        risk_amount = self.equity * self.risk_percent
        position_size = risk_amount / risk_per_unit
        position_size = int(round(position_size))

        if position_size > 0:
            # Track entry details
            self.entry_price = self.data.Close[-1]
            self.entry_time = len(self.data)

            self.buy(size=position_size)

            print(f"🚀 LONG ENTRY: Size={position_size} @ {self.entry_price:.2f}")
            print(f"   SL: {stop_loss:.2f} | RSI: {self.rsi[-1]:.1f}")
            print(f"   BB Width: {self.bb_width[-1]:.1f} vs MA: {self.bb_width_ma[-1]:.1f}")

    def check_exit_conditions(self):
        """Enhanced Exit Logic Implementation"""
        current_price = self.data.Close[-1]
        current_time = len(self.data)

        # Multiple exit conditions for better trade management

        # 1. Bollinger Band exits
        if current_price < self.lower_band[-1]:
            self.position.close()
            print(f"🌙✨ BB LOWER EXIT: {current_price:.2f}")
            self.reset_trade_params()
            return

        # 2. RSI exits (both overbought and trend reversal)
        if self.rsi[-1] > 65:  # Reduced from 70 for quicker exits
            self.position.close()
            print(f"📈 RSI OVERBOUGHT EXIT: RSI {self.rsi[-1]:.1f}")
            self.reset_trade_params()
            return

        # 3. Trailing stop using middle band
        if self.entry_price and current_price > self.entry_price * 1.01:  # 1% profit
            if current_price < self.middle_band[-1]:
                self.position.close()
                print(f"📊 MIDDLE BAND TRAILING EXIT: {current_price:.2f}")
                self.reset_trade_params()
                return

        # 4. MACD momentum reversal
        if (
            len(self.macd_hist) > 2
            and self.macd_hist[-1] < self.macd_hist[-2] < self.macd_hist[-3]
            and self.entry_price
            and current_price > self.entry_price
        ):  # Only if profitable
            self.position.close()
            print(f"🔄 MACD REVERSAL EXIT: {current_price:.2f}")
            self.reset_trade_params()
            return

        # 5. Time-based exit (reduced from 100 to 50 bars)
        if self.entry_time and (current_time - self.entry_time) > 50:
            self.position.close()
            print(f"⏰ TIME EXIT: {current_price:.2f} (50 bars)")
            self.reset_trade_params()
            return

        # 6. Volatility exit - low volatility environment (relaxed threshold)
        if (
            len(self.bb_width_ma) > 0
            and not np.isnan(self.bb_width_ma[-1])
            and self.bb_width[-1] < self.bb_width_ma[-1] * 0.4
        ):  # Reduced from 0.5
            self.position.close()
            print(f"🌊 LOW VOLATILITY EXIT: BB Width {self.bb_width[-1]:.1f}")
            self.reset_trade_params()
            return

    def reset_trade_params(self):
        """Reset trade parameters"""
        self.entry_price = None
        self.entry_time = None


# Run backtest
print("🌙 Starting DivergenceBand Backtest...")
print("=" * 50)

bt = Backtest(data, DivergenceBand, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 DivergenceBand Strategy Results:")
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

print("\n🌙 DivergenceBand backtest completed successfully! ✨")
