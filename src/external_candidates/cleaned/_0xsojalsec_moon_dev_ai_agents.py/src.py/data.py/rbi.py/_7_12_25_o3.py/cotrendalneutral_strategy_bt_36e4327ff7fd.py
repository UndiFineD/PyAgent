# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\CoTrendalNeutral_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev CoTrendalNeutral – simplified SPX/VIX co-trendality proxy using BTC price & ATR 📊
# NOTE: Because we only have BTC-USD OHLCV here, we proxy market stress with ATR.
# Rising ATR ~ rising VIX, falling ATR ~ falling VIX.

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class CoTrendalNeutralStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing CoTrendalNeutral indicators… 🚀")
        # Trend for BTC (acting as SPX)
        self.ma50 = self.I(talib.SMA, self.data.Close, 50)
        self.ma200 = self.I(talib.SMA, self.data.Close, 200)
        # ATR as volatility stress proxy (acting as VIX)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr_ma = self.I(talib.SMA, self.atr, 50)

    def next(self):
        price = self.data.Close[-1]
        up_trend = self.ma50[-1] > self.ma200[-1]
        down_trend = self.ma50[-1] < self.ma200[-1]
        atr_low = self.atr[-1] < self.atr_ma[-1]
        atr_high = self.atr[-1] > self.atr_ma[-1]
        atr_val = self.atr[-1]

        # Manage existing position
        if self.position:
            rr_target = 3 * self.position.risk  # track risk:reward 3:1
            if self.position.is_long and (price - self.position.entry_price >= rr_target or atr_high):
                print("🌙 Moon Dev CoTrendalNeutral closing LONG ✨")
                self.position.close()
            elif self.position.is_short and (self.position.entry_price - price >= rr_target or atr_low):
                print("🌙 Moon Dev CoTrendalNeutral closing SHORT ✨")
                self.position.close()
            return

        # Long SPX analogue: uptrend & low VIX analogue
        if up_trend and atr_low:
            sl = price - 1 * atr_val
            tp = price + 3 * atr_val
            self._enter("buy", sl, tp)
            return

        # Short VIX analogue: downtrend & high VIX analogue
        if down_trend and atr_high:
            sl = price + 1 * atr_val
            tp = price - 3 * atr_val
            self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        risk_amount = self.equity * 0.01
        size = int(round(risk_amount / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev CoTrendalNeutral {side.upper()} entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for CoTrendalNeutral… 🌐")
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
        CoTrendalNeutralStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev CoTrendalNeutral backtest done! ✨\n", stats)
