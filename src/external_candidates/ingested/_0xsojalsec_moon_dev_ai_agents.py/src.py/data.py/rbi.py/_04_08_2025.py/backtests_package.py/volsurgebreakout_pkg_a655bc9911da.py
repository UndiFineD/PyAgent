# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests_package\VolSurgeBreakout_PKG.py
# Current celestial readings 🌠
price = self.data.Close[-1]
volume = self.data.Volume[-1]
volume_avg = self.volume_sma[-1]

# Cosmic volume surge validation (prevent division by zero)
volume_surge = (volume >= 1.5 * volume_avg) if volume_avg > 0 else False
