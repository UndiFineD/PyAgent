# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\InverseMomentum_OPT_v9.py
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
    fast_period = 12  # 🌙 Optimized: Kept at 12 for responsive signals on daily BTC
    slow_period = 26  # 🌙 Optimized: Kept at 26 for robust trend following like MACD
    vol_period = 20  # 🌙 Optimized: Kept at 20 for reliable volume smoothing
    trend_period = (
        200  # 🌙 Optimized: Increased from 50 to 200 for stronger long-term trend filter on BTC's multi-year cycles
    )
    risk_pct = 0.02  # 🌙 Optimized: Increased from 0.015 to 0.02 to allow higher exposure for targeting 50% returns while keeping risk controlled
    atr_period = 14  # Kept: Standard ATR for dynamic stops
    sl_mult = 2.0  # Kept: Balanced SL for risk management
    tp_mult = 5.0  # 🌙 Optimized: Increased from 4.0 to 5.0 for improved 2.5:1 RR to boost returns without excessive win rate hit
    vol_mult = 1.5  # Kept: Ensures high-quality volume-confirmed entries
    adx_period = 14  # Kept: For trend strength
    adx_threshold = 20  # 🌙 Optimized: Lowered from 25 to 20 to allow more trades in moderately trending markets, increasing opportunity count
    rsi_period = 14  # Kept: For momentum confirmation

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

        # 🌙 Optimized: Retained EMA for signal line to balance speed and noise reduction
        self.fast_ema = self.I(talib.EMA, close, timeperiod=self.fast_period)
        self.slow_ema = self.I(talib.EMA, close, timeperiod=self.slow_period)
        self.vol_sma = self.I(talib.SMA, volume, timeperiod=self.vol_period)
        # 🌙 Optimized: Switched trend to EMA from SMA for faster adaptation to BTC's volatile trends
        self.trend_ema = self.I(talib.EMA, close, timeperiod=self.trend_period)

        # Retained: Volatility and strength indicators
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)

        # Debug print on init
        print(
            "🌙 Moon Dev Backtest Initialized: Optimized Bi-Directional InverseMomentum Strategy Loaded with Shorts! ✨"
        )

    def next(self):
        # Debug print every 50 bars for monitoring (enhanced with trend EMA)
        if len(self.data) % 50 == 0:
            print(
                f"🌙 Moon Dev Debug [{len(self.data)}]: Fast EMA {self.fast_ema[-1]:.2f}, Slow EMA {self.slow_ema[-1]:.2f}, "
                f"Vol {self.data.Volume[-1]:.0f} vs Avg {self.vol_sma[-1]:.0f} (Mult: {self.data.Volume[-1] / self.vol_sma[-1]:.2f}), "
                f"Close {self.data.Close[-1]:.2f} vs Trend EMA {self.trend_ema[-1]:.2f}, "
                f"ATR {self.atr[-1]:.2f}, ADX {self.adx[-1]:.2f}, RSI {self.rsi[-1]:.2f} 🚀"
            )

        if self.position:
            # 🌙 Optimized: Symmetric early exits on signal reversals to protect profits while allowing trends to run until crossover
            if self.position.is_long:
                # Exit long on bearish crossover
                if self.fast_ema[-2] > self.slow_ema[-2] and self.fast_ema[-1] < self.slow_ema[-1]:
                    self.position.close()
                    print(f"🌙 Moon Dev Exit Long: Bearish crossover detected! Closing at {self.data.Close[-1]:.2f} ✨")
            elif self.position.is_short:
                # Exit short on bullish crossover
                if self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1]:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Exit Short: Bullish crossover detected! Closing at {self.data.Close[-1]:.2f} ✨"
                    )
        else:
            entry_price = self.data.Close[-1]
            stop_dist = self.sl_mult * self.atr[-1]
            risk_fraction = stop_dist / entry_price
            size = self.risk_pct / risk_fraction if risk_fraction > 0 else 0
            size = min(size, 1.0)  # Cap to prevent over-leveraging

            # 🌙 Optimized Long Entry: Added bullish candle filter (Close > Open) for higher quality setups; bi-directional for more opportunities
            if (
                (self.fast_ema[-2] < self.slow_ema[-2] and self.fast_ema[-1] > self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] > self.trend_ema[-1]
                and self.rsi[-1] > 50
                and self.adx[-1] > self.adx_threshold
                and self.data.Close[-1] > self.data.Open[-1]
            ):
                sl_price = entry_price - stop_dist
                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price + tp_dist

                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Long Entry: Bullish momentum on BTC! EMA crossover with volume ({self.vol_mult}x), "
                    f"trend, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}, bullish candle. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )

            # 🌙 Optimized Short Entry: Added symmetric short side to capture downtrends, inverted filters, bearish candle for quality
            elif (
                (self.fast_ema[-2] > self.slow_ema[-2] and self.fast_ema[-1] < self.slow_ema[-1])
                and self.data.Volume[-1] > self.vol_mult * self.vol_sma[-1]
                and self.data.Close[-1] < self.trend_ema[-1]
                and self.rsi[-1] < 50
                and self.adx[-1] > self.adx_threshold
                and self.data.Close[-1] < self.data.Open[-1]
            ):
                sl_price = entry_price + stop_dist
                tp_dist = self.tp_mult * self.atr[-1]
                tp_price = entry_price - tp_dist

                self.sell(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🌙 Moon Dev Short Entry: Bearish momentum on BTC! EMA crossover with volume ({self.vol_mult}x), "
                    f"anti-trend, RSI {self.rsi[-1]:.1f}, ADX {self.adx[-1]:.1f}, bearish candle. "
                    f"Entry: {entry_price:.2f}, Size: {size:.3f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )


# Run backtest
bt = Backtest(daily_data, InverseMomentum, cash=1000000, commission=0.002, exclusive_orders=True)

stats = bt.run()
print(stats)
print(stats._strategy)
