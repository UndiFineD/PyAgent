# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\ATRChannelSystem_BT.py
# 🌙 Moon Dev's ATR Channel System Strategy 🌙
# WORKING STRATEGY - ATR-based channel breakout with dynamic levels
# Targeting 70-200 trades with 2.0+ Sharpe through volatility-adaptive channels

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


class ATRChannelSystem(Strategy):
    """
    🌙 ATR CHANNEL SYSTEM STRATEGY 🌙

    A volatility-adaptive channel breakout strategy designed for:
    - Dynamic channel levels based on ATR (Average True Range)
    - Breakout detection with volatility expansion
    - Channel mean reversion and breakout momentum
    - 70-200 trades with 2.0+ Sharpe ratio

    Strategy Logic:
    - Create upper/lower channels using SMA ± (ATR * multiplier)
    - Enter long on breakout above upper channel with momentum
    - Enter short on breakdown below lower channel with momentum
    - Exit on channel reversion or opposite breakout
    """

    # Strategy parameters
    sma_period = 20
    atr_period = 14
    channel_multiplier = 1.5
    momentum_period = 5
    volume_threshold = 1.3
    position_size = 0.95
    profit_atr_mult = 2.5
    stop_atr_mult = 1.5
    max_hold_bars = 80

    def init(self):
        # Simple Moving Average for channel center
        def calc_sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # ATR calculation
        def calc_atr(high, low, close, period=14):
            h = pd.Series(high)
            l = pd.Series(low)
            c = pd.Series(close)
            tr1 = h - l
            tr2 = abs(h - c.shift(1))
            tr3 = abs(l - c.shift(1))
            tr = pd.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
            return tr.rolling(window=period).mean().values

        # Channel levels
        def calc_upper_channel(sma, atr, multiplier):
            return pd.Series(sma) + (pd.Series(atr) * multiplier)

        def calc_lower_channel(sma, atr, multiplier):
            return pd.Series(sma) - (pd.Series(atr) * multiplier)

        # Price momentum
        def calc_momentum(close, period):
            c = pd.Series(close)
            return ((c / c.shift(period)) - 1).values * 100

        # Initialize base indicators
        self.sma = self.I(calc_sma, self.data.Close, self.sma_period)
        self.atr = self.I(calc_atr, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.volume_sma = self.I(calc_sma, self.data.Volume, 20)
        self.momentum = self.I(calc_momentum, self.data.Close, self.momentum_period)

        # Channel levels
        self.upper_channel = self.I(calc_upper_channel, self.sma, self.atr, self.channel_multiplier)
        self.lower_channel = self.I(calc_lower_channel, self.sma, self.atr, self.channel_multiplier)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None

        print("🌙✨ ATR Channel System Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.sma_period, self.atr_period, 20) + 2:
            return

        current_price = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_volume = self.data.Volume[-1]
        current_momentum = self.momentum[-1]
        current_time = len(self.data)

        # Channel levels
        upper_channel = self.upper_channel[-1]
        lower_channel = self.lower_channel[-1]
        middle_channel = self.sma[-1]
        current_atr = self.atr[-1]

        # Volume confirmation
        volume_surge = current_volume > self.volume_sma[-1] * self.volume_threshold

        # Channel position analysis
        channel_width = upper_channel - lower_channel
        price_channel_position = (current_price - lower_channel) / channel_width

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

            # Channel reversion exits
            if self.position.is_long:
                # Exit long when price returns to middle channel
                if current_price <= middle_channel:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 LONG CHANNEL REVERSION @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

            else:  # short position
                # Exit short when price returns to middle channel
                if current_price >= middle_channel:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 SHORT CHANNEL REVERSION @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

        # Look for channel breakout signals
        else:
            # Long breakout: Price breaks above upper channel with momentum and volume
            if (
                current_high > upper_channel
                and current_price > upper_channel
                and current_momentum > 1.0
                and volume_surge
            ):
                self.buy(size=self.position_size)
                self.entry_price = current_price
                self.stop_loss = current_price - (current_atr * self.stop_atr_mult)
                self.take_profit = current_price + (current_atr * self.profit_atr_mult)
                self.entry_time = current_time

                breakout_strength = ((current_price - upper_channel) / upper_channel) * 100
                print(f"🚀 LONG CHANNEL BREAKOUT @ {current_price:.2f}")
                print(f"   Upper Channel: {upper_channel:.2f} | Breakout: {breakout_strength:.2f}%")
                print(f"   Momentum: {current_momentum:.2f}% | ATR: {current_atr:.2f}")
                print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")

            # Short breakdown: Price breaks below lower channel with momentum and volume
            elif (
                current_low < lower_channel
                and current_price < lower_channel
                and current_momentum < -1.0
                and volume_surge
            ):
                self.sell(size=self.position_size)
                self.entry_price = current_price
                self.stop_loss = current_price + (current_atr * self.stop_atr_mult)
                self.take_profit = current_price - (current_atr * self.profit_atr_mult)
                self.entry_time = current_time

                breakdown_strength = ((lower_channel - current_price) / lower_channel) * 100
                print(f"📉 SHORT CHANNEL BREAKDOWN @ {current_price:.2f}")
                print(f"   Lower Channel: {lower_channel:.2f} | Breakdown: {breakdown_strength:.2f}%")
                print(f"   Momentum: {current_momentum:.2f}% | ATR: {current_atr:.2f}")
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
print("🌙 Starting ATR Channel System Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, ATRChannelSystem, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 ATR CHANNEL SYSTEM - DEFAULT RESULTS")
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
    sma_period=range(18, 24, 2),
    atr_period=range(12, 18, 2),
    channel_multiplier=[1.2, 1.5, 1.8, 2.0],
    momentum_period=range(4, 8, 1),
    volume_threshold=[1.2, 1.3, 1.4, 1.5],
    profit_atr_mult=[2.0, 2.5, 3.0, 3.5],
    stop_atr_mult=[1.2, 1.5, 1.8, 2.0],
    max_hold_bars=range(60, 100, 15),
    maximize="Sharpe Ratio",
)

print("\n🌙 ATR CHANNEL SYSTEM - OPTIMIZED RESULTS")
print("=" * 80)
print(stats_opt)

print(f"\n🚀 OPTIMIZED METRICS:")
print(f"📊 Total Trades: {stats_opt['# Trades']}")
print(f"💰 Total Return: {stats_opt['Return [%]']:.2f}%")
print(f"📈 Sharpe Ratio: {stats_opt['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats_opt['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats_opt['Win Rate [%]']:.2f}%")

# Success metrics check
trade_requirement = stats_opt["# Trades"] >= 35
sharpe_requirement = stats_opt["Sharpe Ratio"] > 2.0

print(f"\n✅ STRATEGY VALIDATION:")
print(
    f"📊 Trade Count Requirement (>35): {'✅ PASS' if trade_requirement else '❌ FAIL'} ({stats_opt['# Trades']} trades)"
)
print(
    f"📈 Sharpe Ratio Requirement (>2.0): {'✅ PASS' if sharpe_requirement else '❌ FAIL'} ({stats_opt['Sharpe Ratio']:.2f})"
)

if trade_requirement and sharpe_requirement:
    print("\n🏆 ATR CHANNEL SYSTEM STRATEGY: SUCCESS! 🏆")
    print("🌟 This strategy meets both requirements!")
    print("   ✅ Volatility-adaptive channels")
    print("   ✅ Dynamic breakout detection")
    print("   ✅ ATR-based risk management")
    print("   ✅ Channel reversion exits")
else:
    print("\n⚠️ Strategy shows promise but needs further optimization...")

print("\n🌙 ATR Channel System backtest completed! ✨")
