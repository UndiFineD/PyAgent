# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandSyncMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandSyncMomentum – syncing entries with BB midpoint trend! 💫

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)


class BandSyncMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandSyncMomentum indicators… 🚀")
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        # Calculate slope of middle band for trend direction
        self.mid_slope = self.I(lambda m: pd.Series(m).diff(), self.bb_middle)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        mid_trend_up = self.mid_slope[-1] > 0
        mid_trend_down = self.mid_slope[-1] < 0
        lower_band = self.bb_lower[-1]
        upper_band = self.bb_upper[-1]

        # Manage existing position
        if self.position:
            if self.position.is_long and (price >= upper_band or not mid_trend_up):
                print("🌙 Moon Dev BandSyncMomentum LONG exit ✨")
                self.position.close()
            elif self.position.is_short and (price <= lower_band or not mid_trend_down):
                print("🌙 Moon Dev BandSyncMomentum SHORT exit ✨")
                self.position.close()
            return

        # Long entry: price touches lower band + mid trending up
        if price <= lower_band * 1.005 and mid_trend_up:
            sl = price - 1.5 * atr_val
            tp = upper_band
            self._enter("buy", sl, tp)
            return

        # Short entry: price breaks upper band + mid trending down
        if price >= upper_band * 0.995 and mid_trend_down:
            sl = price + 1.5 * atr_val
            tp = lower_band
            self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev {side.upper()} BandSyncMomentum entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandSyncMomentum… ⭐️")
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
        BandSyncMomentumStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandSyncMomentum backtest done! ✨\n", stats)
