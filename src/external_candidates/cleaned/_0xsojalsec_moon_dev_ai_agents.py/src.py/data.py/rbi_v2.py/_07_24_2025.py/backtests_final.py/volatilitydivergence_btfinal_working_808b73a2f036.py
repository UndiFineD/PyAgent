# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\VolatilityDivergence_BTFinal_WORKING.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolatilityDivergence(Strategy):
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)
        self.vix_sma = self.I(talib.SMA, self.data.VIX, timeperiod=5)
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

        self.rsi_prev_low = np.nan
        self.price_prev_low = np.nan
        self.entry_price = np.nan
        self.stop_loss = np.nan
        self.take_profit_1 = np.nan
        self.take_profit_2 = np.nan

    def next(self):
        if not self.position:
            if (
                self.data.Close[-1] < self.price_prev_low
                and self.rsi[-1] > self.rsi_prev_low
                and self.rsi[-1] > 30
                and self.data.VIX[-1] > self.vix_sma[-1]
                and self.data.Close[-1] > self.sma200[-1]
            ):
                self.entry_price = self.data.Open[0]
                self.stop_loss = self.entry_price - 1.5 * self.atr[-1]
                self.take_profit_1 = self.entry_price + 3 * self.atr[-1]
                self.take_profit_2 = self.entry_price + 1.5 * self.atr[-1]

                position_size = int(round(1000000 * 0.02 / (self.entry_price - self.stop_loss)))
                self.buy(size=position_size)
                print(f"🌙 Opened long position of {position_size} shares at ${self.entry_price:.2f}")
            else:
                self.rsi_prev_low = self.rsi[-1] if self.data.Close[-1] < self.price_prev_low else self.rsi_prev_low
                self.price_prev_low = min(self.data.Close[-1], self.price_prev_low)
        else:
            if self.data.Close[-1] <= self.stop_loss or self.data.VIX[-1] < self.vix_sma[-1]:
                self.position.close()
                print(f"🚨 Closed position at ${self.data.Close[-1]:.2f} due to stop loss or VIX crossover")
            elif self.data.Close[-1] >= self.take_profit_1:
                self.position.close_portion(0.5)
                self.take_profit_2 = self.data.Close[-1] - 2 * self.atr[-1]
                print(f"✨ Took 50% profit at ${self.data.Close[-1]:.2f}, trailing stop to ${self.take_profit_2:.2f}")
            elif self.data.Close[-2] < self.take_profit_2 and self.data.Close[-1] > self.take_profit_2:
                self.position.close()
                print(f"🎉 Closed remaining position at ${self.data.Close[-1]:.2f} with trailing take profit")


# Load data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Add VIX data (replace with actual VIX data)
data["VIX"] = np.random.normal(15, 5, len(data))

# Run backtest
bt = Backtest(data, VolatilityDivergence, cash=1000000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
