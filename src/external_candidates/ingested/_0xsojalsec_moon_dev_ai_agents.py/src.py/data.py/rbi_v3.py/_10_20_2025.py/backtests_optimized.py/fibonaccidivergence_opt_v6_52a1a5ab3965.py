# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\FibonacciDivergence_OPT_v6.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.set_index(pd.to_datetime(data["datetime"]))
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class FibonacciDivergence(Strategy):
    sma_period = 200
    rsi_period = 14
    atr_period = 14
    adx_period = 14  # 🌙 New: ADX for trend strength filter
    vol_sma_period = 20  # 🌙 New: Volume SMA for confirmation
    strength = 7  # 🌙 Improved: Increased from 5 to 7 for stronger, more reliable pivots (fewer false signals)
    risk_pct = 0.015  # 🌙 Improved: Increased from 0.01 to 0.015 for higher exposure to achieve target returns while managing risk
    key_fib_levels = [
        0.0,
        0.236,
        0.382,
        0.5,
        0.618,
        0.786,
        1.0,
        1.272,
        1.618,
    ]  # 🌙 Improved: Removed 2.618 to focus on more common levels, reducing noise
    fib_tolerance = 0.02  # 🌙 Improved: Tightened from 0.05 to 0.02 for more precise Fib level hits (better entry quality)
    min_divergence_strength = (
        5  # 🌙 New: Minimum RSI divergence threshold for significant signals only
    )
    min_swing_atr_mult = (
        1.5  # 🌙 New: Minimum swing size relative to ATR for significant moves
    )
    adx_threshold = (
        25  # 🌙 New: ADX > 25 to ensure trending market (avoid choppy conditions)
    )
    vol_mult = 1.5  # 🌙 New: Volume must be 1.5x average for confirmation (higher conviction entries)
    rr_ratio = 3  # 🌙 Improved: Increased TP from 2x ATR to 3x ATR for better risk-reward (aiming for higher returns)

    def init(self):
        self.bar_index = -1
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )
        self.sma = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_period)
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )  # 🌙 Added: ADX for market regime filter
        self.vol_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=self.vol_sma_period
        )  # 🌙 Added: Volume SMA for momentum filter
        self.low_pivots = []
        self.high_pivots = []
        print(
            "🌙 Moon Dev: Indicators initialized with optimizations! ADX & Volume filters active. ✨"
        )

    def next(self):
        self.bar_index += 1
        current_bar = self.bar_index
        if self.position:
            return

        equity = self._broker.equity
        risk_amount = equity * self.risk_pct

        # 🌙 Improved: Added volume, ADX, and swing size filters before processing signals for higher quality entries
        current_volume = self.data.Volume[current_bar]
        current_vol_sma = self.vol_sma[current_bar]
        current_adx = self.adx[current_bar]
        current_atr = self.atr[current_bar]
        has_volume_confirm = current_volume > self.vol_mult * current_vol_sma
        has_trend_confirm = current_adx > self.adx_threshold

        # Detect pivot lows (delayed by strength)
        i = current_bar - self.strength
        if i >= self.strength:
            low_slice_start = max(0, i - self.strength)
            low_slice_end = i + self.strength + 1
            if low_slice_end <= current_bar + 1:
                low_slice = self.data.Low[low_slice_start:low_slice_end]
                if len(low_slice) == 2 * self.strength + 1:
                    pivot_rel_idx = i - low_slice_start
                    if low_slice[pivot_rel_idx] == low_slice.min():
                        pivot_i = low_slice_start + pivot_rel_idx
                        if not self.low_pivots or self.low_pivots[-1][0] != pivot_i:
                            low_val = self.data.Low[pivot_i]
                            rsi_val = self.rsi[pivot_i]
                            self.low_pivots.append((pivot_i, low_val, rsi_val))
                            print(
                                f"🌙 Moon Dev: Pivot low detected at bar {pivot_i}, low={low_val:.2f}, RSI={rsi_val:.2f} 🔍"
                            )
                            if (
                                len(self.low_pivots) >= 2
                                and self.data.Close[current_bar] > self.sma[current_bar]
                            ):
                                prev_i, prev_low, prev_rsi = self.low_pivots[-2]
                                curr_i, curr_low, curr_rsi = self.low_pivots[-1]
                                # 🌙 Improved: Added significant divergence check and RSI oversold filter
                                if (
                                    curr_low < prev_low
                                    and curr_rsi
                                    > prev_rsi + self.min_divergence_strength
                                    and curr_rsi < 50
                                ):  # Higher low in RSI, significant diff, not overbought
                                    high_start = prev_i + 1
                                    high_end = curr_i + 1
                                    if (
                                        high_start < high_end
                                        and high_end <= current_bar + 1
                                    ):
                                        swing_high_slice = self.data.High[
                                            high_start:high_end
                                        ]
                                        swing_high = swing_high_slice.max()
                                        fib_range = swing_high - prev_low
                                        # 🌙 Improved: Added minimum swing size filter for significant setups
                                        if (
                                            fib_range
                                            > self.min_swing_atr_mult * self.atr[prev_i]
                                        ):
                                            retrace_pct = (
                                                swing_high - curr_low
                                            ) / fib_range
                                            is_at_fib = any(
                                                abs(retrace_pct - level)
                                                < self.fib_tolerance
                                                for level in self.key_fib_levels
                                            )
                                            if (
                                                is_at_fib
                                                and has_volume_confirm
                                                and has_trend_confirm
                                            ):
                                                print(
                                                    f"🌙 Moon Dev: Bullish divergence at Fib! Retrace PCT={retrace_pct:.3f}, Filters passed! Entry signal! 🚀"
                                                )
                                                entry_price = self.data.Close[
                                                    current_bar
                                                ]
                                                atr_val = current_atr
                                                if atr_val > 0:
                                                    sl_price = entry_price - atr_val
                                                    tp_price = (
                                                        entry_price
                                                        + self.rr_ratio * atr_val
                                                    )  # 🌙 Improved: Dynamic RR for better exits
                                                    stop_distance = (
                                                        entry_price - sl_price
                                                    )
                                                    position_size = (
                                                        risk_amount / stop_distance
                                                    )  # 🌙 Improved: Use float for precise fractional sizing (no int rounding)
                                                    if (
                                                        position_size > 0
                                                        and sl_price
                                                        < entry_price
                                                        < tp_price
                                                    ):
                                                        self.buy(
                                                            size=position_size,
                                                            limit=entry_price,
                                                            sl=sl_price,
                                                            tp=tp_price,
                                                        )
                                                        print(
                                                            f"🌙 Entering LONG at {entry_price:.2f}, size={position_size:.6f}, SL={sl_price:.2f}, TP={tp_price:.2f} ✨"
                                                        )
                            # Limit pivots to recent 10 for efficiency
                            if len(self.low_pivots) > 10:
                                self.low_pivots.pop(0)

        # Detect pivot highs (delayed by strength)
        i = current_bar - self.strength
        if i >= self.strength:
            high_slice_start = max(0, i - self.strength)
            high_slice_end = i + self.strength + 1
            if high_slice_end <= current_bar + 1:
                high_slice = self.data.High[high_slice_start:high_slice_end]
                if len(high_slice) == 2 * self.strength + 1:
                    pivot_rel_idx = i - high_slice_start
                    if high_slice[pivot_rel_idx] == high_slice.max():
                        pivot_i = high_slice_start + pivot_rel_idx
                        if not self.high_pivots or self.high_pivots[-1][0] != pivot_i:
                            high_val = self.data.High[pivot_i]
                            rsi_val = self.rsi[pivot_i]
                            self.high_pivots.append((pivot_i, high_val, rsi_val))
                            print(
                                f"🌙 Moon Dev: Pivot high detected at bar {pivot_i}, high={high_val:.2f}, RSI={rsi_val:.2f} 🔍"
                            )
                            if (
                                len(self.high_pivots) >= 2
                                and self.data.Close[current_bar] < self.sma[current_bar]
                            ):
                                prev_i, prev_high, prev_rsi = self.high_pivots[-2]
                                curr_i, curr_high, curr_rsi = self.high_pivots[-1]
                                # 🌙 Improved: Added significant divergence check and RSI overbought filter
                                if (
                                    curr_high > prev_high
                                    and curr_rsi
                                    < prev_rsi - self.min_divergence_strength
                                    and curr_rsi > 50
                                ):  # Lower high in RSI, significant diff, overbought
                                    low_start = prev_i + 1
                                    low_end = curr_i + 1
                                    if (
                                        low_start < low_end
                                        and low_end <= current_bar + 1
                                    ):
                                        swing_low_slice = self.data.Low[
                                            low_start:low_end
                                        ]
                                        swing_low = swing_low_slice.min()
                                        fib_range = prev_high - swing_low
                                        # 🌙 Improved: Added minimum swing size filter for significant setups
                                        if (
                                            fib_range
                                            > self.min_swing_atr_mult * self.atr[prev_i]
                                        ):
                                            retrace_pct = (
                                                curr_high - swing_low
                                            ) / fib_range
                                            is_at_fib = any(
                                                abs(retrace_pct - level)
                                                < self.fib_tolerance
                                                for level in self.key_fib_levels
                                            )
                                            if (
                                                is_at_fib
                                                and has_volume_confirm
                                                and has_trend_confirm
                                            ):
                                                print(
                                                    f"🌙 Moon Dev: Bearish divergence at Fib! Retrace PCT={retrace_pct:.3f}, Filters passed! Short signal! 🚀"
                                                )
                                                entry_price = self.data.Close[
                                                    current_bar
                                                ]
                                                atr_val = current_atr
                                                if atr_val > 0:
                                                    sl_price = entry_price + atr_val
                                                    tp_price = (
                                                        entry_price
                                                        - self.rr_ratio * atr_val
                                                    )  # 🌙 Improved: Dynamic RR for better exits
                                                    stop_distance = (
                                                        sl_price - entry_price
                                                    )
                                                    position_size = (
                                                        risk_amount / stop_distance
                                                    )  # 🌙 Improved: Use float for precise fractional sizing (no int rounding)
                                                    if (
                                                        position_size > 0
                                                        and tp_price
                                                        < entry_price
                                                        < sl_price
                                                    ):
                                                        self.sell(
                                                            size=position_size,
                                                            limit=entry_price,
                                                            sl=sl_price,
                                                            tp=tp_price,
                                                        )
                                                        print(
                                                            f"🌙 Entering SHORT at {entry_price:.2f}, size={position_size:.6f}, SL={sl_price:.2f}, TP={tp_price:.2f} ✨"
                                                        )
                            # Limit pivots to recent 10 for efficiency
                            if len(self.high_pivots) > 10:
                                self.high_pivots.pop(0)


bt = Backtest(
    data,
    FibonacciDivergence,
    cash=1000000,
    commission=0.002,
    exclusive_orders=True,
    trade_on_close=True,
)
stats = bt.run()
print(stats)
print(stats._strategy)
