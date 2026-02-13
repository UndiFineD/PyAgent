# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\SynergisticConfluence_OPT_v4.py
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
    swing_period = (
        5  # 🌙 Moon Dev: Tightened swing period for more responsive stop placement
    )
    avg_atr_period = 20
    risk_per_trade = 0.015  # 🌙 Moon Dev: Increased risk per trade to 1.5% for higher potential returns while maintaining control
    max_bars_held = (
        30  # 🌙 Moon Dev: Extended hold time to allow more room for trends to develop
    )

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

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
        # 🌙 Moon Dev: Added volume SMA for confirmation filter to avoid low-volume fakeouts
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        # 🌙 Moon Dev: Added 200 EMA trend filter to align trades with the broader trend
        self.ema200 = self.I(talib.EMA, close, timeperiod=200)

        self.entry_price = 0
        self.stop_price = 0
        self.tp_price = 0
        self.risk_distance = (
            0  # 🌙 Moon Dev: Track risk distance for dynamic partial exits
        )
        self.partial_taken = False
        self.entry_bar = 0
        self.is_long = False

    def next(self):
        if (
            len(self.data) < 200
        ):  # 🌙 Moon Dev: Increased warmup for EMA200 to ensure reliable signals
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
        current_vol = self.data.Volume[
            -1
        ]  # 🌙 Moon Dev: Current volume for confirmation
        vol_confirm = (
            current_vol > self.vol_sma[-1]
        )  # 🌙 Moon Dev: Simple volume surge filter

        # 🌙 Moon Dev: Loosened volatility filter slightly to allow more trade opportunities in moderate volatility
        vol_filter = current_atr > 0.8 * current_avg_atr
        # 🌙 Moon Dev: Tightened ADX for stronger trend confirmation
        trend_filter = current_adx > 25

        # Manage existing position
        if self.position:
            bars_held = len(self.data) - self.entry_bar
            if bars_held > self.max_bars_held:
                self.position.close()
                print(f"🌙 Moon Dev Time Exit after {bars_held} bars 🚀")
                return

            # Update trailing stop (unchanged but now works with refined stops)
            if self.is_long:
                trail_sl = current_close - 1.5 * current_atr
                self.stop_price = max(self.stop_price, trail_sl)
                if current_low <= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Long SL Hit at {current_low}, Trail SL {self.stop_price} ✨"
                    )
                    return
            else:  # short
                trail_sl = current_close + 1.5 * current_atr
                self.stop_price = min(self.stop_price, trail_sl)
                if current_high >= self.stop_price:
                    self.position.close()
                    print(
                        f"🌙 Moon Dev Short SL Hit at {current_high}, Trail SL {self.stop_price} ✨"
                    )
                    return

            # 🌙 Moon Dev: Always check full TP regardless of partial (fixed bug where TP was only after partial)
            if self.is_long:
                if current_close >= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Long at {current_close} 🚀")
                    return
            else:
                if current_close <= self.tp_price:
                    self.position.close()
                    print(f"🌙 Moon Dev Full TP Short at {current_close} 🚀")
                    return

            # 🌙 Moon Dev: Improved partial profit to 50% at 1:1 RR (price-based, not indicator reversal) for better scaling
            if not self.partial_taken:
                if self.is_long:
                    partial_level = self.entry_price + self.risk_distance
                    if current_close >= partial_level:
                        self.sell(
                            size=self.position.size * 0.5
                        )  # 🌙 Moon Dev: Fixed to close half the actual position size
                        self.partial_taken = True
                        print(
                            f"🌙 Moon Dev Partial TP Long at {current_close} (1:1 RR) ✨"
                        )
                else:
                    partial_level = self.entry_price - self.risk_distance
                    if current_close <= partial_level:
                        self.buy(
                            size=abs(self.position.size) * 0.5
                        )  # 🌙 Moon Dev: Fixed to cover half the actual position size
                        self.partial_taken = True
                        print(
                            f"🌙 Moon Dev Partial TP Short at {current_close} (1:1 RR) ✨"
                        )
            return

        # No position, check entries
        if not vol_filter or not trend_filter:
            return

        # Long entry
        long_rsi_cross = (
            current_rsi > 30 and prev_rsi <= 30
        )  # 🌙 Moon Dev: Simplified RSI cross, removed <50 cap for more opportunities
        long_bb_touch = current_low <= current_bb_lower
        long_macd_cross = current_macd > current_signal and prev_macd <= prev_signal
        long_hist_expand = current_hist > prev_hist and current_hist > 0
        long_trend = (
            current_close > self.ema200[-1]
        )  # 🌙 Moon Dev: Added EMA200 trend filter for longs
        if (
            long_rsi_cross
            and long_bb_touch
            and long_macd_cross
            and long_hist_expand
            and vol_confirm
            and long_trend
        ):
            if self.position and not self.is_long:
                self.position.close()
            stop_price = current_swing_low - 2 * current_atr
            risk_distance = current_close - stop_price
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = int(round(size))
                self.buy(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                # 🌙 Moon Dev: Improved RR to 3:1 for higher reward potential
                self.tp_price = current_close + 3 * risk_distance
                self.risk_distance = risk_distance
                self.partial_taken = False
                self.entry_bar = len(self.data)
                self.is_long = True
                print(
                    f"🌙 Moon Dev LONG Entry at {current_close}, Size: {size}, SL: {stop_price}, TP: {self.tp_price} 🚀"
                )

        # Short entry
        short_rsi_cross = (
            current_rsi < 70 and prev_rsi >= 70
        )  # 🌙 Moon Dev: Simplified RSI cross, removed >50 cap for more opportunities
        short_bb_touch = current_high >= current_bb_upper
        short_macd_cross = current_macd < current_signal and prev_macd >= prev_signal
        short_hist_expand = current_hist < prev_hist and current_hist < 0
        short_trend = (
            current_close < self.ema200[-1]
        )  # 🌙 Moon Dev: Added EMA200 trend filter for shorts
        if (
            short_rsi_cross
            and short_bb_touch
            and short_macd_cross
            and short_hist_expand
            and vol_confirm
            and short_trend
        ):
            if self.position and self.is_long:
                self.position.close()
            stop_price = current_swing_high + 2 * current_atr
            risk_distance = stop_price - current_close
            if risk_distance > 0:
                risk_amount = self.equity * self.risk_per_trade
                size = risk_amount / risk_distance
                size = int(round(size))
                self.sell(size=size)
                self.entry_price = current_close
                self.stop_price = stop_price
                # 🌙 Moon Dev: Improved RR to 3:1 for higher reward potential
                self.tp_price = current_close - 3 * risk_distance
                self.risk_distance = risk_distance
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
