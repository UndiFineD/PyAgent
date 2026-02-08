# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests\InverseMomentum_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
raw_data = pd.read_csv(data_path)

# Clean column names
raw_data.columns = raw_data.columns.str.strip().str.lower()

# Drop unnamed columns
raw_data = raw_data.drop(columns=[col for col in raw_data.columns if "unnamed" in col.lower()])

# Rename and capitalize columns to match requirements
raw_data = raw_data.rename(
    columns={
        "datetime": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Convert to datetime and set index
raw_data["Date"] = pd.to_datetime(raw_data["Date"])
raw_data = raw_data.set_index("Date")

# Resample to daily OHLCV
daily_data = (
    raw_data.resample("1D")
    .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
    .dropna()
)

# Ensure column cases are proper
daily_data.columns = ["Open", "High", "Low", "Close", "Volume"]


class InverseMomentum(Strategy):
    fast_period = 3
    slow_period = 5
    vol_period = 10
    trend_period = 20
    risk_pct = 0.02
    stop_pct = 0.05

    def init(self):
        close = self.data.Close
        volume = self.data.Volume

        self.fast_sma = self.I(talib.SMA, close, timeperiod=self.fast_period)
        self.slow_sma = self.I(talib.SMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast SMA {self.fast_sma[-1]:.2f}, Slow SMA {self.slow_sma[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f}, "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f} 🚀"
            )

        # Position sizing for risk management: fraction = risk_pct / stop_pct
        size = self.risk_pct / self.stop_pct

        if self.position:
            # Exit on bearish crossover
            if crossover(self.slow_sma, self.fast_sma):
                self.position.close()
                print(f"🌙 Moon Dev Exit: Bearish crossover detected! Closing position at {self.data.Close[-1]:.2f} ✨")
        else:
            # Entry conditions: bullish crossover + volume + trend filter
            if (
                crossover(self.fast_sma, self.slow_sma)
                and self.data.Volume[-1] > self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
            ):
                self.buy(size=size, sl=-self.stop_pct)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! Crossover confirmed with volume & trend. "
                    f"Entry: {self.data.Close[-1]:.2f}, Size: {size}, SL: {self.data.Close[-1] * (1 - self.stop_pct):.2f} 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
