# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\MACDDivergence_BT.py
# 🌙 Moon Dev's MACD Divergence Strategy 🌙
# WORKING STRATEGY - MACD histogram divergence trading with momentum confirmation
# Targeting 80-200 trades with 2.0+ Sharpe through divergence signal capture

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


class MACDDivergence(Strategy):
    """
    🌙 MACD DIVERGENCE STRATEGY 🌙

    A divergence-based strategy designed for:
    - Detecting momentum divergences between price and MACD
    - Early trend reversal signal capture
    - MACD histogram and signal line analysis
    - 80-200 trades with 2.0+ Sharpe ratio

    Strategy Logic:
    - Enter long when MACD shows bullish divergence (price lower low, MACD higher low)
    - Enter short when MACD shows bearish divergence (price higher high, MACD lower high)
    - Use MACD crossover signals for confirmation
    - Exit on opposite MACD signal or profit target
    """

    # Strategy parameters
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    divergence_lookback = 15
    min_divergence_strength = 0.01  # Minimum divergence percentage
    position_size = 0.95
    profit_target_pct = 2.5
    stop_loss_pct = 1.5
    max_hold_bars = 80

    def init(self):
        # MACD calculation function
        def calc_macd(values, fast=12, slow=26, signal=9):
            close = pd.Series(values)
            ema_fast = close.ewm(span=fast).mean()
            ema_slow = close.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            return macd_line.values, signal_line.values, histogram.values

        # Simple Moving Average for trend context
        def calc_sma(values, period):
            return pd.Series(values).rolling(window=period).mean().values

        # Initialize MACD indicators
        macd, signal, histogram = calc_macd(self.data.Close, self.macd_fast, self.macd_slow, self.macd_signal)
        self.macd_line = self.I(lambda: macd)
        self.macd_signal = self.I(lambda: signal)
        self.macd_histogram = self.I(lambda: histogram)

        # Trend context
        self.sma_50 = self.I(calc_sma, self.data.Close, 50)

        # Trade management
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.entry_time = None

        print("🌙✨ MACD Divergence Strategy Initialized! ✨")

    def next(self):
        # Skip if not enough data
        if len(self.data) < max(self.macd_slow + self.macd_signal, self.divergence_lookback, 50) + 5:
            return

        current_price = self.data.Close[-1]
        current_time = len(self.data)

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

            # MACD-based exit signals
            if self.position.is_long:
                # Exit long on bearish MACD crossover
                if self.macd_line[-1] < self.macd_signal[-1] and self.macd_line[-2] >= self.macd_signal[-2]:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 LONG MACD EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return
            else:
                # Exit short on bullish MACD crossover
                if self.macd_line[-1] > self.macd_signal[-1] and self.macd_line[-2] <= self.macd_signal[-2]:
                    self.position.close()
                    pnl = self.calculate_pnl(current_price)
                    print(f"🔄 SHORT MACD EXIT @ {current_price:.2f} ({pnl:.2f}%)")
                    self.reset_trade_params()
                    return

        # Look for divergence signals
        else:
            # Check for bullish divergence
            bullish_div = self.detect_bullish_divergence()
            if bullish_div["detected"]:
                # Confirm with MACD bullish crossover or histogram turning up
                macd_bullish = (
                    self.macd_line[-1] > self.macd_signal[-1] or self.macd_histogram[-1] > self.macd_histogram[-2]
                )

                if macd_bullish:
                    self.buy(size=self.position_size)
                    self.entry_price = current_price
                    self.stop_loss = current_price * (1 - self.stop_loss_pct / 100)
                    self.take_profit = current_price * (1 + self.profit_target_pct / 100)
                    self.entry_time = current_time

                    print(f"🚀 LONG BULLISH DIV @ {current_price:.2f} | Strength: {bullish_div['strength']:.3f}")
                    print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")

            # Check for bearish divergence
            bearish_div = self.detect_bearish_divergence()
            if bearish_div["detected"]:
                # Confirm with MACD bearish crossover or histogram turning down
                macd_bearish = (
                    self.macd_line[-1] < self.macd_signal[-1] or self.macd_histogram[-1] < self.macd_histogram[-2]
                )

                if macd_bearish:
                    self.sell(size=self.position_size)
                    self.entry_price = current_price
                    self.stop_loss = current_price * (1 + self.stop_loss_pct / 100)
                    self.take_profit = current_price * (1 - self.profit_target_pct / 100)
                    self.entry_time = current_time

                    print(f"📉 SHORT BEARISH DIV @ {current_price:.2f} | Strength: {bearish_div['strength']:.3f}")
                    print(f"   SL: {self.stop_loss:.2f} | TP: {self.take_profit:.2f}")

    def detect_bullish_divergence(self):
        """Detect bullish divergence between price and MACD"""
        if len(self.data) < self.divergence_lookback + 5:
            return {"detected": False, "strength": 0}

        # Find recent price and MACD lows
        price_data = self.data.Close[-self.divergence_lookback :]
        macd_data = self.macd_line[-self.divergence_lookback :]

        # Find two significant lows
        price_lows = []
        macd_lows = []

        for i in range(2, len(price_data) - 2):
            # Price low detection
            if (
                price_data[i] < price_data[i - 1]
                and price_data[i] < price_data[i - 2]
                and price_data[i] < price_data[i + 1]
                and price_data[i] < price_data[i + 2]
            ):
                price_lows.append((i, price_data[i]))

            # MACD low detection
            if (
                macd_data[i] < macd_data[i - 1]
                and macd_data[i] < macd_data[i - 2]
                and macd_data[i] < macd_data[i + 1]
                and macd_data[i] < macd_data[i + 2]
            ):
                macd_lows.append((i, macd_data[i]))

        # Need at least 2 lows for divergence
        if len(price_lows) < 2 or len(macd_lows) < 2:
            return {"detected": False, "strength": 0}

        # Check for divergence: price making lower low, MACD making higher low
        recent_price_low = min(price_lows, key=lambda x: x[1])  # Lowest price
        recent_macd_low = min(macd_lows, key=lambda x: x[1])  # Lowest MACD

        # Find previous lows
        prev_price_lows = [low for low in price_lows if low[0] < recent_price_low[0]]
        prev_macd_lows = [low for low in macd_lows if low[0] < recent_macd_low[0]]

        if not prev_price_lows or not prev_macd_lows:
            return {"detected": False, "strength": 0}

        prev_price_low = min(prev_price_lows, key=lambda x: x[1])
        prev_macd_low = min(prev_macd_lows, key=lambda x: x[1])

        # Check divergence conditions
        price_lower = recent_price_low[1] < prev_price_low[1]
        macd_higher = recent_macd_low[1] > prev_macd_low[1]

        if price_lower and macd_higher:
            # Calculate divergence strength
            price_change = (prev_price_low[1] - recent_price_low[1]) / prev_price_low[1]
            macd_change = (
                (recent_macd_low[1] - prev_macd_low[1]) / abs(prev_macd_low[1]) if prev_macd_low[1] != 0 else 0
            )
            strength = price_change + macd_change

            if strength >= self.min_divergence_strength:
                return {"detected": True, "strength": strength}

        return {"detected": False, "strength": 0}

    def detect_bearish_divergence(self):
        """Detect bearish divergence between price and MACD"""
        if len(self.data) < self.divergence_lookback + 5:
            return {"detected": False, "strength": 0}

        # Find recent price and MACD highs
        price_data = self.data.Close[-self.divergence_lookback :]
        macd_data = self.macd_line[-self.divergence_lookback :]

        # Find two significant highs
        price_highs = []
        macd_highs = []

        for i in range(2, len(price_data) - 2):
            # Price high detection
            if (
                price_data[i] > price_data[i - 1]
                and price_data[i] > price_data[i - 2]
                and price_data[i] > price_data[i + 1]
                and price_data[i] > price_data[i + 2]
            ):
                price_highs.append((i, price_data[i]))

            # MACD high detection
            if (
                macd_data[i] > macd_data[i - 1]
                and macd_data[i] > macd_data[i - 2]
                and macd_data[i] > macd_data[i + 1]
                and macd_data[i] > macd_data[i + 2]
            ):
                macd_highs.append((i, macd_data[i]))

        # Need at least 2 highs for divergence
        if len(price_highs) < 2 or len(macd_highs) < 2:
            return {"detected": False, "strength": 0}

        # Check for divergence: price making higher high, MACD making lower high
        recent_price_high = max(price_highs, key=lambda x: x[1])  # Highest price
        recent_macd_high = max(macd_highs, key=lambda x: x[1])  # Highest MACD

        # Find previous highs
        prev_price_highs = [high for high in price_highs if high[0] < recent_price_high[0]]
        prev_macd_highs = [high for high in macd_highs if high[0] < recent_macd_high[0]]

        if not prev_price_highs or not prev_macd_highs:
            return {"detected": False, "strength": 0}

        prev_price_high = max(prev_price_highs, key=lambda x: x[1])
        prev_macd_high = max(prev_macd_highs, key=lambda x: x[1])

        # Check divergence conditions
        price_higher = recent_price_high[1] > prev_price_high[1]
        macd_lower = recent_macd_high[1] < prev_macd_high[1]

        if price_higher and macd_lower:
            # Calculate divergence strength
            price_change = (recent_price_high[1] - prev_price_high[1]) / prev_price_high[1]
            macd_change = (
                (prev_macd_high[1] - recent_macd_high[1]) / abs(prev_macd_high[1]) if prev_macd_high[1] != 0 else 0
            )
            strength = price_change + macd_change

            if strength >= self.min_divergence_strength:
                return {"detected": True, "strength": strength}

        return {"detected": False, "strength": 0}

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
print("🌙 Starting MACD Divergence Backtest (Default Parameters)...")
print("=" * 80)

bt = Backtest(data, MACDDivergence, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 MACD DIVERGENCE - DEFAULT RESULTS")
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
    macd_fast=range(10, 16, 2),
    macd_slow=range(24, 30, 2),
    macd_signal=range(8, 12, 1),
    divergence_lookback=range(10, 18, 2),
    min_divergence_strength=[0.005, 0.01, 0.015, 0.02],
    profit_target_pct=[2.0, 2.5, 3.0, 3.5],
    stop_loss_pct=[1.2, 1.5, 1.8, 2.0],
    max_hold_bars=range(60, 100, 10),
    maximize="Sharpe Ratio",
)

print("\n🌙 MACD DIVERGENCE - OPTIMIZED RESULTS")
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
    print("\n🏆 MACD DIVERGENCE STRATEGY: SUCCESS! 🏆")
    print("🌟 This strategy meets both requirements!")
    print("   ✅ Divergence detection system")
    print("   ✅ MACD confirmation signals")
    print("   ✅ Early reversal capture")
    print("   ✅ Momentum-based exits")
else:
    print("\n⚠️ Strategy shows promise but needs further optimization...")

print("\n🌙 MACD Divergence backtest completed! ✨")
