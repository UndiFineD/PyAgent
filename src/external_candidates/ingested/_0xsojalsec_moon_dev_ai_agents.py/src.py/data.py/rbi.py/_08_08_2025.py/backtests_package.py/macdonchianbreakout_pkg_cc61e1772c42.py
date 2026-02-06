# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\08_08_2025\backtests_package\MACDonchianBreakout_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class MACDonchianBreakout(Strategy):
    # Define strategy parameters
    donchian_length = 20
    atr_period = 14
    atr_multiplier = 2.0
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    buffer_k = 0.0
    confirm_window = 0

    def init(self):
        print(
            "🌙✨ Moon Dev Package AI: Initializing indicators without backtesting.lib... 🚫📦"
        )

        # Calculate Donchian channel using TA-Lib
        self.upper = self.I(talib.MAX, self.data.High, timeperiod=self.donchian_length)
        self.lower = self.I(talib.MIN, self.data.Low, timeperiod=self.donchian_length)

        # Calculate MACD histogram using TA-Lib
        self.macd_line, self.macd_signal_line, self.macd_hist = self.I(
            talib.MACD,
            self.data.Close,
            fastperiod=self.macd_fast,
            slowperiod=self.macd_slow,
            signalperiod=self.macd_signal,
        )

        # Calculate ATR using TA-Lib
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )

        print("🌙✨ Indicators ready: Donchian, MACD, ATR all set via TA-Lib! 📈")

    def next(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        # Crossovers without backtesting.lib
        price_crosses_above_upper = (
            close[-2] < self.upper[-2] and close[-1] > self.upper[-1]
        )
        price_crosses_below_lower = (
            close[-2] > self.lower[-2] and close[-1] < self.lower[-1]
        )

        macd_cross_up = self.macd_hist[-2] <= 0 and self.macd_hist[-1] > 0
        macd_cross_down = self.macd_hist[-2] >= 0 and self.macd_hist[-1] < 0

        if not self.position:
            # Long entry
            if price_crosses_above_upper and macd_cross_up:
                entry_price = close[-1]
                sl_price = entry_price - (self.atr[-1] * self.atr_multiplier)
                size = int(round(1000000 / entry_price))

                self.buy(size=size, sl=sl_price)
                print(
                    f"🌙 Long signal! Buying at {entry_price:.2f} with SL at {sl_price:.2f}. 🚀 [No backtesting.lib used]"
                )

            # Short entry
            elif price_crosses_below_lower and macd_cross_down:
                entry_price = close[-1]
                sl_price = entry_price + (self.atr[-1] * self.atr_multiplier)
                size = int(round(1000000 / entry_price))

                self.sell(size=size, sl=sl_price)
                print(
                    f"🌙 Short signal! Selling at {entry_price:.2f} with SL at {sl_price:.2f}. 🚀 [No backtesting.lib used]"
                )

        else:
            current_price = close[-1]
            # Use rolling Donchian levels as trailing references
            if self.position.is_long:
                trail_stop = self.upper[-1] - (self.atr[-1] * self.atr_multiplier)
                if current_price < trail_stop:
                    self.position.close()
                    print("🌙 Exiting long position due to trailing stop hit. 🌟")

            elif self.position.is_short:
                trail_stop = self.lower[-1] + (self.atr[-1] * self.atr_multiplier)
                if current_price > trail_stop:
                    self.position.close()
                    print("🌙 Exiting short position due to trailing stop hit. 🌟")


# Load data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=True,
    index_col=0,
)

# Backtest the strategy
bt = Backtest(data, MACDonchianBreakout, cash=1000000, trade_on_close=True)
stats = bt.run()
print(stats)
