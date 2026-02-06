# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\BandedMACD_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class BandedMACD(Strategy):
    def init(self):
        # Calculate MACD
        self.macd, self.signal, _ = self.I(
            talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        # Calculate Bollinger Bands
        self.upperband, self.middleband, self.lowerband = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        # Calculate swing highs
        self.swing_highs = self.I(talib.MAX, self.data.High, timeperiod=20)

    def next(self):
        # Exit long position based on exit strategy
        if self.position.is_long:
            # Exit condition: MACD crossover & price exceeds upper band
            if (
                self.macd[-2] < self.signal[-2] and self.macd[-1] > self.signal[-1]
            ) and self.data.Close[-1] > self.upperband[-1]:
                # Look for significant pullback below recent swing high
                recent_swing_high = self.swing_highs[-1]
                if self.data.Close[-1] < recent_swing_high:
                    self.position.close()
                    print(
                        f"🌙 Exit signal triggered! Closing position at {self.data.Close[-1]} 🚀"
                    )

    def size(self, price, stop):
        # Calculate position size based on risk percentage and volatility
        risk_amount = 0.01 * self.equity
        volatility = self.upperband[-1] - self.lowerband[-1]
        risk = price - stop
        position_size = risk_amount / risk if risk != 0 else 0
        return int(round(position_size))


bt = Backtest(data, BandedMACD, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
