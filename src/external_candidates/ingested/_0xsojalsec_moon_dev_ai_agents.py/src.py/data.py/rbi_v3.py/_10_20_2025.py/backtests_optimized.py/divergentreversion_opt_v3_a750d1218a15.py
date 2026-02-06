# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v3.py
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
    bb_std = 2.0
    rsi_period = 14
    vol_period = 20
    vol_mult = 1.2  # 🌙 Reduced from 1.5 to allow more volume-confirmed entries for higher trade frequency without excessive noise
    atr_period = 14
    risk_pct = 0.02  # 🌙 Increased from 0.01 to 0.02 for larger position sizes, aiming for compounded returns toward 50% target
    sl_mult = 2.0  # 🌙 Increased from 1.5 to 2.0 for wider stops, reducing premature exits in volatile BTC 15m while managing risk
    lookback_div = 10  # 🌙 Increased from 5 to 10 for better divergence detection over slightly longer recent history
    max_bars = 20  # 🌙 Increased from 15 to 20 to give trades more time to revert in choppy conditions
    ema_period = 200  # 🌙 New: Added long-term EMA for trend filter to avoid counter-trend trades
    rsi_long_threshold = (
        30  # 🌙 New: RSI oversold threshold for long entries to tighten quality
    )
    rsi_short_threshold = (
        70  # 🌙 New: RSI overbought threshold for short entries to tighten quality
    )
    rr_ratio = 2.0  # 🌙 New: Risk-reward ratio for take-profit to lock in profits at 2:1, improving win rate contribution to returns

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
        self.ema200 = self.I(
            talib.EMA, self.data.Close, timeperiod=self.ema_period
        )  # 🌙 New: Trend filter EMA
        self.entry_bar = None
        self.tp_price = None  # 🌙 New: Track take-profit price for RR-based exits
        self.initial_risk_dist = (
            None  # 🌙 New: Track initial risk distance for TP calculation
        )
        print("🌙 DivergentReversion Strategy Initialized ✨")

    def next(self):
        if (
            len(self.data)
            < max(
                self.bb_period,
                self.rsi_period,
                self.atr_period,
                self.lookback_div,
                self.ema_period,
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
        ema200_val = self.ema200[-1]  # 🌙 New: EMA for trend filter

        # Debug prints for overextension
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

        # Handle existing position
        if self.position:
            bars_in = (
                len(self.data) - self.entry_bar if self.entry_bar is not None else 0
            )
            if bars_in > self.max_bars:
                self.position.close()
                print(f"🌙 Time-based EXIT after {bars_in} bars ✨")
                return

            # 🌙 New: RR-based Take Profit
            if self.tp_price is not None:
                if self.position.is_long and close >= self.tp_price:
                    self.position.close()
                    print(
                        f"🌙 LONG TP EXIT at {close:.2f} (Target {self.tp_price:.2f}, RR {self.rr_ratio}:1) 🚀"
                    )
                    return
                elif self.position.is_short and close <= self.tp_price:
                    self.position.close()
                    print(
                        f"🌙 SHORT TP EXIT at {close:.2f} (Target {self.tp_price:.2f}, RR {self.rr_ratio}:1) 🚀"
                    )
                    return

            # Existing mean reversion exits
            if self.position.is_long and close > middle:
                self.position.close()
                print(
                    f"🌙 LONG Reversion EXIT to mean at {close:.2f} (Middle BB {middle:.2f}) 🚀"
                )
                return
            elif self.position.is_short and close < middle:
                self.position.close()
                print(
                    f"🌙 SHORT Reversion EXIT to mean at {close:.2f} (Middle BB {middle:.2f}) 🚀"
                )
                return
            return  # No new entry if in position

        # No position: Check for entries
        start_idx = len(self.data) - self.lookback_div - 1
        if start_idx < 0:
            return

        # Bullish Divergence Check
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

        # 🌙 New: RSI threshold filter for long
        rsi_long_ok = rsi_val < self.rsi_long_threshold
        # 🌙 New: Trend filter for long (uptrend bias)
        trend_long_ok = close > ema200_val

        # Long Entry - Tightened with RSI and trend filters
        if (
            close < lower
            and bullish_div
            and volume > self.vol_mult * v_sma
            and rsi_long_ok
            and trend_long_ok
        ):
            entry_price = close
            sl_price = lower - self.sl_mult * atr_val
            risk_dist = entry_price - sl_price
            if risk_dist > 0:
                size = int(round((self.risk_pct * self.equity) / risk_dist))
                if size > 0:
                    self.buy(size=size, sl=sl_price)
                    self.entry_bar = len(self.data)
                    self.initial_risk_dist = risk_dist  # 🌙 Track for TP
                    self.tp_price = (
                        entry_price + self.rr_ratio * risk_dist
                    )  # 🌙 Set TP at 2:1 RR
                    print(
                        f"🌙 LONG ENTRY SIGNAL: Price {entry_price:.2f}, Size {size}, SL {sl_price:.2f}, TP {self.tp_price:.2f}, Risk {self.risk_pct*100}% 🚀"
                    )
                    return

        # Bearish Divergence Check
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

        # 🌙 New: RSI threshold filter for short
        rsi_short_ok = rsi_val > self.rsi_short_threshold
        # 🌙 New: Trend filter for short (downtrend bias)
        trend_short_ok = close < ema200_val

        # Short Entry - Tightened with RSI and trend filters
        if (
            close > upper
            and bearish_div
            and volume > self.vol_mult * v_sma
            and rsi_short_ok
            and trend_short_ok
        ):
            entry_price = close
            sl_price = upper + self.sl_mult * atr_val
            risk_dist = sl_price - entry_price
            if risk_dist > 0:
                size = int(round((self.risk_pct * self.equity) / risk_dist))
                if size > 0:
                    self.sell(size=size, sl=sl_price)
                    self.entry_bar = len(self.data)
                    self.initial_risk_dist = risk_dist  # 🌙 Track for TP
                    self.tp_price = (
                        entry_price - self.rr_ratio * risk_dist
                    )  # 🌙 Set TP at 2:1 RR
                    print(
                        f"🌙 SHORT ENTRY SIGNAL: Price {entry_price:.2f}, Size {size}, SL {sl_price:.2f}, TP {self.tp_price:.2f}, Risk {self.risk_pct*100}% 🚀"
                    )
                    return


bt = Backtest(
    data, DivergentReversion, cash=1000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
