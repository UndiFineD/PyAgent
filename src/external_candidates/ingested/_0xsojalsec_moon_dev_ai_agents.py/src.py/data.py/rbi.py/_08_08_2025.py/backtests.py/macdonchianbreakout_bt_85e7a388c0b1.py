# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\08_08_2025\backtests\MACDonchianBreakout_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


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
        # Clean and format data
        self.data.columns = self.data.columns.str.strip().str.lower()
        self.data = self.data.drop(
            columns=[col for col in self.data.columns if "unnamed" in col.lower()]
        )
        self.data.columns = ["open", "high", "low", "close", "volume"]

        # Calculate Donchian channel
        self.upper = self.I(talib.MAX, self.data.high, self.donchian_length)
        self.lower = self.I(talib.MIN, self.data.low, self.donchian_length)

        # Calculate MACD histogram
        macd, macd_signal_line, macd_hist = self.I(
            talib.MACD,
            self.data.close,
            self.macd_fast,
            self.macd_slow,
            self.macd_signal,
        )
        self.macd_hist = macd_hist

        # Calculate ATR
        self.atr = self.I(
            talib.ATR, self.data.high, self.data.low, self.data.close, self.atr_period
        )

    def next(self):
        # Entry conditions
        if not self.position:
            # Long entry
            if (
                crossover(self.data.close, self.upper)
                and self.macd_hist > 0
                and self.macd_hist[-1] <= 0
            ):
                entry_price = self.data.close
                stop_loss = entry_price - (self.atr * self.atr_multiplier)

                self.position_size = int(round(1000000 / entry_price))
                self.buy(size=self.position_size, sl=stop_loss)
                print(
                    f"🌙 Long signal! Buying at {entry_price} with SL at {stop_loss}. 🚀"
                )

            # Short entry
            elif (
                crossover(self.lower, self.data.close)
                and self.macd_hist < 0
                and self.macd_hist[-1] >= 0
            ):
                entry_price = self.data.close
                stop_loss = entry_price + (self.atr * self.atr_multiplier)

                self.position_size = int(round(1000000 / entry_price))
                self.sell(size=self.position_size, sl=stop_loss)
                print(
                    f"🌙 Short signal! Selling at {entry_price} with SL at {stop_loss}. 🚀"
                )

        # Exit conditions using ATR trailing stop
        else:
            current_price = self.data.close
            # Long position exit
            if self.position.is_long:
                trail_stop = self.data.high.max() - (self.atr * self.atr_multiplier)
                if current_price < trail_stop:
                    self.position.close()
                    print("🌙 Exiting long position due to trailing stop hit. 🌟")

            # Short position exit
            elif self.position.is_short:
                trail_stop = self.data.low.min() + (self.atr * self.atr_multiplier)
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
