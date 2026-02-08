# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_10_2025\backtests\ForceSqueeze_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean data columns
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class ForceSqueeze(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators with TA-Lib
        self.efi = self.I(talib.FORCEINDEX, self.data.Close, self.data.Volume, 13, name="EFI 🌊")

        # Bollinger Bands components
        self.bb_upper = self.I(talib.BBANDS, self.data.Close, 20, 2, 2, 0, name="BB_UP", index=0)
        self.bb_mid = self.I(talib.BBANDS, self.data.Close, 20, 2, 2, 0, name="BB_MID", index=1)
        self.bb_lower = self.I(talib.BBANDS, self.data.Close, 20, 2, 2, 0, name="BB_LO", index=2)

        # Calculate BB width and SMA
        self.bb_width = self.I(
            lambda u, l, m: (u - l) / m,
            self.bb_upper,
            self.bb_lower,
            self.bb_mid,
            name="BB_WIDTH 📏",
        )
        self.bb_width_sma10 = self.I(talib.SMA, self.bb_width, 10, name="BB_WIDTH_SMA10 📈")

        self.stop_loss_level = None  # Trailing stop tracker

    def next(self):
        # Skip early bars without indicator values
        if len(self.efi) < 2 or len(self.bb_width) < 2:
            return

        current_efi = self.efi[-1]
        prev_efi = self.efi[-2]
        current_width = self.bb_width[-1]
        prev_width = self.bb_width[-2]
        width_sma = self.bb_width_sma10[-1]

        # Moon Dev Entry Logic 🚀
        if not self.position:
            if crossover(current_efi, 0) and (current_width < prev_width):
                entry_price = self.data.Close[-1]
                sl_price = self.bb_lower[-1]

                # Calculate position size
                risk_amount = self.equity * self.risk_percent
                risk_per_share = entry_price - sl_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=sl_price)
                        self.stop_loss_level = sl_price
                        print(
                            f"🚀 MOON DEV LONG ENTRY: {position_size} units at {entry_price:.2f} | SL: {sl_price:.2f}"
                        )

        # Moon Dev Exit Logic 🌙
        else:
            # Update trailing stop
            current_lower_bb = self.bb_lower[-1]
            self.stop_loss_level = max(self.stop_loss_level, current_lower_bb)

            # Check volatility expansion exit
            if current_width > width_sma:
                self.position.close()
                print(f"🌙 VOLATILITY EXPANSION EXIT | Width {current_width:.4f} > SMA {width_sma:.4f}")

            # Check trailing stop
            elif self.data.Low[-1] < self.stop_loss_level:
                self.position.close()
                print(f"✨ TRAILING STOP TRIGGERED | Exit at {self.stop_loss_level:.2f}")


# Execute backtest
bt = Backtest(data, ForceSqueeze, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
