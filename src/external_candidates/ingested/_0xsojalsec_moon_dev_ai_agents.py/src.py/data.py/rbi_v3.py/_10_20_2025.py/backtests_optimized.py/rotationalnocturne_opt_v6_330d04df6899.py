# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\RotationalNocturne_OPT_v6.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
df = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
df.columns = df.columns.str.strip().str.lower()
df = df.drop(columns=[col for col in df.columns if "unnamed" in col.lower()])
df = df.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Resample to 1H
ohlc_dict = {
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum",
}
data = df.resample("1H").agg(ohlc_dict).dropna()

# Ensure columns are correct
data.columns = ["Open", "High", "Low", "Close", "Volume"]


class RotationalNocturne(Strategy):
    rsi_entry_threshold = 50  # 🌙 Moon Dev Optimization: Lowered from 55 to 50 to increase entry frequency by capturing earlier momentum shifts, boosting trade opportunities realistically
    rsi_exit_threshold = 30  # 🌙 Moon Dev Optimization: Lowered from 35 to 30 to extend holding periods during pullbacks, improving win rate on trending moves
    risk_per_trade = 0.02  # 🌙 Moon Dev Optimization: Increased from 0.015 to 0.02 to scale up exposure per trade, accelerating returns while keeping risk controlled below 2%
    reward_risk_ratio = 3.0  # 🌙 Moon Dev Optimization: Raised from 2.5 to 3.0 to aim for higher reward capture in BTC's volatile uptrends, enhancing overall expectancy
    trail_entry_pct = 0.015  # 🌙 Moon Dev Optimization: Tightened from 0.02 to 0.015 to initiate trailing stops sooner, securing profits earlier in fast reversals
    trail_atr_mult = 2.5  # 🌙 Moon Dev Optimization: Increased from 2.0 to 2.5 to provide additional room for price swings, minimizing whipsaws in high-volatility overnight sessions
    max_hold_bars = 12  # 🌙 Moon Dev Optimization: Extended from 6 to 12 hours to capture longer overnight trends, allowing more development time without excessive exposure
    vol_multiplier = 0.3  # 🌙 Moon Dev Optimization: Lowered from 0.4 to 0.3 to permit more entries in moderate volume conditions, increasing frequency without entering dead markets
    prev_highs_period = 4  # 🌙 Moon Dev Optimization: Reduced from 6 to 4 hours for quicker "new high" detection, enabling earlier entries on building momentum and raising trade count
    atr_period = 14
    vol_sma_period = 20
    downtrend_sma_period = 1200  # 🌙 Moon Dev Optimization: Shortened from 4800 (~200 days) to 1200 (~50 days on 1H) for a more responsive trend filter, aligning with shorter-term BTC cycles to avoid missing opportunities
    atr_sma_period = 100
    min_stop_pct = 0.01
    max_stop_pct = 0.08
    base_stop_pct = 0.03  # 🌙 Moon Dev Optimization: Tightened from 0.04 to 0.03 for sharper risk control, paired with volatility adjustment to maintain adaptability

    # 🌙 Moon Dev Optimization: Retained MACD but added histogram check for stronger momentum confirmation, filtering out weak crossovers
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    macd_threshold = 0  # MACD line > signal for bullish bias

    # 🌙 Moon Dev Optimization: Lowered ADX threshold and added DI+ > DI- for directional strength, refining regime filter to include more trending but non-choppy setups
    adx_period = 14
    adx_threshold = 20  # Lowered from 25 to allow trading in moderately trending markets, increasing opportunities

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        vol = self.data.Volume

        self.sma200 = self.I(talib.SMA, close, self.downtrend_sma_period)
        self.atr = self.I(talib.ATR, high, low, close, self.atr_period)
        self.avg_atr = self.I(talib.SMA, self.atr, self.atr_sma_period)
        self.rsi = self.I(talib.RSI, close, 14)
        self.avg_vol = self.I(talib.SMA, vol, self.vol_sma_period)

        # 🌙 Moon Dev Optimization: Initialize MACD, ADX, and plus_di/minus_di for enhanced confirmation
        self.macd_line, self.macd_signal, self.macd_hist = self.I(
            talib.MACD, close, self.macd_fast, self.macd_slow, self.macd_signal
        )
        self.adx = self.I(talib.ADX, high, low, close, self.adx_period)
        self.plus_di = self.I(talib.PLUS_DI, high, low, close, self.adx_period)
        self.minus_di = self.I(talib.MINUS_DI, high, low, close, self.adx_period)

        self.max_high = 0
        self.entry_bar = 0
        self.just_entered = False
        self.partial_exited = False  # 🌙 Moon Dev Optimization: Track partial exit to avoid multiple partial closes

    def next(self):
        if len(self.data) < max(
            self.prev_highs_period + 1,
            self.atr_period,
            self.vol_sma_period,
            self.downtrend_sma_period,
            self.adx_period,
        ):
            return

        current_hour = self.data.index[-1].hour
        in_overnight_session = current_hour < 9  # 00:00 to 08:59 UTC approx overnight
        price = self.data.Close[-1]
        high_prev_max = (
            self.data.High[-self.prev_highs_period - 1 : -1].max()
            if len(self.data) > self.prev_highs_period
            else 0
        )
        new_60m_high = price > high_prev_max
        vol_ok = self.data.Volume[-1] > self.avg_vol[-1] * self.vol_multiplier
        trend_ok = price > self.sma200[-1] if not np.isnan(self.sma200[-1]) else True
        erod_ok = (
            self.rsi[-1] > self.rsi_entry_threshold
            if not np.isnan(self.rsi[-1])
            else False
        )

        # 🌙 Moon Dev Optimization: Enhanced MACD and ADX filters with histogram positivity and DI directional bias for higher-quality entries
        macd_ok = (
            (
                self.macd_line[-1] > self.macd_signal[-1]
                and self.macd_hist[-1] > self.macd_threshold
            )
            if not (
                np.isnan(self.macd_line[-1])
                or np.isnan(self.macd_signal[-1])
                or np.isnan(self.macd_hist[-1])
            )
            else True
        )
        adx_ok = (
            self.adx[-1] > self.adx_threshold and self.plus_di[-1] > self.minus_di[-1]
            if not (
                np.isnan(self.adx[-1])
                or np.isnan(self.plus_di[-1])
                or np.isnan(self.minus_di[-1])
            )
            else False
        )

        # 🌙 Moon Dev Optimization: Added bullish candle filter to confirm entry strength, reducing false breakouts on doji-like bars
        bull_candle_ok = self.data.Close[-1] > self.data.Open[-1]

        # Exit if not in session
        if self.position and not in_overnight_session:
            self.position.close()
            print(f"🌙 Moon Dev Session End Exit at {price:.2f} 📅")
            return

        if self.position:
            bars_held = len(self.data) - 1 - self.entry_bar
            entry_price = self.trades[-1].entry_price if self.trades else price
            current_profit_pct = (price - entry_price) / entry_price
            stop_frac = (
                (entry_price - self.position.sl) / entry_price
                if self.position.sl
                else 0
            )

            # Time-based exit
            if bars_held >= self.max_hold_bars:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars at {price:.2f} ⏰")
                return

            # EROD reversal exit
            if self.rsi[-1] < self.rsi_exit_threshold:
                self.position.close()
                print(f"🌙 Moon Dev EROD Reversal Exit at {price:.2f} 🚫")
                return

            # 🌙 Moon Dev Optimization: Added partial exit at 1:1 RR to lock in profits early, scaling out 50% while trailing the remainder for upside
            if not self.partial_exited and current_profit_pct >= stop_frac:
                half_size = self.position.size * 0.5
                self.sell(size=half_size)
                self.partial_exited = True
                print(f"🌙 Moon Dev Partial Exit (50%) at {price:.2f} after 1:1 RR 🎯")

            # Update max high
            self.max_high = max(self.max_high, self.data.High[-1])

            # Trailing logic
            if current_profit_pct > self.trail_entry_pct:
                # Move to breakeven if not already
                if self.position.sl < entry_price:
                    self.position.sl = entry_price
                    print(f"🌙 Moon Dev Breakeven Trail at {entry_price:.2f} 🔒")

                # ATR trail
                trail_sl = self.max_high - self.trail_atr_mult * self.atr[-1]
                if trail_sl > self.position.sl:
                    self.position.sl = trail_sl
                    print(
                        f"🌙 Moon Dev ATR Trail SL to {trail_sl:.2f} at {price:.2f} ✨"
                    )

            return

        # Entry logic with added filters
        if (
            not self.position
            and in_overnight_session
            and new_60m_high
            and vol_ok
            and trend_ok
            and erod_ok
            and macd_ok
            and adx_ok
            and bull_candle_ok
        ):
            approx_entry = self.data.Close[-1]  # Approximate entry with close
            atr_val = self.atr[-1]
            avg_atr_val = (
                self.avg_atr[-1] if not np.isnan(self.avg_atr[-1]) else atr_val
            )
            volatility_mult = atr_val / avg_atr_val if avg_atr_val != 0 else 1.0
            stop_dist_pct = self.base_stop_pct * volatility_mult
            stop_dist = max(
                self.min_stop_pct * approx_entry,
                min(self.max_stop_pct * approx_entry, stop_dist_pct * approx_entry),
            )
            sl_price = approx_entry - stop_dist
            tp_price = approx_entry + self.reward_risk_ratio * stop_dist
            stop_frac = stop_dist / approx_entry
            risk_amount = self.equity * self.risk_per_trade
            size = risk_amount / stop_dist
            size = int(
                round(size * (1 / volatility_mult))
            )  # 🌙 Moon Dev Optimization: Retained inverse volatility scaling, now paired with higher risk_per_trade for balanced amplification

            if size > 0:
                self.buy(size=size, sl=sl_price, tp=tp_price)
                self.max_high = approx_entry
                self.entry_bar = len(self.data) - 1
                self.partial_exited = False  # Reset partial exit flag
                print(
                    f"🌙 Moon Dev RotationalNocturne Entry Long at ~{approx_entry:.2f}, Size: {size}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )
                print(
                    f"   - New 60m High Confirmed 🌟 | RSI (EROD Proxy): {self.rsi[-1]:.1f} | Vol OK: {vol_ok} | Trend OK: {trend_ok} | MACD OK: {macd_ok} | ADX OK: {adx_ok} | Bull Candle: {bull_candle_ok}"
                )


bt = Backtest(data, RotationalNocturne, cash=1_000_000, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
