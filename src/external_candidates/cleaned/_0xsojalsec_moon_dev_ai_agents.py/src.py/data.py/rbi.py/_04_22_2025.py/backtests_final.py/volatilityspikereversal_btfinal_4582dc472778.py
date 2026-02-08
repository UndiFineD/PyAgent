# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\VolatilitySpikeReversal_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data handling
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


class VolatilitySpikeReversal(Strategy):
    def init(self):
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.std_dev20 = self.I(talib.STDDEV, self.data.Close, timeperiod=20)
        self.ema20 = self.I(talib.EMA, self.data.Close, timeperiod=20)
        self.atr20 = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20)
        self.current_day = None
        self.daily_high_equity = 0
        self.stop_trading = False
        self.entry_bar = 0
        self.stop_loss_price = 0
        self.entry_sma20 = 0
        self.entry_std_dev20 = 0

    def next(self):
        current_date = self.data.index[-1].date()
        if current_date != self.current_day:
            self.current_day = current_date
            self.daily_high_equity = self.equity
            self.stop_trading = False

        if self.stop_trading:
            return

        current_drawdown = (
            (self.daily_high_equity - self.equity) / self.daily_high_equity if self.daily_high_equity != 0 else 0
        )
        if current_drawdown >= 0.05:
            if self.position:
                self.position.close()
                print(f"🌙 MOON DEV DAILY LOSS LIMIT: 5% drawdown reached 🔴")
            self.stop_trading = True
            return

        if not self.position:
            if (self.data.Close[-1] <= (self.sma20[-1] - 3 * self.std_dev20[-1])) and (
                self.data.funding_rate[-1] >= 0.001
            ):
                risk_amount = self.equity * 0.01
                std_dev_value = self.std_dev20[-1]
                if std_dev_value <= 0:
                    return
                position_size = int(round(risk_amount / std_dev_value))
                if position_size <= 0:
                    return
                self.entry_sma20 = self.sma20[-1]
                self.entry_std_dev20 = self.std_dev20[-1]
                self.stop_loss_price = self.entry_sma20 - 4 * self.entry_std_dev20
                self.buy(size=position_size)
                self.entry_bar = len(self.data)
                print(f"🌙 MOON DEV ENTRY: Long {position_size} units at {self.data.Close[-1]:.2f} ✨")
        else:
            current_upper_keltner = self.ema20[-1] + 2.5 * self.atr20[-1]
            if self.data.High[-1] >= current_upper_keltner:
                self.position.close()
                print(f"🌙 MOON DEV PROFIT TAKEN: Keltner target {current_upper_keltner:.2f} 🎯")
            elif self.data.Low[-1] <= self.stop_loss_price:
                self.position.close()
                print(f"🌙 MOON DEV EMERGENCY EXIT: 4σ stop {self.stop_loss_price:.2f} 🚨")
            elif len(self.data) - self.entry_bar >= 192:
                self.position.close()
                print(f"🌙 MOON DEV TIME EXIT: 48 hours passed 🕒")


bt = Backtest(data, VolatilitySpikeReversal, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
