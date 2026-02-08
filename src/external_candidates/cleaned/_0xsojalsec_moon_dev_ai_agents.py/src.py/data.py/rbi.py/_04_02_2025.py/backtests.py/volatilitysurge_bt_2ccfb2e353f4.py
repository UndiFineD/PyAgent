# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests\VolatilitySurge_BT.py
# 🌙 Moon Dev's VolatilitySurge Backtest Script 🚀

import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# Clean and prepare moon data 🌑
def prepare_data(path):
    data = pd.read_csv(path)
    # Clean column names
    data.columns = data.columns.str.strip().str.lower()
    # Remove unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
    # Proper case mapping
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
    return data


# Load cosmic data 🌌
data = prepare_data("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")


class VolatilitySurge(Strategy):
    risk_pct = 0.01  # 1% risk per trade 🌕
    atr_multiplier = 1.5
    rr_ratio = 2

    def init(self):
        # 🌗 Calculate volatility indicators using TA-Lib
        self.atr_short = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr_daily = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 96)
        self.atr_daily_ma = self.I(talib.SMA, self.atr_daily, 20 * 96)  # 20-day average

    def next(self):
        if not self.position:
            # 🌑 Check for volatility surge entry condition
            if len(self.atr_short) > 1 and len(self.atr_daily) > 1:
                atr_surge = self.atr_short[-2] > (self.atr_daily[-2] * 1.5)
                volatility_ok = self.atr_daily[-2] > (self.atr_daily_ma[-2] * 0.5)

                if atr_surge and volatility_ok:
                    # 🌕 Calculate moon position size
                    risk_amount = self.equity * self.risk_pct
                    atr_val = self.atr_short[-2]
                    entry_price = self.data.Close[-1]

                    position_size = risk_amount / atr_val
                    position_size = int(round(position_size))

                    if position_size > 0:
                        sl = entry_price - atr_val
                        tp = entry_price + (atr_val * self.rr_ratio)
                        self.buy(
                            size=position_size,
                            sl=sl,
                            tp=tp,
                            tag={"entry_atr": atr_val, "peak_price": entry_price},
                        )
                        print(f"🌕 MOON ENTRY 🌙 | Size: {position_size} @ {entry_price:.2f} | ATR: {atr_val:.2f}")
        else:
            # 🚀 Manage open position
            pos = self.position
            current_high = self.data.High[-1]
            entry_atr = pos.tag["entry_atr"]

            # Update trailing stop
            new_peak = max(pos.tag["peak_price"], current_high)
            trailing_stop = new_peak - (entry_atr * 1.5)
            pos.tag["peak_price"] = new_peak

            # Update stop loss to trailing value
            if trailing_stop > pos.sl:
                pos.sl = trailing_stop
                print(f"🌗 TRAILING STOP 🛡 | New SL: {trailing_stop:.2f}")

            # Check emergency exit
            current_atr = self.atr_short[-1]
            if current_atr < (self.atr_daily[-1] * 0.75):
                self.position.close()
                print(f"🌧 EMERGENCY EXIT 🚨 | ATR Drop: {current_atr:.2f}")


# Launch moon mission 🚀
bt = Backtest(data, VolatilitySurge, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# Print cosmic results 🌠
print("\n🌌 FINAL MOON STATS 🌌")
print(stats)
print("\n🌠 STRATEGY DETAILS 🌠")
print(stats._strategy)
