# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\DivergentPulse_AI8_Ultra.py
#!/usr/bin/env python3
# 🌙 AI8 - DivergentPulse Ultra Strategy - High Frequency Trend Follower
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


class DivergentPulseUltra(Strategy):
    def init(self):
        print("🌙 Initializing DivergentPulseUltra strategy...")

        # Multi-timeframe trend following system 🚀
        self.ema8 = self.I(talib.EMA, self.data.Close, 8)
        self.ema21 = self.I(talib.EMA, self.data.Close, 21)
        self.ema55 = self.I(talib.EMA, self.data.Close, 55)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.macd, self.macd_signal, _ = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        # Trend strength indicators
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20)

        self.trade_count = 0
        self.last_entry_price = 0

        print("✨ Ultra pulse indicators initialized!")

    def next(self):
        if len(self.data) < 60:
            return

        current_price = self.data.Close[-1]

        # Trend following with multiple timeframes 🎯
        if not self.position and self.trade_count < 20:  # Allow more trades
            # Strong trend conditions
            ema_stack = self.ema8[-1] > self.ema21[-1] > self.ema55[-1]  # Bullish EMA stack
            macd_bullish = self.macd[-1] > self.macd_signal[-1] and self.macd[-1] > 0
            trend_strength = self.adx[-1] > 25  # Strong trend
            rsi_not_overbought = self.rsi[-1] < 70

            # Entry on pullback to EMA8 in strong trend
            pullback_entry = (
                current_price > self.ema8[-1] * 0.999  # At or near EMA8
                and self.data.Close[-2] < self.ema8[-2]
            )  # Was below yesterday

            # Breakout entry
            recent_high = max(self.data.High[-5:])
            breakout_entry = current_price > recent_high * 1.001  # Breaking above recent high

            # Volume confirmation
            volume_surge = self.data.Volume[-1] > self.volume_sma[-1] * 1.1

            # Avoid entries too close to last one
            price_distance = abs(current_price - self.last_entry_price) / current_price > 0.05

            if (
                ema_stack
                and macd_bullish
                and trend_strength
                and rsi_not_overbought
                and (pullback_entry or breakout_entry)
                and volume_surge
                and price_distance
            ):
                # Aggressive position sizing for high returns 💪
                risk_amount = self.equity * 0.25  # 25% of equity per trade
                atr_value = self.atr[-1] if len(self.atr) > 0 else current_price * 0.02

                # Position size based on ATR stop
                stop_distance = atr_value * 1.5
                position_size = int(risk_amount / stop_distance)

                # Cap position size to reasonable amount
                max_position_value = self.equity * 0.8
                max_size = int(max_position_value / current_price)
                position_size = min(position_size, max_size)

                if position_size > 0:
                    stop_loss = current_price - stop_distance

                    self.buy(size=position_size, sl=stop_loss)
                    self.trade_count += 1
                    self.last_entry_price = current_price

                    print(f"🚀💥 PULSE ULTRA ENTRY #{self.trade_count}! Size: {position_size} @ {current_price:.2f}")
                    print(f"   📈 EMA Stack: {self.ema8[-1]:.0f} > {self.ema21[-1]:.0f} > {self.ema55[-1]:.0f}")
                    print(f"   🛡️ Stop: {stop_loss:.2f}, ADX: {self.adx[-1]:.1f}")

        # Trend-following exits 🌊
        else:
            if self.position:
                entry_price = self.position.entry_price if hasattr(self.position, "entry_price") else current_price

                # Exit on trend weakness or profit targets
                ema_bearish = self.ema8[-1] < self.ema21[-1]  # Fast EMA crosses below
                macd_bearish = self.macd[-1] < self.macd_signal[-1]
                rsi_overbought = self.rsi[-1] > 80

                # Profit targets
                profit_pct = (current_price - entry_price) / entry_price
                big_profit = profit_pct > 0.12  # 12% profit
                good_profit = profit_pct > 0.06  # 6% profit with weakness

                if (
                    ema_bearish
                    or macd_bearish
                    or rsi_overbought
                    or big_profit
                    or (good_profit and (ema_bearish or macd_bearish))
                ):
                    self.position.close()
                    print(f"💰 PULSE EXIT! P&L: {profit_pct * 100:.1f}% @ {current_price:.2f}")


if __name__ == "__main__":
    print("🌙🚀 Starting DivergentPulseUltra Backtest...")

    # Run backtest with lunar power 🌕
    bt = Backtest(data, DivergentPulseUltra, cash=1_000_000, commission=0.002)
    stats = bt.run()

    # Print full statistics with cosmic flair ✨
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔 ULTRA PULSE STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print(f"\n🎯 Target: Beat Buy & Hold {stats['Buy & Hold Return [%]']:.1f}%")
    print(f"🚀 Strategy Return: {stats['Return [%]']:.1f}%")
    print(f"📊 Number of Trades: {stats['# Trades']}")

    if stats["Return [%]"] > stats["Buy & Hold Return [%]"] and stats["# Trades"] >= 5:
        print("🏆 SUCCESS! Strategy beats buy & hold with 5+ trades! 🌙🚀")
    else:
        print("🔄 Needs optimization...")

    print("\n🌙 DivergentPulseUltra Backtest Complete! 🚀")
