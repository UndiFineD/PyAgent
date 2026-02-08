# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_31_2025\backtests_final\VolatilityThreshold_BTFinal.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolatilityThreshold(Strategy):
    risk_percentage = 0.01  # 1% risk per trade
    trailing_atr_multiplier = 2
    exit_bars = 480  # 5 days in 15m intervals (4*24*5=480)

    def init(self):
        # Clean data and calculate indicators
        self.atr_values = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20, name="ATR_20")

        # Calculate 10th percentile using pandas rolling quantile
        atr_series = pd.Series(self.atr_values)
        self.atr_percentile = self.I(lambda: atr_series.rolling(200).quantile(0.10).values, name="ATR_PCTL")

        self.sma200 = self.I(talib.SMA, self.data.Close, 200, name="SMA_200")

        self.entry_bar = 0
        self.trailing_stop = 0

    def next(self):
        if not self.position:
            current_atr = self.atr_values[-1]
            current_pctl = self.atr_percentile[-1]
            price_above_sma = self.data.Close[-1] > self.sma200[-1]

            if current_atr < current_pctl and price_above_sma:
                risk_amount = self.equity * self.risk_percentage
                stop_loss = self.data.Close[-1] - (self.trailing_atr_multiplier * current_atr)
                risk_per_unit = abs(self.data.Close[-1] - stop_loss)

                if risk_per_unit == 0:
                    print("🌑 Moon Dev Alert: Zero risk detected! Skipping entry")
                    return

                position_size = int(round(risk_amount / risk_per_unit))
                if position_size == 0:
                    print(f"🌑 Moon Dev Alert: {risk_amount:.2f} risk too small for position")
                    return

                self.buy(size=position_size, sl=stop_loss)
                self.entry_bar = len(self.data)
                self.trailing_stop = stop_loss
                print(f"🚀 Moon Dev LONG Entry: {self.data.Close[-1]:.2f}, Size: {position_size}")
        else:
            # Update trailing stop
            new_stop = self.data.High[-1] - (self.trailing_atr_multiplier * self.atr_values[-1])
            self.trailing_stop = max(self.trailing_stop, new_stop)
            self.position.sl = self.trailing_stop

            # Check exit conditions
            bars_in_trade = len(self.data) - self.entry_bar
            if bars_in_trade >= self.exit_bars or self.data.Close[-1] < self.trailing_stop:
                self.position.close()
                print(
                    f"🔻 Moon Dev Exit: {'Time' if bars_in_trade >= self.exit_bars else 'Stop'} | Price: {self.data.Close[-1]:.2f}"
                )


# Data handling
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
data.columns = [col.strip().lower() for col in data.columns]
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

# Run backtest
bt = Backtest(data, VolatilityThreshold, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕 Moon Dev Backtest Complete! 🌕")
print("=" * 40)
print(stats)
print("\n✨ Strategy Details:")
print(stats._strategy)
