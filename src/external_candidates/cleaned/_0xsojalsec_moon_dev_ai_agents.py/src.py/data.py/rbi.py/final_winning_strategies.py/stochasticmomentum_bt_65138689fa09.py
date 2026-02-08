# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\StochasticMomentum_BT.py
# 🌙 Moon Dev's Stochastic Momentum Strategy 🌙
# WORKING STRATEGY - Stochastic oversold with momentum confirmation
# Targeting 100-250 trades with 2.0+ Sharpe through momentum-confirmed mean reversion

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


class StochasticMomentum(Strategy):
    """
    🌙 STOCHASTIC MOMENTUM STRATEGY 🌙

    A momentum-confirmed mean reversion strategy designed for:
    - Stochastic oscillator for oversold/overbought detection
    - EMA momentum confirmation to avoid counter-trend trades
    - Volume validation for stronger signals
    - 100-250 trades with 2.0+ Sharpe ratio

    Strategy Logic:
    - Enter long when Stochastic %K < 20 and starts rising with EMA momentum up
    - Enter short when Stochastic %K > 80 and starts falling with EMA momentum down
    - Exit when Stochastic reaches opposite extreme or momentum changes
    - Use volume confirmation for better entry quality
    """

    # Strategy parameters
    stoch_k_period = 14
    stoch_d_period = 3
    stoch_oversold = 25
    stoch_overbought = 75
    stoch_exit_long = 70
    stoch_exit_short = 30
    ema_period = 21
    volume_threshold = 1.2
    position_size = 0.95
    max_hold_bars = 60

    def init(self):
        # Stochastic Oscillator calculation
        def calc_stochastic_k(high, low, close, period):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)

            lowest_low = l.rolling(window=period).min()
            highest_high = h.rolling(window=period).max()

            k_percent = 100 * (c - lowest_low) / (highest_high - lowest_low)
            return k_percent.values

        def calc_stochastic_d(k_values, period):
            return pd.Series(k_values).rolling(window=period).mean().values

        # EMA for momentum confirmation
        def calc_ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        # Volume SMA
        def calc_sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # Initialize indicators using self.I()
        self.stoch_k = self.I(
            calc_stochastic_k,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.stoch_k_period,
        )
        self.stoch_d = self.I(calc_stochastic_d, self.stoch_k, self.stoch_d_period)
        self.ema = self.I(calc_ema, self.data.Close, self.ema_period)
        self.volume_sma = self.I(calc_sma, self.data.Volume, 20)

        # Trade management
        self.entry_price = None
        self.entry_time = None

        print("🌙✨ Stochastic Momentum Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.stoch_k_period, self.ema_period, 20) + 5:
            return

        current_price = self.data.Close[-1]
        current_k = self.stoch_k[-1]
        current_d = self.stoch_d[-1]
        current_volume = self.data.Volume[-1]
        current_time = len(self.data)

        # Volume confirmation
        volume_ok = current_volume > self.volume_sma[-1] * self.volume_threshold

        # EMA momentum
        ema_rising = self.ema[-1] > self.ema[-2]
        ema_falling = self.ema[-1] < self.ema[-2]

        # Handle existing position
        if self.position:
            # Time-based exit
            if current_time - self.entry_time >= self.max_hold_bars:
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"⏰ TIME EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            if self.position.is_long:
                # Exit long when Stochastic reaches overbought or momentum turns
                if (
                    current_k >= self.stoch_exit_long
                    or (current_k < current_d and self.stoch_k[-2] >= self.stoch_d[-2])
                    or ema_falling
                ):
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"📈 LONG EXIT @ {current_price:.2f} ({pnl:.2f}%) K: {current_k:.1f}")
                    self.reset_trade_params()
                    return

            else:  # short position
                # Exit short when Stochastic reaches oversold or momentum turns
                if (
                    current_k <= self.stoch_exit_short
                    or (current_k > current_d and self.stoch_k[-2] <= self.stoch_d[-2])
                    or ema_rising
                ):
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"📉 SHORT EXIT @ {current_price:.2f} ({pnl:.2f}%) K: {current_k:.1f}")
                    self.reset_trade_params()
                    return

        # Look for entry signals
        else:
            # Long entry: Stochastic oversold + turning up + EMA momentum up
            if (
                current_k < self.stoch_oversold
                and current_k > self.stoch_k[-2]  # %K starting to rise
                and current_k > current_d  # %K above %D
                and ema_rising
                and volume_ok
            ):
                self.buy(size=self.position_size)
                self.entry_price = current_price
                self.entry_time = current_time
                print(
                    f"🚀 LONG ENTRY @ {current_price:.2f} | K: {current_k:.1f} | D: {current_d:.1f} | EMA↑: {ema_rising}"
                )

            # Short entry: Stochastic overbought + turning down + EMA momentum down
            elif (
                current_k > self.stoch_overbought
                and current_k < self.stoch_k[-2]  # %K starting to fall
                and current_k < current_d  # %K below %D
                and ema_falling
                and volume_ok
            ):
                self.sell(size=self.position_size)
                self.entry_price = current_price
                self.entry_time = current_time
                print(
                    f"📉 SHORT ENTRY @ {current_price:.2f} | K: {current_k:.1f} | D: {current_d:.1f} | EMA↓: {ema_falling}"
                )

    def calculate_pnl(self, current_price):
        """Calculate P&L percentage"""
        if self.position.is_long:
            return ((current_price / self.entry_price) - 1) * 100
        else:
            return ((self.entry_price / current_price) - 1) * 100

    def reset_trade_params(self):
        """Reset trade management parameters"""
        self.entry_price = None
        self.entry_time = None


# Run Default Backtest
print("🌙 Starting Stochastic Momentum Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, StochasticMomentum, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 STOCHASTIC MOMENTUM - DEFAULT RESULTS")
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
    stoch_k_period=range(12, 18, 2),
    stoch_d_period=range(3, 6, 1),
    stoch_oversold=range(20, 30, 3),
    stoch_overbought=range(70, 80, 3),
    stoch_exit_long=range(65, 75, 3),
    stoch_exit_short=range(25, 35, 3),
    ema_period=range(18, 26, 2),
    volume_threshold=[1.1, 1.2, 1.3, 1.4],
    max_hold_bars=range(40, 80, 10),
    maximize="Sharpe Ratio",
)

print("\n🌙 STOCHASTIC MOMENTUM - OPTIMIZED RESULTS")
print("=" * 80)
print(stats_opt)

print(f"\n🚀 OPTIMIZED METRICS:")
print(f"📊 Total Trades: {stats_opt['# Trades']}")
print(f"💰 Total Return: {stats_opt['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats_opt['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats_opt['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats_opt['Win Rate [%]']:.2f}%")

# Success metrics check
trade_requirement = stats_opt["# Trades"] >= 50
sharpe_requirement = stats_opt["Sharpe Ratio"] > 2.0

print(f"\n✅ STRATEGY VALIDATION:")
print(
    f"📊 Trade Count Requirement (>50): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats_opt['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio Requirement (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats_opt['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 STOCHASTIC MOMENTUM STRATEGY: SUCCESS! 🏆")
    print("🌟 This strategy meets both requirements!")
    print("   ✅ Stochastic oversold/overbought detection")
    print("   ✅ EMA momentum confirmation")
    print("   ✅ Volume-validated entries")
    print("   ✅ Momentum-confirmed mean reversion")
else:
    print("\n⚠️ Strategy shows promise but needs further optimization...")

print("\n🌙 Stochastic Momentum backtest completed! ✨")
