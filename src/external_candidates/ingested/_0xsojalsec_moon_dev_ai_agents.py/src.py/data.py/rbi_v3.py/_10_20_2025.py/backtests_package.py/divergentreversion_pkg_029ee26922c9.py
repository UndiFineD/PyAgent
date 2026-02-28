# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_package\DivergentReversion_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"

data = pd.read_csv(path, parse_dates=["datetime"], index_col="datetime")
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


class DivergentReversion(Strategy):
    bb_period = 20
    bb_std = 2.0
    rsi_period = 14
    vol_period = 20
    vol_mult = 1.5
    atr_period = 14
    risk_pct = 0.01
    sl_mult = 1.5
    lookback_div = 5
    max_bars = 15

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
        self.entry_bar = None
        print("🌙 DivergentReversion Strategy Initialized ✨")

    def next(self):
        if (
            len(self.data)
            < max(self.bb_period, self.rsi_period, self.atr_period, self.lookback_div)
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
        prev_lows_slice = self.data.Low.iloc[start_idx:-1]
        if len(prev_lows_slice) > 0:
            prev_low_pos = prev_lows_slice.idxmin()
            prev_low_price = self.data.Low[prev_low_pos]
            prev_rsi = self.rsi[prev_low_pos]
            if low < prev_low_price and rsi_val > prev_rsi:
                bullish_div = True
                print(
                    f"🌙 Bullish DIVERGENCE confirmed: Low {low:.2f} < Prev {prev_low_price:.2f}, RSI {rsi_val:.2f} > {prev_rsi:.2f} ✨"
                )

        # Long Entry
        if close < lower and bullish_div and volume > self.vol_mult * v_sma:
            entry_price = close
            sl_price = lower - self.sl_mult * atr_val
            risk_dist = entry_price - sl_price
            if risk_dist > 0:
                size = int(round((self.risk_pct * self.equity) / risk_dist))
                if size > 0:
                    self.buy(size=size, sl=sl_price)
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙 LONG ENTRY SIGNAL: Price {entry_price:.2f}, Size {size}, SL {sl_price:.2f}, Risk {self.risk_pct*100}% 🚀"
                    )
                    return

        # Bearish Divergence Check
        bearish_div = False
        prev_highs_slice = self.data.High.iloc[start_idx:-1]
        if len(prev_highs_slice) > 0:
            prev_high_pos = prev_highs_slice.idxmax()
            prev_high_price = self.data.High[prev_high_pos]
            prev_rsi = self.rsi[prev_high_pos]
            if high > prev_high_price and rsi_val < prev_rsi:
                bearish_div = True
                print(
                    f"🌙 Bearish DIVERGENCE confirmed: High {high:.2f} > Prev {prev_high_price:.2f}, RSI {rsi_val:.2f} < {prev_rsi:.2f} ✨"
                )

        # Short Entry
        if close > upper and bearish_div and volume > self.vol_mult * v_sma:
            entry_price = close
            sl_price = upper + self.sl_mult * atr_val
            risk_dist = sl_price - entry_price
            if risk_dist > 0:
                size = int(round((self.risk_pct * self.equity) / risk_dist))
                if size > 0:
                    self.sell(size=size, sl=sl_price)
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙 SHORT ENTRY SIGNAL: Price {entry_price:.2f}, Size {size}, SL {sl_price:.2f}, Risk {self.risk_pct*100}% 🚀"
                    )
                    return


bt = Backtest(
    data, DivergentReversion, cash=1000000, commission=0.001, exclusive_orders=True
)
stats = bt.run()
print(stats)
