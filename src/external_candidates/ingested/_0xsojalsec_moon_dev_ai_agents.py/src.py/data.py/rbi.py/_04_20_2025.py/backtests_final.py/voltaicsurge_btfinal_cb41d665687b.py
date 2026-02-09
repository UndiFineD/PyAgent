# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\VoltaicSurge_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
required_columns = {
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
data = data.rename(columns=required_columns)
data = data[["Open", "High", "Low", "Close", "Volume"]]

# Calculate daily ATR
daily_df = data.resample("D").agg(
    {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
)
daily_df["daily_atr"] = talib.ATR(
    daily_df["High"], daily_df["Low"], daily_df["Close"], timeperiod=14
)
data["daily_atr"] = daily_df["daily_atr"].reindex(data.index).ffill()


class VoltaicSurge(Strategy):
    def init(self):
        self.atr_15m = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

    def next(self):
        for trade in self.trades:
            if trade.is_long:
                if trade.sl is None:
                    entry_price = trade.entry_price
                    sl = entry_price - 2 * trade.tag["breakout_atr"]
                    trade.sl = sl
                    trade.tag["high_water"] = entry_price
                    print(f"🌕 Moon Dev: Initial SL set at {sl:.2f} ✨")
                else:
                    current_high = self.data.High[-1]
                    if current_high > trade.tag["high_water"]:
                        trade.tag["high_water"] = current_high
                        new_sl = current_high - 2 * trade.tag["breakout_atr"]
                        if new_sl > trade.sl:
                            trade.sl = new_sl
                            print(
                                f"🌙 Moon Dev: Trailing SL updated to {new_sl:.2f} 🚀"
                            )

        if not self.position:
            atr_15 = self.atr_15m[-1]
            daily_atr = self.data.daily_atr[-1]
            vol = self.data.Volume[-1]
            vol_sma = self.volume_sma[-1]

            if atr_15 > daily_atr * 1.5 and vol > vol_sma:
                risk = 0.01 * self.equity
                atr_value = daily_atr * 1.5
                risk_per_share = 2 * atr_value
                size = int(round(risk / risk_per_share))

                if size > 0:
                    self.buy(
                        size=size, tag={"breakout_atr": atr_value, "high_water": None}
                    )
                    print(
                        f"✨ Moon Dev: Entered long position with {size} units @ {self.data.Close[-1]:.2f} 🌕"
                    )


bt = Backtest(data, VoltaicSurge, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
