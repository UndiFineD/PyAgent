# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\AI_OPTIMIZED_STRATEGIES\test_all_strategies.py
# 🌙 Moon Dev's AI-Optimized Strategies Test Suite 🌙
# Comprehensive testing of all three optimized strategies

import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import pandas_ta as ta
from backtesting import Backtest, Strategy

warnings.filterwarnings("ignore")

# 🌙 Data Loading Function
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


def load_btc_data(file_path):
    """Load and prepare BTC data with adaptive header detection"""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df = df.drop(
            columns=[col for col in df.columns if "unnamed" in col.lower()],
            errors="ignore",
        )

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

        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")

        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Required column {col} not found")

        df = df[required_cols].dropna()
        df = df[df > 0]
        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        raise


# Load the data once
print("🌙 Loading BTC-USD 15m data for all strategies...")
data = load_btc_data(data_path)
print(f"📊 Data loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]}")


# Import strategy classes (simplified versions for testing)
class HybridMomentumMeanReversion(Strategy):
    """Hybrid Momentum Mean Reversion Strategy"""

    risk_per_trade = 0.01
    ema_fast = 9
    ema_slow = 21
    rsi_period = 9
    bb_period = 15
    atr_period = 12
    rsi_oversold = 35
    rsi_overbought = 65
    atr_multiplier = 1.5

    def init(self):
        self.ema_fast_line = self.I(ta.ema, self.data.Close, self.ema_fast)
        self.ema_slow_line = self.I(ta.ema, self.data.Close, self.ema_slow)
        self.rsi = self.I(ta.rsi, self.data.Close, self.rsi_period)
        bb_data = ta.bbands(self.data.Close, length=self.bb_period, std=1.8)
        self.bb_upper = self.I(lambda: bb_data[f"BBU_{self.bb_period}_1.8"].values)
        self.bb_lower = self.I(lambda: bb_data[f"BBL_{self.bb_period}_1.8"].values)
        self.atr = self.I(
            ta.atr, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.volume_sma = self.I(ta.sma, self.data.Volume, 10)
        self.entry_time = None

    def next(self):
        if len(self.data) < max(self.ema_slow, self.bb_period) + 1:
            return
        if self.position:
            if len(self.data) - self.entry_time > 25:  # Time exit
                self.position.close()
                self.entry_time = None
            return

        current_close = self.data.Close[-1]
        ema_bullish = self.ema_fast_line[-1] > self.ema_slow_line[-1]
        rsi_oversold = self.rsi[-1] < self.rsi_oversold
        rsi_overbought = self.rsi[-1] > self.rsi_overbought
        bb_oversold = current_close < self.bb_lower[-1]
        bb_overbought = current_close > self.bb_upper[-1]
        volume_ok = self.data.Volume[-1] > self.volume_sma[-1] * 0.8

        if ema_bullish and (rsi_oversold or bb_oversold) and volume_ok:
            stop_loss = current_close - (self.atr[-1] * self.atr_multiplier)
            risk_per_share = current_close - stop_loss
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_time = len(self.data)
        elif not ema_bullish and (rsi_overbought or bb_overbought) and volume_ok:
            stop_loss = current_close + (self.atr[-1] * self.atr_multiplier)
            risk_per_share = stop_loss - current_close
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_time = len(self.data)


class VolatilityBreakoutScalper(Strategy):
    """Volatility Breakout Scalper Strategy"""

    risk_per_trade = 0.01
    bb_period = 12
    atr_period = 8
    max_hold_bars = 15

    def init(self):
        bb_data = ta.bbands(self.data.Close, length=self.bb_period, std=1.6)
        self.bb_upper = self.I(lambda: bb_data[f"BBU_{self.bb_period}_1.6"].values)
        self.bb_lower = self.I(lambda: bb_data[f"BBL_{self.bb_period}_1.6"].values)
        self.bb_middle = self.I(lambda: bb_data[f"BBM_{self.bb_period}_1.6"].values)
        self.atr = self.I(
            ta.atr, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.volume_sma = self.I(ta.sma, self.data.Volume, 10)
        self.rsi = self.I(ta.rsi, self.data.Close, 7)
        self.entry_time = None

    def next(self):
        if len(self.data) < max(self.bb_period, self.atr_period) + 1:
            return
        if self.position:
            if len(self.data) - self.entry_time >= self.max_hold_bars:
                self.position.close()
                self.entry_time = None
            return

        current_close = self.data.Close[-1]
        volume_surge = self.data.Volume[-1] > self.volume_sma[-1] * 1.2
        rsi_not_extreme = 25 < self.rsi[-1] < 75

        if current_close > self.bb_upper[-1] and volume_surge and rsi_not_extreme:
            stop_loss = current_close - (self.atr[-1] * 1.0)
            risk_per_share = current_close - stop_loss
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_time = len(self.data)
        elif current_close < self.bb_lower[-1] and volume_surge and rsi_not_extreme:
            stop_loss = current_close + (self.atr[-1] * 1.0)
            risk_per_share = stop_loss - current_close
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_time = len(self.data)


class AdaptiveTrendFollower(Strategy):
    """Adaptive Trend Follower Strategy"""

    risk_per_trade = 0.01
    ema_fast = 9
    ema_slow = 21
    ema_trend = 50
    atr_period = 14

    def init(self):
        self.ema_fast_line = self.I(ta.ema, self.data.Close, self.ema_fast)
        self.ema_slow_line = self.I(ta.ema, self.data.Close, self.ema_slow)
        self.ema_trend_line = self.I(ta.ema, self.data.Close, self.ema_trend)
        macd_data = ta.macd(self.data.Close, fast=8, slow=21, signal=6)
        self.macd_hist = self.I(lambda: macd_data.iloc[:, 2].values)
        self.atr = self.I(
            ta.atr, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.volume_sma = self.I(ta.sma, self.data.Volume, 20)
        self.rsi = self.I(ta.rsi, self.data.Close, 14)
        self.entry_time = None

    def next(self):
        if len(self.data) < max(self.ema_trend, self.atr_period) + 1:
            return
        if self.position:
            if len(self.data) - self.entry_time > 50:  # Time exit
                self.position.close()
                self.entry_time = None
            return

        current_close = self.data.Close[-1]
        trend_bullish = (
            self.ema_fast_line[-1] > self.ema_slow_line[-1]
            and current_close > self.ema_trend_line[-1]
        )
        trend_bearish = (
            self.ema_fast_line[-1] < self.ema_slow_line[-1]
            and current_close < self.ema_trend_line[-1]
        )
        macd_positive = self.macd_hist[-1] > 0
        volume_ok = self.data.Volume[-1] > self.volume_sma[-1] * 1.1
        rsi_ok = 25 < self.rsi[-1] < 75

        if trend_bullish and macd_positive and volume_ok and rsi_ok:
            stop_loss = current_close - (self.atr[-1] * 2.0)
            risk_per_share = current_close - stop_loss
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_time = len(self.data)
        elif trend_bearish and not macd_positive and volume_ok and rsi_ok:
            stop_loss = current_close + (self.atr[-1] * 2.0)
            risk_per_share = stop_loss - current_close
            if risk_per_share > 0:
                risk_amount = self.equity * self.risk_per_trade
                position_size = int(risk_amount / risk_per_share)
                if position_size > 0:
                    self.sell(size=position_size)
                    self.entry_time = len(self.data)


def test_strategy(strategy_class, strategy_name):
    """Test a single strategy and return results"""
    print(f"\n🌙 Testing {strategy_name}...")
    print("=" * 60)

    try:
        # Run default backtest
        bt = Backtest(data, strategy_class, cash=1000000, commission=0.002)
        stats = bt.run()

        # Extract key metrics
        metrics = {
            "Strategy": strategy_name,
            "Total Trades": stats["# Trades"],
            "Total Return (%)": stats["Return [%]"],
            "Sharpe Ratio": stats["Sharpe Ratio"],
            "Max Drawdown (%)": stats["Max. Drawdown [%]"],
            "Win Rate (%)": stats["Win Rate [%]"],
            "Trade Requirement (>100)": stats["# Trades"] > 100,
            "Sharpe Requirement (>2.0)": stats["Sharpe Ratio"] > 2.0,
            "Overall Success": stats["# Trades"] > 100 and stats["Sharpe Ratio"] > 2.0,
        }

        # Print results
        print(f"📊 Total Trades: {metrics['Total Trades']}")
        print(f"💰 Total Return: {metrics['Total Return (%)']:.2f}%")
        print(f"📈 Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
        print(f"📉 Max Drawdown: {metrics['Max Drawdown (%)']:.2f}%")
        print(f"🎯 Win Rate: {metrics['Win Rate (%)']:.2f}%")

        # Validation
        print(f"\n✅ VALIDATION:")
        print(
            f"📊 Trade Count (>100): {'✅ PASS' if metrics['Trade Requirement (>100)'] else '❌ FAIL'}"
        )
        print(
            f"📈 Sharpe Ratio (>2.0): {'✅ PASS' if metrics['Sharpe Requirement (>2.0)'] else '❌ FAIL'}"
        )
        print(
            f"🏆 Overall: {'✅ SUCCESS' if metrics['Overall Success'] else '❌ NEEDS WORK'}"
        )

        return metrics

    except Exception as e:
        print(f"❌ Error testing {strategy_name}: {e}")
        return {"Strategy": strategy_name, "Error": str(e), "Overall Success": False}


def run_all_tests():
    """Run all strategy tests and generate summary report"""
    print("🌙" + "=" * 78 + "🌙")
    print("                    MOON DEV'S AI-OPTIMIZED STRATEGIES")
    print("                        COMPREHENSIVE TEST SUITE")
    print("🌙" + "=" * 78 + "🌙")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Data Period: {data.index[0]} to {data.index[-1]} ({len(data)} bars)")

    # Test all strategies
    strategies = [
        (HybridMomentumMeanReversion, "Hybrid Momentum Mean Reversion"),
        (VolatilityBreakoutScalper, "Volatility Breakout Scalper"),
        (AdaptiveTrendFollower, "Adaptive Trend Follower"),
    ]

    results = []
    for strategy_class, strategy_name in strategies:
        result = test_strategy(strategy_class, strategy_name)
        results.append(result)

    # Generate summary report
    print(f"\n🌙 COMPREHENSIVE SUMMARY REPORT")
    print("=" * 80)

    successful_strategies = [r for r in results if r.get("Overall Success", False)]
    failed_strategies = [r for r in results if not r.get("Overall Success", False)]

    print(f"\n📊 OVERALL RESULTS:")
    print(f"✅ Successful Strategies: {len(successful_strategies)}/3")
    print(f"❌ Failed Strategies: {len(failed_strategies)}/3")

    if successful_strategies:
        print(f"\n🏆 SUCCESSFUL STRATEGIES:")
        for result in successful_strategies:
            if "Error" not in result:
                print(
                    f"   ✅ {result['Strategy']}: {result['Total Trades']} trades, "
                    f"{result['Sharpe Ratio']:.2f} Sharpe, {result['Total Return (%)']:.2f}% return"
                )

    if failed_strategies:
        print(f"\n⚠️ STRATEGIES NEEDING OPTIMIZATION:")
        for result in failed_strategies:
            if "Error" in result:
                print(f"   ❌ {result['Strategy']}: ERROR - {result['Error']}")
            else:
                issues = []
                if not result.get("Trade Requirement (>100)", False):
                    issues.append(f"Low trades ({result.get('Total Trades', 0)})")
                if not result.get("Sharpe Requirement (>2.0)", False):
                    issues.append(f"Low Sharpe ({result.get('Sharpe Ratio', 0):.2f})")
                print(f"   ❌ {result['Strategy']}: {', '.join(issues)}")

    # Detailed comparison table
    print(f"\n📊 DETAILED COMPARISON:")
    print("-" * 80)
    print(
        f"{'Strategy':<25} {'Trades':<8} {'Return%':<9} {'Sharpe':<8} {'Drawdown%':<11} {'Success':<8}"
    )
    print("-" * 80)

    for result in results:
        if "Error" not in result:
            print(
                f"{result['Strategy']:<25} "
                f"{result['Total Trades']:<8} "
                f"{result['Total Return (%)']:<9.2f} "
                f"{result['Sharpe Ratio']:<8.2f} "
                f"{result['Max Drawdown (%)']:<11.2f} "
                f"{'✅' if result['Overall Success'] else '❌':<8}"
            )
        else:
            print(
                f"{result['Strategy']:<25} {'ERROR':<8} {'N/A':<9} {'N/A':<8} {'N/A':<11} {'❌':<8}"
            )

    print("-" * 80)

    # Final assessment
    print(f"\n🎯 FINAL ASSESSMENT:")
    if len(successful_strategies) == 3:
        print("🏆 MISSION ACCOMPLISHED! All 3 strategies meet requirements!")
        print("   ✅ >100 trades per strategy")
        print("   ✅ >2.0 Sharpe ratio per strategy")
        print("   ✅ Ready for production deployment")
    elif len(successful_strategies) >= 2:
        print("🌟 PARTIAL SUCCESS! Most strategies meet requirements.")
        print("   ✅ Multiple strategies performing well")
        print("   ⚠️ Some strategies may need fine-tuning")
    elif len(successful_strategies) >= 1:
        print("⚠️ LIMITED SUCCESS! Some strategies show promise.")
        print("   ✅ At least one strategy meets requirements")
        print("   ❌ Additional optimization needed for others")
    else:
        print("❌ OPTIMIZATION NEEDED! No strategies currently meet requirements.")
        print("   ❌ All strategies need parameter adjustment")
        print("   🔄 Consider running individual optimizations")

    print(f"\n🌙 Test Suite completed successfully! ✨")
    return results


if __name__ == "__main__":
    # Run the comprehensive test suite
    results = run_all_tests()
