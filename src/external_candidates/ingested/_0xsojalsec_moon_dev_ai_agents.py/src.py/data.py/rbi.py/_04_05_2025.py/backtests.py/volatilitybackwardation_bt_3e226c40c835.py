# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\VolatilityBackwardation_BT.py
# 🌙 Moon Dev Backtest Implementation for VolatilityBackwardation Strategy 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# ========================
# DATA PREPARATION 🌐
# ========================
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"

# Load and clean data
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

# Map columns to backtesting.py format 🗺️
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


# ========================
# STRATEGY IMPLEMENTATION 🚀
# ========================
class VolatilityBackwardation(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌕

    def init(self):
        # 🌗 Volatility Indicators
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 20, name="ATR_20"
        )

        # 🌓 Rolling Percentile Calculation
        def rolling_percentile(series):
            return series.rolling(252).quantile(0.1)

        self.atr_percentile = self.I(rolling_percentile, self.atr, name="ATR_P10")

        # 🌍 VIX Structure Data (assuming vix_front/vix_second columns exist)
        self.vix_front = self.data["vix_front"]
        self.vix_second = self.data["vix_second"]

        print("🌙 Moon Dev Indicators Ready! Tracking cosmic volatility patterns... 🛰️")

    def next(self):
        # 🌑 No position management when in trade
        if self.position:
            trade = self.trades[-1]
            entry_atr = trade.tag["atr_entry"]
            take_profit = trade.entry_price + 2 * entry_atr

            if self.data.High[-1] >= take_profit:
                self.position.close()
                print(
                    f"🌕 Moon Profit Achieved! Closed at {self.data.Close[-1]} (▲ {2*entry_atr:.2f}) 🌙"
                )
            return

        # 🌒 Entry Conditions Check
        current_atr = self.atr[-1]
        atr_threshold = self.atr_percentile[-1]
        vix_confirm = self.vix_front[-1] > self.vix_second[-1]

        if current_atr < atr_threshold and vix_confirm and current_atr != 0:
            # 🌓 Position Sizing with Moon Math 🌌
            risk_amount = self.equity * self.risk_percent
            position_size = int(round(risk_amount / current_atr))

            if position_size > 0:
                self.buy(
                    size=position_size,
                    tag={"atr_entry": current_atr},
                    limit=self.data.Close[-1],
                )
                print(
                    f"🚀 Lunar Launch! Long {position_size} units ▲▲▲ "
                    f"| Entry: {self.data.Close[-1]:.2f} 🌙"
                )


# ========================
# BACKTEST EXECUTION 🔄
# ========================
bt = Backtest(data, VolatilityBackwardation, cash=1_000_000, exclusive_orders=True)
stats = bt.run()

# 🌟 Final Moon Report 🌟
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("Moon Dev Backtest Complete! Cosmic Performance Summary:")
print(stats)
print(stats._strategy)
print("To the moon and beyond! 🚀🌙")
