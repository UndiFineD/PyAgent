# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_gemini\CoTrendalNeutral_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class CoTrendalNeutralStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initiating CoTrendalNeutral strategy (BTC adaptation)! 🚀")
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr_ma = self.I(talib.SMA, self.atr, 50)

    def next(self):
        if self.position:
            return

        # Long Entry: Uptrend in price, decreasing volatility
        is_uptrend = self.ema50[-1] > self.ema200[-1]
        is_price_above_ema = self.data.Close[-1] > self.ema50[-1]
        is_vol_decreasing = self.atr[-1] < self.atr_ma[-1]
        is_rsi_bullish = self.rsi[-1] > 50 and self.rsi[-2] <= 50

        if is_uptrend and is_price_above_ema and is_vol_decreasing and is_rsi_bullish:
            print("🌙 Moon Dev bullish CoTrendalNeutral setup! Entering long. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price - 2 * self.atr[-1]
            tp = entry_price + 6 * self.atr[-1]  # 3:1 R:R
            risk_per_unit = entry_price - sl
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.buy(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered long with size {position_size}! ✨")

        # Short Entry: Downtrend in price, increasing volatility
        is_downtrend = self.ema50[-1] < self.ema200[-1]
        is_price_below_ema = self.data.Close[-1] < self.ema50[-1]
        is_vol_increasing = self.atr[-1] > self.atr_ma[-1]
        is_rsi_bearish = self.rsi[-1] < 50 and self.rsi[-2] >= 50

        if is_downtrend and is_price_below_ema and is_vol_increasing and is_rsi_bearish:
            print("🌙 Moon Dev bearish CoTrendalNeutral setup! Entering short. 🚀")
            entry_price = self.data.Close[-1]
            sl = entry_price + 2 * self.atr[-1]
            tp = entry_price - 6 * self.atr[-1]  # 3:1 R:R
            risk_per_unit = sl - entry_price
            if risk_per_unit <= 0:
                return
            risk_amount = self.equity * 0.01
            position_size = risk_amount / risk_per_unit
            position_size = int(round(position_size))
            if position_size > 0:
                self.sell(size=position_size, sl=sl, tp=tp)
                print(f"🌙 Moon Dev entered short with size {position_size}! ✨")


if __name__ == "__main__":
    data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
    print("🌙 Moon Dev loading BTC-USD data... 🚀")
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    print("🌙 Moon Dev data cleaning complete! ✨")

    bt = Backtest(
        data, CoTrendalNeutralStrategy, cash=1000000, margin=1, commission=0.001
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
