# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\ChikouVolatility_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev ChikouVolatility strategy – Ichimoku Chikou span + Bollinger Bands 🌖

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ChikouVolatilityStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing ChikouVolatility indicators… 🚀")
        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # Ensure we have at least 27 bars for Chikou Span calculation
        if len(self.data.Close) < 27:
            return
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        chikou_span = self.data.Close[-26]  # lagging line 26 periods back
        upper_band = self.bb_upper[-1]
        lower_band = self.bb_lower[-1]

        # Manage current position
        if self.position:
            target_band = upper_band if self.position.is_long else lower_band
            # Take-profit when price hits opposite band
            if (self.position.is_long and price >= target_band) or (self.position.is_short and price <= target_band):
                print("🌙 Moon Dev ChikouVolatility TP reached! 🎯")
                self.position.close()
            return

        # Bullish entry condition
        if chikou_span < price and price <= lower_band:
            # Enter long when price closes back inside bands
            if self.data.Close[-2] < lower_band and price > lower_band:
                sl = price - 0.5 * atr_val
                tp = upper_band
                self._enter("buy", sl, tp)
                return

        # Bearish entry condition
        if chikou_span > price and price >= upper_band:
            if self.data.Close[-2] > upper_band and price < upper_band:
                sl = price + 0.5 * atr_val
                tp = lower_band
                self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev {side.upper()} ChikouVolatility entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for ChikouVolatility… 🌕")
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
        ChikouVolatilityStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev ChikouVolatility backtest done! ✨\n", stats)
