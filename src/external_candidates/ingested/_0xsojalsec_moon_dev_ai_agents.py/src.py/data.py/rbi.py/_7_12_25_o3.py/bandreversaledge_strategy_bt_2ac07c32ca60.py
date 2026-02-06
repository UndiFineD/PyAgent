# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandReversalEdge_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandReversalEdge – quick 3-bar mean reversion 🌑

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)


class BandReversalEdgeStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandReversalEdge indicators… 🚀")
        # 50-period Bollinger
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 50, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 50, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 50, 2, 2)[2], self.data.Close),
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        # bar counter for 3-bar window
        self.bar_since_entry = None

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        upper_band = self.bb_upper[-1]
        lower_band = self.bb_lower[-1]

        if self.position:
            self.bar_since_entry += 1
            # Profit target or time/stop
            tp_hit = (
                price >= upper_band if self.position.is_long else price <= lower_band
            )
            time_up = self.bar_since_entry >= 3
            sl_hit = (
                price <= self.position.entry_price - 0.5 * atr_val
                if self.position.is_long
                else price >= self.position.entry_price + 0.5 * atr_val
            )
            if tp_hit or time_up or sl_hit:
                print("🌙 Moon Dev BandReversalEdge exiting position ✨")
                self.position.close()
                self.bar_since_entry = None
            return

        # Entry condition – price below lower band (oversold)
        if price < lower_band:
            sl = price - 0.5 * atr_val
            self._enter("buy", sl)
            return

        # (Bearish counterpart omitted per spec focusing on oversold reversals)

    def _enter(self, side: str, sl: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev entering {side.upper()} BandReversalEdge! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl)
        else:
            self.sell(size=size, sl=sl)
        self.bar_since_entry = 0


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandReversalEdge… 🌘")
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
        BandReversalEdgeStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandReversalEdge backtest done! ✨\n", stats)
