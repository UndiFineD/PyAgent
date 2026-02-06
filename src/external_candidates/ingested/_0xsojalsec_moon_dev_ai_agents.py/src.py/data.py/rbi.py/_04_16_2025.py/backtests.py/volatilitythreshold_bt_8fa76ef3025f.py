# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_16_2025\backtests\VolatilityThreshold_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolatilityThreshold(Strategy):
    def init(self):
        # Calculate required indicators
        self.atr_20 = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=20,
            name="ATR_20",
        )
        self.sma_200 = self.I(
            talib.SMA, self.data.Close, timeperiod=200, name="SMA_200"
        )
        self.high_5 = self.I(
            talib.MAX, self.data.High, timeperiod=480, name="High_5"
        )  # 5 days in 15m intervals

        # Calculate ATR 10th percentile with 1-year lookback
        lookback = 35040  # 1 year in 15m periods (365 days * 24h * 4)
        self.atr_10th = self.I(
            lambda x: x.rolling(lookback).quantile(0.1), self.atr_20, name="ATR_10th"
        )

    def next(self):
        # Moon-themed progress updates
        if len(self.data) % 1000 == 0:
            print(
                f"🌙 Processing bar {len(self.data)}/{len(self.data.df)} - Moon Dev tracking progress ✨"
            )

        # Skip early when indicators are not ready
        if len(self.data) < 200 or len(self.atr_10th) < 1:
            return

        current_close = self.data.Close[-1]
        current_atr = self.atr_20[-1]
        atr_threshold = self.atr_10th[-1]
        sma_200 = self.sma_200[-1]

        # Entry conditions
        if not self.position:
            if current_atr < atr_threshold and current_close > sma_200:
                # Calculate position size with 1% risk
                risk_amount = self.equity * 0.01
                stop_distance = 2 * current_atr

                if stop_distance <= 0:
                    print("⚠️ Moon Alert: Zero stop distance! Aborting launch 🚫")
                    return

                position_size = int(round(risk_amount / stop_distance))
                if position_size <= 0:
                    print(f"⚠️ Moon Alert: Invalid size {position_size} ✨")
                    return

                # Execute trade with stop loss
                entry_price = self.data.Open[-1]
                stop_price = entry_price - stop_distance
                self.buy(size=position_size, sl=stop_price)
                print(
                    f"🚀🌕 Moon Dev Launch! LONG {position_size} @ {entry_price} | SL {stop_price} 🌌"
                )

        # Exit conditions
        else:
            # Take profit at 5-day high
            if current_close > self.high_5[-1]:
                self.sell()
                print(f"🎯 Profit captured! Closing @ {current_close} 💰")


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and format data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

# Execute backtest
bt = Backtest(data, VolatilityThreshold, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
