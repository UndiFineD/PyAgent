# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_17_2025\backtests_package\VolatilitySpread_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Rename columns to match backtesting requirements
column_mapping = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data.rename(columns=column_mapping, inplace=True)


class VolatilitySpread(Strategy):
    risk_pct = 0.02  # 2% risk per trade
    atr_period = 14
    sma_period = 20
    tp_multiplier = 2
    sl_multiplier = 1.5

    def init(self):
        # Calculate indicators using TA-Lib
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.sma = self.I(talib.SMA, self.data.Close, self.sma_period)
        self.upper_band = self.I(lambda sma, atr: sma + 0.8 * atr, self.sma, self.atr)
        self.lower_band = self.I(lambda sma, atr: sma - 0.2 * atr, self.sma, self.atr)
        self.prev_atr = None

    def next(self):
        price = self.data.Close[-1]
        atr = self.atr[-1]
        sma = self.sma[-1]
        upper = self.upper_band[-1]
        lower = self.lower_band[-1]

        # Calculate volatility direction
        atr_decreasing = self.prev_atr and atr < self.prev_atr
        atr_increasing = self.prev_atr and atr > self.prev_atr
        self.prev_atr = atr

        if not self.position:
            # Long entry logic
            if price > upper and atr_decreasing:
                sl = price - self.sl_multiplier * atr
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (price - sl)))
                if position_size > 0:
                    print(
                        f"🌙 MOON DEV LONG SIGNAL 🚀 | Price: {price:.2f} | Size: {position_size}"
                    )
                    self.buy(
                        size=position_size, sl=sl, tp=price + self.tp_multiplier * atr
                    )

            # Short entry logic
            elif price < lower and atr_increasing:
                sl = price + self.sl_multiplier * atr
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (sl - price)))
                if position_size > 0:
                    print(
                        f"🌙 MOON DEV SHORT SIGNAL 🌑 | Price: {price:.2f} | Size: {position_size}"
                    )
                    self.sell(
                        size=position_size, sl=sl, tp=price - self.tp_multiplier * atr
                    )
        else:
            # Exit conditions
            if self.position.is_long:
                if price < sma or atr_increasing:
                    print(f"🌙 MOON DEV CLOSE LONG ✨ | Price: {price:.2f}")
                    self.position.close()
            elif self.position.is_short:
                if price > sma or atr_decreasing:
                    print(f"🌙 MOON DEV CLOSE SHORT ✨ | Price: {price:.2f}")
                    self.position.close()


# Run backtest
bt = Backtest(data, VolatilitySpread, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
