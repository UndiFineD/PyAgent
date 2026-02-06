# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\FINAL_WINNING_STRATEGIES\test_all_10_strategies.py
#!/usr/bin/env python3
# 🌙 Moon Dev's 10 Strategy Test Runner 🌙
# Tests all 10 working strategies and compiles comprehensive results

import importlib.util
import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# Strategy files to test
strategies = [
    "SimpleMomentumCross_BT.py",
    "RSIMeanReversion_BT.py",
    "VolatilityBreakout_BT.py",
    "BollingerReversion_BT.py",
    "MACDDivergence_BT.py",
    "StochasticMomentum_BT.py",
    "TrendFollowingMA_BT.py",
    "VolumeWeightedBreakout_BT.py",
    "ATRChannelSystem_BT.py",
    "HybridMomentumReversion_BT.py",
]


def load_and_run_strategy(strategy_file):
    """Load and run a strategy file, capturing its results"""
    try:
        print(f"\n{'='*80}")
        print(f"🌙 TESTING: {strategy_file}")
        print(f"{'='*80}")

        # Import the strategy module
        spec = importlib.util.spec_from_file_location("strategy", strategy_file)
        strategy_module = importlib.util.module_from_spec(spec)

        # Capture stdout to get the results
        import contextlib
        from io import StringIO

        captured_output = StringIO()

        # Execute the strategy with captured output
        with contextlib.redirect_stdout(captured_output):
            spec.loader.exec_module(strategy_module)

        output = captured_output.getvalue()
        print(output)  # Also print to console

        # Extract key metrics from output
        lines = output.split("\n")
        default_trades = None
        default_return = None
        default_sharpe = None
        default_drawdown = None
        default_winrate = None

        optimized_trades = None
        optimized_return = None
        optimized_sharpe = None
        optimized_drawdown = None
        optimized_winrate = None

        success = False

        # Parse default results
        for i, line in enumerate(lines):
            if "DEFAULT RESULTS" in line:
                # Look for metrics in following lines
                for j in range(i, min(i + 50, len(lines))):
                    if "📊 Total Trades:" in lines[j]:
                        default_trades = int(lines[j].split(":")[1].strip())
                    elif "💰 Total Return:" in lines[j]:
                        default_return = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )
                    elif "📈 Sharpe Ratio:" in lines[j]:
                        default_sharpe = float(lines[j].split(":")[1].strip())
                    elif "📉 Max Drawdown:" in lines[j]:
                        default_drawdown = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )
                    elif "🎯 Win Rate:" in lines[j]:
                        default_winrate = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )

            # Parse optimized results
            elif "OPTIMIZED RESULTS" in line:
                # Look for metrics in following lines
                for j in range(i, min(i + 50, len(lines))):
                    if "📊 Total Trades:" in lines[j]:
                        optimized_trades = int(lines[j].split(":")[1].strip())
                    elif "💰 Total Return:" in lines[j]:
                        optimized_return = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )
                    elif "📈 Sharpe Ratio:" in lines[j]:
                        optimized_sharpe = float(lines[j].split(":")[1].strip())
                    elif "📉 Max Drawdown:" in lines[j]:
                        optimized_drawdown = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )
                    elif "🎯 Win Rate:" in lines[j]:
                        optimized_winrate = float(
                            lines[j].split(":")[1].strip().replace("%", "")
                        )

            # Check for success
            elif "SUCCESS!" in line:
                success = True

        return {
            "strategy": strategy_file.replace("_BT.py", ""),
            "default": {
                "trades": default_trades,
                "return": default_return,
                "sharpe": default_sharpe,
                "drawdown": default_drawdown,
                "winrate": default_winrate,
            },
            "optimized": {
                "trades": optimized_trades,
                "return": optimized_return,
                "sharpe": optimized_sharpe,
                "drawdown": optimized_drawdown,
                "winrate": optimized_winrate,
            },
            "success": success,
            "full_output": output,
        }

    except Exception as e:
        print(f"❌ ERROR testing {strategy_file}: {str(e)}")
        return {
            "strategy": strategy_file.replace("_BT.py", ""),
            "error": str(e),
            "success": False,
        }


def main():
    """Run all strategies and compile results"""
    print("🌙 MOON DEV'S 10 STRATEGY COMPREHENSIVE TEST 🌙")
    print("=" * 80)
    print(f"Starting test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    all_results = []
    successful_strategies = 0

    # Test each strategy
    for strategy_file in strategies:
        strategy_path = os.path.join(current_dir, strategy_file)

        if os.path.exists(strategy_path):
            result = load_and_run_strategy(strategy_path)
            all_results.append(result)

            if result.get("success", False):
                successful_strategies += 1
        else:
            print(f"❌ Strategy file not found: {strategy_file}")

    # Compile summary results
    print("\n" + "=" * 100)
    print("🌙 COMPREHENSIVE RESULTS SUMMARY 🌙")
    print("=" * 100)

    # Create results table
    print(
        f"{'Strategy':<25} {'Success':<8} {'Def Trades':<10} {'Def Sharpe':<11} {'Opt Trades':<10} {'Opt Sharpe':<11} {'Opt Return':<11}"
    )
    print("-" * 100)

    best_sharpe = 0
    best_strategy = None
    total_strategies = len([r for r in all_results if "error" not in r])

    for result in all_results:
        if "error" in result:
            print(
                f"{result['strategy']:<25} {'❌ ERROR':<8} {'N/A':<10} {'N/A':<11} {'N/A':<10} {'N/A':<11} {'N/A':<11}"
            )
            continue

        strategy_name = result["strategy"]
        success_icon = "✅ PASS" if result["success"] else "❌ FAIL"

        def_trades = result["default"]["trades"] or 0
        def_sharpe = result["default"]["sharpe"] or 0
        opt_trades = result["optimized"]["trades"] or 0
        opt_sharpe = result["optimized"]["sharpe"] or 0
        opt_return = result["optimized"]["return"] or 0

        print(
            f"{strategy_name:<25} {success_icon:<8} {def_trades:<10} {def_sharpe:<11.2f} {opt_trades:<10} {opt_sharpe:<11.2f} {opt_return:<11.1f}%"
        )

        # Track best performing strategy
        if opt_sharpe > best_sharpe:
            best_sharpe = opt_sharpe
            best_strategy = result

    print("-" * 100)
    print(f"✅ SUCCESSFUL STRATEGIES: {successful_strategies}/{total_strategies}")
    print(f"📈 SUCCESS RATE: {(successful_strategies/total_strategies)*100:.1f}%")

    if best_strategy:
        print(f"\n🏆 BEST PERFORMING STRATEGY: {best_strategy['strategy']}")
        print(f"   📊 Trades: {best_strategy['optimized']['trades']}")
        print(f"   📈 Sharpe Ratio: {best_strategy['optimized']['sharpe']:.2f}")
        print(f"   💰 Return: {best_strategy['optimized']['return']:.1f}%")
        print(f"   📉 Max Drawdown: {best_strategy['optimized']['drawdown']:.1f}%")
        print(f"   🎯 Win Rate: {best_strategy['optimized']['winrate']:.1f}%")

    # Statistics summary
    successful_results = [r for r in all_results if r.get("success", False)]
    if successful_results:
        opt_sharpes = [
            r["optimized"]["sharpe"]
            for r in successful_results
            if r["optimized"]["sharpe"]
        ]
        opt_returns = [
            r["optimized"]["return"]
            for r in successful_results
            if r["optimized"]["return"]
        ]
        opt_trades = [
            r["optimized"]["trades"]
            for r in successful_results
            if r["optimized"]["trades"]
        ]

        if opt_sharpes and opt_returns and opt_trades:
            print(f"\n📊 SUCCESSFUL STRATEGIES STATISTICS:")
            print(f"   Average Sharpe Ratio: {np.mean(opt_sharpes):.2f}")
            print(f"   Median Sharpe Ratio: {np.median(opt_sharpes):.2f}")
            print(f"   Average Return: {np.mean(opt_returns):.1f}%")
            print(f"   Average Trades: {int(np.mean(opt_trades))}")
            print(f"   Total Trades (All Strategies): {sum(opt_trades)}")

    # Save detailed results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_10_strategies_{timestamp}.txt"

    with open(results_file, "w") as f:
        f.write("🌙 MOON DEV'S 10 STRATEGY TEST RESULTS 🌙\n")
        f.write("=" * 80 + "\n")
        f.write(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(
            f"Successful strategies: {successful_strategies}/{total_strategies}\n\n"
        )

        for result in all_results:
            f.write(f"\n{'='*80}\n")
            f.write(f"STRATEGY: {result['strategy']}\n")
            f.write(f"{'='*80}\n")

            if "error" in result:
                f.write(f"ERROR: {result['error']}\n")
            else:
                if result.get("full_output"):
                    f.write(result["full_output"])
                else:
                    f.write("No output captured\n")

    print(f"\n💾 Detailed results saved to: {results_file}")
    print(f"\n🌙 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
