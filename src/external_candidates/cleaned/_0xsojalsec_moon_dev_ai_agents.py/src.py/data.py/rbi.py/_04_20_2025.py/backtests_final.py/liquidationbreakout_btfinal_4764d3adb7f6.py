# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\LiquidationBreakout_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

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


class LiquidationBreakout(Strategy):
    risk_percent = 0.01

    def init(self):
        self.ema = self.I(talib.EMA, self.data.Close, timeperiod=20, name="EMA 20")
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=20,
            name="ATR 20",
        )
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=20, name="Swing High")
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20, name="Swing Low")

    def next(self):
        if len(self.data) < 20:
            return

        current_close = self.data.Close[-1]
        upper_band = self.ema[-1] + 2 * self.atr[-1]
        lower_band = self.ema[-1] - 2 * self.atr[-1]

        if not self.position:
            # Long entry logic
            if current_close > upper_band and self.data.High[-1] >= self.swing_high[-1]:
                stop_loss = max(lower_band, self.swing_low[-1])
                risk_amount = self.equity * self.risk_percent
                stop_distance = current_close - stop_loss
                if stop_distance > 0:
                    position_size = int(round(risk_amount / stop_distance))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss, tp=self.swing_high[-1])
                        print(
                            f"🌙🚀 MOON DEV LONG ENTRY @ {current_close:.2f}! Cluster Breakout Confirmed! TP: {self.swing_high[-1]:.2f} | SL: {stop_loss:.2f} 🌕"
                        )

            # Short entry logic
            elif current_close < lower_band and self.data.Low[-1] <= self.swing_low[-1]:
                stop_loss = min(upper_band, self.swing_high[-1])
                risk_amount = self.equity * self.risk_percent
                stop_distance = stop_loss - current_close
                if stop_distance > 0:
                    position_size = int(round(risk_amount / stop_distance))
                    if position_size > 0:
                        self.sell(size=position_size, sl=stop_loss, tp=self.swing_low[-1])
                        print(
                            f"🌙🌌 MOON DEV SHORT ENTRY @ {current_close:.2f}! Liquidation Zone Activated! TP: {self.swing_low[-1]:.2f} | SL: {stop_loss:.2f} 🌠"
                        )


bt = Backtest(data, LiquidationBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
