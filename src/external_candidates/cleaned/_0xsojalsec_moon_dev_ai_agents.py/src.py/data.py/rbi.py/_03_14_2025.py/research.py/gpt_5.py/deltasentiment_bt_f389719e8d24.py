# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\research\GPT-5\DeltaSentiment_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG


class DeltaSentiment(Strategy):
    def init(self):
        # Clean up column names and remove any unnamed columns
        self.data.df.columns = [col.strip().lower() for col in self.data.df.columns]
        self.data.df = self.data.df.loc[:, ~self.data.df.columns.str.contains("unnamed")]

        # Define the 20-day Delta-Neutral VIX Futures Spread as a proxy for institutional sentiment
        self.vix_spread = self.I(talib.SMA, self.data.Close, timeperiod=20)

        # Define liquidity as volume (Note: Bid-ask spreads and order book depth not available in this dataset)
        self.high_liquidity = self.I(talib.SMA, self.data.Volume, timeperiod=20)

    def next(self):
        liquidity_threshold = self.high_liquidity[-1]  # Placeholder for high liquidity contracts
        sentiment = self.vix_spread[-1] - self.vix_spread[-2]

        if self.data.Volume[-1] > liquidity_threshold:
            if sentiment < 0:  # Narrowing spread, bullish sentiment
                if not self.position.is_long:
                    print(
                        f"🌙 Moon Dev Alert: Entering Long Position 🚀 | Volume: {self.data.Volume[-1]:,.0f} | Sentiment: Bullish"
                    )
                    position_size = int(round(1000000 / self.data.Close[-1]))
                    self.buy(size=position_size)

            elif sentiment > 0:  # Widening spread, bearish sentiment
                if not self.position.is_short:
                    print(
                        f"🌙 Moon Dev Alert: Entering Short Position 🚀 | Volume: {self.data.Volume[-1]:,.0f} | Sentiment: Bearish"
                    )
                    position_size = int(round(1000000 / self.data.Close[-1]))
                    self.sell(size=position_size)

        # Exit Logic
        if self.position.is_long and sentiment > 0:
            print(f"🌙 Moon Dev Alert: Exiting Long Position 🚀 | Sentiment Shifted to Bearish")
            self.position.close()

        if self.position.is_short and sentiment < 0:
            print(f"🌙 Moon Dev Alert: Exiting Short Position 🚀 | Sentiment Shifted to Bullish")
            self.position.close()


# Load and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=True,
    index_col="datetime",
)
data.columns = ["Open", "High", "Low", "Close", "Volume"]

# Run backtest
bt = Backtest(data, DeltaSentiment, cash=1000000, commission=0.002)
stats = bt.run()
print(f"🌙 Moon Dev Backtest Complete ✨\n{stats}")
