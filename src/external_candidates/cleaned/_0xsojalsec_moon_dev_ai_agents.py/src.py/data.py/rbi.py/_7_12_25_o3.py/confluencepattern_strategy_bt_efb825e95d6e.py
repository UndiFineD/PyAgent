# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\ConfluencePattern_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# 🌙 Moon Dev backtest for the ConfluencePattern strategy 🪐
# ---------------------------------------------------------
# This strategy looks for confluence between EMA trend, RSI momentum, MACD alignment
# and a simple breakout confirmation.  The implementation is a streamlined version
# of the detailed spec found in the accompanying research file while strictly following
# Moon Dev coding guidelines – lots of emojis 🥳, slim code (no unnecessary try/except),
# and plenty of debug prints for fast troubleshooting.

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class ConfluencePatternStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing ConfluencePattern indicators… 🚀")
        # Trend & momentum indicators
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)
        self.ema200 = self.I(talib.EMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

        # MACD returns 3-tuple -> take macd line & signal line
        def _macd_line(close):
            return talib.MACD(close, 12, 26, 9)[0]

        def _macd_signal(close):
            return talib.MACD(close, 12, 26, 9)[1]

        self.macd_line = self.I(_macd_line, self.data.Close)
        self.macd_signal = self.I(_macd_signal, self.data.Close)

        # Volatility for adaptive stops
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        ema50 = self.ema50[-1]
        ema200 = self.ema200[-1]
        rsi_val = self.rsi[-1]
        macd_line = self.macd_line[-1]
        macd_signal = self.macd_signal[-1]
        atr_val = self.atr[-1]

        # --- Manage existing position first ---
        if self.position:
            if self.position.is_long:
                # Exit if RSI turns overbought or price dips below EMA50
                if rsi_val > 70 or price < ema50:
                    print("🌙 Moon Dev exit long – RSI/EMA trigger! ✨")
                    self.position.close()
            else:  # short position
                if rsi_val < 30 or price > ema50:
                    print("🌙 Moon Dev exit short – RSI/EMA trigger! ✨")
                    self.position.close()
            return  # Only one trade at a time

        # --- Long setup (bullish confluence) ---
        # Trend confirmation: price > EMA50 > EMA200
        bullish_trend = price > ema50 > ema200
        # RSI rising out of oversold territory
        rsi_confirmation = rsi_val > 30 and rsi_val > self.rsi[-2]
        # MACD bullish alignment
        macd_confirmation = macd_line > macd_signal
        # Simple breakout above recent 20-bar high
        breakout_level = max(self.data.Close[-20:])
        breakout = price > breakout_level

        if bullish_trend and rsi_confirmation and macd_confirmation and breakout:
            sl = price - 2 * atr_val
            tp = price + 2 * atr_val
            self._risk_managed_entry("buy", sl, tp)
            return

        # --- Short setup (bearish confluence) ---
        bearish_trend = price < ema50 < ema200
        rsi_bear = rsi_val < 70 and rsi_val < self.rsi[-2]
        macd_bear = macd_line < macd_signal
        breakdown_level = min(self.data.Close[-20:])
        breakdown = price < breakdown_level

        if bearish_trend and rsi_bear and macd_bear and breakdown:
            sl = price + 2 * atr_val
            tp = price - 2 * atr_val
            self._risk_managed_entry("sell", sl, tp)

    # -------------- helper --------------
    def _risk_managed_entry(self, side: str, sl: float, tp: float):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        risk_per_unit = abs(price - sl)
        if risk_per_unit <= 0:
            return
        risk_amount = self.equity * 0.01  # risk 1% of equity
        size = int(round(risk_amount / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev {side.upper()} signal! price={price:.2f}, SL={sl:.2f}, TP={tp:.2f}, size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


# ----------- Backtest Execution -----------
if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD data for ConfluencePattern … 📈")
    data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
    data.columns = data.columns.str.strip().str.title()  # Ensure proper column names
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
        ConfluencePatternStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )

    stats = bt.run()
    print("🌙 Moon Dev backtest complete! ✨\n", stats)
