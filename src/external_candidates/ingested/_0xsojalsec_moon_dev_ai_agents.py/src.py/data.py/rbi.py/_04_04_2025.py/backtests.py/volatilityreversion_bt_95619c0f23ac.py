# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_04_2025\backtests\VolatilityReversion_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean column names and format
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


class VolatilityReversion(Strategy):
    risk_pct = 0.01  # Risk 1% of equity per trade
    stop_loss_pct = 0.02  # 2% stop loss
    max_holding_bars = 480  # 5 days in 15m intervals (24*4*5=480)

    def init(self):
        # Moon Dev Indicators 🌙
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 20)
        self.atr_percentile = self.I(ta.percentile, self.atr, length=100, percentile=10)
        self.sma200 = self.I(talib.SMA, self.data.Close, 200)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

        print("🌙✨ Moon Dev Strategy Activated! Initialized with:")
        print(f"ATR(20) | SMA200 | RSI(14) | ATR Percentile(10)")

    def next(self):
        # Moon Dev Debug Prints
        if len(self.data) % 1000 == 0:
            print(f"\n🌙 Bar {len(self.data)} | Price: {self.data.Close[-1]:.2f}")
            print(
                f"   ATR: {self.atr[-1]:.2f} | Percentile: {self.atr_percentile[-1]:.2f}"
            )
            print(f"   SMA200: {self.sma200[-1]:.2f} | RSI: {self.rsi[-1]:.2f}")

        # Skip if not enough data
        if len(self.data) < 200 or len(self.atr) < 100:
            return

        # Entry Logic 🌙➡️🚀
        if not self.position:
            atr_condition = self.atr[-1] < self.atr_percentile[-1]
            trend_condition = self.data.Close[-1] > self.sma200[-1]

            if atr_condition and trend_condition:
                # Calculate moon-sized position 🌕
                equity = self.equity
                risk_amount = equity * self.risk_pct
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * (1 - self.stop_loss_pct)
                risk_per_share = entry_price - stop_loss

                position_size = risk_amount / risk_per_share
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss)
                    self.entry_bar = len(self.data)
                    print(
                        f"\n🚀🌕 MOON SHOT! Long {position_size} shares @ {entry_price:.2f}"
                    )
                    print(f"   SL: {stop_loss:.2f} | Risk: {risk_amount:.2f}")

        # Exit Logic 🚀➡️🌙
        if self.position.is_long:
            # RSI Exit
            if crossover(self.rsi, 70):
                self.position.close()
                print(f"\n✨📉 RSI OVERHEAT! Exit @ {self.data.Close[-1]:.2f}")

            # Time Exit
            elif (len(self.data) - self.entry_bar) >= self.max_holding_bars:
                self.position.close()
                print(f"\n🌙⏳ TIME'S UP! Exit @ {self.data.Close[-1]:.2f}")


# Launch Moon Dev Backtest 🚀
bt = Backtest(data, VolatilityReversion, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
