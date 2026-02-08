# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests\MomentumBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class MomentumBreakout(Strategy):
    donchian_period = 20
    atr_period = 14
    risk_pct = 0.01

    def init(self):
        self.donchian_upper = self.I(talib.MAX, self.data.High, self.donchian_period)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, self.donchian_period)
        _, _, self.macd_hist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.trailing_stop = None
        self.peak = None

    def next(self):
        if len(self.data) < self.donchian_period + 1:
            return

        current_idx = len(self.data) - 1
        macd_current = self.macd_hist[-1]
        macd_prev = self.macd_hist[-2] if current_idx > 1 else 0

        # Risk calculation
        equity = self.broker.equity
        risk_amount = equity * self.risk_pct
        atr_value = self.atr[-1]

        # Exit logic
        if self.position.is_long:
            self.peak = max(self.peak, self.data.High[-1])
            self.trailing_stop = self.peak - 2 * atr_value
            if self.data.Low[-1] <= self.trailing_stop:
                self.position.close()
                print(
                    f"🌙 Moon Exit! Closed LONG at {self.data.Close[-1]:.2f} | ATR Trail: {self.trailing_stop:.2f} ✨"
                )

        elif self.position.is_short:
            self.trough = min(self.trough, self.data.Low[-1])
            self.trailing_stop = self.trough + 2 * atr_value
            if self.data.High[-1] >= self.trailing_stop:
                self.position.close()
                print(
                    f"🌙 Moon Exit! Closed SHORT at {self.data.Close[-1]:.2f} | ATR Trail: {self.trailing_stop:.2f} ✨"
                )

        # Entry logic
        if not self.position:
            if (self.data.Close[-1] > self.donchian_upper[-1]) and (macd_current > macd_prev):
                stop_distance = 2 * atr_value
                position_size = int(round(risk_amount / stop_distance))
                if position_size > 0:
                    self.buy(size=position_size)
                    self.peak = self.data.High[-1]
                    print(f"🚀 Moon Boost! LONG {position_size} @ {self.data.Close[-1]:.2f} | MACD Rising 🌛")

            elif (self.data.Close[-1] < self.donchian_lower[-1]) and (macd_current < macd_prev):
                stop_distance = 2 * atr_value
                position_size = int(round(risk_amount / stop_distance))
                if position_size > 0:
                    self.sell(size=position_size)
                    self.trough = self.data.Low[-1]
                    print(f"🌒 Moon Dip! SHORT {position_size} @ {self.data.Close[-1]:.2f} | MACD Falling 🌜")


bt = Backtest(data, MomentumBreakout, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
