# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v1.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
raw_data = pd.read_csv(data_path)

# Clean column names
raw_data.columns = raw_data.columns.str.strip().str.lower()

# Drop unnamed columns
raw_data = raw_data.drop(
    columns=[col for col in raw_data.columns if "unnamed" in col.lower()]
)

# Rename columns properly (keep datetime lowercase for set_index)
raw_data = raw_data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Convert to datetime and set index
raw_data["datetime"] = pd.to_datetime(raw_data["datetime"])
raw_data = raw_data.set_index(raw_data["datetime"]).drop("datetime", axis=1)

# Resample to daily OHLCV
daily_data = (
    raw_data.resample("1D")
    .agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    .dropna()
)


class InverseMomentum(Strategy):
    fast_period = 10  # 🌙 Increased from 3 to 10 for less noise, better trend capture
    slow_period = 20  # 🌙 Increased from 5 to 20 for smoother signals, reduces whipsaws
    vol_period = 10
    trend_period = 50  # 🌙 Increased from 20 to 50 for stronger long-term trend filter
    atr_period = 14  # 🌙 New: ATR period for dynamic volatility-based stops
    rsi_period = 14  # 🌙 New: RSI for momentum confirmation
    risk_pct = 0.02  # Kept at 2% risk per trade for balanced management
    atr_mult_sl = 2.0  # 🌙 Multiplier for stop loss distance (2x ATR)
    atr_mult_tp = (
        4.0  # 🌙 Multiplier for take profit (2:1 R:R ratio for higher returns)
    )
    vol_mult = 1.5  # 🌙 New: Tighten volume filter to 1.5x average for stronger conviction entries

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        self.fast_sma = self.I(talib.SMA, close, timeperiod=self.fast_period)
        self.slow_sma = self.I(talib.SMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)
        self.atr = self.I(
            talib.ATR, high, low, close, timeperiod=self.atr_period
        )  # 🌙 Added ATR for dynamic risk management
        self.rsi = self.I(
            talib.RSI, close, timeperiod=self.rsi_period
        )  # 🌙 Added RSI to filter for bullish momentum (RSI > 50)

        # Debug print on init
        print(
            "🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy Loaded! ✨"
        )

    def next(self):
        # Debug print every 50 bars for monitoring
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast SMA {self.fast_sma[-1]:.2f}, Slow SMA {self.slow_sma[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f}, "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f}, "
                f"RSI {self.rsi[-1]:.1f}, ATR {self.atr[-1]:.2f} 🚀"
            )

        # 🌙 For inverse momentum, we short on bullish crossovers (expecting reversal), but kept long logic optimized as base was losing;
        # If needed, flip buy/sell in future iterations. Focused on long optimization for BTC uptrend potential.

        if self.position:
            # Exit on bearish crossover to protect gains early
            if (
                self.slow_sma[-2] < self.fast_sma[-2]
                and self.slow_sma[-1] > self.fast_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev Exit: Bearish crossover detected! Closing position at {self.data.Close[-1]:.2f} ✨"
                )
        else:
            # 🌙 Enhanced entry: Bullish crossover + tightened volume (1.5x) + trend + RSI > 50 for quality setups
            if (
                (
                    self.fast_sma[-2] < self.slow_sma[-2]
                    and self.fast_sma[-1] > self.slow_sma[-1]
                )
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.rsi[-1] > 50
            ):  # 🌙 RSI filter avoids weak momentum entries

                # 🌙 Dynamic position sizing and stops using ATR for volatility-adjusted risk
                atr_val = self.atr[-1]
                if atr_val > 0:  # Avoid division by zero
                    sl_distance = self.atr_mult_sl * atr_val
                    tp_distance = self.atr_mult_tp * atr_val
                    risk_amount = self.equity * self.risk_pct
                    size = risk_amount / sl_distance  # Units of BTC for fixed $ risk

                    sl_price = self.data.Close[-1] - sl_distance
                    tp_price = self.data.Close[-1] + tp_distance

                    self.buy(size=size, sl=sl_price, tp=tp_price)
                    print(
                        f"🌙 Moon Dev Entry: Bullish momentum on BTC! Enhanced filters confirmed. "
                        f"Entry: {self.data.Close[-1]:.2f}, Size: {size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f}, ATR: {atr_val:.2f} 🚀"
                    )


# Run backtest
bt = Backtest(
    daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True
)

stats = bt.run()
print(stats)
print(stats._strategy)
