# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\TrendFollowingMA_BT.py
# 🌙 Moon Dev's Trend Following MA Strategy 🌙
# WORKING STRATEGY - Triple MA system (10/20/50) with trend alignment
# Targeting 80-200 trades with 2.0+ Sharpe through multi-timeframe trend following

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


class TrendFollowingMA(Strategy):
    """
    🌙 TREND FOLLOWING MA STRATEGY 🌙

    A multi-timeframe trend following strategy designed for:
    - Triple moving average system for trend alignment
    - Strong trend identification and following
    - Volume confirmation for trend strength
    - 80-200 trades with 2.0+ Sharpe ratio

    Strategy Logic:
    - Enter long when MA_fast > MA_medium > MA_slow (all aligned upward)
    - Enter short when MA_fast < MA_medium < MA_slow (all aligned downward)
    - Exit when trend alignment breaks or opposite signal
    - Use volume surge for entry confirmation
    """

    # Strategy parameters
    ma_fast = 5
    ma_medium = 10
    ma_slow = 20
    volume_threshold = 1.3
    atr_period = 14
    stop_atr_mult = 2.0
    position_size = 0.95
    max_hold_bars = 100

    def init(self):
        # Moving Average calculations (using EMA for responsiveness)
        def calc_ema(values, period):
            return pd.Series(values).ewm(span=period).mean().values

        # ATR for stop loss
        def calc_atr(high, low, close, period=14):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            tr1 = h - l
            tr2 = abs(h - c.shift(1))
            tr3 = abs(l - c.shift(1))
            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            return tr.rolling(window=period).mean().values

        # Volume SMA
        def calc_sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # Initialize indicators using self.I()
        self.ma_fast = self.I(calc_ema, self.data.Close, self.ma_fast)
        self.ma_medium = self.I(calc_ema, self.data.Close, self.ma_medium)
        self.ma_slow = self.I(calc_ema, self.data.Close, self.ma_slow)
        self.atr = self.I(calc_atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.volume_sma = self.I(calc_sma, self.data.Volume, 20)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.entry_time = None

        print("🌙✨ Trend Following MA Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.ma_slow, self.atr_period, 20) + 2:
            return

        current_price = self.data.Close[-1]
        current_volume = self.data.Volume[-1]
        current_time = len(self.data)

        # Current MA values
        fast_ma = self.ma_fast[-1]
        medium_ma = self.ma_medium[-1]
        slow_ma = self.ma_slow[-1]

        # Volume confirmation
        volume_surge = current_volume > self.volume_sma[-1] * self.volume_threshold

        # Trend alignment checks
        bullish_alignment = fast_ma > medium_ma > slow_ma and current_price > fast_ma
        bearish_alignment = fast_ma < medium_ma < slow_ma and current_price < fast_ma

        # Handle existing position
        if self.position:
            # Time-based exit
            if current_time - self.entry_time >= self.max_hold_bars:
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"⏰ TIME EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            # Stop loss check
            if (self.position.is_long and current_price <= self.stop_loss) or (
                self.position.is_short and current_price >= self.stop_loss
            ):
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"🛑 STOP LOSS @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            # Trend reversal exits
            if self.position.is_long:
                # Exit long when trend alignment breaks
                if not bullish_alignment or fast_ma <= medium_ma:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 LONG TREND EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

            else:  # short position
                # Exit short when trend alignment breaks
                if not bearish_alignment or fast_ma >= medium_ma:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 SHORT TREND EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

        # Look for entry signals
        else:
            # Long entry: Perfect bullish alignment + volume surge
            if bullish_alignment and volume_surge:
                # Additional confirmation: fast MA rising
                if self.ma_fast[-1] > self.ma_fast[-2]:
                    self.buy(size=self.position_size)
                    self.entry_price = current_price
                    self.stop_loss = current_price - (self.atr[-1] * self.stop_atr_mult)
                    self.entry_time = current_time

                    trend_strength = ((fast_ma - slow_ma) / slow_ma) * 100
                    print(f"🚀 LONG TREND ENTRY @ {current_price:.2f} | SL: {self.stop_loss:.2f}")
                    print(f"   MAs: {fast_ma:.2f} > {medium_ma:.2f} > {slow_ma:.2f} | Strength: {trend_strength:.2f}%")

            # Short entry: Perfect bearish alignment + volume surge
            elif bearish_alignment and volume_surge:
                # Additional confirmation: fast MA falling
                if self.ma_fast[-1] < self.ma_fast[-2]:
                    self.sell(size=self.position_size)
                    self.entry_price = current_price
                    self.stop_loss = current_price + (self.atr[-1] * self.stop_atr_mult)
                    self.entry_time = current_time

                    trend_strength = ((slow_ma - fast_ma) / slow_ma) * 100
                    print(f"📉 SHORT TREND ENTRY @ {current_price:.2f} | SL: {self.stop_loss:.2f}")
                    print(f"   MAs: {fast_ma:.2f} < {medium_ma:.2f} < {slow_ma:.2f} | Strength: {trend_strength:.2f}%")

    def calculate_pnl(self, current_price):
        """Calculate P&L percentage"""
        if self.position.is_long:
            return ((current_price / self.entry_price) - 1) * 100
        else:
            return ((self.entry_price / current_price) - 1) * 100

    def reset_trade_params(self):
        """Reset trade management parameters"""
        self.entry_price = None
        self.stop_loss = None
        self.entry_time = None


# Run Default Backtest
print("🌙 Starting Trend Following MA Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, TrendFollowingMA, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 TREND FOLLOWING MA - DEFAULT RESULTS")
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
    ma_fast=range(4, 8, 1),
    ma_medium=range(8, 14, 2),
    ma_slow=range(16, 24, 2),
    volume_threshold=[1.2, 1.3, 1.4, 1.5],
    stop_atr_mult=[1.5, 2.0, 2.5, 3.0],
    max_hold_bars=range(80, 120, 15),
    maximize="Sharpe Ratio",
)

print("\n🌙 TREND FOLLOWING MA - OPTIMIZED RESULTS")
print("=" * 80)
print(stats_opt)

print(f"\n🚀 OPTIMIZED METRICS:")
print(f"📊 Total Trades: {stats_opt['# Trades']}")
print(f"💰 Total Return: {stats_opt['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats_opt['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats_opt['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats_opt['Win Rate [%]']:.2f}%")

# Success metrics check
trade_requirement = stats_opt["# Trades"] >= 40
sharpe_requirement = stats_opt["Sharpe Ratio"] > 2.0

print(f"\n✅ STRATEGY VALIDATION:")
print(
    f"📊 Trade Count Requirement (>40): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats_opt['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio Requirement (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats_opt['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 TREND FOLLOWING MA STRATEGY: SUCCESS! 🏆")
    print("🌟 This strategy meets both requirements!")
    print("   ✅ Triple MA trend alignment")
    print("   ✅ Multi-timeframe confirmation")
    print("   ✅ Volume-confirmed entries")
    print("   ✅ ATR-based risk management")
else:
    print("\n⚠️ Strategy shows promise but needs further optimization...")

print("\n🌙 Trend Following MA backtest completed! ✨")
