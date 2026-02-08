# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\DivergentBands_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder

# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class DivergentBands(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators using TA-Lib
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        macd, macd_signal, macd_hist = self.I(talib.MACD, self.data.Close, 12, 26, 9)
        self.macd_hist = macd_hist
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

        # Define rolling percentiles
        def rolling_percentile(series, window, perc):
            return series.rolling(window).quantile(perc / 100)

        self.p20 = self.I(rolling_percentile, self.data.Close, 20, 20)
        self.p80 = self.I(rolling_percentile, self.data.Close, 20, 80)

        # Track swing highs/lows
        self.price_highs = self.I(talib.MAX, self.data.High, 5)
        self.rsi_highs = self.I(talib.MAX, self.rsi, 5)
        self.macd_lows = self.I(talib.MIN, self.macd_hist, 5)

    def next(self):
        # Wait for sufficient data
        if len(self.data.Close) < 20 or len(self.rsi) < 5:
            return

        # Check divergences
        current_price_high = self.price_highs[-1]
        prev_price_high = self.price_highs[-2]
        current_rsi_high = self.rsi_highs[-1]
        prev_rsi_high = self.rsi_highs[-2]

        current_macd_low = self.macd_lows[-1]
        prev_macd_low = self.macd_lows[-2]

        bearish_div = (current_price_high > prev_price_high) and (current_rsi_high < prev_rsi_high)
        bullish_macd = current_macd_low > prev_macd_low
        volume_decreasing = self.data.Volume[-3] > self.data.Volume[-2] > self.data.Volume[-1]

        # Entry logic
        if not self.position and bearish_div and bullish_macd and volume_decreasing:
            if crossunder(self.data.Close, self.p20):
                atr_value = self.atr[-1]
                risk_amount = self.equity * self.risk_percent
                risk_per_share = atr_value  # SL = 1x ATR

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        entry_price = self.data.Close[-1]
                        sl = entry_price + atr_value
                        tp = entry_price - 1.5 * atr_value

                        self.sell(size=position_size, sl=sl, tp=tp)
                        print(
                            f"🌙🚀 SHORT ENTRY! Size: {position_size} | Entry: {entry_price:.2f} | SL: {sl:.2f} | TP: {tp:.2f}"
                        )

        # Exit logic
        if self.position.is_short:
            if crossover(self.data.High, self.p80):
                self.position.close()
                print(f"🌙✨ EXIT! Price crossed 80th percentile ({self.p80[-1]:.2f})")


# Run backtest
bt = Backtest(data, DivergentBands, cash=1_000_000, margin=1.0)
stats = bt.run()
print(stats)
print(stats._strategy)
