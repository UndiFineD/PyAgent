# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests\VolatilityReversal_BT.py
# 🌙 Moon Dev's Volatility Reversal Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# ========================
# DATA PREPARATION
# ========================
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and prepare data
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


# ========================
# VOLATILITY REVERSAL STRATEGY
# ========================
class VolatilityReversal(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade
    swing_period = 20  # Swing low lookback

    def init(self):
        # 🌙 Core Indicators
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_period)

        print("🌙✨ Strategy Initialized with Moon Power! ✨")

    def next(self):
        current_close = self.data.Close[-1]
        current_adx = self.adx[-1]

        # ========================
        # ENTRY LOGIC
        # ========================
        if not self.position:
            # EMA crossover condition (Golden Cross)
            ema_crossover = crossover(self.ema50, self.ema200)

            # ADX filter for low volatility
            adx_filter = current_adx < 20

            if ema_crossover and adx_filter:
                # 🌙 Risk Management Calculations
                swing_low_price = self.swing_low[-1]
                risk_per_share = current_close - swing_low_price

                if risk_per_share > 0:  # Validate positive risk
                    equity = self._broker.equity
                    risk_amount = equity * self.risk_per_trade
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=swing_low_price)
                        print(
                            f"🌙✨ GOLDEN CROSS! Long @ {current_close:.2f} "
                            f"| Size: {position_size} ✨"
                            f" | Stop Loss: {swing_low_price:.2f}"
                        )

        # ========================
        # EXIT LOGIC
        # ========================
        else:
            # Exit when ADX shows strong trend
            if current_adx > 30:
                self.position.close()
                print(
                    f"🚀🌙 ADX BREAKOUT! Exit @ {current_close:.2f} "
                    f"| Profit: {self.position.pl_pct:.2f}%"
                )

            # Additional exit if price hits swing low (stop loss)
            # Handled automatically by backtesting.py's SL


# ========================
# BACKTEST EXECUTION
# ========================
bt = Backtest(data, VolatilityReversal, cash=1_000_000, exclusive_orders=True)

stats = bt.run()
print("\n🌕🌕🌕 FINAL MOON STATS 🌕🌕🌕")
print(stats)
print(stats._strategy)
print("Moon Dev Trading Complete! 🚀🌙")
