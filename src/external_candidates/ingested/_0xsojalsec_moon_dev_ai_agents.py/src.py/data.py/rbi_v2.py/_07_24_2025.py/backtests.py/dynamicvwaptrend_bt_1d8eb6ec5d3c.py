# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests\DynamicVWAPTrend_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class DynamicVWAPTrend(Strategy):
    adx_period = 14
    risk_per_trade = 0.01
    size = 1000000

    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(
            columns=[col for col in self.data.df.columns if "unnamed" in col.lower()]
        )

        # Calculate indicators
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.vwap = self.I(
            talib.SMA,
            (self.data.Close * self.data.Volume).cumsum() / self.data.Volume.cumsum(),
        )

        # Track recent highs/lows for stop placement
        self.recent_high = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.recent_low = self.I(talib.MIN, self.data.Low, timeperiod=20)

    def next(self):
        if len(self.data.Close) < 20:  # Wait for enough data
            return

        current_price = self.data.Close[-1]
        vwap = self.vwap[-1]
        adx = self.adx[-1]

        # Moon Dev debug prints 🌙
        print(f"\n🌙 Moon Dev Debug 🌙")
        print(f"Price: {current_price:.2f} | VWAP: {vwap:.2f} | ADX: {adx:.2f}")

        # Check if we're in a position
        if self.position:
            if self.position.is_long:
                # Long exit conditions
                if current_price < vwap:
                    print("🚀 Closing LONG position (Price below VWAP)")
                    self.position.close()
            elif self.position.is_short:
                # Short exit conditions
                if current_price > vwap:
                    print("🚀 Closing SHORT position (Price above VWAP)")
                    self.position.close()
            return

        # Only trade when ADX shows strong trend
        if adx < 25:
            print("🌙 ADX too weak (<25), skipping trade")
            return

        # Calculate position size based on risk
        atr = talib.ATR(self.data.High, self.data.Low, self.data.Close, timeperiod=14)[
            -1
        ]
        risk_amount = self.equity * self.risk_per_trade
        position_size = int(round(risk_amount / atr))

        # Long entry logic
        if current_price > vwap and self.data.Close[-2] <= vwap:
            stop_loss = min(self.recent_low[-1], vwap)
            print(f"✨ LONG signal! Entering at {current_price:.2f}")
            print(f"🌙 Stop loss: {stop_loss:.2f} | Position size: {position_size}")
            self.buy(size=position_size, sl=stop_loss)

        # Short entry logic
        elif current_price < vwap and self.data.Close[-2] >= vwap:
            stop_loss = max(self.recent_high[-1], vwap)
            print(f"✨ SHORT signal! Entering at {current_price:.2f}")
            print(f"🌙 Stop loss: {stop_loss:.2f} | Position size: {position_size}")
            self.sell(size=position_size, sl=stop_loss)


# Load and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")
data.columns = ["Open", "High", "Low", "Close", "Volume"]

# Run backtest
bt = Backtest(data, DynamicVWAPTrend, commission=0.002, margin=1.0)
stats = bt.run()
print(stats)
print(stats._strategy)
