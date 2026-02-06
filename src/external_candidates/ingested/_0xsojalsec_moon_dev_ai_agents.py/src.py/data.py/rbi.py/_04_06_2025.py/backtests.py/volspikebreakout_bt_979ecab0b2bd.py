# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_06_2025\backtests\VolSpikeBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean column names and drop unnamed columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Rename columns to match backtesting.py requirements
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Convert datetime and set as index
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")


class VolSpikeBreakout(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    bb_period = 20
    bb_dev = 2
    volume_multiplier = 2
    atr_period = 14

    def init(self):
        # Define helper functions for BBANDS components
        def get_upper_band(close):
            upper, _, _ = talib.BBANDS(
                close,
                timeperiod=self.bb_period,
                nbdevup=self.bb_dev,
                nbdevdn=self.bb_dev,
            )
            return upper

        def get_middle_band(close):
            _, middle, _ = talib.BBANDS(
                close,
                timeperiod=self.bb_period,
                nbdevup=self.bb_dev,
                nbdevdn=self.bb_dev,
            )
            return middle

        # Initialize indicators with self.I()
        self.upper_band = self.I(get_upper_band, self.data.Close)
        self.sma_20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )

    def next(self):
        # Wait until we have enough data
        if len(self.data) < max(self.bb_period, 20, self.atr_period) + 1:
            return

        # Moon Dev debug check 🌙
        current_close = self.data.Close[-1]
        current_upper = self.upper_band[-1]
        print(
            f"🌙 Moon Scan: Close {current_close:.2f} vs Upper BB {current_upper:.2f}"
        )

        # Exit if price touches SMA20
        if self.position and self.data.Low[-1] <= self.sma_20[-1]:
            self.position.close()
            print(f"✨ Cosmic Exit! Price {current_close:.2f} reached SMA20 ✨")

        # Entry conditions
        if not self.position:
            # Check previous candle conditions
            prev_close = self.data.Close[-2]
            prev_upper = self.upper_band[-2]
            prev_volume = self.data.Volume[-2]
            prev_volume_sma = self.volume_sma[-2]

            if (
                prev_close > prev_upper
                and prev_volume > self.volume_multiplier * prev_volume_sma
            ):
                # Calculate position size with stellar precision 🌠
                entry_price = self.data.Open[-1]
                atr_value = self.atr[-1]
                stop_loss = entry_price - 2 * atr_value
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (entry_price - stop_loss)))

                if position_size > 0:
                    self.buy(size=position_size)
                    print(f"🚀 LIFTOFF! Long {position_size} @ {entry_price:.2f}")
                    print(f"   Starlink SL: {stop_loss:.2f} | ATR: {atr_value:.2f} 🌌")


# Launch backtest with 1M lunar credits 🌕
bt = Backtest(data, VolSpikeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full mission report 📊
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("Moon Dev Strategy Final Report:")
print(stats)
print(stats._strategy)
