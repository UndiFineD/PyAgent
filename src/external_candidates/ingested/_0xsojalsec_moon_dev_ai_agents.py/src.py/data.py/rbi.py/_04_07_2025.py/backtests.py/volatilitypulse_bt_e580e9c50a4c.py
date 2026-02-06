# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests\VolatilityPulse_BT.py
# 🌙 Moon Dev's Volatility Pulse Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🚀 DATA PREPARATION
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns
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


class VolatilityPulse(Strategy):
    atr_period = 14
    risk_per_trade = 0.01  # 1% risk

    def init(self):
        # 🌗 INDICATOR CALCULATION
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.atr_period,
            name="ATR",
        )
        self.atr_ma = self.I(talib.SMA, self.atr, 20, name="ATR_MA")
        self.vix_low = self.I(
            talib.MIN, self.data.df["vix"], 1920, name="VIX_LOW"
        )  # 20 days in 15m

        self.trade_stops = {}  # 🌊 Trailing stop tracker

    def next(self):
        price = self.data.Close[-1]

        # 🌈 ENTRY LOGIC
        if not self.position and len(self.atr) > 20:
            atr_cross = (self.atr[-1] > self.atr_ma[-1]) and (
                self.atr[-2] <= self.atr_ma[-2]
            )
            vix_ok = self.data.df["vix"][-1] < self.vix_low[-1]

            if atr_cross and vix_ok:
                risk_amount = self.equity * self.risk_per_trade
                stop_dist = 2 * self.atr[-1]

                if stop_dist > 0:
                    size = int(round(risk_amount / stop_dist))
                    entry_price = self.data.Open[-1]
                    max_size = int(self.cash // entry_price)
                    size = min(size, max_size)

                    if size > 0:
                        self.buy(size=size, tag="🌙 VOLATILITY BREAKOUT")
                        print(f"🚀 ENTRY | Size: {size} BTC | Entry: {entry_price:.2f}")
                        self.trade_stops[self.position.id] = entry_price - stop_dist

        # 🌧️ EXIT LOGIC
        for trade in self.trades:
            if trade.is_long:
                trail_stop = self.data.High[-1] - 2 * self.atr[-1]
                self.trade_stops[trade.id] = max(
                    trail_stop, self.trade_stops.get(trade.id, trail_stop)
                )

                if self.data.Low[-1] < self.trade_stops[trade.id]:
                    self.position.close()
                    print(f"🌧️ EXIT | Price: {price:.2f} | Profit: {trade.pl_pct:.2%}")
                    del self.trade_stops[trade.id]


# 🚀 BACKTEST EXECUTION
bt = Backtest(data, VolatilityPulse, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 RESULTS DISPLAY
print("\n" + "=" * 50)
print("🌙 MOON DEV VOLATILITY PULSE RESULTS 🚀")
print("=" * 50)
print(stats)
print("\nSTRATEGY ANALYSIS:")
print(stats._strategy)
