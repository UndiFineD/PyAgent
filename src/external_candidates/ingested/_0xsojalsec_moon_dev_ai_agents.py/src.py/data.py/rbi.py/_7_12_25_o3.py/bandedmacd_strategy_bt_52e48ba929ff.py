# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandedMACD_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandedMACD strategy – capturing overbought exits based on MACD + BB 📉

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)


class BandedMACDStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandedMACD indicators… 🚀")
        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        # MACD
        self.macd_line = self.I(lambda c: talib.MACD(c, 12, 26, 9)[0], self.data.Close)
        self.macd_signal = self.I(
            lambda c: talib.MACD(c, 12, 26, 9)[1], self.data.Close
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        macd_line = self.macd_line[-1]
        macd_signal = self.macd_signal[-1]
        upper_band = self.bb_upper[-1]
        atr_val = self.atr[-1]

        # Strategy is primarily an EXIT strategy; we'll simulate by entering a long position
        # when MACD turns bullish **below** upper band, and closing when price touches upper band
        if self.position:
            # Exit logic – price touched/exceeded upper BB OR bearish MACD cross
            if price >= upper_band or macd_line < macd_signal:
                print(
                    "🌙 Moon Dev BandedMACD exiting LONG – overbought or MACD cross! ✨"
                )
                self.position.close()
            return

        # Entry logic – bullish MACD crossover below upper BB
        if macd_line > macd_signal and price < upper_band:
            sl = price - 2 * atr_val
            tp = upper_band  # exit target at BB upper
            self._enter_long(sl, tp)

    def _enter_long(self, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev entering LONG on BandedMACD! size={size} 🚀")
        self.buy(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandedMACD… 📈")
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
        BandedMACDStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandedMACD backtest done! ✨\n", stats)
