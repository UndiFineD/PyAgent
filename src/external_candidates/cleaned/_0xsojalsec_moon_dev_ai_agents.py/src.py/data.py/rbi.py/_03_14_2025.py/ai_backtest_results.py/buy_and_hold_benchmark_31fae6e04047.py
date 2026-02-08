# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\buy_and_hold_benchmark.py
# 🌙 Buy and Hold Benchmark for BTC-USD 15m Data
import pandas as pd

# Load data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# Calculate buy and hold performance
initial_price = data["Close"].iloc[0]
final_price = data["Close"].iloc[-1]
buy_hold_return = (final_price - initial_price) / initial_price

print(f"🌙 BTC-USD 15m Buy and Hold Benchmark")
print(f"Initial Price: ${initial_price:.2f}")
print(f"Final Price: ${final_price:.2f}")
print(f"Buy and Hold Return: {buy_hold_return:.4f} ({buy_hold_return * 100:.2f}%)")
print(f"$1M Portfolio Final Value: ${1000000 * (1 + buy_hold_return):,.2f}")
