# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests_final\VolSurgeBreakout_BTFinal.py
# Lunar imports for celestial calculations 🌙
import numpy as np
from backtesting import Strategy


class VolSurgeBreakout(Strategy):
    def init(self):
        # Cosmic indicators initialization
        self.volume_sma = self.I(SMA, self.data.Volume, 20)
        self.bb_upper_2std = self.I(BollingerBands, self.data.Close, 20, 2, True)
        self.bb_lower_2std = self.I(BollingerBands, self.data.Close, 20, 2, False)
        self.bb_upper_1std = self.I(BollingerBands, self.data.Close, 20, 1, True)
        self.bb_lower_1std = self.I(BollingerBands, self.data.Close, 20, 1, False)

        print("🌌 Moon Dev Debug: Indicators initialized successfully!")

    def next(self):
        # Current celestial readings 🌠
        price = self.data.Close[-1]
        volume = self.data.Volume[-1]
        volume_avg = self.volume_sma[-1]

        # Cosmic volume surge validation (prevent division by zero)
        volume_surge = (volume >= 1.5 * volume_avg) if volume_avg > 0 else False

        # Lunar position sizing (2% of equity)
        position_size = 0.02  # Fixed as fraction for percentage-based sizing

        # Debug print for cosmic readings
        print(f"🌕 Moon Dev Debug: Price={price:.2f}, Volume={volume}, AvgVol={volume_avg:.2f}, Surge={volume_surge}")

        # Long entry conditions
        if price > self.bb_upper_2std[-1] and volume_surge and not self.position.is_long:
            print("🚀 Moon Dev Debug: Long entry signal detected!")
            self.buy(size=position_size)

        # Short entry conditions
        elif price < self.bb_lower_2std[-1] and volume_surge and not self.position.is_short:
            print("🌑 Moon Dev Debug: Short entry signal detected!")
            self.sell(size=position_size)

        # Long exit conditions
        elif self.position.is_long and price <= self.bb_upper_1std[-1]:
            print("🌓 Moon Dev Debug: Long exit signal detected!")
            self.position.close()

        # Short exit conditions
        elif self.position.is_short and price >= self.bb_lower_1std[-1]:
            print("🌗 Moon Dev Debug: Short exit signal detected!")
            self.position.close()
