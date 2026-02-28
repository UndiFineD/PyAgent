# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\BandSyncMomentum_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=True,
    index_col="datetime",
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.columns = ["Open", "High", "Low", "Close", "Volume"]


class BandSyncMomentum(Strategy):
    def init(self):
        # Calculate Bollinger Bands
        self.upper_band, self.middle_band, self.lower_band = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        print(f"🌙 Bollinger Bands initialized 🚀")

    def next(self):
        price = self.data.Close[-1]
        lower_band = self.lower_band[-1]
        middle_band = self.middle_band[-1]
        upper_band = self.upper_band[-1]

        # Long Entry Condition
        if price <= lower_band and middle_band > self.middle_band[-2]:
            print(f"✨ Price touched lower band with upward momentum at {price} 🌙")
            sl = lower_band * 0.99
            position_size = int(round(1000000 / price))
            self.buy(size=position_size, sl=sl)
            print(f"🚀 Long Entry: Buy at {price}, SL at {sl}, Size: {position_size}")

        # Short Entry Condition
        elif price >= upper_band and middle_band < self.middle_band[-2]:
            print(
                f"✨ Price broke above upper band with downward momentum at {price} 🌙"
            )
            sl = upper_band * 1.01
            position_size = int(round(1000000 / price))
            self.sell(size=position_size, sl=sl)
            print(f"🚀 Short Entry: Sell at {price}, SL at {sl}, Size: {position_size}")

        # Long Exit Condition
        if self.position.is_long and (
            price >= upper_band or middle_band <= self.middle_band[-2]
        ):
            print(f"🌙 Long Exit: Sell at {price} 🚀")
            self.position.close()

        # Short Exit Condition
        if self.position.is_short and (
            price <= lower_band or middle_band >= self.middle_band[-2]
        ):
            print(f"🌙 Short Exit: Buy to cover at {price} 🚀")
            self.position.close()


# Run backtest
bt = Backtest(data, BandSyncMomentum, cash=1000000, commission=0.002)
stats = bt.run()
print(stats)
