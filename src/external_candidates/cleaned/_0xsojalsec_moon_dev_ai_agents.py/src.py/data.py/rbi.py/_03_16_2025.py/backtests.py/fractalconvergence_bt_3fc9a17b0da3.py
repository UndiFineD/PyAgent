# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests\FractalConvergence_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class FractalConvergenceStrategy(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    risk_reward_ratio = 2
    stop_loss_pct = 0.01  # 1% stop loss

    def init(self):
        self.max_high = self.I(talib.MAX, self.data.High, timeperiod=5)
        self.min_low = self.I(talib.MIN, self.data.Low, timeperiod=5)
        self.willr = self.I(talib.WILLR, self.data.High, self.data.Low, self.data.Close, 14)
        self.williams_d = self.I(talib.SMA, self.willr, 3)
        self.sma20 = self.I(talib.SMA, self.data.Close, 20)

    def next(self):
        if len(self.data) < 20 or len(self.williams_d) < 2:
            return

        # Calculate fractal signals 🌙
        bullish_fractal = self.data.High[-3] == self.max_high[-1]
        bearish_fractal = self.data.Low[-3] == self.min_low[-1]

        # Trend analysis ✨
        downtrend = self.data.Close[-1] < self.sma20[-1]
        uptrend = self.data.Close[-1] > self.sma20[-1]

        # Williams %D convergence 🚀
        williams_d_rising = self.williams_d[-1] > self.williams_d[-2]
        williams_d_falling = self.williams_d[-1] < self.williams_d[-2]

        entry_price = self.data.Close[-1]

        if not self.position:
            # Long entry logic 🌙✨
            if bullish_fractal and downtrend and williams_d_rising:
                sl_price = entry_price * (1 - self.stop_loss_pct)
                tp_price = entry_price * (1 + (self.stop_loss_pct * self.risk_reward_ratio))
                self.calculate_position_size(entry_price, sl_price, True)

            # Short entry logic 🌙✨
            elif bearish_fractal and uptrend and williams_d_falling:
                sl_price = entry_price * (1 + self.stop_loss_pct)
                tp_price = entry_price * (1 - (self.stop_loss_pct * self.risk_reward_ratio))
                self.calculate_position_size(entry_price, sl_price, False)

    def calculate_position_size(self, entry_price, sl_price, is_long):
        risk_amount = self.equity * self.risk_per_trade
        risk_per_share = abs(entry_price - sl_price)

        if risk_per_share == 0:
            return

        position_size = risk_amount / risk_per_share
        position_size = int(round(position_size))

        if position_size > 0:
            if is_long:
                self.buy(
                    size=position_size,
                    sl=sl_price,
                    tp=entry_price + 2 * (entry_price - sl_price),
                )
                print(f"🌙✨🚀 BULLISH Convergence! LONG {position_size} @ {entry_price:.2f}")
            else:
                self.sell(
                    size=position_size,
                    sl=sl_price,
                    tp=entry_price - 2 * (sl_price - entry_price),
                )
                print(f"🌙✨🚀 BEARISH Divergence! SHORT {position_size} @ {entry_price:.2f}")


# Data handling 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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

# Run backtest 🚀
bt = Backtest(data, FractalConvergenceStrategy, cash=1_000_000, trade_on_close=True)
stats = bt.run()
print(stats)
print(stats._strategy)
