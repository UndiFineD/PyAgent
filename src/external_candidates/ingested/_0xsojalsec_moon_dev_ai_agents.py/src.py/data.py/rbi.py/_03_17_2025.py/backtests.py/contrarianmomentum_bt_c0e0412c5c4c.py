# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_17_2025\backtests\ContrarianMomentum_BT.py
# 🌙 Moon Dev's Contrarian Momentum Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🚀 Data Preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# 🌙 Clean and format data columns
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


class ContrarianMomentum(Strategy):
    # 🌕 Strategy Parameters
    risk_percent = 0.01  # 1% risk per trade
    stop_loss_pct = 0.01  # 1% stop loss
    rsi_oversold = 30
    bb_period = 20
    rsi_period = 14

    def init(self):
        # 🌀 Indicator Calculation
        # Bollinger Bands
        upper, _, _ = talib.BBANDS(
            self.data.Close, timeperiod=self.bb_period, nbdevup=2, nbdevdn=2, matype=0
        )
        self.upper_bb = self.I(lambda: upper, name="Upper BB")

        # RSI
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period, name="RSI")

        # 3-Day Return System
        self.daily_ret = self.I(
            lambda close: (
                close / close.shift(96) - 1
            ),  # 96 periods = 1 day in 15m data
            self.data.Close,
            name="Daily Return",
        )

        self.three_day_avg = self.I(
            lambda x: x.rolling(3).mean(),  # 3-day average
            self.daily_ret,
            name="3-Day Avg",
        )

    def next(self):
        # 🌓 Moon Dev Entry Logic
        if not self.position:
            if (
                self.data.Close[-1] > self.upper_bb[-1]
                and self.rsi[-1] < self.rsi_oversold
            ):

                # 🛡 Risk Management Calculation
                equity = self.equity
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * (1 - self.stop_loss_pct)
                risk_amount = equity * self.risk_percent
                risk_per_share = entry_price - stop_loss

                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    print(
                        f"🌙✨🚀 MOON DEV ENTRY: Long {position_size} units at {entry_price:.2f}"
                    )
                    take_profit = entry_price + (risk_per_share * 2)  # 2:1 reward
                    self.buy(size=position_size, sl=stop_loss, tp=take_profit)

        # 🌑 Moon Dev Exit Logic
        else:
            current_ret = self.daily_ret[-1]
            avg_ret = self.three_day_avg[-1]

            if current_ret < avg_ret and not np.isnan(avg_ret):
                print(
                    f"🌙✨🌑 MOON DEV EXIT: Return {current_ret:.2%} < Avg {avg_ret:.2%}"
                )
                self.position.close()


# 🚀 Launch Backtest
bt = Backtest(data, ContrarianMomentum, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Print Full Moon Stats
print("\n🌙✨🌕 FINAL MOON DEV STATS 🌕✨🌙")
print(stats)
print(stats._strategy)
