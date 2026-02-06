# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\MoonDev_AI8_ULTIMATE.py
#!/usr/bin/env python3
# 🌙 AI8 - MoonDev ULTIMATE Strategy - The Final Solution
# Moon Dev Trading Command Center - ULTIMATE VICTORY

import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data with lunar precision 🌕
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

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


class MoonDevUltimate(Strategy):
    def init(self):
        print("🌙 Initializing MoonDev ULTIMATE strategy...")

        # The ULTIMATE solution - Buy early, hold long 🚀
        self.sma10 = self.I(talib.SMA, self.data.Close, 10)
        self.sma30 = self.I(talib.SMA, self.data.Close, 30)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

        self.trade_count = 0
        self.entry_dates = []

        print("✨ Ultimate victory system ready!")

    def next(self):
        if len(self.data) < 50:
            return

        current_date = self.data.index[-1]
        current_price = self.data.Close[-1]

        # ULTIMATE STRATEGY: Buy every 6-8 weeks during uptrend and HOLD LONG 🎯
        if not self.position and self.trade_count < 8:  # Max 8 strategic entries

            # Check if enough time has passed since last trade (6 weeks minimum)
            if self.entry_dates:
                last_entry = self.entry_dates[-1]
                weeks_since = (current_date - last_entry).days / 7
                if weeks_since < 6:
                    return

            # Only enter during clear uptrends
            uptrend = self.sma10[-1] > self.sma30[-1] and current_price > self.sma10[-1]

            # RSI not extremely overbought
            rsi_ok = self.rsi[-1] < 75

            # Price momentum (higher than 20 bars ago)
            momentum_bars = min(20, len(self.data) - 10)  # Safe lookback
            momentum = current_price > self.data.Close[-momentum_bars]

            if uptrend and rsi_ok and momentum:
                # Use substantial position size for major gains
                position_value = self.equity * 0.90  # 90% of equity
                position_size = int(position_value / current_price)

                if position_size > 0:
                    # Wide stop loss - let trends run
                    stop_loss = current_price * 0.80  # 20% stop

                    self.buy(size=position_size, sl=stop_loss)
                    self.trade_count += 1
                    self.entry_dates.append(current_date)

                    print(f"🚀🌟 ULTIMATE ENTRY #{self.trade_count}!")
                    print(f"   💎 Size: {position_size} @ {current_price:.2f}")
                    print(f"   📅 Date: {current_date.strftime('%Y-%m-%d')}")
                    print(
                        f"   📊 SMA10: {self.sma10[-1]:.0f}, SMA30: {self.sma30[-1]:.0f}"
                    )
                    print(f"   🛡️ Stop: {stop_loss:.2f}")

        # HOLD LONG - Only exit on major reversals or massive profits 🌊
        else:
            if self.position:
                entry_price = (
                    self.position.entry_price
                    if hasattr(self.position, "entry_price")
                    else current_price
                )
                profit_pct = (current_price - entry_price) / entry_price

                # Only exit on severe conditions
                major_bear = (
                    self.sma10[-1] < self.sma30[-1]
                    and current_price < self.sma30[-1] * 0.95
                )  # 5% below SMA30

                massive_profit = profit_pct > 1.5  # 150% profit

                # Time-based exit (hold for at least 4 weeks, exit after 12 weeks max)
                entry_date = self.entry_dates[-1] if self.entry_dates else current_date
                weeks_held = (current_date - entry_date).days / 7
                time_exit = weeks_held > 12  # Exit after 12 weeks regardless

                if major_bear or massive_profit or time_exit:
                    self.position.close()
                    exit_reason = (
                        "MAJOR BEAR"
                        if major_bear
                        else ("MASSIVE PROFIT" if massive_profit else "TIME EXIT")
                    )
                    print(f"💰🌟 ULTIMATE EXIT! {exit_reason}")
                    print(f"   🎯 P&L: {profit_pct*100:.1f}% @ {current_price:.2f}")
                    print(f"   ⏰ Held for {weeks_held:.1f} weeks")


if __name__ == "__main__":
    print("🌙🚀 Starting MoonDev ULTIMATE Backtest...")

    # Run backtest with lunar power 🌕
    bt = Backtest(data, MoonDevUltimate, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print full statistics with cosmic flair ✨
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔 ULTIMATE MOONDEV STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print(f"\n🎯 Target: Beat Buy & Hold {stats['Buy & Hold Return [%]']:.1f}%")
    print(f"🚀 Strategy Return: {stats['Return [%]']:.1f}%")
    print(f"📊 Number of Trades: {stats['# Trades']}")

    if stats["# Trades"] > 0:
        print(f"🏆 Win Rate: {stats['Win Rate [%]']:.1f}%")
        print(f"📈 Best Trade: {stats['Best Trade [%]']:.1f}%")
        print(f"📉 Max Drawdown: {stats['Max. Drawdown [%]']:.1f}%")

    # Victory conditions
    beats_buy_hold = stats["Return [%]"] > stats["Buy & Hold Return [%]"]
    enough_trades = stats["# Trades"] >= 5

    if beats_buy_hold and enough_trades:
        print("\n🏆🌙🚀 ULTIMATE VICTORY ACHIEVED! 🚀🌙🏆")
        print("🎉🎉🎉 STRATEGY BEATS BUY & HOLD WITH 5+ TRADES! 🎉🎉🎉")
        print("🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨🌙🚀✨")
    elif enough_trades:
        print(f"\n✅ Great! {stats['# Trades']} trades completed")
        return_ratio = stats["Return [%]"] / stats["Buy & Hold Return [%]"]
        print(f"📊 Performance: {return_ratio*100:.1f}% of buy-and-hold")
        if stats["Return [%]"] > 100:
            print("🎊 Excellent returns over 100%! 🎊")
    elif beats_buy_hold:
        print(f"\n🎯 Beats buy-and-hold but only {stats['# Trades']} trades")
    else:
        print("\n🔄 Continuing to optimize...")

    print(f"\n📈 Final Analysis:")
    print(f"   💰 Total Return: {stats['Return [%]']:.1f}%")
    print(f"   📊 Buy & Hold: {stats['Buy & Hold Return [%]']:.1f}%")
    print(
        f"   🎯 Difference: {stats['Return [%]'] - stats['Buy & Hold Return [%]']:.1f}%"
    )

    print("\n🌙 MoonDev ULTIMATE Backtest Complete! 🚀")
