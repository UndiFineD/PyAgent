# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\SynergisticConfluence_OPT_v1.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "datetime": "Datetime",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data = data.set_index(pd.to_datetime(data["Datetime"]))


class SynergisticConfluence(Strategy):
    adx_period = 14
    atr_period = 14
    rsi_period = 14
    bb_period = 20
    bb_std = 2
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    swing_period = 10
    avg_atr_period = 20
    ema_period = 50  # 🌙 Moon Dev: Added EMA50 for trend filter to avoid counter-trend trades
    vol_ma_period = 20  # 🌙 Moon Dev: Added volume MA for confirmation on entries
    risk_per_trade = (
        0.02  # 🌙 Moon Dev: Increased risk per trade to 2% for higher potential returns while managing drawdown
    )
    max_bars_held = (
        15  # 🌙 Moon Dev: Reduced max hold time to 15 bars (3.75 hours on 15m) to exit stagnant trades faster
    )

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume  # 🌙 Moon Dev: Use volume for entry confirmation

        self.rsi = self.I(talib.RSI, close, timeperiod=self.rsi_period)
        bb_upper, bb_middle, bb_lower = self.I(
            talib.BBANDS,
            close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_std,
            nbdevdn=self.bb_std,
            matype=0,
        )
        self.bb_upper = bb_upper
        self.bb_middle = bb_middle
        self.bb_lower = bb_lower
        self.macd, self.signal, self.hist = self.I(
            talib.MACD,
            close,
            fastperiod=self.macd_fast,
            slowperiod=self.macd_slow,
            signalperiod=self.macd_signal,
        )
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)
        self.adx = self.I(talib.ADX, high, low, close, timeperiod=self.adx_period)
        self.avg_atr = self.I(talib.SMA, self.atr, timeperiod=self.avg_atr_period)
        self.swing_high = self.I(talib.MAX, high, timeperiod=self.swing_period)
        self.swing_low = self.I(talib.MIN, low, timeperiod=self.swing_period)
        self.ema50 = self.I(talib.EMA, close, timeperiod=self.ema_period)  # 🌙 Moon Dev: EMA50 for directional bias
        self.vol_ma = self.I(
            talib.SMA, volume, timeperiod=self.vol_ma_period
        )  # 🌙 Moon Dev: Volume MA for momentum filter

        self.entry_price = 0
        self.stop_price = 0
        self.tp_price = 0
        self.partial_taken = False
        self.entry_bar = 0
        self.is_long = False

    def next(self):
        if len(self.data) < 50:  # Warmup
            return

        current_close = self.data.Close[-1]
        current_high = self.data.High[-1]
        current_low = self.data.Low[-1]
        current_rsi = self.rsi[-1]
        prev_rsi = self.rsi[-2]
        current_macd = self.macd[-1]
        prev_macd = self.macd[-2]
        current_signal = self.signal[-1]
        prev_signal = self.signal[-2]
        current_hist = self.hist[-1]
        prev_hist = self.hist[-2]
        current_bb_lower = self.bb_lower[-1]
        current_bb_upper = self.bb_upper[-1]
        current_bb_middle = self.bb_middle[-1]
        current_atr = self.atr[-1]
        current_adx = self.adx[-1]
        current_avg_atr = self.avg_atr[-1]
        current_swing_low = self.swing_low[-1]
        current_swing_high = self.swing_high[-1]
        current_ema50 = self.ema50[-1]
        current_volume = self.data.Volume[-1]
        current_vol_ma = self.vol_ma[-1]

        # 🌙 Moon Dev: Strengthened volatility filter to require higher volatility (1.2x avg) for better setups
        vol_filter = current_atr > 1.2 * current_avg_atr
        # 🌙 Moon Dev: Tightened trend filter to ADX > 25 for stronger trends only
        trend_filter = current_adx > 25

        # Manage existing position
        if self.position:
            bars_held = len(self.data) - self.entry_bar
            if bars_held > self.max_bars_held:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars 🚀")
                return

            # 🌙 Moon Dev: Tightened trailing stop to 1*ATR for better risk management and locking profits sooner
            if self.is_long:
                trail_sl = current_close - 1 * current_atr
                self.stop_price = max(self.stop_price, trail_sl)
                if current_low <= self.stop_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Long SL Hit at {current_low}, Trail SL {self.stop_price} ✨")
                    return
                # 🌙 Moon Dev: Improved partial profit to 50% at 1:1 RR instead of BB/RSI for more precise scaling
                risk_distance = self.entry_price - self.stop_price  # Recalculate for accuracy
                partial_level = self.entry_price + risk_distance
                if current_close >= partial_level and not self.partial_taken:
                    partial_size = self.position.size * 0.5
                    self.sell(size=partial_size)
                    self.partial_taken = True
                    print(f"🌙 Moon Dev Partial Profit Long at {current_close} (1:1 RR) ✨")
                # 🌙 Moon Dev: Full TP at 3:1 RR for higher reward potential
                if self.partial_taken and current_close >= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Long at {current_close} 🚀")
                    return
            else:  # short
                trail_sl = current_close + 1 * current_atr
                self.stop_price = min(self.stop_price, trail_sl)
                if current_high >= self.stop_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Short SL Hit at {current_high}, Trail SL {self.stop_price} ✨")
                    return
                # Partial profit for short
                risk_distance = self.stop_price - self.entry_price
                partial_level = self.entry_price - risk_distance
                if current_close <= partial_level and not self.partial_taken:
                    partial_size = abs(self.position.size) * 0.5
                    self.buy(size=partial_size)
                    self.partial_taken = True
                    print(f"🌙 Moon Dev Partial Profit Short at {current_close} (1:1 RR) ✨")
                # Full TP for short
                if self.partial_taken and current_close <= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Short at {current_close} 🚀")
                    return
            return

        # No position, check entries
        if not vol_filter or not trend_filter:
            return

        # Long entry with tightened RSI (35/60 bounds) and added EMA/Volume filters for higher quality
        long_rsi_cross = current_rsi > 35 and prev_rsi <= 35 and current_rsi < 60
        long_bb_touch = current_low <= current_bb_lower
        long_macd_cross = current_macd > current_signal and prev_macd <= prev_signal
        long_hist_expand = current_hist > prev_hist and current_hist > 0
        long_ema_filter = current_close > current_ema50  # 🌙 Moon Dev: Only long above EMA50
        long_vol_filter = current_volume > current_vol_ma  # 🌙 Moon Dev: Volume confirmation
        if (
            long_rsi_cross
            and long_bb_touch
            and long_macd_cross
            and long_hist_expand
            and long_ema_filter
            and long_vol_filter
        ):
            if self.position and not self.is_long:
                self.position.close()
            stop_price = current_swing_low - 2 * current_atr
            risk_distance = current_close - stop_price
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(1, int(round(size)))  # 🌙 Moon Dev: Ensure min size 1 for viability
                self.buy(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                # 🌙 Moon Dev: Set TP to 3:1 RR for improved reward:risk
                self.tp_price = current_close + 3 * risk_distance
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = True
                print(
                    f"🌙 Moon Dev LONG Entry at {current_close}, Size: {size}, SL: {stop_price}, TP: {self.tp_price} 🚀"
                )

        # Short entry with tightened RSI (65/40 bounds, symmetric) and added EMA/Volume filters
        short_rsi_cross = current_rsi < 65 and prev_rsi >= 65 and current_rsi > 40
        short_bb_touch = current_high >= current_bb_upper
        short_macd_cross = current_macd < current_signal and prev_macd >= prev_signal
        short_hist_expand = current_hist < prev_hist and current_hist < 0
        short_ema_filter = current_close < current_ema50  # 🌙 Moon Dev: Only short below EMA50
        short_vol_filter = current_volume > current_vol_ma  # 🌙 Moon Dev: Volume confirmation
        if (
            short_rsi_cross
            and short_bb_touch
            and short_macd_cross
            and short_hist_expand
            and short_ema_filter
            and short_vol_filter
        ):
            if self.position and self.is_long:
                self.position.close()
            stop_price = current_swing_high + 2 * current_atr
            risk_distance = stop_price - current_close
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(1, int(round(size)))  # 🌙 Moon Dev: Ensure min size 1 for viability
                self.sell(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                # 🌙 Moon Dev: Set TP to 3:1 RR for improved reward:risk
                self.tp_price = current_close - 3 * risk_distance
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = False
                print(
                    f"🌙 Moon Dev SHORT Entry at {current_close}, Size: {size}, SL: {stop_price}, TP: {self.tp_price} 🚀"
                )


# Run backtest
bt = Backtest(data, SynergisticConfluence, cash=1000000, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
