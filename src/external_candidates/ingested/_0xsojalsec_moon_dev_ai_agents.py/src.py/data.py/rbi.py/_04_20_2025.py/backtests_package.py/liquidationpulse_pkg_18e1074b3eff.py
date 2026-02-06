# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\LiquidationPulse_PKG.py
import pandas as pd
import pandas_ta as pta
import talib as ta
from backtesting import Backtest, Strategy


class LiquidationPulse(Strategy):
    def init(self):
        self.volatility = self.I(ta.STDDEV, self.data.Close, timeperiod=20)
        self.mean_vol = self.I(ta.SMA, self.volatility, timeperiod=2880)
        self.std_vol = self.I(ta.STDDEV, self.volatility, timeperiod=2880)
        self.median_vol = self.I(pta.median, self.volatility, length=2880)
        self.atr = self.I(ta.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.high_20 = self.I(ta.MAX, self.data.High, 20)
        self.oi_sma = self.I(ta.SMA, self.data.OpenInterest, 5)

    def next(self):
        if self.position:
            if self.volatility[-1] < self.median_vol[-1]:
                self.position.close()
                print(
                    f"🌙 Volatility contraction! Closing Moon Position at {self.data.Close[-1]} ✨"
                )
        else:
            if self.data.BtcDominance[-1] > 45:
                return

            if (
                self.data.FundingRate[-1] < 0
                and self.data.Close[-1] >= 0.99 * self.high_20[-1]
                and self.data.OpenInterest[-1] > self.oi_sma[-1]
            ):

                current_vol = self.volatility[-1]
                mean = self.mean_vol[-1]
                std = self.std_vol[-1]
                z_score = (current_vol - mean) / std if std != 0 else 0

                if z_score > 2.0:
                    atr = self.atr[-1]
                    stop_loss = self.data.Close[-1] + 2 * atr
                    risk_amount = 0.01 * self.equity
                    position_size = int(
                        round(risk_amount / (stop_loss - self.data.Close[-1]))
                    )

                    if position_size > 0:
                        self.sell(size=position_size, sl=stop_loss)
                        print(
                            f"🚀 MOON SHORT! Entry: {self.data.Close[-1]}, Stop: {stop_loss}, Size: {position_size} 🌙"
                        )


# Data preprocessing
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "funding rate": "FundingRate",
        "open interest": "OpenInterest",
        "btc dominance": "BtcDominance",
    }
)

bt = Backtest(data, LiquidationPulse, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
