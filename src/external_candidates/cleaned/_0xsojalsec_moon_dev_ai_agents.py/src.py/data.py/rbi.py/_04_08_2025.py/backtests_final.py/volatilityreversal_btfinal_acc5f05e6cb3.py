# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests_final\VolatilityReversal_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# =====================
# MOON DEV DATA PREP 🌙
# =====================
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean and format columns with Moon Dev precision ✨
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
    adx_period = 14  # Fixed typo from original (was adx_period)
    risk_pct = 0.02
    atr_multiplier = 2

    def init(self):
        # Moon Dev Indicators ✨
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_short)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_long)
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

    def next(self):
        # Moon Dev Core Logic 🌑➔🌕
        price = self.data.Close[-1]

        # Entry Signal (replaced crossover with manual check)
        if not self.position:
            # Bullish EMA crossover detection
            ema_cross = self.ema50[-2] < self.ema200[-2] and self.ema50[-1] > self.ema200[-1]

            if ema_cross and self.adx[-1] < 20:
                risk_amount = self.equity * self.risk_pct
                current_atr = self.atr[-1]

                if current_atr > 0:
                    position_size = risk_amount / (self.atr_multiplier * current_atr)
                    position_size = int(round(position_size))  # Moon Dev precision: whole units only 🚀

                    if position_size > 0:
                        sl = price - (self.atr_multiplier * current_atr)
                        self.buy(size=position_size, sl=sl)
                        print(
                            f"🌙✨ GOLDEN CROSS ALERT ✨🌙 | Entry: {price:.2f} | Size: {position_size} units | SL: {sl:.2f} | ADX: {self.adx[-1]:.1f}"
                        )

        # Exit Signal
        elif self.adx[-1] > 30 and self.adx[-2] <= 30:  # Fixed indentation and added elif
            self.position.close()
            print(
                f"🚀 ADX OVERDRIVE EXIT 🌕🚀 | Price: {price:.2f} | Profit: {self.position.pl_pct:.2f}% | Moon Phase: Profit Harvest"
            )


# =====================
# MOON DEV BACKTEST 🌕
# =====================
bt = Backtest(data, VolatilityReversal, cash=1_000_000, commission=0.002)
stats = bt.run()

# Moon Dev Results Display ✨
print("\n" + "🌙" * 40)
print("MOON DEV BACKTEST RESULTS".center(40))
print("🌙" * 40)
print(stats)
print("\n" + "✨" * 40)
print("STRATEGY PERFORMANCE METRICS".center(40))
print("✨" * 40)
print(stats._strategy)
