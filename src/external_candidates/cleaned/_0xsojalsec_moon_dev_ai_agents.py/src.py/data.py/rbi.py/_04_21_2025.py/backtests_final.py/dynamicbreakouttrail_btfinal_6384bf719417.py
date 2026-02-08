# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\DynamicBreakoutTrail_BTFinal.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)
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


class DynamicBreakoutTrail(Strategy):
    def init(self):
        self.donchian_upper = self.I(talib.MAX, self.data.High, timeperiod=20, name="Donchian Upper")
        self.donchian_lower = self.I(talib.MIN, self.data.Low, timeperiod=20, name="Donchian Lower")
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ADX 14",
        )
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR 14",
        )
        self.trailing_stop = None

    def next(self):
        if len(self.data) < 20:
            return

        current_close = self.data.Close[-1]
        adx_value = self.adx[-1]
        atr_value = self.atr[-1]

        # Moon Dev Debug Prints
        print(f"🌙 Moon Dev Indicators >> Close: {current_close:.2f}, ADX: {adx_value:.2f}, ATR: {atr_value:.2f}")

        # Entry Logic
        if not self.position:
            if current_close > self.donchian_upper[-1] and adx_value > 25:
                risk_percent = 0.02
                risk_amount = self.equity * risk_percent
                position_size = int(round(risk_amount / (2 * atr_value)))
                if position_size > 0:
                    self.buy(size=position_size)
                    self.trailing_stop = current_close - 2 * atr_value
                    print(f"🚀 LONG ENTRY: Moon Dev Rocket Launch! Price: {current_close:.2f}, Size: {position_size}")

            elif current_close < self.donchian_lower[-1] and adx_value > 25:
                risk_percent = 0.02
                risk_amount = self.equity * risk_percent
                position_size = int(round(risk_amount / (2 * atr_value)))
                if position_size > 0:
                    self.sell(size=position_size)
                    self.trailing_stop = current_close + 2 * atr_value
                    print(f"📉 SHORT ENTRY: Moon Dev Short Signal! Price: {current_close:.2f}, Size: {position_size}")

        # Exit Logic with Trailing Stop
        if self.position:
            if self.position.is_long:
                self.trailing_stop = max(self.trailing_stop, current_close - 2 * atr_value)
                if self.data.Low[-1] <= self.trailing_stop:
                    self.position.close()
                    print(
                        f"🌙 LONG EXIT: Trailing Stop Activated! Price: {current_close:.2f}, Profit: {self.position.pl:.2f}"
                    )
            else:
                self.trailing_stop = min(self.trailing_stop, current_close + 2 * atr_value)
                if self.data.High[-1] >= self.trailing_stop:
                    self.position.close()
                    print(
                        f"🌙 SHORT EXIT: Trailing Stop Activated! Price: {current_close:.2f}, Profit: {self.position.pl:.2f}"
                    )


bt = Backtest(data, DynamicBreakoutTrail, cash=1000000, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
