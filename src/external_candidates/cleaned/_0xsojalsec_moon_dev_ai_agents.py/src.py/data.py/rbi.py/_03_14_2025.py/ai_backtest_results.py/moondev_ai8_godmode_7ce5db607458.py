# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\MoonDev_AI8_GODMODE.py
#!/usr/bin/env python3
# 🌙 AI8 - MoonDev GODMODE Strategy - INFINITE VICTORY
# Moon Dev Trading Command Center - GOD MODE ACTIVATED

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data with lunar precision 🌕
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean data columns with cosmic care ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Rename columns to match backtesting requirements
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

# Convert datetime and set index with lunar alignment 🌑
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

print(f"🌙 Data loaded: {len(data)} rows from {data.index[0]} to {data.index[-1]}")


class MoonDevGodMode(Strategy):
    def init(self):
        print("🌙 Initializing MoonDev GODMODE strategy...")

        # GOD MODE indicators 🚀
        self.sma10 = self.I(talib.SMA, self.data.Close, 10)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

        self.trade_count = 0
        self.last_trade_bar = 0

        print("✨ GOD MODE ACTIVATED!")

    def next(self):
        if len(self.data) < 50:
            return

        current_bar = len(self.data) - 1
        current_price = self.data.Close[-1]

        # GOD MODE STRATEGY: More frequent trades but with godly timing 🎯
        if not self.position and self.trade_count < 8:  # Allow up to 8 trades
            # Space trades by 3500 bars (about 5 weeks) for more opportunities
            if current_bar - self.last_trade_bar < 3500:
                return

            # GOD MODE entry conditions - simpler but more effective
            price_momentum = current_price > self.sma10[-1]  # Above short-term trend
            rsi_oversold_recovery = 25 < self.rsi[-1] < 55  # Recovery from oversold

            # Volume surge (when available)
            volume_surge = True  # Keep simple for now

            if price_momentum and rsi_oversold_recovery:
                # GOD MODE position sizing 💪
                position_multiplier = 1.0 + (self.trade_count * 0.1)  # Increase size with experience
                base_equity = min(self.equity * 0.95, 1000000)  # Use 95% of equity
                position_size = int((base_equity * position_multiplier) / current_price)

                if position_size > 0:
                    # Wide stop loss for trend following
                    stop_loss = current_price * 0.85  # 15% stop

                    self.buy(size=position_size, sl=stop_loss)
                    self.trade_count += 1
                    self.last_trade_bar = current_bar

                    print(f"🚀⚡ GOD MODE ENTRY #{self.trade_count}!")
                    print(f"   ⚡ Size: {position_size} @ {current_price:.2f}")
                    print(f"   📊 SMA10: {self.sma10[-1]:.0f}, RSI: {self.rsi[-1]:.1f}")
                    print(f"   🛡️ Stop: {stop_loss:.2f}")

        # GOD MODE exits - Let winners run but take profits strategically 🌊
        else:
            if self.position:
                entry_price = self.position.entry_price if hasattr(self.position, "entry_price") else current_price
                profit_pct = (current_price - entry_price) / entry_price
                bars_held = current_bar - self.last_trade_bar

                # Dynamic profit targets based on market conditions
                base_profit_target = 1.20  # 120% base target
                profit_target = base_profit_target + (self.trade_count * 0.15)  # Higher targets with experience

                # Exit conditions
                mega_profit = profit_pct > profit_target
                trend_broken = current_price < self.sma10[-1] * 0.92  # 8% below SMA10
                time_exit = bars_held > 6000 and profit_pct > 0.30  # Exit after holding long enough with good profit

                if mega_profit or trend_broken or time_exit:
                    self.position.close()
                    exit_reason = "MEGA PROFIT" if mega_profit else ("TREND BROKEN" if trend_broken else "TIME EXIT")
                    print(f"💰⚡ GOD MODE EXIT! {exit_reason}")
                    print(f"   ⚡ GODLY P&L: {profit_pct * 100:.1f}% @ {current_price:.2f}")
                    print(f"   📊 Target was: {profit_target * 100:.0f}%")


if __name__ == "__main__":
    print("🌙🚀 Starting MoonDev GODMODE Backtest...")

    # Run backtest with lunar power 🌕
    bt = Backtest(data, MoonDevGodMode, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print full statistics with cosmic flair ✨
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔 GODMODE MOONDEV STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print(f"\n🎯 Target: Beat Buy & Hold {stats['Buy & Hold Return [%]']:.1f}%")
    print(f"🚀 Strategy Return: {stats['Return [%]']:.1f}%")
    print(f"📊 Number of Trades: {stats['# Trades']}")

    if stats["# Trades"] > 0:
        print(f"🏆 Win Rate: {stats['Win Rate [%]']:.1f}%")
        print(f"📈 Best Trade: {stats['Best Trade [%]']:.1f}%")
        if not pd.isna(stats["Sharpe Ratio"]):
            print(f"💎 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")

    # GOD MODE victory conditions
    beats_buy_hold = stats["Return [%]"] > stats["Buy & Hold Return [%]"]
    enough_trades = stats["# Trades"] >= 5

    if beats_buy_hold and enough_trades:
        print("\n⚡👑🚀 GOD MODE VICTORY ACHIEVED! 🚀👑⚡")
        print("🎉⚡🎉 STRATEGY BEATS BUY & HOLD WITH 5+ TRADES! 🎉⚡🎉")
        print("🌙⚡✨👑✨⚡🌙⚡✨👑✨⚡🌙⚡✨👑✨⚡🌙⚡✨👑✨⚡🌙")
        print("🎯⚡ GODMODE MISSION: ABSOLUTELY CONQUERED! ⚡🎯")
    elif enough_trades:
        performance_ratio = stats["Return [%]"] / stats["Buy & Hold Return [%]"] * 100
        print(f"\n⚡ EXCELLENT! {stats['# Trades']} trades achieving {performance_ratio:.1f}% of buy-and-hold! ⚡")

        if stats["Return [%]"] > 100:
            print("🎊⚡ PHENOMENAL! Over 100% returns achieved! ⚡🎊")
        elif stats["Return [%]"] > 80:
            print("🌟⚡ OUTSTANDING! Over 80% returns! ⚡🌟")
    else:
        print(f"\n📊 {stats['# Trades']} trades with {stats['Return [%]']:.1f}% return - GODMODE processing...")

    # GODMODE analysis
    print(f"\n📈⚡ GODMODE Analysis:")
    print(f"   💰 Strategy: {stats['Return [%]']:.1f}%")
    print(f"   📊 Buy&Hold: {stats['Buy & Hold Return [%]']:.1f}%")
    print(f"   ⚡ Power Ratio: {stats['Return [%]'] / stats['Buy & Hold Return [%]'] * 100:.1f}%")

    if stats["# Trades"] >= 5:
        print(f"   ✅ Trade Count: {stats['# Trades']} (MINIMUM ACHIEVED)")
    else:
        print(f"   📊 Trade Count: {stats['# Trades']} (targeting 5+)")

    print("\n🌙⚡ MoonDev GODMODE Backtest Complete! ⚡🚀")
