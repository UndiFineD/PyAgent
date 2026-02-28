# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\ExpiryVolatility_PKG.py
# 🌙 MOON DEV BACKTESTING IMPLEMENTATION FOR EXPIRYVOLATILITY STRATEGY 🚀

import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ExpiryVolatility(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    position_size_pct = 0.2  # 20% of equity
    rr_ratio = 2  # Reward:Risk ratio

    def init(self):
        # 🌟 Calculate required indicators using TA-Lib
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.daily_high = self.I(
            talib.MAX, self.data.High, timeperiod=96
        )  # 96 bars = 24hrs in 15m
        self.daily_low = self.I(talib.MIN, self.data.Low, timeperiod=96)

        # 🌙 Calculate daily range and volatility threshold
        self.daily_range = self.I(lambda: self.daily_high - self.daily_low)

    def next(self):
        # 🛑 Exit existing positions first
        self.check_time_based_exits()

        # 🌙 Check entry conditions
        if not self.position and self.entry_signal():
            self.enter_trade()

    def entry_signal(self):
        # 📅 Contract must be 5+ days past expiry
        if self.data.days_past_expiry[-1] < 5:
            return False

        # 🌪️ Volatility check
        current_atr = self.atr[-1]
        current_range = self.daily_range[-1]

        # 🔍 Range must exceed ATR by 25% of ATR
        if (current_range - current_atr) >= 0.25 * current_atr:
            print(
                f"🌙✨ VOLATILITY SPIKE DETECTED! ATR: {current_atr:.2f}, Range: {current_range:.2f}"
            )
            return True
        return False

    def enter_trade(self):
        # 💰 Calculate position size
        price = self.data.Close[-1]
        size = (self.equity * self.position_size_pct) / price
        size = int(round(size))

        if size == 0:
            print("🌙⚠️  Zero position size calculated, skipping trade")
            return

        # 🛡️ Risk management calculations
        risk_amount = self.equity * self.risk_per_trade
        risk_per_unit = risk_amount / size
        stop_loss = price - risk_per_unit
        take_profit = price + (self.rr_ratio * risk_per_unit)

        # 🚀 Enter trade with OCO orders
        self.buy(size=size, sl=stop_loss, tp=take_profit, tag="ExpiryVolatility Trade")

        print(
            f"🌙🚀 MOON DEV TRADE ENTERED! Size: {size} | Entry: {price:.2f} | SL: {stop_loss:.2f} | TP: {take_profit:.2f}"
        )

    def check_time_based_exits(self):
        # ⏳ Close positions older than 5 days
        for trade in self.trades:
            days_in_trade = (self.data.index[-1] - trade.entry_time).days
            if days_in_trade >= 5:
                trade.close()
                print(
                    f"🌙⏳ TIME EXIT | Position closed after 5 days at {self.data.Close[-1]:.2f}"
                )


# DATA PREPROCESSING 🌙
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# � Clean and prepare data
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

# 🚨 Add dummy expiration data (real implementation should use actual expiration dates)
data["days_past_expiry"] = 5  # Placeholder for testing

# BACKTEST EXECUTION 🌙
bt = Backtest(data, ExpiryVolatility, cash=1_000_000)
stats = bt.run()
