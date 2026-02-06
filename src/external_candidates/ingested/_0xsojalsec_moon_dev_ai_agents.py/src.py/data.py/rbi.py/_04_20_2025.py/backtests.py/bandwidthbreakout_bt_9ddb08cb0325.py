# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests\BandwidthBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandwidthBreakout(Strategy):
    def init(self):
        self.ema50 = self.I(talib.EMA, self.data.Close, 50)

        def calc_bbands(close):
            upper, _, lower = talib.BBANDS(close, 20, 2, 2)
            return upper, lower

        bb_upper, bb_lower = self.I(
            calc_bbands, self.data.Close, name=["BB_upper", "BB_lower"]
        )

        self.bandwidth = self.I(
            lambda u, l: (u - l) / self.I(talib.SMA, self.data.Close, 20),
            bb_upper,
            bb_lower,
        )
        self.bandwidth_low = self.I(talib.MIN, self.bandwidth, 17280)

        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        if not self.position:
            price = self.data.Close[-1]
            ema = self.ema50[-1]
            bw = self.bandwidth[-1]
            bw_low = self.bandwidth_low[-1]
            atr = self.atr[-1]

            if bw == bw_low:
                if price > ema:
                    risk = 0.01 * self.equity
                    size = int(round(risk / (atr * 1)))
                    if size:
                        self.buy(size=size, sl=price - atr, tp=price + 2 * atr)
                        print(
                            f"🌙🚀 LONG! Price: {price:.2f}, Size: {size}, Risk: {atr:.2f}"
                        )
                elif price < ema:
                    risk = 0.01 * self.equity
                    size = int(round(risk / (atr * 1)))
                    if size:
                        self.sell(size=size, sl=price + atr, tp=price - 2 * atr)
                        print(
                            f"🌙💫 SHORT! Price: {price:.2f}, Size: {size}, Risk: {atr:.2f}"
                        )


data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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
data["DateTime"] = pd.to_datetime(data["datetime"])
data = data.set_index("DateTime")

bt = Backtest(data, BandwidthBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
