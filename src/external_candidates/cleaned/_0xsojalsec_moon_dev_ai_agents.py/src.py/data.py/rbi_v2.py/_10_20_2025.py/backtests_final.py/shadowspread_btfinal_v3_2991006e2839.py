# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\10_20_2025\backtests_final\ShadowSpread_BTFinal_v3.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Ensure proper column mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Set datetime as index
data = data.set_index(pd.to_datetime(data["datetime"]))

# Drop any NaN rows
data = data.dropna()


class ShadowSpread(Strategy):
    # Parameters
    vol_threshold = 0.25  # 25% of average volume
    rsi_period = 14
    rsi_overbought = 70
    bb_period = 20
    bb_std = 2
    ema_short = 5
    risk_usd = 1000000  # Fixed USD size
    sl_pct = 0.02  # 2% stop loss above entry
    tp_pct = 0.05  # 5% take profit below entry
    max_bars_hold = 28  # Approx 7 hours (28 * 15min), time-based exit

    def init(self):
        # Indicators using self.I and talib
        self.vol_avg = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        upper, middle, lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_std,
            nbdevdn=self.bb_std,
            matype=0,
        )
        self.bb_upper = upper
        self.ema5 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_short)

        # Track entry price and bars held
        self.entry_price = None
        self.entry_bar = None

    def next(self):
        # Debug print with Moon Dev theme
        if self._i % 100 == 0:
            print(
                f"🌙 Moon Dev Backtest Update: Bar {self._i}, Close: {self.data.Close[-1]:.2f}, Volume: {self.data.Volume[-1]:.2f}, RSI: {self.rsi[-1]:.2f} ✨"
            )

        # Entry logic: Low volume, overbought RSI, near BB upper, bearish bias (Close < EMA5 for initial weakness)
        low_vol = self.data.Volume[-1] < self.vol_threshold * self.vol_avg[-1]
        overbought = self.rsi[-1] > self.rsi_overbought
        near_resistance = self.data.Close[-1] > self.bb_upper[-1]
        bearish_bias = self.data.Close[-1] < self.ema5[-1]

        if not self.position and low_vol and overbought and near_resistance and bearish_bias:
            # Calculate position size in BTC units for 1,000,000 USD
            price = self.data.Close[-1]
            size = self.risk_usd / price
            size = int(round(size))
            self.sell(size=size)
            self.entry_price = price
            self.entry_bar = self._i
            print(
                f"🚀 Moon Dev: Entering ShadowSpread bearish position on BTC at {price:.2f}! Size: {size} BTC. Low vol detected! 🌙"
            )

        # Exit logic if in position
        if self.position:
            bars_held = self._i - self.entry_bar
            current_price = self.data.Close[-1]

            # Stop loss: 2% above entry
            sl_price = self.entry_price * (1 + self.sl_pct)
            # Take profit: 5% below entry
            tp_price = self.entry_price * (1 - self.tp_pct)
            # Time-based exit
            time_exit = bars_held >= self.max_bars_hold

            if current_price >= sl_price or current_price <= tp_price or time_exit:
                self.position.close()
                if current_price >= sl_price:
                    reason = "Stop Loss hit! 📉"
                elif current_price <= tp_price:
                    reason = "Take Profit hit! 💰"
                else:
                    reason = "Time-based exit! ⏰"
                print(
                    f"🌙 Moon Dev: Exiting ShadowSpread at {current_price:.2f}. Reason: {reason} Held for {bars_held} bars. ✨"
                )
                self.entry_price = None
                self.entry_bar = None


# Run backtest
bt = Backtest(data, ShadowSpread, cash=10000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
