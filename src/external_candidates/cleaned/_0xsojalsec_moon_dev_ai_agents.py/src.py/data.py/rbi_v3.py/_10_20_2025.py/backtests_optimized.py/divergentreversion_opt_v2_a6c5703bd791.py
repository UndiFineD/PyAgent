# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v2.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"

data = pd.read_csv(path)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)
data = data.set_index(pd.to_datetime(data["datetime"]))


class DivergentReversion(Strategy):
    bb_period = 20
    bb_std = 2.0  # Kept standard, but could tune to 1.8 for more signals if needed
    rsi_period = 14
    vol_period = 20
    vol_mult = 1.2  # Reduced from 1.5 to allow more entries with slightly lower volume confirmation, increasing trade frequency realistically
    atr_period = 14
    risk_pct = 0.015  # Increased from 0.01 to 1.5% risk per trade for higher exposure and potential returns, while still managing risk
    sl_mult = 1.5
    tp_mult = 3.0  # New: Added take profit multiplier for 1:3 risk-reward ratio to improve average win size and overall returns
    lookback_div = 10  # Increased from 5 to capture better, longer-term divergences without curve-fitting
    max_bars = 15
    adx_period = 14
    adx_threshold = 25  # New: ADX filter to only trade in ranging markets (ADX < 25) where mean reversion works best, avoiding strong trends
    rsi_oversold = 30  # New: RSI threshold for long entries to tighten oversold condition
    rsi_overbought = 70  # New: RSI threshold for short entries to tighten overbought condition
    sma_trend_period = 50  # New: Simple trend filter using SMA(50) - only long above SMA (uptrend reversion), short below (downtrend reversion) for better context

    def init(self):
        upper, middle, lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_std,
            nbdevdn=self.bb_std,
        )
        self.bb_upper = upper
        self.bb_middle = middle
        self.bb_lower = lower
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=self.vol_period)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )  # New: ADX for market regime filter
        self.sma_trend = self.I(
            talib.SMA, self.data.Close, timeperiod=self.sma_trend_period
        )  # New: SMA for basic trend filter
        self.entry_bar = None
        print(
            "🌙 Optimized DivergentReversion Strategy Initialized: Added RSI thresholds, TP, ADX filter, trend SMA, adjusted params for higher returns ✨"
        )

    def next(self):
        if (
            len(self.data)
            < max(
                self.bb_period,
                self.rsi_period,
                self.atr_period,
                self.lookback_div,
                self.adx_period,
                self.sma_trend_period,
            )
            + 1
        ):
            return

        close = self.data.Close[-1]
        high = self.data.High[-1]
        low = self.data.Low[-1]
        volume = self.data.Volume[-1]
        upper = self.bb_upper[-1]
        lower = self.bb_lower[-1]
        middle = self.bb_middle[-1]
        v_sma = self.vol_sma[-1]
        atr_val = self.atr[-1]
        rsi_val = self.rsi[-1]
        adx_val = self.adx[-1]
        sma_trend = self.sma_trend[-1]

        # Debug prints for overextension (kept as-is)
        if close < lower:
            vol_ratio = volume / v_sma if v_sma > 0 else 0
            print(
                f"🌙 Overextended LOW detected: Close {close:.2f} < Lower BB {lower:.2f}, RSI {rsi_val:.2f}, Vol Ratio {vol_ratio:.2f} 🚀"
            )
        if close > upper:
            vol_ratio = volume / v_sma if v_sma > 0 else 0
            print(
                f"🌙 Overextended HIGH detected: Close {close:.2f} > Upper BB {upper:.2f}, RSI {rsi_val:.2f}, Vol Ratio {vol_ratio:.2f} 🚀"
            )

        # New: Market regime filter - skip if trending (high ADX)
        if adx_val > self.adx_threshold:
            return  # Avoid trades in strong trends where reversion fails

        # Handle existing position (kept, but now TP will also trigger exits)
        if self.position:
            bars_in = len(self.data) - self.entry_bar if self.entry_bar is not None else 0
            if bars_in > self.max_bars:
                self.position.close()
                print(f"🌙 Time-based EXIT after {bars_in} bars ✨")
                return

            if self.position.is_long and close > middle:
                self.position.close()
                print(f"🌙 LONG Reversion EXIT to mean at {close:.2f} (Middle BB {middle:.2f}) 🚀")
                return
            elif self.position.is_short and close < middle:
                self.position.close()
                print(f"🌙 SHORT Reversion EXIT to mean at {close:.2f} (Middle BB {middle:.2f}) 🚀")
                return
            return  # No new entry if in position

        # No position: Check for entries
        start_idx = len(self.data) - self.lookback_div - 1
        if start_idx < 0:
            return

        # Bullish Divergence Check (kept logic, but longer lookback)
        bullish_div = False
        lows_slice = self.data.Low[start_idx:-1]
        if len(lows_slice) > 0:
            min_idx_rel = np.argmin(lows_slice)
            prev_low_idx = start_idx + min_idx_rel
            prev_low_price = self.data.Low[prev_low_idx]
            prev_rsi = self.rsi[prev_low_idx]
            if low < prev_low_price and rsi_val > prev_rsi:
                bullish_div = True
                print(
                    f"🌙 Bullish DIVERGENCE confirmed: Low {low:.2f} < Prev {prev_low_price:.2f}, RSI {rsi_val:.2f} > {prev_rsi:.2f} ✨"
                )

        # New: Trend filter for long - only if above SMA (revert in uptrend)
        long_trend_ok = close > sma_trend

        # Optimized Long Entry: Added RSI < 30, trend filter, volume, TP
        if (
            close < lower
            and bullish_div
            and rsi_val < self.rsi_oversold  # New: Tighten with RSI oversold
            and volume > self.vol_mult * v_sma
            and long_trend_ok
        ):  # New: Trend filter
            entry_price = close
            sl_price = lower - self.sl_mult * atr_val
            risk_dist = entry_price - sl_price
            if risk_dist > 0:
                size = (
                    self.risk_pct * self.equity
                ) / risk_dist  # Changed to float for fractional shares, allowing precise sizing
                if size > 0:
                    tp_price = entry_price + self.tp_mult * risk_dist  # New: Take profit at 3x risk
                    self.buy(size=size, sl=sl_price, tp=tp_price)
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙 LONG ENTRY SIGNAL: Price {entry_price:.2f}, Size {size:.4f}, SL {sl_price:.2f}, TP {tp_price:.2f}, Risk {self.risk_pct * 100}% 🚀"
                    )
                    return

        # Bearish Divergence Check (kept logic, longer lookback)
        bearish_div = False
        highs_slice = self.data.High[start_idx:-1]
        if len(highs_slice) > 0:
            max_idx_rel = np.argmax(highs_slice)
            prev_high_idx = start_idx + max_idx_rel
            prev_high_price = self.data.High[prev_high_idx]
            prev_rsi = self.rsi[prev_high_idx]
            if high > prev_high_price and rsi_val < prev_rsi:
                bearish_div = True
                print(
                    f"🌙 Bearish DIVERGENCE confirmed: High {high:.2f} > Prev {prev_high_price:.2f}, RSI {rsi_val:.2f} < {prev_rsi:.2f} ✨"
                )

        # New: Trend filter for short - only if below SMA (revert in downtrend)
        short_trend_ok = close < sma_trend

        # Optimized Short Entry: Added RSI > 70, trend filter, volume, TP
        if (
            close > upper
            and bearish_div
            and rsi_val > self.rsi_overbought  # New: Tighten with RSI overbought
            and volume > self.vol_mult * v_sma
            and short_trend_ok
        ):  # New: Trend filter
            entry_price = close
            sl_price = upper + self.sl_mult * atr_val
            risk_dist = sl_price - entry_price
            if risk_dist > 0:
                size = (self.risk_pct * self.equity) / risk_dist  # Changed to float for fractional shares
                if size > 0:
                    tp_price = entry_price - self.tp_mult * risk_dist  # New: Take profit at 3x risk
                    self.sell(size=size, sl=sl_price, tp=tp_price)
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙 SHORT ENTRY SIGNAL: Price {entry_price:.2f}, Size {size:.4f}, SL {sl_price:.2f}, TP {tp_price:.2f}, Risk {self.risk_pct * 100}% 🚀"
                    )
                    return


bt = Backtest(data, DivergentReversion, cash=1000000, commission=0.001, exclusive_orders=True)
stats = bt.run()
print(stats)
