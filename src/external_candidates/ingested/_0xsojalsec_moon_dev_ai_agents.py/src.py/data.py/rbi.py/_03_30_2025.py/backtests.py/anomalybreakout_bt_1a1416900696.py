# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_30_2025\backtests\AnomalyBreakout_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class AnomalyBreakout(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    funding_threshold = -0.001  # -0.1%
    exit_funding_threshold = -0.0005  # -0.05%
    atr_multiplier = 2
    max_atr_multiplier = 3

    def init(self):
        self.sma50 = self.I(talib.SMA, self.data.Close, 50, name="SMA 50")
        self.atr14 = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 14, name="ATR 14"
        )
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20, name="Volume SMA 20")

        print("🌙 Moon Dev Indicators Activated: SMA50 | ATR14 | Volume SMA20 ✨")

    def next(self):
        if not self.position:
            if (
                self.data.Close[-1] < self.sma50[-1]
                and self.data.fundingrate[-1] < self.funding_threshold
                and self.data.Volume[-1] > self.volume_sma[-1]
            ):

                atr_value = self.atr14[-1]
                if atr_value == 0:
                    return

                stop_distance = min(
                    self.atr_multiplier * atr_value, self.max_atr_multiplier * atr_value
                )
                risk_amount = self.equity * self.risk_percent
                position_size = int(round(risk_amount / stop_distance))

                if position_size > 0:
                    entry_price = self.data.Open[-1]
                    print(
                        f"🚀 MOON DEV SHORT SIGNAL 🚀"
                        f"\nEntry Price: {entry_price:.2f}"
                        f"\nSMA50: {self.sma50[-1]:.2f}"
                        f"\nFunding Rate: {self.data.fundingrate[-1]:.4%}"
                        f"\nPosition Size: {position_size} units 🌙"
                    )

                    self.sell(
                        size=position_size,
                        sl=entry_price + stop_distance,
                        trailing_stop=stop_distance,
                    )
        else:
            if self.data.fundingrate[-1] >= self.exit_funding_threshold:
                print(
                    f"✨ FUNDING RATE NORMALIZATION EXIT ✨"
                    f"\nCurrent Rate: {self.data.fundingrate[-1]:.4%}"
                    f"\nPosition Closed at: {self.data.Open[-1]:.2f} 🌙"
                )
                self.position.close()


# Data preprocessing
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and prepare data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
    errors="ignore",
)

print(
    "🌙 DATA PREPARED WITH MOON DEV PROTOCOLS 🌙"
    f"\nColumns: {data.columns.tolist()}"
    f"\nFirst 3 rows:\n{data.iloc[:3]}"
)

# Execute backtest
bt = Backtest(data, AnomalyBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST COMPLETE")
print("FULL STRATEGY STATS:")
print(stats)
print("\nSTRATEGY DETAILS:")
print(stats._strategy)
