# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentVolume_AI8_Ultra.py
#!/usr/bin/env python3
# 🌙 AI8 - DivergentVolume Ultra Strategy - Major Trend Catcher
# Moon Dev Trading Command Center

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


class DivergentVolumeUltra(Strategy):
    def init(self):
        print("🌙 Initializing DivergentVolumeUltra strategy...")

        # Major trend identification system 🚀
        self.ema20 = self.I(talib.EMA, self.data.Close, 20)
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.macd_signal, _ = self.I(talib.MACD, self.data.Close, 12, 26, 9)

        # Volume analysis for institutional moves
        self.volume_sma20 = self.I(talib.SMA, self.data.Volume, 20)
        self.volume_sma50 = self.I(talib.SMA, self.data.Volume, 50)

        # Volatility and trend strength
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2)

        self.trade_count = 0
        self.last_trade_time = None

        print("✨ Ultra volume trend indicators initialized!")

    def next(self):
        if len(self.data) < 250:  # Need 200+ bars for EMA200
            return

        current_time = self.data.index[-1]
        current_price = self.data.Close[-1]

        # Major trend detection 🎯
        if not self.position and self.trade_count < 10:
            # Long-term trend alignment
            bull_market = self.ema20[-1] > self.ema50[-1] > self.ema200[-1] and current_price > self.ema200[-1]

            # Momentum confirmation
            macd_momentum = self.macd[-1] > self.macd_signal[-1] and self.macd[-1] > self.macd[-5]  # Accelerating

            # Volume surge indicating institutional interest
            volume_surge = (
                self.data.Volume[-1] > self.volume_sma20[-1] * 1.5
                and self.volume_sma20[-1] > self.volume_sma50[-1] * 1.2
            )

            # RSI in sweet spot (not too low, not too high)
            rsi_healthy = 40 < self.rsi[-1] < 65

            # Price action - breaking above resistance or pullback buy
            recent_high = max(self.data.High[-20:])
            breakout = current_price > recent_high * 1.002  # Breaking above 20-period high

            pullback_buy = current_price > self.ema20[-1] and self.data.Low[-1] <= self.ema20[-1] * 1.01  # Touch EMA20

            # Time filter - avoid overtrading
            time_ok = True
            if self.last_trade_time:
                hours_since_last = (current_time - self.last_trade_time).total_seconds() / 3600
                time_ok = hours_since_last > 168  # 1 week minimum between trades

            if (
                bull_market
                and macd_momentum
                and volume_surge
                and rsi_healthy
                and (breakout or pullback_buy)
                and time_ok
            ):
                # Major position sizing for trend following 💪
                # Risk 40% of equity per trade for maximum returns
                risk_amount = self.equity * 0.40

                # Use ATR for position sizing
                atr_value = self.atr[-1] if len(self.atr) > 0 else current_price * 0.03
                stop_distance = atr_value * 3  # Wider stops for trends

                position_size = int(risk_amount / stop_distance)

                # Ensure reasonable position size
                max_position_value = self.equity * 0.90
                max_size = int(max_position_value / current_price)
                position_size = min(position_size, max_size)

                if position_size > 0:
                    stop_loss = current_price - stop_distance

                    self.buy(size=position_size, sl=stop_loss)
                    self.trade_count += 1
                    self.last_trade_time = current_time

                    entry_type = "BREAKOUT" if breakout else "PULLBACK"
                    print(f"🚀🌟 ULTRA VOLUME ENTRY #{self.trade_count}! {entry_type}")
                    print(f"   💰 Size: {position_size} @ {current_price:.2f}")
                    print(f"   📊 Volume: {self.data.Volume[-1] / self.volume_sma20[-1]:.1f}x avg")
                    print(f"   📈 EMA Stack: {self.ema20[-1]:.0f} > {self.ema50[-1]:.0f} > {self.ema200[-1]:.0f}")
                    print(f"   🛡️ Stop: {stop_loss:.2f}")

        # Trend-following exits with profit maximization 🌊
        else:
            if self.position:
                entry_price = self.position.entry_price if hasattr(self.position, "entry_price") else current_price
                profit_pct = (current_price - entry_price) / entry_price

                # Major trend reversal signals
                bear_market = self.ema20[-1] < self.ema50[-1] or current_price < self.ema50[-1]

                macd_bearish = self.macd[-1] < self.macd_signal[-1] and self.macd[-1] < self.macd[-5]  # Decelerating

                rsi_overbought = self.rsi[-1] > 75

                # Profit targets for different scenarios
                massive_profit = profit_pct > 0.50  # 50% profit
                big_profit = profit_pct > 0.25  # 25% profit
                good_profit = profit_pct > 0.15  # 15% profit

                # Exit logic
                should_exit = False
                exit_reason = ""

                if massive_profit:
                    should_exit = True
                    exit_reason = "MASSIVE PROFIT"
                elif big_profit and (bear_market or macd_bearish):
                    should_exit = True
                    exit_reason = "BIG PROFIT + TREND WEAK"
                elif good_profit and bear_market and rsi_overbought:
                    should_exit = True
                    exit_reason = "GOOD PROFIT + BEAR SIGNALS"
                elif bear_market and macd_bearish and profit_pct < -0.05:
                    should_exit = True
                    exit_reason = "TREND REVERSAL"

                if should_exit:
                    self.position.close()
                    print(f"💎 ULTRA EXIT! {exit_reason}")
                    print(f"   💰 P&L: {profit_pct * 100:.1f}% @ {current_price:.2f}")


if __name__ == "__main__":
    print("🌙🚀 Starting DivergentVolumeUltra Backtest...")

    # Run backtest with lunar power 🌕
    bt = Backtest(data, DivergentVolumeUltra, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print full statistics with cosmic flair ✨
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔 ULTRA VOLUME STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print(f"\n🎯 Target: Beat Buy & Hold {stats['Buy & Hold Return [%]']:.1f}%")
    print(f"🚀 Strategy Return: {stats['Return [%]']:.1f}%")
    print(f"📊 Number of Trades: {stats['# Trades']}")

    if stats["Return [%]"] > stats["Buy & Hold Return [%]"] and stats["# Trades"] >= 5:
        print("🏆 SUCCESS! Strategy beats buy & hold with 5+ trades! 🌙🚀")
    else:
        print("🔄 Needs optimization...")

    print("\n🌙 DivergentVolumeUltra Backtest Complete! 🚀")
