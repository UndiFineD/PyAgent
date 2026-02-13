# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_17_2025\backtests\BandMACDRebound_BT.py
# 🌙 Moon Dev's BandMACD Rebound Backtest 🌕
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class BandMACDRebound(Strategy):
    risk_pct = 0.01  # 1% risk per trade 🌕
    bb_period = 20
    bb_dev = 2
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9

    def init(self):
        # 🌙 Calculate indicators using TA-Lib
        close = self.data.Close

        # Bollinger Bands ✨
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_dev,
            nbdevdn=self.bb_dev,
            name=["BB_Upper", "BB_Middle", "BB_Lower"],
        )

        # MACD Oscillator 🚀
        self.macd_line, self.macd_signal, self.macd_hist = self.I(
            talib.MACD,
            close,
            fastperiod=self.macd_fast,
            slowperiod=self.macd_slow,
            signalperiod=self.macd_signal,
            name=["MACD", "Signal", "Histogram"],
        )

    def next(self):
        current_close = self.data.Close[-1]
        current_lower = self.bb_lower[-1]
        macd_hist = self.macd_hist[-1]

        # 🌙 Entry Conditions Check
        if not self.position:
            # Price near lower BB & MACD conditions
            if (
                current_close <= current_lower * 1.02
                and macd_hist > 0
                and self.macd_line[-1] > self.macd_signal[-1]
            ):

                # Risk Management Calculations 🌕
                stop_loss = current_lower * 0.98
                risk_amount = self.equity * self.risk_pct
                price_diff = current_close - stop_loss

                if price_diff > 0:
                    position_size = risk_amount / price_diff
                    position_size = int(round(position_size))

                    if position_size > 0:
                        take_profit = self.bb_middle[-1]

                        # Moon Dev Debug Prints 🌙✨
                        print(f"\n🚀🌙 BUY SIGNAL @ {current_close:.2f}")
                        print(
                            f"BB Lower: {current_lower:.2f} | MACD Hist: {macd_hist:.2f}"
                        )
                        print(f"SL: {stop_loss:.2f} | TP: {take_profit:.2f}")
                        print(f"Position Size: {position_size} units 🌕")

                        self.buy(size=position_size, sl=stop_loss, tp=take_profit)


# 🌙 Data Preparation Ritual
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Cleanse column names ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Align with backtesting.py requirements 🌕
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date",
    },
    inplace=True,
)

data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)

# 🌙 Launch Backtest
bt = Backtest(data, BandMACDRebound, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Print Full Moon Stats
print("\n" + "=" * 50)
print("🌙✨ FINAL BACKTEST STATS 🚀🌕")
print("=" * 50 + "\n")
print(stats)
print("\n" + "=" * 50)
print("🌕 STRATEGY DETAIL ANALYSIS 🌙")
print("=" * 50 + "\n")
print(stats._strategy)
