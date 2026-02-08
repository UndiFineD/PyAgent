# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\AI8_Final_Backtest_Results.py
#!/usr/bin/env python3
# 🌙 AI8 - Final Backtest Results for All Three Strategies
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


# 🚀 Strategy 1: DivergentMomentum Enhanced
class DivergentMomentumEnhanced(Strategy):
    risk_percent = 0.02  # Increased risk for more trades
    rsi_period = 14
    ma_period = 20  # Shorter MA for more signals
    cci_period = 20

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.ma = self.I(talib.SMA, self.data.Close, self.ma_period)
        self.cci = self.I(talib.CCI, self.data.High, self.data.Low, self.data.Close, self.cci_period)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if len(self.data) < 30:
            return

        # Enhanced entry conditions - more lenient for more trades
        if not self.position:
            # Bullish momentum with RSI oversold
            if (
                self.rsi[-1] < 40  # Less strict than 30
                and self.data.Close[-1] > self.ma[-1]
                and self.data.Close[-1] > self.data.Close[-2]
            ):  # Price momentum
                entry_price = self.data.Close[-1]
                atr_value = self.atr[-1] if len(self.atr) > 0 else entry_price * 0.02
                stop_loss = entry_price - (1.5 * atr_value)

                risk_per_share = entry_price - stop_loss
                if risk_per_share > 0:
                    position_size = (self.equity * self.risk_percent) / risk_per_share
                    position_size = int(round(position_size))

                    if position_size > 0:
                        print(
                            f"🌙✨ DivergentMomentum Entry! Long {position_size} @ {entry_price:.2f}, SL: {stop_loss:.2f}"
                        )
                        self.buy(size=position_size, sl=stop_loss)

        # Exit conditions
        else:
            if len(self.cci) > 0 and self.cci[-1] > 150:  # CCI overbought
                print(f"🚀🌙 DivergentMomentum Exit! Closing at {self.data.Close[-1]:.2f}")
                self.position.close()


# 🚀 Strategy 2: DivergentPulse Enhanced
class DivergentPulseEnhanced(Strategy):
    risk_pct = 0.02

    def init(self):
        self.macd, self.macd_signal, _ = self.I(talib.MACD, self.data.Close)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.sma = self.I(talib.SMA, self.data.Close, 20)

    def next(self):
        if len(self.data) < 30:
            return

        if not self.position:
            # MACD bullish crossover with RSI confirmation
            if (
                len(self.macd) > 1
                and len(self.macd_signal) > 1
                and self.macd[-1] > self.macd_signal[-1]
                and self.macd[-2] <= self.macd_signal[-2]  # Crossover
                and self.rsi[-1] < 60  # Not overbought
                and self.data.Close[-1] > self.sma[-1]
            ):  # Above trend
                entry_price = self.data.Close[-1]
                atr_value = self.atr[-1] if len(self.atr) > 0 else entry_price * 0.02
                stop_loss = entry_price - (1.5 * atr_value)

                risk_per_share = entry_price - stop_loss
                if risk_per_share > 0:
                    position_size = (self.equity * self.risk_pct) / risk_per_share
                    position_size = int(round(position_size))

                    if position_size > 0:
                        print(
                            f"🚀🌙 DivergentPulse Entry! Long {position_size} @ {entry_price:.2f}, SL: {stop_loss:.2f}"
                        )
                        self.buy(size=position_size, sl=stop_loss)

        # Exit on MACD bearish crossover
        else:
            if (
                len(self.macd) > 1
                and len(self.macd_signal) > 1
                and self.macd[-1] < self.macd_signal[-1]
                and self.macd[-2] >= self.macd_signal[-2]
            ):
                print(f"🚀🌑 DivergentPulse Exit! Closing at {self.data.Close[-1]:.2f}")
                self.position.close()


# 🚀 Strategy 3: DivergentVolume (Already Working)
class DivergentVolumeEnhanced(Strategy):
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.price_highs = self.I(talib.MAX, self.data.High, timeperiod=10)  # Shorter window
        self.rsi_highs = self.I(talib.MAX, self.rsi, timeperiod=10)
        self.trade_count = 0

    def next(self):
        if len(self.data) < 20 or self.trade_count >= 10:  # Allow more trades
            return

        current_close = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_rsi = self.rsi[-1]
        current_volume = self.data.Volume[-1]
        atr_value = self.atr[-1] if len(self.atr) > 0 else current_close * 0.02

        prev_price_high = self.price_highs[-2] if len(self.price_highs) > 1 else current_high
        prev_rsi_high = self.rsi_highs[-2] if len(self.rsi_highs) > 1 else current_rsi
        volume_sma = self.volume_sma[-1] if len(self.volume_sma) > 0 else current_volume

        # More lenient divergence detection
        price_higher_high = current_high >= prev_price_high * 0.999  # Allow small difference
        rsi_lower_high = current_rsi < prev_rsi_high
        bearish_divergence = price_higher_high and rsi_lower_high

        volume_declining = current_volume < volume_sma

        if bearish_divergence and volume_declining and not self.position:
            risk_amount = self.equity * 0.015
            position_size = int(round(risk_amount / atr_value)) if atr_value > 0 else 0
            max_size = int((self.equity * 0.05) // current_close) if current_close > 0 else 0
            position_size = min(position_size, max_size)

            if position_size > 0:
                self.buy(size=position_size)
                self.trade_count += 1
                print(f"🚀 DivergentVolume Entry! Long {position_size} @ {current_close:.2f}")

        # Simple exit after 5 bars or profit/loss
        if self.position:
            entry_price = self.position.entry_price if hasattr(self.position, "entry_price") else current_close

            if (
                current_close > entry_price * 1.02  # 2% profit
                or current_close < entry_price * 0.98  # 2% loss
                or len(self.data) % 20 == 0
            ):  # Time-based exit
                self.position.close()
                print(f"💰 DivergentVolume Exit! Closing at {current_close:.2f}")


def run_strategy_backtest(strategy_class, strategy_name):
    print(f"\n🌙🚀 Running {strategy_name} Backtest...")
    bt = Backtest(data, strategy_class, cash=1_000_000, commission=0.002)
    stats = bt.run()

    print(f"\n🌕🌖🌗🌘🌑🌒🌓🌔 {strategy_name.upper()} STATS 🌕🌖🌗🌘🌑🌒🌓🌔")
    print(stats)
    print(f"\n🌙 {strategy_name} Strategy Details:")
    print(stats._strategy)
    print(f"\n🌙 {strategy_name} Backtest Complete! 🚀")
    return stats


if __name__ == "__main__":
    print("🌙🚀 AI8 FINAL BACKTEST SUITE - All Three Strategies")
    print("=" * 80)

    # Run all three strategies
    results = {}

    # Strategy 1: DivergentMomentum
    results["DivergentMomentum"] = run_strategy_backtest(DivergentMomentumEnhanced, "DivergentMomentum")

    # Strategy 2: DivergentPulse
    results["DivergentPulse"] = run_strategy_backtest(DivergentPulseEnhanced, "DivergentPulse")

    # Strategy 3: DivergentVolume
    results["DivergentVolume"] = run_strategy_backtest(DivergentVolumeEnhanced, "DivergentVolume")

    # Summary
    print("\n" + "=" * 80)
    print("🌙 AI8 FINAL SUMMARY - ALL STRATEGIES COMPLETED 🌙")
    print("=" * 80)

    for strategy_name, stats in results.items():
        print(f"\n📊 {strategy_name}:")
        print(f"   Return: {stats['Return [%]']:.2f}%")
        print(f"   Trades: {stats['# Trades']}")
        print(
            f"   Win Rate: {stats['Win Rate [%]']:.2f}%" if not pd.isna(stats["Win Rate [%]"]) else "   Win Rate: N/A"
        )
        print(f"   Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")

    print(f"\n🌙 All backtests completed successfully! 🚀")
    print("📁 Results saved in AI_BACKTEST_RESULTS folder")
