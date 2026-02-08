# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\10_20_2025\backtests\OpenReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
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
data = data[["Open", "High", "Low", "Close", "Volume"]]


class OpenReversal(Strategy):
    # Parameters adapted for spot trading simulation (long for put-selling equivalent)
    ema_period = 5
    vol_ma_period = 20
    vol_threshold = 1.2
    oi_reversal_threshold = 1.05  # Volume increase proxy for OI rise
    sl_pct = 0.02  # 2% stop loss
    tp_pct = 0.02  # 2% take profit (simplified for premium decay equivalent)
    size = 1000000

    def init(self):
        # Indicators using self.I and talib
        self.ema5 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period)
        self.sma_vol20 = self.I(talib.SMA, self.data.Volume, timeperiod=self.vol_ma_period)
        self.prev_vol = self.I(talib.SHIFT, self.data.Volume, timeperiod=1)  # Proxy for previous session volume

    def next(self):
        # Decline confirmation: Close below 5-period EMA
        in_decline = self.data.Close[-1] < self.ema5[-1]

        # High "OI" trigger: Volume > 120% of 20-period MA (volume as OI proxy)
        high_vol_trigger = self.data.Volume[-1] > (self.vol_threshold * self.sma_vol20[-1])

        # Entry: Long position simulating bullish put sell (contrarian reversal)
        if in_decline and high_vol_trigger and not self.position:
            entry_price = self.data.Close[-1]
            sl_price = entry_price * (1 - self.sl_pct)
            tp_price = entry_price * (1 + self.tp_pct)
            position_size = int(round(self.size))
            self.buy(size=position_size, sl=sl_price, tp=tp_price)
            print(
                f"🌙 Moon Dev Entry: OpenReversal Long at {entry_price:.2f} BTC | Size: {position_size} | SL: {sl_price:.2f} | TP: {tp_price:.2f} 🚀✨"
            )

        # Exit on "OI reversal": Volume increase >5% (proxy for OI rise signaling renewed pressure)
        if self.position and self.data.Volume[-1] > (self.oi_reversal_threshold * self.data.Volume[-2]):
            self.position.close()
            print(f"🌙 Moon Dev Exit: OI Reversal Signal | Volume Surge Detected ✨🔄")


# Run backtest with initial cash (e.g., 10M USD for large size feasibility)
bt = Backtest(data, OpenReversal, cash=10000000, commission=0.001, exclusive_orders=True)

# Run and print full stats
stats = bt.run()
print(stats)
print(stats._strategy)
