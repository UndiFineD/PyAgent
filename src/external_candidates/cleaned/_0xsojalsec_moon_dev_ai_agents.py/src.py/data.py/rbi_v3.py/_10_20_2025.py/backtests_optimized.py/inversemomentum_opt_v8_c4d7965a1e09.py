# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v8.py
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
raw_data = raw_data.drop(columns=[col for col in raw_data.columns if "unnamed" in col.lower()])

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
    .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
    .dropna()
)


class InverseMomentum(Strategy):
    fast_period = (
        9  # 🌙 Optimized: Shortened from 12 to 9 for more responsive signals and increased trade frequency on BTC daily
    )
    slow_period = 21  # 🌙 Optimized: Adjusted from 26 to 21 to align with faster EMA while capturing trend
    vol_period = 20  # Retained: 20 for smooth volume average
    trend_period = (
        200  # 🌙 Optimized: Increased from 50 to 200 SMA for stronger long-term uptrend filter in BTC's bull market
    )
    risk_pct = 0.02  # 🌙 Optimized: Increased from 0.015 to 0.02 to take slightly more risk per trade for higher compounded returns
    atr_period = 14  # Retained: Standard ATR for volatility
    sl_mult = 2.0  # Retained: 2x ATR for stop loss
    tp_mult = (
        5.0  # 🌙 Optimized: Increased from 4.0 to 5.0 for better 2.5:1 RR, aiming for larger winners in trending BTC
    )
    vol_mult = 1.2  # 🌙 Optimized: Reduced from 1.5 to 1.2 to allow more quality entries without being too restrictive
    adx_period = 14  # Retained: ADX for trend strength
    adx_threshold = (
        20  # 🌙 Optimized: Lowered from 25 to 20 to capture more trending opportunities while avoiding extreme chop
    )
    rsi_period = 14  # Retained: RSI for momentum
    trail_trigger = 2.0  # New: ATR multiple to trigger trailing stop (after 2x ATR profit)
    trail_mult = 1.5  # New: Trailing stop distance (1.5x ATR below high)

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Retained: EMA for responsive trend detection
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)  # SMA fine for volume
        self.trend_sma = self.I(talib.SMA, close, timeperiod=self.trend_period)  # SMA for long-term trend

        # 🌙 Retained: Volatility and momentum indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print("🌙 Moon Dev Backtest Initialized: Optimized InverseMomentum Strategy Loaded! ✨")

    def next(self):
        # Debug print every 50 bars for monitoring (updated with new params)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend {self.trend_sma[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Optimized: Removed early bearish crossover exit to let winners run to TP or trailing SL, reducing premature closes in BTC uptrends
            # New: Implement trailing stop after hitting trigger profit to lock in gains dynamically
            entry_price = self.position.entry_price
            unrealized_pnl = self.data.Close[-1] - entry_price
            if unrealized_pnl > self.trail_trigger * self.atr[-1]:
                # Trail SL to current close minus trail_mult * ATR, but not below initial SL
                new_sl = self.data.Close[-1] - self.trail_mult * self.atr[-1]
                if new_sl > self.position.sl:
                    self.position.sl = new_sl
                    print(
                        f"🌙 Moon Dev Trailing Update: Adjusted SL to {new_sl:.2f} (Profit: {unrealized_pnl:.2f}, ATR: {self.atr[-1]:.2f}) ✨"
                    )
        else:
            # 🌙 Optimized Entry: Bullish EMA crossover + loosened volume (1.2x) + stronger trend filter (200 SMA) + RSI (>45 for more momentum entries) + ADX (>20)
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_sma[-1]
                and self.rsi[-1] > 45
                and self.adx[-1] > self.adx_threshold
            ):
                entry_price = self.data.Close[-1]
                stop_dist = self.sl_mult * self.atr[-1]
                sl_price = entry_price - stop_dist
                # 🌙 Retained: Dynamic position sizing based on ATR for consistent risk
                risk_fraction = stop_dist / entry_price
                size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
                # Cap size to avoid over-leveraging
                size = min(size, 1.0)

                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Entry: Bullish momentum on BTC! EMA crossover confirmed with volume ({self.vol_mult}x), "
                    f"trend, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
