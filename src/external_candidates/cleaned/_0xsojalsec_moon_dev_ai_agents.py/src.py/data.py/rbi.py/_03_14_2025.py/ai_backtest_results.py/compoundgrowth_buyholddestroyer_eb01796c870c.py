# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\CompoundGrowth_BuyHoldDestroyer.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compound Growth Buy & Hold Destroyer Strategy
AI6 Implementation for Moon Dev Trading System 🌙
Target: Beat 127.77% buy & hold return with 5+ trades

Strategy: Leverage compound growth through strategic early entries and full reinvestment
Key insight: Beat buy & hold by getting in early and letting compound growth work
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


class CompoundGrowthDestroyer(Strategy):
    """
    Compound Growth Strategy to Destroy Buy & Hold

    Strategy:
    1. Get in early with large positions during clear uptrends
    2. Hold through volatility with wide stops
    3. Take profits at major resistance and reinvest
    4. Scale position sizes with growing equity
    """

    # Strategy parameters - designed for compound growth
    ma_period = 30  # Trend identification
    entry_threshold = 0.02  # 2% above MA for entry
    profit_target = 0.25  # 25% profit target
    stop_loss = 0.15  # 15% stop loss (wide for volatility)
    max_positions = 8  # Limit number of trades for concentration

    def init(self):
        # Simple moving average for trend
        def calc_sma(data, period):
            return pd.Series(data).rolling(window=period).mean().values

        self.ma = self.I(calc_sma, self.data.Close, self.ma_period)

        # Track compound growth
        self.trades_taken = 0
        self.entry_price = None
        self.profit_target_price = None
        self.stop_loss_price = None
        self.last_trade_time = 0

    def next(self):
        if len(self.data) < self.ma_period + 1:
            return

        current_time = len(self.data)

        # Exit management
        if self.position:
            self.manage_compound_exits()
            return

        # Entry logic - only take high-conviction trades
        if self.trades_taken < self.max_positions and current_time - self.last_trade_time > 1000:  # Space out trades
            self.check_compound_entry()

    def check_compound_entry(self):
        """Look for high-conviction compound growth opportunities"""
        current_price = self.data.Close[-1]
        ma_level = self.ma[-1]

        # Strong uptrend condition
        uptrend = current_price > ma_level * (1 + self.entry_threshold)

        # Momentum confirmation - price rising
        momentum = len(self.data.Close) > 10 and current_price > self.data.Close[-10]

        # Volume confirmation
        recent_volume = np.mean([self.data.Volume[i] for i in range(-5, 0)])
        avg_volume = np.mean([self.data.Volume[i] for i in range(-25, -5)])
        volume_surge = recent_volume > avg_volume * 1.2

        # All conditions must be met for entry
        if uptrend and momentum and volume_surge:
            self.execute_compound_entry()

    def execute_compound_entry(self):
        """Execute compound growth entry with full capital deployment"""
        current_price = self.data.Close[-1]

        # Use most available capital for compound growth
        # Scale position size with equity growth
        if self.trades_taken == 0:
            capital_fraction = 0.95  # Go big on first trade
        elif self.trades_taken <= 2:
            capital_fraction = 0.90  # Maintain aggression
        else:
            capital_fraction = 0.85  # Stay aggressive

        available_capital = self.equity * capital_fraction
        position_size = int(available_capital / current_price)

        if position_size > 0:
            self.entry_price = current_price
            self.profit_target_price = current_price * (1 + self.profit_target)
            self.stop_loss_price = current_price * (1 - self.stop_loss)
            self.trades_taken += 1
            self.last_trade_time = len(self.data)

            self.buy(size=position_size)

            print(f"🚀 COMPOUND ENTRY #{self.trades_taken}: Size={position_size} @ {current_price:.2f}")
            print(f"   Capital Used: ${available_capital:.0f} ({capital_fraction:.0%})")
            print(f"   Profit Target: {self.profit_target_price:.2f} (+{self.profit_target:.0%})")
            print(f"   Stop Loss: {self.stop_loss_price:.2f} (-{self.stop_loss:.0%})")
            print(f"   Equity: ${self.equity:.0f}")

    def manage_compound_exits(self):
        """Manage exits for maximum compound growth"""
        current_price = self.data.Close[-1]

        # Take profit at target
        if current_price >= self.profit_target_price:
            profit_amount = self.equity - 1000000  # Profit from initial capital
            profit_pct = ((current_price - self.entry_price) / self.entry_price) * 100
            self.position.close()
            print(f"🎯 COMPOUND PROFIT @ {current_price:.2f} | Profit: {profit_pct:.1f}%")
            print(f"   Total Profit: ${profit_amount:.0f} | New Equity: ${self.equity:.0f}")
            self.reset_compound_position()
            return

        # Stop loss
        if current_price <= self.stop_loss_price:
            loss_pct = ((current_price - self.entry_price) / self.entry_price) * 100
            self.position.close()
            print(f"🛑 COMPOUND STOP @ {current_price:.2f} | Loss: {loss_pct:.1f}%")
            print(f"   Remaining Equity: ${self.equity:.0f}")
            self.reset_compound_position()
            return

        # Trailing stop for big winners (50%+ gains)
        if current_price > self.entry_price * 1.5:
            trailing_stop = current_price * 0.9  # 10% trailing
            if trailing_stop > self.stop_loss_price:
                self.stop_loss_price = trailing_stop
                print(f"📈 COMPOUND TRAILING STOP: {self.stop_loss_price:.2f}")

    def reset_compound_position(self):
        """Reset position for next compound opportunity"""
        self.entry_price = None
        self.profit_target_price = None
        self.stop_loss_price = None


# Run backtest
print("🌙 Starting Compound Growth Buy & Hold Destroyer...")
print("Target: Beat 127.77% through Strategic Compound Growth")
print("=" * 70)

bt = Backtest(data, CompoundGrowthDestroyer, cash=1000000, commission=0.002)
stats = bt.run()

print("\n🌙 Compound Growth Destroyer Results:")
print("=" * 70)
print(stats)

# Key metrics
print(f"\n⭐ Compound Growth Performance:")
print(f"💰 Total Return: {stats['Return [%]']:.2f}%")
print(f"🎯 Buy & Hold Benchmark: 127.77%")
print(f"📈 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"🎯 Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"📊 Total Trades: {stats['# Trades']}")

# Calculate compound annual growth rate
if stats["Return [%]"] > 0:
    days = 323
    cagr = (((1 + stats["Return [%]"] / 100) ** (365 / days)) - 1) * 100
    print(f"📈 Compound Annual Growth Rate: {cagr:.1f}%")

# Success check
if stats["Return [%]"] > 127.77 and stats["# Trades"] >= 5:
    print(f"\n🏆 SUCCESS! Compound Growth DESTROYS buy & hold!")
    print(f"   Strategy: {stats['Return [%]']:.2f}% vs Buy & Hold: 127.77%")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")
    print(f"   Outperformance: {stats['Return [%]'] - 127.77:.2f}%")
    print(f"   🔥 COMPOUND GROWTH VICTORY! 🔥")
elif stats["# Trades"] >= 5:
    print(f"\n✅ TRADE COUNT MET but return insufficient")
    print(f"   Strategy: {stats['Return [%]']:.2f}% vs Buy & Hold: 127.77%")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")
    print(f"   Underperformance: {stats['Return [%]'] - 127.77:.2f}%")
else:
    print(f"\n❌ Requirements not met")
    print(f"   Return: {stats['Return [%]']:.2f}% (Target: >127.77%)")
    print(f"   Trades: {stats['# Trades']} (Required: 5+)")

print("\n🌙 Compound Growth Destroyer completed! ✨")
