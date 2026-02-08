# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests\VolatilitySpikeReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean column names
data.columns = data.columns.str.strip().str.lower()

# Drop unnamed columns
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Rename and format columns
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Set datetime index
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class VolatilitySpikeReversal(Strategy):
    def init(self):
        # Calculate indicators using TA-Lib
        close = self.data.Close

        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        self.upper_band = self.I(lambda: upper, name="Upper Band")
        self.lower_band = self.I(lambda: lower, name="Lower Band")

        # ADX
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, close, timeperiod=14)

        # Volume SMA
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=30)

    def next(self):
        # Wait for sufficient data
        if len(self.data) < 30:
            return

        # Moon Dev Debug Prints 🌙
        print(f"\n🌙 Moon Dev Analysis - Bar {len(self.data)}:")
        print(f"   Current Close: {self.data.Close[-1]:.2f}")
        print(f"   Upper Band: {self.upper_band[-1]:.2f}")
        print(f"   Lower Band: {self.lower_band[-1]:.2f}")
        print(f"   ADX: {self.adx[-1]:.2f}")
        print(f"   Volume Ratio: {self.data.Volume[-1] / self.volume_sma[-1]:.2f}x")

        # Long entry conditions
        if (
            not self.position
            and self.data.Low[-1] <= self.lower_band[-1]
            and self.adx[-1] < 20
            and self.data.Volume[-1] > self.volume_sma[-1]
        ):
            # Risk management calculations
            risk_pct = 0.01  # 1% risk
            entry_price = self.data.Close[-1]
            stop_loss = self.lower_band[-1]
            risk_per_share = entry_price - stop_loss

            if risk_per_share > 0:
                position_size = (self.equity * risk_pct) / risk_per_share
                position_size = int(round(position_size))

                # Moon Dev Position Sizing ✨
                print(f"\n🚀 Moon Dev Trade Signal!")
                print(f"   Entry Price: {entry_price:.2f}")
                print(f"   Stop Loss: {stop_loss:.2f}")
                print(f"   Calculated Size: {position_size} units")

                self.buy(size=position_size)

        # Exit conditions
        if self.position.is_long:
            # Take profit at upper band
            if self.data.High[-1] >= self.upper_band[-1]:
                print(f"\n💰 Moon Dev Profit Capture!")
                print(f"   Upper Band Hit: {self.upper_band[-1]:.2f}")
                self.position.close()

            # Stop loss at lower band
            elif self.data.Close[-1] < self.lower_band[-1]:
                print(f"\n🌧️ Moon Dev Risk Protection!")
                print(f"   Lower Band Breach: {self.lower_band[-1]:.2f}")
                self.position.close()


# Execute backtest
bt = Backtest(data, VolatilitySpikeReversal, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
