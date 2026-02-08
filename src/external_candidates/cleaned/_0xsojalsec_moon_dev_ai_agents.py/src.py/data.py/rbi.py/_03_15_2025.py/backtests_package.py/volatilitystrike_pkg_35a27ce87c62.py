# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\VolatilityStrike_PKG.py
# 🌙 Moon Dev's VolatilityStrike Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🚀 DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and prepare data
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


class VolatilityStrike(Strategy):
    risk_per_trade = 0.02  # 2% risk per trade 🌙

    def init(self):
        # ✨ INDICATORS (using talib)
        self.swing_high = self.I(talib.MAX, self.data.High, timeperiod=20, name="SWING_HIGH")
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )
        self.entry_atr = None
        self.entry_bar = None
        self.entry_price = None
        self.entry_risk = None

    def next(self):
        current_idx = len(self.data) - 1

        if not self.position:
            # 🌙 ENTRY LOGIC
            if self.data.High[-1] == self.swing_high[-1] and (self.atr[-1] / self.data.Close[-1]) * 100 >= 2:
                # 🚀 RISK MANAGEMENT
                risk_amount = self.equity * self.risk_per_trade
                stop_loss = self.data.Close[-1] * 1.01  # 1% stop
                take_profit = self.data.Close[-1] * 0.98  # 2% target

                risk_per_unit = stop_loss - self.data.Close[-1]
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    self.sell(size=position_size, sl=stop_loss, tp=take_profit)
                    self.entry_atr = self.atr[-1]
                    self.entry_bar = current_idx
                    self.entry_price = self.data.Close[-1]
                    self.entry_risk = risk_amount

                    print(f"🌙✨ ENTRY: Short {position_size} units at {self.data.Close[-1]:.2f}")
                    print(f"   ATR%: {(self.atr[-1] / self.data.Close[-1]) * 100:.2f}% 🚀")
        else:
            # 🌙 EXIT CONDITIONS
            days_in_trade = (current_idx - self.entry_bar) / 96  # 96=15m bars/day

            # IV Drop Condition
            if (self.entry_atr - self.atr[-1]) / self.entry_atr >= 0.25:
                self.position.close()
                print(f"🌙📉 EXIT: IV dropped 25%! Closed at {self.data.Close[-1]:.2f}")

            # Time Exit (1 day before 7-day expiration)
            elif days_in_trade >= 6:
                self.position.close()
                print(f"🌙⏳ EXIT: 6 days held! Closed at {self.data.Close[-1]:.2f}")

            # Stop Loss (50% of risk)
            elif self.position.pl <= -0.5 * self.entry_risk:
                self.position.close()
                print(f"🌙💥 EXIT: 50% loss hit! Closed at {self.data.Close[-1]:.2f}")


# 🚀 BACKTEST EXECUTION
bt = Backtest(data, VolatilityStrike, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌙 RESULTS
print("\n" + "=" * 50)
print("✨🌙 MOON DEV FINAL STATS 🌙✨")
print("=" * 50)
print(stats)
print(stats._strategy)
