# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_01_2025\backtests\FundingBandit_BT.py
# 🌙 Moon Dev's FundingBandit Backtest Implementation
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class FundingBandit(Strategy):
    # Strategy parameters 🌙
    bb_period = 20
    bb_dev = 2
    high_funding = 0.001  # 0.1% threshold
    normal_funding = 0.0005  # Exit threshold
    risk_pct = 0.01  # 1% risk per trade
    trail_stop = 0.03  # 3% trailing stop

    def init(self):
        # Initialize Bollinger Bands using TA-Lib 🌙📈
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_dev,
            nbdevdn=self.bb_dev,
            matype=talib.MA_Type.SMA,
        )

        # Print Moon Dev initialization message 🌙✨
        print("🌙✨ Moon Dev Indicators Activated! Tracking Funding Bandit Signals...")

    def next(self):
        current_close = self.data.Close[-1]
        current_funding = self.data.Funding_Rate[-1]

        # Entry Logic 🌙🚀
        if not self.position:
            if (current_close < self.bb_lower[-1]) and (
                current_funding > self.high_funding
            ):
                # Risk management calculation 🌙💰
                risk_amount = self.equity * self.risk_pct
                risk_per_unit = current_close * self.trail_stop
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    self.buy(size=position_size)
                    self.trailing_high = current_close  # Initialize trailing high
                    print(
                        f"🌙🚀 MOON ENTRY! Price: {current_close:.2f}, Size: {position_size} units"
                    )
                    print(
                        f"   Funding Rate: {current_funding:.4%} 🌡️, Lower BB: {self.bb_lower[-1]:.2f} 📉"
                    )

        # Exit Logic 🌙🛑
        else:
            # Update trailing high 🌙📈
            self.trailing_high = max(self.trailing_high, self.data.High[-1])
            stop_price = self.trailing_high * (1 - self.trail_stop)

            # Trailing stop check 🌙🔍
            if self.data.Low[-1] <= stop_price:
                self.position.close()
                print(f"🌙🛑 TRAILING STOP! Exit at: {stop_price:.2f}")

            # Funding normalization check 🌙🌡️
            elif current_funding < self.normal_funding:
                self.position.close()
                print(f"🌙🛑 FUNDING NORMALIZED! Rate: {current_funding:.4%}")


# Data Preparation 🌙📂
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and format data 🌙🧹
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "funding_rate": "Funding_Rate",  # Must exist in original data
    }
)

# Run Backtest 🌙⚡
bt = Backtest(data, FundingBandit, cash=1_000_000, commission=0.002)
stats = bt.run()

# Moon Dev Performance Report 🌙📊
print("\n🌙✨ MOON DEV FINAL REPORT ✨🌙")
print(stats)
print(stats._strategy)
