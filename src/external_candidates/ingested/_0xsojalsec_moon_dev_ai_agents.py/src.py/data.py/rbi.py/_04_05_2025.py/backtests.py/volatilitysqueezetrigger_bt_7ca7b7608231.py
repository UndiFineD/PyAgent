# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\VolatilitySqueezeTrigger_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and format columns 🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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


class VolatilitySqueezeTrigger(Strategy):
    def init(self):
        # 🌙 Moon Dev Indicator Setup
        close = self.data.Close

        # Bollinger Bands Width Calculation
        upper, middle, lower = talib.BBANDS(close, 20, 2, 2)
        bb_width = (upper - lower) / middle
        self.bb_width = self.I(lambda: bb_width, name="BB_WIDTH")
        self.bb_low = self.I(talib.MIN, self.bb_width, 126, name="BB_LOW_126")

        # Klinger Volume Oscillator ✨
        kvo_df = ta.kvo(
            self.data.High, self.data.Low, close, self.data.Volume, 34, 55, 13
        )
        self.kvo = self.I(lambda: kvo_df.iloc[:, 0], name="KVO")
        self.kvo_sma = self.I(talib.SMA, self.kvo, 20, name="KVO_SMA_20")

        # ATR for Risk Management 🛡️
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, close, 14, name="ATR_14"
        )

        print(
            "🌙✨ Moon Dev Indicators Activated! BB Width:",
            bb_width[-1],
            "| KVO:",
            self.kvo[-1],
        )

    def next(self):
        # 🌙 Moon Dev Exit Conditions
        for trade in self.trades:
            current_bb = self.bb_width[-1] == self.bb_low[-1]
            if current_bb:
                trade.close()
                print(f"🌙🛑 Moon Dev Exit! BB Width Squeeze at {self.data.index[-1]}")

        if len(self.data) < 130:  # Ensure enough history
            return

        # 🌙 Entry Signal Detection
        prev_bb_squeeze = self.bb_width[-2] == self.bb_low[-2]
        kvo_cross = (self.kvo[-2] > self.kvo_sma[-2]) and (
            self.kvo[-3] <= self.kvo_sma[-3]
        )

        if prev_bb_squeeze and kvo_cross and not self.position and len(self.trades) < 3:
            # 🚀 Calculate Position Size
            risk_percent = 0.01
            atr_value = self.atr[-1]
            risk_amount = self.equity * risk_percent
            size = int(round(risk_amount / (2 * atr_value)))

            if size > 0:
                entry_price = self.data.Open[-1]
                self.buy(
                    size=size,
                    sl=entry_price - 2 * atr_value,
                    tp=entry_price + 2 * atr_value,
                )
                print(f"🌙🚀✨ MOONSHOT ALERT! Long {size} units at {entry_price} ✨")


# 🌙 Backtest Execution
bt = Backtest(data, VolatilitySqueezeTrigger, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST RESULTS:")
print(stats)
print(stats._strategy)
print("🌙 Strategy Simulation Complete! To the moon! 🚀")
