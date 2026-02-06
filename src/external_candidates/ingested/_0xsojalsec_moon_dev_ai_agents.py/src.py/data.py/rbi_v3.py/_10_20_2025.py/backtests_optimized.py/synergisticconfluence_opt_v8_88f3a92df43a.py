# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\SynergisticConfluence_OPT_v8.py
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
    rsi_period = 9  # 🌙 Moon Dev: Reduced RSI period for faster, more responsive signals to catch trends earlier
    bb_period = 20
    bb_std = 2
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    swing_period = 10
    avg_atr_period = 20
    ema_period = 200  # 🌙 Moon Dev: Added 200 EMA for trend filter to only trade in direction of major trend
    vol_sma_period = 20  # 🌙 Moon Dev: Added volume SMA for volume confirmation filter
    risk_per_trade = 0.02  # 🌙 Moon Dev: Increased risk per trade to 2% for higher potential returns while still managing risk
    max_bars_held = 50  # 🌙 Moon Dev: Extended max hold time to allow more room for trends to develop

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low
        volume = self.data.Volume  # 🌙 Moon Dev: Use volume for additional filter

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
        self.ema200 = self.I(
            talib.EMA, close, timeperiod=self.ema_period
        )  # 🌙 Moon Dev: EMA trend filter
        self.vol_sma = self.I(
            talib.SMA, volume, timeperiod=self.vol_sma_period
        )  # 🌙 Moon Dev: Volume filter

        self.entry_price = 0
        self.stop_price = 0
        self.tp_price = 0
        self.partial_tp_price = (
            0  # 🌙 Moon Dev: Added partial TP level for scaling out at 1.5:1 RR
        )
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
        current_ema = self.ema200[-1]
        current_vol = self.data.Volume[-1]
        current_vol_sma = self.vol_sma[-1]

        # Enhanced filters: Volatility, trend strength, volume, and EMA trend direction
        vol_filter = (
            current_atr > current_avg_atr and current_vol > current_vol_sma
        )  # 🌙 Moon Dev: Added volume > SMA for higher conviction entries
        trend_filter = (
            current_adx > 25
        )  # 🌙 Moon Dev: Tightened ADX threshold to 25 for stronger trends only
        ema_long_filter = (
            current_close > current_ema
        )  # 🌙 Moon Dev: Longs only above EMA200
        ema_short_filter = (
            current_close < current_ema
        )  # 🌙 Moon Dev: Shorts only below EMA200

        # Manage existing position
        if self.position:
            bars_held = len(self.data) - self.entry_bar
            if bars_held > self.max_bars_held:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars 🚀")
                return

            # Update trailing stop with wider buffer for better trend riding
            if self.is_long:
                trail_sl = (
                    current_close - 2 * current_atr
                )  # 🌙 Moon Dev: Increased trailing multiplier to 2x ATR for less whipsaw
                self.stop_price = max(self.stop_price, trail_sl)
                if current_low <= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long SL Hit at {current_low}, Trail SL {self.stop_price} ✨"
                    )
                    return
                # Partial profit at 1.5:1 RR
                if not self.partial_taken and current_close >= self.partial_tp_price:
                    self.sell(size=0.5)
                    self.partial_taken = True
                    print(
                        f"🌙 Moon Dev Partial Profit Long at {current_close} (1.5:1) ✨"
                    )
                # Full TP at 3:1 RR after partial
                if self.partial_taken and current_close >= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Long at {current_close} (3:1) 🚀")
                    return
            else:  # short
                trail_sl = (
                    current_close + 2 * current_atr
                )  # 🌙 Moon Dev: Increased trailing multiplier to 2x ATR
                self.stop_price = min(self.stop_price, trail_sl)
                if current_high >= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Short SL Hit at {current_high}, Trail SL {self.stop_price} ✨"
                    )
                    return
                # Partial profit at 1.5:1 RR
                if not self.partial_taken and current_close <= self.partial_tp_price:
                    self.buy(size=0.5)  # Buy to cover partial
                    self.partial_taken = True
                    print(
                        f"🌙 Moon Dev Partial Profit Short at {current_close} (1.5:1) ✨"
                    )
                # Full TP at 3:1 RR
                if self.partial_taken and current_close <= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Short at {current_close} (3:1) 🚀")
                    return
            return

        # No position, check entries with enhanced filters
        if not vol_filter or not trend_filter:
            return

        # Long entry with EMA filter
        long_rsi_cross = current_rsi > 30 and prev_rsi <= 30 and current_rsi < 50
        long_bb_touch = current_low <= current_bb_lower
        long_macd_cross = current_macd > current_signal and prev_macd <= prev_signal
        long_hist_expand = current_hist > prev_hist and current_hist > 0
        if (
            long_rsi_cross
            and long_bb_touch
            and long_macd_cross
            and long_hist_expand
            and ema_long_filter
        ):
            if self.position and not self.is_long:
                self.position.close()
            stop_price = (
                current_swing_low - 1.5 * current_atr
            )  # 🌙 Moon Dev: Tightened initial SL to 1.5x ATR beyond swing for better risk/reward
            risk_distance = current_close - stop_price
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(
                    1, int(round(size))
                )  # 🌙 Moon Dev: Ensure min size 1, but allow fractional if needed
                self.buy(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                self.tp_price = (
                    current_close + 3 * risk_distance
                )  # 🌙 Moon Dev: Improved to 3:1 RR for higher returns
                self.partial_tp_price = (
                    current_close + 1.5 * risk_distance
                )  # 🌙 Moon Dev: Partial at 1.5:1 to scale out profits
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = True
                print(
                    f"🌙 Moon Dev LONG Entry at {current_close}, Size: {size}, SL: {stop_price}, Partial TP: {self.partial_tp_price}, Full TP: {self.tp_price} 🚀"
                )

        # Short entry with EMA filter
        short_rsi_cross = current_rsi < 70 and prev_rsi >= 70 and current_rsi > 50
        short_bb_touch = current_high >= current_bb_upper
        short_macd_cross = current_macd < current_signal and prev_macd >= prev_signal
        short_hist_expand = current_hist < prev_hist and current_hist < 0
        if (
            short_rsi_cross
            and short_bb_touch
            and short_macd_cross
            and short_hist_expand
            and ema_short_filter
        ):
            if self.position and self.is_long:
                self.position.close()
            stop_price = (
                current_swing_high + 1.5 * current_atr
            )  # 🌙 Moon Dev: Tightened initial SL to 1.5x ATR beyond swing
            risk_distance = stop_price - current_close
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = max(1, int(round(size)))
                self.sell(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                self.tp_price = (
                    current_close - 3 * risk_distance
                )  # 🌙 Moon Dev: Improved to 3:1 RR
                self.partial_tp_price = (
                    current_close - 1.5 * risk_distance
                )  # 🌙 Moon Dev: Partial at 1.5:1
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = False
                print(
                    f"🌙 Moon Dev SHORT Entry at {current_close}, Size: {size}, SL: {stop_price}, Partial TP: {self.partial_tp_price}, Full TP: {self.tp_price} 🚀"
                )


# Run backtest
bt = Backtest(data, SynergisticConfluence, cash=1000000, commission=0.001)
stats = bt.run()
print(stats)
print(stats._strategy)
