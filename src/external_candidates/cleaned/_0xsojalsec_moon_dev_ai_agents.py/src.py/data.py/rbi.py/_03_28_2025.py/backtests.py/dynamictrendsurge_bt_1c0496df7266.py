# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\DynamicTrendSurge_BT.py
# 🌙✨ Moon Dev's DynamicTrendSurge Backtest Implementation 🚀

import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import TrailingStop


class DynamicTrendSurge(Strategy):
    ema_period_fast = 50
    ema_period_slow = 200
    adx_period = 14
    rsi_period = 14
    atr_period = 14
    risk_pct = 0.01  # 1% risk per trade 🌕

    def init(self):
        # 🌙 TA-Lib Indicators with self.I() wrapper
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_fast)
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_period_slow)
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.adx_period,
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )

    def next(self):
        # 🌑 Need at least 3 bars for crossover checks
        if len(self.data) < 3:
            return

        # 🌙✨ ENTRY LOGIC: Golden Cross + ADX Strength
        if not self.position:
            # Check previous bar's conditions
            prev_ema50 = self.ema50[-2]
            prev_ema200 = self.ema200[-2]
            prev_adx = self.adx[-2]

            # EMA crossover confirmation
            ema_crossover = (prev_ema50 > prev_ema200) and (self.ema50[-3] <= self.ema200[-3])

            # ADX strength confirmation
            adx_strong = (prev_adx > 25) and (self.adx[-3] < prev_adx)

            if ema_crossover and adx_strong:
                # 🚀 Calculate position size with risk management
                atr_value = self.atr[-2]
                risk_amount = self.equity * self.risk_pct
                position_size = int(round(risk_amount / (2 * atr_value)))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        sl=TrailingStop(2 * atr_value),
                        tag="MoonSurgeEntry",
                    )
                    print(f"🌙✨ BUY SIGNAL! Size: {position_size} | Entry: {self.data.Open[-1]:.2f} 🚀")

        # 🌑 EXIT LOGIC: RSI Overbought or Trend Weakness
        else:
            current_rsi = self.rsi[-1]
            current_adx = self.adx[-1]

            if current_rsi > 70:
                self.position.close()
                print(f"🌑✨ SELL SIGNAL! RSI {current_rsi:.1f} >70 | Exit: {self.data.Open[-1]:.2f}")
            elif current_adx < 20:
                self.position.close()
                print(f"🌑✨ SELL SIGNAL! ADX {current_adx:.1f} <20 | Exit: {self.data.Open[-1]:.2f}")


# 🌙 DATA PREPARATION
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# 🧹 Cleanse and format data
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# 🚀 Launch Backtest
bt = Backtest(data, DynamicTrendSurge, cash=1_000_000, trade_on_close=False)
stats = bt.run()

# 🌕 Print Full Results
print("\n" + "=" * 50)
print("🌙✨ MOON DEV BACKTEST RESULTS 🚀🌑")
print("=" * 50)
print(stats)
print(stats._strategy)
