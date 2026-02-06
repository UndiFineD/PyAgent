# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\CrossVolatility_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class CrossVolatilityStrategy(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # Moon Dev Indicator Setup 🌙
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50, name="SMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200, name="EMA200")
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR14",
        )
        self.atr_avg = self.I(talib.SMA, self.atr, timeperiod=20, name="ATR_Avg")
        self.swing_high = self.I(
            talib.MAX, self.data.High, timeperiod=20, name="SwingHigh"
        )

        print(
            "🌙✨ Moon Dev Indicators Activated: SMA50, EMA200, ATR14, Swing Highs! �"
        )

    def next(self):
        price = self.data.Close[-1]

        # Moon Dev Trading Logic 🌙
        if not self.position:
            # Golden Cross Detection (replaced crossover)
            if self.sma50[-2] < self.ema200[-2] and self.sma50[-1] > self.ema200[-1]:
                if (
                    price > self.sma50[-1]
                    and price > self.ema200[-1]
                    and self.atr[-1] > self.atr_avg[-1]
                ):

                    # Moon Dev Risk Calculation 🌙
                    entry_price = price
                    atr_value = self.atr[-1]

                    # Dynamic Stop Loss Calculation
                    swing_high = self.swing_high[-2]  # Previous swing high
                    min_stop_distance = entry_price - 0.1 * atr_value
                    stop_loss = (
                        min(swing_high, min_stop_distance)
                        if swing_high < entry_price
                        else min_stop_distance
                    )

                    risk_distance = entry_price - stop_loss
                    position_size = int(
                        round((self.risk_per_trade * self.equity) / risk_distance)
                    )

                    if position_size > 0:
                        take_profit = entry_price + 0.2 * atr_value

                        # Moon Dev Entry Signal 🌙
                        self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                        print(
                            f"🚀🌙 MOON DEV LONG SIGNAL 🚀\n"
                            f"Entry: {entry_price:.2f} | "
                            f"Size: {position_size} | "
                            f"SL: {stop_loss:.2f} | "
                            f"TP: {take_profit:.2f} ✨"
                        )
        else:
            # Moon Dev Exit Checks 🌙
            if self.position.pl > 0:
                print(f"🌈 MOON DEV PROFIT TAKEN 🌈 +{self.position.pl:.2f}")
            elif self.position.pl < 0:
                print(f"🌑 MOON DEV STOP HIT 🌑 {self.position.pl:.2f}")


# Moon Dev Data Preparation 🌙
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and format data
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
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

print("🌙✨ MOON DEV BACKTEST INITIATED 🌙✨")
bt = Backtest(data, CrossVolatilityStrategy, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST RESULTS 🚀🌙")
print(stats)
print(stats._strategy)
