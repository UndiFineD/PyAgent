# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\VolatilityBreakout_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)
data = data.sort_index()


class VolatilityBreakout(Strategy):
    risk_pct = 0.01

    def init(self):
        # Bollinger Bands Upper
        def bbands_upper(close):
            upper, _, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return upper

        self.upper_band = self.I(bbands_upper, self.data.Close)

        # ATR and its moving average
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.atr_ma = self.I(talib.SMA, self.atr, 10)

    def next(self):
        if len(self.data) < 20:  # Ensure enough data for indicators
            return

        if not self.position:
            # Check previous candle conditions
            if (self.atr[-2] < self.atr_ma[-2]) and (self.data.Close[-2] > self.upper_band[-2]):
                entry_price = self.data.Open[-1]
                atr_value = self.atr[-2]
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / atr_value))

                if position_size > 0:
                    sl = entry_price - atr_value
                    tp = entry_price + (1.5 * atr_value)
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙 MOON DEV BREAKOUT! 🚀 Entry: {entry_price:.2f} | Size: {position_size} | TP: {tp:.2f} | SL: {sl:.2f} ✨"
                    )


bt = Backtest(data, VolatilityBreakout, cash=1_000_000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
