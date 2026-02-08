# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests_package\VolTerminus_PKG.py
# 🌙 Moon Dev Backtest AI Implementation for VolTerminus Strategy 🚀
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class VolTerminus(Strategy):
    # Strategy Parameters ✨
    bb_period = 20
    bb_std = 2
    bbw_percentile_window = 252
    bbw_threshold = 0.10  # 10th percentile
    hv_window = 10
    z_score_window = 252
    risk_pct = 0.05
    stop_loss_pct = 0.15

    def init(self):
        # Clean data columns 🌙
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()

        # VIX Term Structure Inversion Check 🔄
        self.vix_front = self.I(lambda: self.data.df["vix_front"])
        self.vix_back = self.I(lambda: self.data.df["vix_back"])
        self.vix_inversion = self.I(lambda: self.vix_front > self.vix_back)

        # Bollinger Bandwidth Calculation 📊
        upper, mid, lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_std,
            nbdevdn=self.bb_std,
        )
        self.bbw = self.I(lambda: (upper - lower) / mid)
        self.bbw_percentile = self.I(lambda: self.bbw.rolling(self.bbw_percentile_window).quantile(self.bbw_threshold))

        # Volatility Spread Analysis 🌪️
        self.hv = self.I(ta.historical_volatility, self.data.Close, self.hv_window)
        self.spread = self.I(lambda: self.hv - self.vix_front)
        spread_mean = self.I(lambda: self.spread.rolling(self.z_score_window).mean())
        spread_std = self.I(lambda: self.spread.rolling(self.z_score_window).std())
        self.z_score = self.I(lambda: (self.spread - spread_mean) / spread_std)

        print("🌙 Moon Dev Indicators Activated! Ready for Launch! 🚀")

    def next(self):
        price = self.data.Close[-1]

        # Entry Logic 🌙➡️🚀
        if not self.position:
            if self.vix_inversion[-1] and self.bbw[-1] < self.bbw_percentile[-1]:
                # Risk Management Calculations 🔒
                equity = self.equity
                position_size = (equity * self.risk_pct) / price
                position_size = int(round(position_size))

                if position_size > 0:
                    stop_price = price * (1 - self.stop_loss_pct)
                    self.buy(size=position_size, sl=stop_price)
                    print(f"🚀 MOON SHOT! Long {position_size} units @ {price:.2f} | Stop {stop_price:.2f} 🌙")

        # Exit Logic 🚀➡️🌑
        else:
            if self.z_score[-1] >= 2:
                self.position.close()
                print(f"🌑 VOL EXPANSION COMPLETE! Closing @ {price:.2f} | Profit: {self.position.pl_usd:.2f} ✨")


# Data Preparation Pipeline 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean and Validate Data 🔍
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
required_cols = ["open", "high", "low", "close", "volume", "vix_front", "vix_back"]
data = data[required_cols].rename(columns=lambda x: x.capitalize())
data.columns = ["Open", "High", "Low", "Close", "Volume", "VIX_Front", "VIX_Back"]
data.set_index(pd.to_datetime(data.index), inplace=True)

# Launch Backtest 🚀
bt = Backtest(data, VolTerminus, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print("\n🌙✨ FINAL MISSION REPORT ✨🌙")
print(stats)
print(stats._strategy)
