# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\ClusterBreakout_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev ClusterBreakout – breakout with volume spike 🌋

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ClusterBreakoutStrategy(Strategy):
    CLUSTER_LOOKBACK = 50  # bars for range detection

    def init(self):
        print("🌙 Moon Dev initializing ClusterBreakout indicators… 🚀")
        self.ma50 = self.I(talib.SMA, self.data.Close, 50)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.vol_ma = self.I(talib.SMA, self.data.Volume, 50)

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        vol_spike = self.data.Volume[-1] > 1.5 * self.vol_ma[-1]
        high_level = max(self.data.Close[-self.CLUSTER_LOOKBACK :])
        low_level = min(self.data.Close[-self.CLUSTER_LOOKBACK :])
        above_ma = price > self.ma50[-1]
        below_ma = price < self.ma50[-1]

        if self.position:
            # Take profit at 2*ATR or stop on opposite breakout
            if self.position.is_long:
                if price - self.position.entry_price >= 2 * atr_val or price < low_level:
                    print("🌙 Moon Dev ClusterBreakout closing LONG ✨")
                    self.position.close()
            else:
                if self.position.entry_price - price >= 2 * atr_val or price > high_level:
                    print("🌙 Moon Dev ClusterBreakout closing SHORT ✨")
                    self.position.close()
            return

        # Long entry
        if price > high_level and vol_spike and above_ma:
            sl = price - 1.5 * atr_val
            tp = price + 2 * atr_val
            self._enter("buy", sl, tp)
            return

        # Short entry
        if price < low_level and vol_spike and below_ma:
            sl = price + 1.5 * atr_val
            tp = price - 2 * atr_val
            self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev {side.upper()} ClusterBreakout entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for ClusterBreakout… 📊")
    data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
    data.columns = data.columns.str.strip().str.title()
    data = data.rename(
        columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume",
        }
    )
    bt = Backtest(
        data,
        ClusterBreakoutStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev ClusterBreakout backtest done! ✨\n", stats)
