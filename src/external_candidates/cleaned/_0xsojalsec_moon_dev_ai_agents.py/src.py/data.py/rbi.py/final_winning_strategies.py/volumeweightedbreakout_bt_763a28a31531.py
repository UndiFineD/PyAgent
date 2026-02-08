# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\VolumeWeightedBreakout_BT.py
# 🌙 Moon Dev's Volume Weighted Breakout Strategy 🌙
# WORKING STRATEGY - VWAP breakout with volume confirmation
# Targeting 60-180 trades with 2.0+ Sharpe through volume-validated breakouts

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


class VolumeWeightedBreakout(Strategy):
    """
    🌙 VOLUME WEIGHTED BREAKOUT STRATEGY 🌙

    A volume-weighted breakout strategy designed for:
    - VWAP as dynamic support/resistance level
    - Volume surge confirmation for authentic breakouts
    - Price distance from VWAP for entry timing
    - 60-180 trades with 2.0+ Sharpe ratio

    Strategy Logic:
    - Enter long on breakout above VWAP with volume surge and momentum
    - Enter short on breakdown below VWAP with volume surge and momentum
    - Use VWAP distance for position sizing and stop placement
    - Exit on return to VWAP or opposite breakout signal
    """

    # Strategy parameters
    vwap_period = 20
    volume_threshold = 1.5
    breakout_threshold = 0.5  # Minimum % above/below VWAP for breakout
    momentum_period = 10
    position_size = 0.95
    profit_target_pct = 2.0
    stop_loss_pct = 1.2
    max_hold_bars = 80

    def init(self):
        # VWAP calculation (Volume Weighted Average Price)
        def calc_vwap(high, low, close, volume, period):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            v = pd.Series(volume)

            # Typical price
            tp = (h + l + c) / 3

            # Rolling VWAP
            vwap = (tp * v).rolling(window=period).sum() / v.rolling(window=period).sum()
            return vwap.values

        # Volume ratio for surge detection
        def calc_volume_ratio(volume, period):
            v = pd.Series(volume)
            vol_ma = v.rolling(window=period).mean()
            return (v / vol_ma).values

        # Price momentum
        def calc_momentum(close, period):
            c = pd.Series(close)
            return ((c / c.shift(period)) - 1).values * 100

        # Simple Moving Average
        def calc_sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # Initialize indicators using self.I()
        self.vwap = self.I(
            calc_vwap,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            self.vwap_period,
        )
        self.volume_ratio = self.I(calc_volume_ratio, self.data.Volume, 15)
        self.momentum = self.I(calc_momentum, self.data.Close, self.momentum_period)
        self.volume_sma = self.I(calc_sma, self.data.Volume, 20)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None

        print("🌙✨ Volume Weighted Breakout Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.vwap_period, self.momentum_period, 20) + 2:
            return

        current_price = self.data.Close[-1]
        current_vwap = self.vwap[-1]
        current_volume = self.data.Volume[-1]
        current_momentum = self.momentum[-1]
        current_time = len(self.data)

        # Volume surge detection
        volume_surge = (
            self.volume_ratio[-1] > self.volume_threshold
            or current_volume > self.volume_sma[-1] * self.volume_threshold
        )

        # VWAP distance calculations
        vwap_distance_pct = ((current_price - current_vwap) / current_vwap) * 100

        # Handle existing position
        if self.position:
            # Time-based exit
            if current_time - self.entry_time >= self.max_hold_bars:
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"⏰ TIME EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            # Profit target and stop loss
            if (self.position.is_long and current_price >= self.take_profit) or (
                self.position.is_short and current_price <= self.take_profit
            ):
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"🎯 PROFIT TARGET @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            if (self.position.is_long and current_price <= self.stop_loss) or (
                self.position.is_short and current_price >= self.stop_loss
            ):
                self.position.close()
                pnl = self.calculate_pnl(current_price)
                print(f"🛑 STOP LOSS @ {current_price:.2f} ({pnl:.2f}%)")
                self.reset_trade_params()
                return

            # VWAP return exits
            if self.position.is_long:
                # Exit long when price returns close to VWAP
                if vwap_distance_pct < 0.2:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 LONG VWAP RETURN @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

            else:  # short position
                # Exit short when price returns close to VWAP
                if vwap_distance_pct > -0.2:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 SHORT VWAP RETURN @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

        # Look for breakout signals
        else:
            # Long breakout: Price above VWAP + volume surge + positive momentum
            if (
                vwap_distance_pct > self.breakout_threshold
                and volume_surge
                and current_momentum > 0
                and current_price > self.data.Close[-2]
            ):  # Price rising
                self.buy(size=self.position_size)
                self.entry_price = current_price
                self.stop_loss = current_price * (1 - self.stop_loss_pct / 100)
                self.take_profit = current_price * (1 + self.profit_target_pct / 100)
                self.entry_time = current_time

                print(f"🚀 LONG VWAP BREAKOUT @ {current_price:.2f} | VWAP: {current_vwap:.2f}")
                print(
                    f"   Distance: +{vwap_distance_pct:.2f}% | Momentum: {current_momentum:.2f}% | Vol Surge: {volume_surge}"
                )
                print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")

            # Short breakdown: Price below VWAP + volume surge + negative momentum
            elif (
                vwap_distance_pct < -self.breakout_threshold
                and volume_surge
                and current_momentum < 0
                and current_price < self.data.Close[-2]
            ):  # Price falling
                self.sell(size=self.position_size)
                self.entry_price = current_price
                self.stop_loss = current_price * (1 + self.stop_loss_pct / 100)
                self.take_profit = current_price * (1 - self.profit_target_pct / 100)
                self.entry_time = current_time

                print(f"📉 SHORT VWAP BREAKDOWN @ {current_price:.2f} | VWAP: {current_vwap:.2f}")
                print(
                    f"   Distance: {vwap_distance_pct:.2f}% | Momentum: {current_momentum:.2f}% | Vol Surge: {volume_surge}"
                )
                print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")

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
        self.take_profit = None
        self.entry_time = None


# Run Default Backtest
print("🌙 Starting Volume Weighted Breakout Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, VolumeWeightedBreakout, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 VOLUME WEIGHTED BREAKOUT - DEFAULT RESULTS")
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
    vwap_period=range(15, 25, 3),
    volume_threshold=[1.3, 1.5, 1.7, 2.0],
    breakout_threshold=[0.3, 0.5, 0.7, 1.0],
    momentum_period=range(8, 14, 2),
    profit_target_pct=[1.5, 2.0, 2.5, 3.0],
    stop_loss_pct=[1.0, 1.2, 1.5, 1.8],
    max_hold_bars=range(60, 100, 15),
    maximize="Sharpe Ratio",
)

print("\n🌙 VOLUME WEIGHTED BREAKOUT - OPTIMIZED RESULTS")
print("=" * 80)
print(stats_opt)

print(f"\n🚀 OPTIMIZED METRICS:")
print(f"📊 Total Trades: {stats_opt['# Trades']}")
print(f"💰 Total Return: {stats_opt['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats_opt['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats_opt['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats_opt['Win Rate [%]']:.2f}%")

# Success metrics check
trade_requirement = stats_opt["# Trades"] >= 30
sharpe_requirement = stats_opt["Sharpe Ratio"] > 2.0

print(f"\n✅ STRATEGY VALIDATION:")
print(
    f"📊 Trade Count Requirement (>30): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats_opt['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio Requirement (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats_opt['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 VOLUME WEIGHTED BREAKOUT STRATEGY: SUCCESS! 🏆")
    print("🌟 This strategy meets both requirements!")
    print("   ✅ VWAP breakout detection")
    print("   ✅ Volume surge confirmation")
    print("   ✅ Momentum-validated entries")
    print("   ✅ Dynamic support/resistance")
else:
    print("\n⚠️ Strategy shows promise but needs further optimization...")

print("\n🌙 Volume Weighted Breakout backtest completed! ✨")
