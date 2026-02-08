# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\SynergisticConfluence_OPT_v3.py
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
    swing_period = 5  # 🌙 Moon Dev: Tightened swing period for more responsive stops
    avg_atr_period = 20
    ema_period = 50  # 🌙 Moon Dev: Added EMA50 for trend regime filter
    vol_sma_period = 20  # 🌙 Moon Dev: Added volume SMA for confirmation filter
    risk_per_trade = 0.015  # 🌙 Moon Dev: Increased risk per trade to 1.5% for higher exposure while managing drawdown
    max_bars_held = 30  # 🌙 Moon Dev: Extended hold time to allow more room for trends

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume

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
        self.vol_sma = self.I(
            talib.SMA, volume, timeperiod=self.vol_sma_period
        )  # 🌙 Moon Dev: Volume SMA for entry confirmation

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
        current_volume = self.data.Volume[-1]
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
        current_vol_sma = self.vol_sma[-1]

        # 🌙 Moon Dev: Enhanced volatility filter to allow slightly lower vol for more opportunities
        vol_filter = current_atr > 0.8 * current_avg_atr
        # 🌙 Moon Dev: Stronger trend filter for higher quality setups
        trend_filter = current_adx > 25
        # 🌙 Moon Dev: Volume filter for entry confirmation
        volume_filter = current_volume > 1.2 * current_vol_sma

        # Manage existing position
        if self.position:
            bars_held = len(self.data) - self.entry_bar
            if bars_held > self.max_bars_held:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars 🚀")
                return

            risk_distance = (
                abs(self.entry_price - self.stop_price) if self.entry_price != 0 else current_atr
            )  # Fallback for initial risk calc

            # Update trailing stop with tighter multiplier
            if self.is_long:
                trail_sl = current_close - 1.2 * current_atr  # 🌙 Moon Dev: Tighter trailing for better profit capture
                self.stop_price = max(self.stop_price, trail_sl)
                if current_low <= self.stop_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Long SL Hit at {current_low}, Trail SL {self.stop_price} ✨")
                    return
                # 🌙 Moon Dev: Improved partial at 1R, then move to breakeven + buffer
                partial_cond = current_close >= (self.entry_price + risk_distance)
                if partial_cond and not self.partial_taken:
                    partial_size = abs(self.position.size) * 0.5  # 🌙 Moon Dev: Fixed to 50% of current position size
                    self.sell(size=partial_size)
                    self.partial_taken = True
                    # Move stop to breakeven + small buffer
                    self.stop_price = max(self.stop_price, self.entry_price + 0.1 * current_atr)
                    print(f"🌙 Moon Dev Partial Profit Long at {current_close}, Size Closed: {partial_size} ✨")
                # 🌙 Moon Dev: Full TP at 3R after partial
                if self.partial_taken and current_close >= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Long at {current_close} 🚀")
                    return
            else:  # short
                trail_sl = current_close + 1.2 * current_atr  # 🌙 Moon Dev: Tighter trailing for better profit capture
                self.stop_price = min(self.stop_price, trail_sl)
                if current_high >= self.stop_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Short SL Hit at {current_high}, Trail SL {self.stop_price} ✨")
                    return
                # 🌙 Moon Dev: Improved partial at 1R, then move to breakeven + buffer
                partial_cond = current_close <= (self.entry_price - risk_distance)
                if partial_cond and not self.partial_taken:
                    partial_size = abs(self.position.size) * 0.5  # 🌙 Moon Dev: Fixed to 50% of current position size
                    self.buy(size=partial_size)
                    self.partial_taken = True
                    # Move stop to breakeven + small buffer
                    self.stop_price = min(self.stop_price, self.entry_price - 0.1 * current_atr)
                    print(f"🌙 Moon Dev Partial Profit Short at {current_close}, Size Covered: {partial_size} ✨")
                # 🌙 Moon Dev: Full TP at 3R after partial
                if self.partial_taken and current_close <= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Short at {current_close} 🚀")
                    return
            return

        # No position, check entries
        if not vol_filter or not trend_filter:
            return

        # Long entry with added EMA and volume filters, tightened RSI
        long_rsi_cross = (
            current_rsi > 30 and prev_rsi <= 30 and current_rsi < 50
        )  # 🌙 Moon Dev: Kept <50 to avoid overbought entries
        long_bb_touch = current_low <= current_bb_lower
        long_macd_cross = current_macd > current_signal and prev_macd <= prev_signal
        long_hist_expand = current_hist > prev_hist and current_hist > 0
        long_trend = current_close > current_ema50  # 🌙 Moon Dev: EMA50 trend filter for longs
        if long_rsi_cross and long_bb_touch and long_macd_cross and long_hist_expand and long_trend and volume_filter:
            if self.position and not self.is_long:
                self.position.close()
            stop_price = current_swing_low - 1.5 * current_atr  # 🌙 Moon Dev: Tighter initial stop for better R:R
            risk_distance = current_close - stop_price
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(1, int(round(size)))  # Ensure min size 1
                self.buy(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                self.tp_price = current_close + 3 * risk_distance  # 🌙 Moon Dev: Increased to 3R for higher returns
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = True
                print(
                    f"🌙 Moon Dev LONG Entry at {current_close}, Size: {size}, SL: {stop_price}, TP: {self.tp_price} 🚀"
                )

        # Short entry with added EMA and volume filters, tightened RSI
        short_rsi_cross = (
            current_rsi < 70 and prev_rsi >= 70 and current_rsi > 50
        )  # 🌙 Moon Dev: Kept >50 to avoid oversold entries
        short_bb_touch = current_high >= current_bb_upper
        short_macd_cross = current_macd < current_signal and prev_macd >= prev_signal
        short_hist_expand = current_hist < prev_hist and current_hist < 0
        short_trend = current_close < current_ema50  # 🌙 Moon Dev: EMA50 trend filter for shorts
        if (
            short_rsi_cross
            and short_bb_touch
            and short_macd_cross
            and short_hist_expand
            and short_trend
            and volume_filter
        ):
            if self.position and self.is_long:
                self.position.close()
            stop_price = current_swing_high + 1.5 * current_atr  # 🌙 Moon Dev: Tighter initial stop for better R:R
            risk_distance = stop_price - current_close
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(1, int(round(size)))  # Ensure min size 1
                self.sell(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                self.tp_price = current_close - 3 * risk_distance  # 🌙 Moon Dev: Increased to 3R for higher returns
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
