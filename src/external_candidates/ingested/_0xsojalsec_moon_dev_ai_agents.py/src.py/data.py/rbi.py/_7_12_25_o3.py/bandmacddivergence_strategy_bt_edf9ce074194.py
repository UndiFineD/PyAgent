# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandMACDDivergence_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandMACDDivergence strategy – combo of BB slope + MACD divergence 🪄

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)

# --- helper for slope calculation ---


def slope(series, lookback: int = 5):
    if len(series) < lookback + 1:
        return 0.0
    return series[-1] - series[-lookback - 1]


class BandMACDDivergenceStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandMACDDivergence indicators… 🚀")
        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        # MACD components
        self.macd_line = self.I(lambda c: talib.MACD(c, 12, 26, 9)[0], self.data.Close)
        self.macd_signal = self.I(
            lambda c: talib.MACD(c, 12, 26, 9)[1], self.data.Close
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        upper_band = self.bb_upper[-1]
        macd_line = self.macd_line[-1]
        macd_signal = self.macd_signal[-1]

        # Calculate slope of upper band over last 5 bars
        upper_slope = slope(self.bb_upper, 5)
        bullish_divergence = macd_line > macd_signal and upper_slope > 0
        bearish_divergence = macd_line < macd_signal and upper_slope < 0

        # position management
        if self.position:
            if self.position.is_long and (upper_slope <= 0 or macd_line < macd_signal):
                print("🌙 Moon Dev closing long – divergence faded! ✨")
                self.position.close()
            elif self.position.is_short and (
                upper_slope >= 0 or macd_line > macd_signal
            ):
                print("🌙 Moon Dev closing short – divergence faded! ✨")
                self.position.close()
            return

        # Entry logic with ATR-based divergence threshold (~1.5 ATR)
        divergence_thresh = 1.5 * atr_val
        if bullish_divergence and price - upper_band < divergence_thresh:
            sl = price - 2 * atr_val
            tp = price + 2 * atr_val
            self._enter("buy", sl, tp)
        elif bearish_divergence and upper_band - price < divergence_thresh:
            sl = price + 2 * atr_val
            tp = price - 2 * atr_val
            self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(
            f"🌙 Moon Dev {side.upper()} signal on BandMACDDivergence! size={size} 🚀"
        )
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandMACDDivergence… 📊")
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
        BandMACDDivergenceStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandMACDDivergence backtest done! ✨\n", stats)
