# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\SynergisticConfluence_OPT_v7.py
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
    risk_per_trade = 0.015  # 🌙 Moon Dev: Increased to 1.5% for higher exposure while maintaining risk control
    max_bars_held = (
        30  # 🌙 Moon Dev: Extended hold time to allow more room for trends to develop
    )
    ema_period = 50  # New parameter for trend filter

    def reset_trade_vars(self):
        # 🌙 Moon Dev: Helper to reset trade state after exits
        self.entry_price = 0
        self.stop_price = 0
        self.tp_price = 0
        self.rr1_price = 0
        self.partial_taken = False
        self.entry_bar = 0
        self.is_long = False

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume  # 🌙 Moon Dev: Access volume for new filter

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
        # 🌙 Moon Dev: Added EMA for trend filter and volume MA for confirmation to improve entry quality
        self.ema50 = self.I(talib.EMA, close, timeperiod=self.ema_period)
        self.vol_ma = self.I(talib.SMA, volume, timeperiod=20)

        self.reset_trade_vars()  # Initialize vars to zero/false

    def next(self):
        if len(self.data) < 200:  # 🌙 Moon Dev: Increased warmup for new EMA indicator
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
        current_atr = self.atr[-1]
        current_adx = self.adx[-1]
        current_avg_atr = self.avg_atr[-1]
        current_swing_low = self.swing_low[-1]
        current_swing_high = self.swing_high[-1]
        current_ema50 = self.ema50[-1]
        current_volume = self.data.Volume[-1]
        current_vol_ma = self.vol_ma[-1]

        # 🌙 Moon Dev: Tightened filters for better regime selection - higher ADX threshold and volatility multiple
        vol_filter = current_atr > 1.2 * current_avg_atr
        trend_filter = current_adx > 25

        # Manage existing position
        if self.position:
            bars_held = len(self.data) - self.entry_bar
            if bars_held > self.max_bars_held:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars 🚀")
                self.reset_trade_vars()
                return

            # Update trailing stop
            if self.is_long:
                trail_sl = current_close - 1.5 * current_atr
                self.stop_price = max(self.stop_price, trail_sl)
                if current_low <= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long SL Hit at {current_low}, Trail SL {self.stop_price} ✨"
                    )
                    self.reset_trade_vars()
                    return
            else:  # short
                trail_sl = current_close + 1.5 * current_atr
                self.stop_price = min(self.stop_price, trail_sl)
                if current_high >= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Short SL Hit at {current_high}, Trail SL {self.stop_price} ✨"
                    )
                    self.reset_trade_vars()
                    return

            # 🌙 Moon Dev: Price-based partial at 1R for better profit locking, regardless of other indicators
            partial_cond = (self.is_long and current_close >= self.rr1_price) or (
                not self.is_long and current_close <= self.rr1_price
            )
            if partial_cond and not self.partial_taken:
                partial_size = abs(self.position.size) * 0.5
                if self.is_long:
                    self.sell(size=partial_size)
                    print(f"🌙 Moon Dev Partial Profit Long at {current_close} (1R) ✨")
                else:
                    self.buy(size=partial_size)
                    print(
                        f"🌙 Moon Dev Partial Profit Short at {current_close} (1R) ✨"
                    )
                self.partial_taken = True

            # 🌙 Moon Dev: Full TP at 3R, now checks regardless of partial to ensure exit on target (improved RR)
            tp_cond = (self.is_long and current_close >= self.tp_price) or (
                not self.is_long and current_close <= self.tp_price
            )
            if tp_cond:
                self.position.close()
                dir_str = "Long" if self.is_long else "Short"
                print(f"🌙 Moon Dev Full TP {dir_str} at {current_close} (3R) 🚀")
                self.reset_trade_vars()
                return
            return

        # No position, check entries
        if not vol_filter or not trend_filter:
            return

        # Long entry
        long_rsi_cross = current_rsi > 30 and prev_rsi <= 30 and current_rsi < 50
        long_bb_touch = current_low <= current_bb_lower
        long_macd_cross = current_macd > current_signal and prev_macd <= prev_signal
        long_hist_expand = current_hist > prev_hist and current_hist > 0
        # 🌙 Moon Dev: Added EMA trend and volume filters to avoid counter-trend/low-conviction entries
        long_trend_ok = current_close > current_ema50
        long_vol_ok = current_volume > current_vol_ma
        if (
            long_rsi_cross
            and long_bb_touch
            and long_macd_cross
            and long_hist_expand
            and long_trend_ok
            and long_vol_ok
        ):
            if self.position and not self.is_long:
                self.position.close()
                self.reset_trade_vars()
            stop_price = current_swing_low - 2 * current_atr
            risk_distance = current_close - stop_price
            if risk_distance <= 0:
                return
            risk_amount = self.equity * self.risk_per_trade
            size = risk_amount / risk_distance
            # 🌙 Moon Dev: Cap size to available cash to prevent over-leveraging; use float for precision
            size = min(size, self.broker.getcash() / current_close * 0.95)
            if size <= 0:
                return
            self.buy(size=size)
            self.entry_price = current_close
            self.stop_price = stop_price
            self.tp_price = (
                current_close + 3 * risk_distance
            )  # 🌙 Moon Dev: Increased to 3R for higher reward potential
            self.rr1_price = current_close + risk_distance  # For partial at 1R
            self.partial_taken = False
            self.entry_bar = len(self.data)
            self.is_long = True
            print(
                f"🌙 Moon Dev LONG Entry at {current_close}, Size: {size}, SL: {stop_price}, TP: {self.tp_price} 🚀"
            )

        # Short entry
        short_rsi_cross = current_rsi < 70 and prev_rsi >= 70 and current_rsi > 50
        short_bb_touch = current_high >= current_bb_upper
        short_macd_cross = current_macd < current_signal and prev_macd >= prev_signal
        short_hist_expand = current_hist < prev_hist and current_hist < 0
        # 🌙 Moon Dev: Added EMA trend and volume filters to avoid counter-trend/low-conviction entries
        short_trend_ok = current_close < current_ema50
        short_vol_ok = current_volume > current_vol_ma
        if (
            short_rsi_cross
            and short_bb_touch
            and short_macd_cross
            and short_hist_expand
            and short_trend_ok
            and short_vol_ok
        ):
            if self.position and self.is_long:
                self.position.close()
                self.reset_trade_vars()
            stop_price = current_swing_high + 2 * current_atr
            risk_distance = stop_price - current_close
            if risk_distance <= 0:
                return
            risk_amount = self.equity * self.risk_per_trade
            size = risk_amount / risk_distance
            # 🌙 Moon Dev: Cap size to available cash to prevent over-leveraging; use float for precision
            size = min(size, self.broker.getcash() / current_close * 0.95)
            if size <= 0:
                return
            self.sell(size=size)
            self.entry_price = current_close
            self.stop_price = stop_price
            self.tp_price = (
                current_close - 3 * risk_distance
            )  # 🌙 Moon Dev: Increased to 3R for higher reward potential
            self.rr1_price = current_close - risk_distance  # For partial at 1R
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
