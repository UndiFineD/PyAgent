# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\BandMomentum_BT.py
# 🌙 Moon Dev's BandMomentum Backtest 🌙
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class BandMomentum(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌕

    def init(self):
        # 🚀 Calculate Bollinger Bands
        self.bb_upper = self.I(
            lambda close: talib.BBANDS(
                close, timeperiod=50, nbdevup=2, nbdevdn=2, matype=0
            )[0],
            self.data.Close,
        )
        self.bb_middle = self.I(
            lambda close: talib.BBANDS(
                close, timeperiod=50, nbdevup=2, nbdevdn=2, matype=0
            )[1],
            self.data.Close,
        )
        self.bb_lower = self.I(
            lambda close: talib.BBANDS(
                close, timeperiod=50, nbdevup=2, nbdevdn=2, matype=0
            )[2],
            self.data.Close,
        )

        # 📈 Calculate momentum and direction of lower band
        self.mom_lower = self.I(talib.MOM, self.bb_lower, timeperiod=1)
        self.direction = self.I(lambda x: np.sign(x), self.mom_lower)
        self.cum_prod = self.I(lambda x: x.cumprod(), self.direction)

    def next(self):
        current_idx = len(self.data) - 1

        # 🌙 Wait for indicators to warm up
        if current_idx < 50 or np.isnan(self.cum_prod[current_idx]):
            return

        # 🪐 Get current values
        cum_prod = self.cum_prod[current_idx]
        close = self.data.Close[current_idx]
        bb_upper = self.bb_upper[current_idx]
        bb_lower = self.bb_lower[current_idx]

        # 💰 Calculate position size
        risk_amount = self.equity * self.risk_percent
        position_size = 0

        # 🚀 Long Entry: Cumprod > 0
        if cum_prod > 0 and not self.position:
            sl_price = bb_lower
            risk_per_share = abs(close - sl_price)
            if risk_per_share > 0:
                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    print(
                        f"🌙 MOON DEV LONG SIGNAL 🚀 | Size: {position_size} | Entry: {close:.2f} | SL: {sl_price:.2f}"
                    )

        # 📉 Short Entry: Cumprod < 0
        elif cum_prod < 0 and not self.position:
            sl_price = bb_upper
            risk_per_share = abs(sl_price - close)
            if risk_per_share > 0:
                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    self.sell(size=position_size, sl=sl_price)
                    print(
                        f"🌙 MOON DEV SHORT SIGNAL 📉 | Size: {position_size} | Entry: {close:.2f} | SL: {sl_price:.2f}"
                    )


# 🌙 Data Preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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
data.set_index(pd.to_datetime(data["datetime"]), inplace=True)
data = data[["Open", "High", "Low", "Close", "Volume"]]

# 🚀 Run Backtest
bt = Backtest(data, BandMomentum, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Print Full Stats
print("\n🌙🌕🌗🌓🌒🌑🌑🌒🌓🌗🌕 MOON DEV BACKTEST RESULTS 🌕🌗🌓🌒🌑🌑🌒🌓🌗🌕🌙")
print(stats)
print(stats._strategy)
