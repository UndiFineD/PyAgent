# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\RotationalNocturne_OPT_v3.py
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
    rsi_entry_threshold = 50  # 🌙 Moon Dev Optimization: Lowered from 55 to 50 to increase trade frequency by capturing earlier momentum shifts, boosting overall returns realistically
    rsi_exit_threshold = 30  # 🌙 Moon Dev Optimization: Lowered from 35 to 30 to extend holding periods for stronger trends, allowing more profit capture before reversals
    risk_per_trade = 0.03  # 🌙 Moon Dev Optimization: Increased from 0.015 to 0.03 to scale up exposure per trade, accelerating returns while keeping risk manageable through vol-adjusted stops
    reward_risk_ratio = 3.5  # 🌙 Moon Dev Optimization: Raised from 2.5 to 3.5 to target superior reward-to-risk, enhancing expectancy and pushing towards target returns
    trail_entry_pct = 0.015  # 🌙 Moon Dev Optimization: Tightened from 0.02 to 0.015 to initiate profit protection sooner, securing gains in BTC's quick reversals
    trail_atr_mult = 1.8  # 🌙 Moon Dev Optimization: Adjusted from 2.0 to 1.8 to balance breathing room with tighter trailing, reducing give-back in volatile sessions
    max_hold_bars = 12  # 🌙 Moon Dev Optimization: Extended from 6 to 12 hours to permit longer trend development during overnight periods, capturing extended moves
    vol_multiplier = 0.25  # 🌙 Moon Dev Optimization: Reduced from 0.4 to 0.25 to allow more entries on moderate volume spikes, increasing opportunity count without liquidity risks
    prev_highs_period = 5  # 🌙 Moon Dev Optimization: Adjusted from 6 to 5 hours for more sensitive breakout detection, generating additional high-quality setups
    atr_period = 14
    vol_sma_period = 20
    downtrend_sma_period = 4800  # Approx 200 days * 24 hours
    atr_sma_period = 100
    min_stop_pct = 0.01
    max_stop_pct = 0.08
    base_stop_pct = 0.05  # 🌙 Moon Dev Optimization: Widened from 0.04 to 0.05 to accommodate BTC volatility better, reducing premature stop-outs and improving win rate

    # 🌙 Moon Dev Optimization: Retained MACD for momentum confirmation, ensuring entries align with accelerating trends
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    macd_threshold = 0  # MACD line > signal for bullish bias

    # 🌙 Moon Dev Optimization: Retained ADX but lowered threshold to 20 for more trades in moderately trending markets, filtering extreme chop while expanding opportunities
    adx_period = 14
    adx_threshold = 20

    # 🌙 Moon Dev Optimization: Added partial profit-taking at 2.5% to lock in gains early, scaling out half the position to compound returns and reduce exposure dynamically
    partial_profit_pct = 0.025

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

        # 🌙 Moon Dev Optimization: Retained MACD and ADX indicators for robust filtering
        self.macd_line, self.macd_signal, _ = self.I(
            talib.MACD, close, self.macd_fast, self.macd_slow, self.macd_signal
        )
        self.adx = self.I(talib.ADX, high, low, close, self.adx_period)

        self.max_high = 0
        self.entry_bar = 0
        self.partial_exited = False  # 🌙 Moon Dev Optimization: Initialize flag for partial profit-taking control

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
            self.data.High[-self.prev_highs_period - 1 : -1].max() if len(self.data) > self.prev_highs_period else 0
        )
        # 🌙 Moon Dev Optimization: Changed to High[-1] for breakout confirmation to include intrabar highs, improving entry timing on true breakouts
        new_60m_high = self.data.High[-1] > high_prev_max
        vol_ok = self.data.Volume[-1] > self.avg_vol[-1] * self.vol_multiplier
        trend_ok = price > self.sma200[-1] if not np.isnan(self.sma200[-1]) else True
        erod_ok = self.rsi[-1] > self.rsi_entry_threshold if not np.isnan(self.rsi[-1]) else False

        # 🌙 Moon Dev Optimization: Retained momentum and trend strength filters, with relaxed ADX for more actionable signals
        macd_ok = (
            self.macd_line[-1] > self.macd_signal[-1]
            if not (np.isnan(self.macd_line[-1]) or np.isnan(self.macd_signal[-1]))
            else True
        )
        adx_ok = self.adx[-1] > self.adx_threshold if not np.isnan(self.adx[-1]) else False

        # 🌙 Moon Dev Optimization: Added bullish candle filter to ensure positive close on breakout bar, confirming immediate momentum for higher-quality entries
        bullish_candle = self.data.Close[-1] > self.data.Open[-1]

        # Exit if not in session
        if self.position and not in_overnight_session:
            self.position.close()
            print(f"🌙 Moon Dev Session End Exit at {price:.2f} 📅")
            self.partial_exited = False  # Reset flag on exit
            return

        if self.position:
            if len(self.trades) == 0:
                return
            entry_price = self.trades[-1].entry_price
            current_profit_pct = (price - entry_price) / entry_price
            bars_held = len(self.data) - 1 - self.entry_bar
            # Time-based exit
            if bars_held >= self.max_hold_bars:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars at {price:.2f} ⏰")
                self.partial_exited = False
                return

            # EROD reversal exit
            if self.rsi[-1] < self.rsi_exit_threshold:
                self.position.close()
                print(f"🌙 Moon Dev EROD Reversal Exit at {price:.2f} 🚫")
                self.partial_exited = False
                return

            # 🌙 Moon Dev Optimization: Added partial profit-taking logic to scale out half at 2.5% profit, locking gains and allowing remainder to run
            if current_profit_pct > self.partial_profit_pct and not self.partial_exited:
                half_size = self.position.size * 0.5
                self.sell(size=half_size)
                self.partial_exited = True
                # Lock remaining at breakeven + small buffer
                self.position.sl = entry_price * 1.005
                print(
                    f"🌙 Moon Dev Partial Profit Taking: Sold {half_size} at {price:.2f} ({current_profit_pct * 100:.1f}%) 💰"
                )

            # Update max high
            self.max_high = max(self.max_high, self.data.High[-1])

            # Trailing logic
            if current_profit_pct > self.trail_entry_pct:
                # Move to breakeven if not already (adjusted for partial)
                if self.position.sl < entry_price * 1.005:
                    self.position.sl = entry_price * 1.005
                    print(f"🌙 Moon Dev Breakeven Trail at {entry_price * 1.005:.2f} 🔒")

                # ATR trail
                trail_sl = self.max_high - self.trail_atr_mult * self.atr[-1]
                if trail_sl > self.position.sl:
                    self.position.sl = trail_sl
                    print(f"🌙 Moon Dev ATR Trail SL to {trail_sl:.2f} at {price:.2f} ✨")

            return

        # Entry logic with enhanced filters
        if (
            not self.position
            and in_overnight_session
            and new_60m_high
            and vol_ok
            and trend_ok
            and erod_ok
            and macd_ok
            and adx_ok
            and bullish_candle
        ):
            approx_entry = self.data.Close[-1]  # Approximate entry with close
            atr_val = self.atr[-1]
            avg_atr_val = self.avg_atr[-1] if not np.isnan(self.avg_atr[-1]) else atr_val
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
            size = (
                risk_amount / stop_dist
            )  # 🌙 Moon Dev Optimization: Simplified to exact floating-point calculation for fractional positions, removed extra vol scaling for standard ATR risk management, enabling precise exposure to boost returns
            if size > 0:
                self.buy(size=size, sl=sl_price, tp=tp_price)
                self.max_high = approx_entry
                self.entry_bar = len(self.data) - 1
                self.partial_exited = False  # Reset for new position
                print(
                    f"🌙 Moon Dev RotationalNocturne Entry Long at ~{approx_entry:.2f}, Size: {size}, SL: {sl_price:.2f}, TP: {tp_price:.2f} 🚀"
                )
                print(
                    f"   - New 60m High Confirmed 🌟 | RSI (EROD Proxy): {self.rsi[-1]:.1f} | Vol OK: {vol_ok} | Trend OK: {trend_ok} | MACD OK: {macd_ok} | ADX OK: {adx_ok} | Bullish Candle: {bullish_candle}"
                )


bt = Backtest(data, RotationalNocturne, cash=1_000_000, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
