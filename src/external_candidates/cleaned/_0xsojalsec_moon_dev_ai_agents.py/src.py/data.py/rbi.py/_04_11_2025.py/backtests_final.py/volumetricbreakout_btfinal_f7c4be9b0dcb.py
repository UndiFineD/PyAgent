# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_11_2025\backtests_final\VolumetricBreakout_BTFinal.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolumetricBreakout(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Calculate indicators using TA-Lib through self.I()
        self.upper, self.middle, self.lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.volume_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        print("✨ MOON INDICATORS INITIALIZED: BBANDS(20,2), SMA(20), RSI(14), ATR(14) ✨")

    def next(self):
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]
        price = current_close

        # Entry Conditions 🌙🚀
        if not self.position and current_close > self.upper[-1] and current_volume > 2 * self.volume_ma[-1]:
            # Risk management calculations
            atr_value = self.atr[-1]
            stop_loss_price = max(0, price - 2 * atr_value)  # Ensure SL doesn't go negative
            risk_amount = self.risk_per_trade * self.equity
            risk_per_unit = price - stop_loss_price

            if risk_per_unit > 0:  # Prevent division by zero
                position_size = round(risk_amount / risk_per_unit)
                position_size = int(min(position_size, self.equity // price))  # Convert to whole units

                print(f"🌙 MOON SIGNAL: BUY TRIGGERED! Size: {position_size} units @ {price:.2f}")
                print(f"🚀 RISK MANAGEMENT: SL={stop_loss_price:.2f}, RSI={self.rsi[-1]:.2f}")

                self.buy(size=position_size, sl=stop_loss_price)

        # Exit Conditions 🌙💤
        if self.position:
            if self.rsi[-2] > 70 and self.rsi[-1] <= 70:
                print(f"💤 MOON EXIT: RSI CROSS BELOW 70 @ {self.data.Close[-1]:.2f}")
                self.position.close()


# Data preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
try:
    data = pd.read_csv(data_path, parse_dates=["datetime"])
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col], errors="ignore")
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    ).set_index("datetime")

    print("🌕 MOON DATA LOADED SUCCESSFULLY!")
    print(f"📅 Date Range: {data.index[0]} to {data.index[-1]}")
    print(f"📊 Columns: {', '.join(data.columns)}")

except Exception as e:
    print(f"🌑 MOON ERROR: Failed to load data - {str(e)}")
    raise

# Run backtest
if not data.empty:
    bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
    stats = bt.run()
    print("\n🌙✨ MOON DEV BACKTEST COMPLETE! FULL STATS BELOW ✨🌙")
    print(stats)
    print(stats._strategy)
else:
    print("🌑 MOON ERROR: No data available for backtesting")
