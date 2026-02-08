# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\VolSqueezeSurge_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean column names and drop unnamed columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Rename columns to match backtesting.py requirements
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "open_interest": "OpenInterest",  # Assuming exists in actual data
    },
    inplace=True,
)


class VolSqueezeSurge(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators
        self.middle_band = self.I(talib.SMA, self.data.Close, 20)
        self.stddev = self.I(talib.STDDEV, self.data.Close, 20)
        self.oi_ma = self.I(talib.SMA, self.data.OpenInterest, 960)  # 10-day MA (960 periods)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        # Track Bollinger Width history
        self.bb_widths = []

    def next(self):
        # Wait for sufficient data
        if len(self.data) < 960 or len(self.bb_widths) < 100:
            return

        # Calculate current Bollinger values
        upper = self.middle_band[-1] + 2 * self.stddev[-1]
        lower = self.middle_band[-1] - 2 * self.stddev[-1]
        current_bb_width = upper - lower
        self.bb_widths.append(current_bb_width)
        self.bb_widths = self.bb_widths[-100:]  # Keep rolling 100 periods

        # Calculate percentiles
        bb_p10 = np.percentile(self.bb_widths, 10)
        bb_p50 = np.percentile(self.bb_widths, 50)
        current_close = self.data.Close[-1]

        if not self.position:
            # Entry conditions 🌙
            oi_ma_value = self.oi_ma[-1]
            current_oi = self.data.OpenInterest[-1]

            if (
                current_bb_width < bb_p10
                and oi_ma_value > 0
                and (current_oi - oi_ma_value) / oi_ma_value > 0.2
                and lower < current_close < upper
            ):
                # Risk management ✨
                atr_value = self.atr[-1]
                stop_loss = current_close - 2 * atr_value
                risk_amount = self.equity * self.risk_percent
                position_size = int(round(risk_amount / (current_close - stop_loss)))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss)
                    print(
                        f"🌙 MOON DEV ENTRY 🚀 | Price: {current_close:.2f} | Size: {position_size} | SL: {stop_loss:.2f}"
                    )

        else:
            # Exit conditions 🌕
            price_range = self.data.High[-1] - self.data.Low[-1]
            volatility_exit = price_range > 1.5 * self.atr[-1]
            bb_exit = current_bb_width > bb_p50

            if volatility_exit or bb_exit:
                self.position.close()
                reason = "Volatility Expansion" if volatility_exit else "BB Width Expansion"
                print(f"🌕 MOON DEV EXIT 🛑 | Price: {current_close:.2f} | Reason: {reason}")


# Run backtest
bt = Backtest(data, VolSqueezeSurge, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
