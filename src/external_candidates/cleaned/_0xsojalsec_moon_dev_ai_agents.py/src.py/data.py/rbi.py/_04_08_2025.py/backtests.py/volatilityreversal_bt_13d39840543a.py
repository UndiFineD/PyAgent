# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests\VolatilityReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# =====================
# MOON DEV DATA PREP 🌙
# =====================
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and format columns
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


# =====================
# MOON DEV STRATEGY 🚀
# =====================
class VolatilityReversal(Strategy):
    ema_period_short = 50
    ema_period_long = 200
    adx_period = 14
    risk_pct = 0.02
    atr_multiplier = 2

    def init(self):
        # Moon Dev Indicators ✨
        self.ema50 = self.I(talib.EMA, self.data.Close, self.ema_period_short)
        self.ema200 = self.I(talib.EMA, self.data.Close, self.ema_period_long)
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, self.adx_period)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        # Moon Dev Core Logic 🌑➔🌕
        price = self.data.Close[-1]

        # Entry Signal
        if not self.position:
            if crossover(self.ema50, self.ema200) and self.adx[-1] < 20:
                risk_amount = self.equity * self.risk_pct
                current_atr = self.atr[-1]

                if current_atr > 0:
                    position_size = risk_amount / (self.atr_multiplier * current_atr)
                    position_size = int(round(position_size))

                    if position_size > 0:
                        sl = price - (self.atr_multiplier * current_atr)
                        self.buy(size=position_size, sl=sl)
                        print(
                            f"🌙✨ GOLDEN CROSS ALERT ✨ | Entry: {price:.2f} | Size: {position_size} | SL: {sl:.2f} | ADX: {self.adx[-1]:.1f}"
                        )

        # Exit Signal
        else:
            if self.adx[-1] > 30 and self.adx[-2] <= 30:
                self.position.close()
                print(f"🚀 ADX OVERDRIVE EXIT 🚀 | Price: {price:.2f} | Profit: {self.position.pl_pct:.2f}%")


# =====================
# MOON DEV BACKTEST 🌕
# =====================
bt = Backtest(data, VolatilityReversal, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
