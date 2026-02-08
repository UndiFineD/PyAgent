# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_final\MonthlyHighLeverage_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 MOON DEV DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# 🌌 Cleanse and align cosmic data
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
)[["Open", "High", "Low", "Close", "Volume"]]


class MonthlyHighLeverage(Strategy):
    risk_pct = 0.01  # 🌑 1% risk per cosmic alignment
    week_bars = 5 * 96  # 🌓 5 lunar days in 15m intervals

    def init(self):
        # 🌌 Celestial Indicators
        self.weekly_high = self.I(talib.MAX, self.data.High, timeperiod=self.week_bars)
        self.month_end_mask = self.data.index.to_series().dt.is_month_end

    def next(self):
        current_dt = self.data.index[-1]
        current_open = self.data.Open[-1]
        current_high = self.data.High[-1]

        # 🌕 NEW MOON ENTRY SIGNAL
        if self.month_end_mask[-1] and current_dt.time() == pd.Timestamp("00:00:00").time():
            if not self.position:
                strike_price = self.weekly_high[-1]

                if pd.isna(strike_price) or strike_price <= current_open:
                    print(f"🌘 Void signal - Strike {strike_price} invalid")
                    return

                # 🛰️ Calculate cosmic risk alignment
                risk_amount = self.equity * self.risk_pct
                risk_per_unit = abs(strike_price - current_open)
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    # 🌑 Ensure stop loss is a price level, not distance
                    stop_loss = strike_price
                    self.sell(size=position_size, sl=stop_loss, tag="Moon Put Strike 🎯")
                    print(
                        f"🚀 LAUNCHING SHORT POSITION 🌑\n"
                        f"Size: {position_size} | Entry: {current_open}\n"
                        f"Cosmic Strike: {strike_price} | Risk: {risk_per_unit / current_open:.2%}"
                    )

        # 🌑 LUNAR CYCLE EXIT (End of month closure)
        if self.position and current_dt.time() == pd.Timestamp("23:45:00").time():
            self.position.close()
            print(f"🌕 FULL MOON CLOSURE 🌕\nFinal Price: {self.data.Close[-1]} | P&L: {self.position.pl_pct:.2%}")


# 🌟 STARGAZER BACKTEST
bt = Backtest(data, MonthlyHighLeverage, cash=1_000_000, commission=0.002)
stats = bt.run()

# 📡 TRANSMITTING MOON STATS
print("\n🌙🌙🌙 MOON DEV FINAL TELEMETRY 🌙🌙🌙")
print(stats)
print(stats._strategy)
