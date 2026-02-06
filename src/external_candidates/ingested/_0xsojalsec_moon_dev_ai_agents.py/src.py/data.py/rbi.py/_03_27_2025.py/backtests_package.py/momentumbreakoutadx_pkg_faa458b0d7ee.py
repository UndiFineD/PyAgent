# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_27_2025\backtests_package\MomentumBreakoutADX_PKG.py
# 🌙 Moon Dev Backtest Engine ✨
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🚀 Data Preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class MomentumBreakoutADX(Strategy):
    ema_period1 = 50
    ema_period2 = 200
    adx_period = 14
    atr_period = 14
    swing_window = 20

    def init(self):
        # 🌙 Core Indicators
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period1)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period2)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, self.adx_period
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )
        self.swing_high = self.I(
            talib.MAX, self.data.High, timeperiod=self.swing_window
        )
        self.atr_sma = self.I(talib.SMA, self.atr, timeperiod=20)

        self.entry_bar = None  # 📅 Track entry timing

    def next(self):
        price = self.data.Close[-1]

        # 🛑 Exit Conditions
        if self.position:
            # Emergency ADX exit
            if self.adx[-1] < 20:
                print(
                    f"🌙🚨 EMERGENCY EXIT! ADX {self.adx[-1]:.1f} < 20 at {price:.2f}"
                )
                self.position.close()

            # Time-based exit
            elif len(self.data) - self.entry_bar >= 5:
                print(f"⏳🕒 TIME EXIT! 5 bars passed at {price:.2f}")
                self.position.close()

        # 🚀 Entry Conditions
        else:
            if len(self.data) < 200:  # Ensure enough data
                return

            # Trend filter - Moon Dev crossover implementation 🌙✨
            ema_cross = (self.ema50[-2] < self.ema200[-2]) and (
                self.ema50[-1] > self.ema200[-1]
            )

            # Momentum confirmation
            adx_rising = self.adx[-1] > self.adx[-2]
            adx_strong = self.adx[-1] > 25

            # Volatility filter
            atr_vol = self.atr[-1] > 1.5 * self.atr_sma[-1]

            # Breakout trigger
            price_break = price > self.swing_high[-2]  # Confirm breakout

            # Volume confirmation
            vol_increase = self.data.Volume[-1] > self.data.Volume[-2]

            if all(
                [ema_cross, adx_rising, adx_strong, atr_vol, price_break, vol_increase]
            ):
                # 🎯 Risk Management
                risk_percent = 0.01  # 1% risk
                stop_loss = price - 2 * self.atr[-1]
                take_profit = price + 6 * self.atr[-1]

                risk_amount = self.equity * risk_percent
                risk_per_share = price - stop_loss
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    print(f"🚀🌙 BUY SIGNAL! Size: {position_size} @ {price:.2f}")
                    self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                    self.entry_bar = len(self.data)


# 🌙 Backtest Execution
bt = Backtest(data, MomentumBreakoutADX, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
