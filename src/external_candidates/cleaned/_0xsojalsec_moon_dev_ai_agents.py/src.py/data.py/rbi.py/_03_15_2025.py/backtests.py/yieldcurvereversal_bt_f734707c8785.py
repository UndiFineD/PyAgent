# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\YieldCurveReversal_BT.py
# 🌙 Moon Dev's Yield Curve Reversal Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🚀 Data Preparation Rocket Launch 🚀
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# 🌌 Cosmic Data Cleaning 🌌
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


class YieldCurveReversal(Strategy):
    risk_pct = 0.02  # 🌑 2% Moon Dust Risk per Trade
    tp_pct = 0.05  # 🚀 5% Rocket Fuel Take Profit
    sl_pct = 0.02  # 🛡️ 2% Force Field Stop Loss

    def init(self):
        # 🌠 Cosmic Indicator Initialization 🌠
        self.vix_curve = self.I(lambda x: x, self.data.df["vix_futures_30d"], name="VIX_CURVE")
        self.treasury_3m = self.I(lambda x: x, self.data.df["treasury_3m"], name="TREASURY_3M")
        self.ma50 = self.I(talib.SMA, self.data.Close, 50, name="MA50")
        self.price = self.data.Close

        print("🌕 Lunar Indicators Activated: VIX Curve, Treasury Yield, MA50")

    def next(self):
        # 🌙 Moon Phase Check - Wait for full indicator formation 🌙
        if len(self.data.Close) < 50:
            return

        current_price = self.data.Close[-1]
        equity = self.equity
        position = self.position

        # 🌓 Cosmic Divergence Detection 🌓
        yield_spread = self.vix_curve[-1] - self.treasury_3m[-1]

        # 🚀 Long Entry: Negative Yield Spread 🌌
        if not position and yield_spread < 0:
            risk_amount = equity * self.risk_pct
            sl_price = current_price * (1 - self.sl_pct)
            risk_per_share = current_price - sl_price

            if risk_per_share > 0:
                position_size = risk_amount / risk_per_share
                position_size = int(round(position_size))

                if position_size > 0:
                    tp_price = current_price * (1 + self.tp_pct)
                    self.buy(size=position_size, sl=sl_price, tp=tp_price)
                    print(f"🌙✨🚀 MOON SHOT! Long Entry @ {current_price:.2f}")
                    print(f"   Size: {position_size} | SL: {sl_price:.2f} | TP: {tp_price:.2f}")

        # 🌗 Exit Signal: Price Descends Below MA50 🌘
        elif position and crossover(self.ma50, self.price):
            self.position.close()
            print(f"🌙☄️ COMET RETREAT! Exit @ {current_price:.2f}")


# 🌕 Launching Moon Base Backtest 🌕
bt = Backtest(data, YieldCurveReversal, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🌟 Cosmic Performance Report 🌟
print("\n🌌🌠🌑 MOON DEV FINAL REPORT 🌑🌠🌌")
print(stats)
print(stats._strategy)
