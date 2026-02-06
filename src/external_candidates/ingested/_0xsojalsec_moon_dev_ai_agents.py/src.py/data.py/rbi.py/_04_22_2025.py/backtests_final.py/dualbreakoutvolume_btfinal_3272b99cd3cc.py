# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\DualBreakoutVolume_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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


class DualBreakoutVolume(Strategy):
    risk_percent = 1.0  # Changed to float for percentage calculation

    def init(self):
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)
        self.volume_avg = self.I(talib.SMA, self.data.Volume, timeperiod=10)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=20)

    def next(self):
        price = self.data.Close[-1]
        vol = self.data.Volume[-1]

        if not self.position:
            # Long entry condition
            if (
                price > self.sma20[-1]
                and price > self.sma50[-1]
                and vol > self.volume_avg[-1]
            ):

                sl = self.swing_low[-1]
                risk = price - sl
                if risk <= 0:
                    print(
                        "🌙⚠️ INVALID RISK | Long Risk:",
                        risk,
                        "| Cosmic Alignment Failed! 🌠",
                    )
                    return

                tp = price + 2 * risk
                position_size = int(
                    round((self.equity * (self.risk_percent / 100)) / risk)
                )
                if position_size > 0:
                    self.buy(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙🚀 LONG ENTRY | Size: {position_size} | Price: {price:.2f} | SL: {sl:.2f} | TP: {tp:.2f} | Moon Rocket Activated! 🌕"
                    )

            # Short entry condition
            elif (
                price < self.sma20[-1]
                and price < self.sma50[-1]
                and vol > self.volume_avg[-1]
            ):

                sl = self.swing_high[-1]
                risk = sl - price
                if risk <= 0:
                    print(
                        "🌙⚠️ INVALID RISK | Short Risk:",
                        risk,
                        "| Black Hole Detected! 🕳️",
                    )
                    return

                tp = price - 2 * risk
                position_size = int(
                    round((self.equity * (self.risk_percent / 100)) / risk)
                )
                if position_size > 0:
                    self.sell(size=position_size, sl=sl, tp=tp)
                    print(
                        f"🌙🌑 SHORT ENTRY | Size: {position_size} | Price: {price:.2f} | SL: {sl:.2f} | TP: {tp:.2f} | Dark Matter Engaged! 🕳️"
                    )

        else:
            # Volume invalidation check
            if vol < self.volume_avg[-1]:
                self.position.close()
                print(
                    f"🌙⚠️ VOLUME COLLAPSE | Exit at {price:.2f} | Cosmic Energy Drained! 🌌"
                )


bt = Backtest(data, DualBreakoutVolume, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
