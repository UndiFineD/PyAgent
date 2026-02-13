# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandStrengthMomentum_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandStrengthMomentum – BB + RSI/Relative Strength for momentum 📈

DATA_PATH = (
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/"
    "src/data/rbi/BTC-USD-15m.csv"
)


class BandStrengthMomentumStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandStrengthMomentum indicators… 🚀")
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        # Use RSI as proxy for relative strength above/below 50
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        rsi_val = self.rsi[-1]
        upper_band = self.bb_upper[-1]
        lower_band = self.bb_lower[-1]
        atr_val = self.atr[-1]

        if self.position:
            if self.position.is_long and (price >= upper_band or rsi_val < 50):
                print("🌙 Moon Dev BandStrengthMomentum exit LONG ✨")
                self.position.close()
            elif self.position.is_short and (price <= lower_band or rsi_val > 50):
                print("🌙 Moon Dev BandStrengthMomentum exit SHORT ✨")
                self.position.close()
            return

        # Long entry: price above lower band + RSI > 55 + bullish candle (close > open)
        if (
            price >= lower_band
            and rsi_val > 55
            and self.data.Close[-1] > self.data.Open[-1]
        ):
            sl = price - 1.5 * atr_val
            tp = upper_band
            self._enter("buy", sl, tp)
            return

        # Short entry: price below upper band + RSI < 45 + bearish candle
        if (
            price <= upper_band
            and rsi_val < 45
            and self.data.Close[-1] < self.data.Open[-1]
        ):
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
        print(f"🌙 Moon Dev {side.upper()} BandStrengthMomentum entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandStrengthMomentum… 🌠")
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
        BandStrengthMomentumStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandStrengthMomentum backtest done! ✨\n", stats)
