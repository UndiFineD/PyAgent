# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandSqueezeTrend_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandSqueezeTrend strategy – riding strong moves after band breakout 🚀

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)


class BandSqueezeTrendStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandSqueezeTrend indicators… 🌌")
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 20
        )  # 20-period ATR

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        upper_band = self.bb_upper[-1]
        middle_band = self.bb_middle[-1]

        # Manage current position
        if self.position:
            if self.position.is_long:
                # Exit if price closes below middle band or reaches TP (1.5 ATR)
                if (
                    price < middle_band
                    or price - self.position.entry_price >= 1.5 * atr_val
                ):
                    print("🌙 Moon Dev BandSqueezeTrend closing LONG ✨")
                    self.position.close()
            return

        # Entry condition: price above upper band AND price below 20-period ATR avg (vol not hyper)
        if price > upper_band and price - upper_band < atr_val:
            sl = price - 0.5 * atr_val
            tp = price + 1.5 * atr_val
            self._enter_long(sl, tp)

    def _enter_long(self, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev entering LONG on BandSqueezeTrend! size={size} 🚀")
        self.buy(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandSqueezeTrend… 🌙")
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
        BandSqueezeTrendStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandSqueezeTrend backtest done! ✨\n", stats)
