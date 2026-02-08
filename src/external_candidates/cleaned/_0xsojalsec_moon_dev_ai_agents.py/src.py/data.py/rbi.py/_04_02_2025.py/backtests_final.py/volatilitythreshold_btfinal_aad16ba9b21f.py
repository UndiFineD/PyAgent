# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests_final\VolatilityThreshold_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and preprocess data with Moon Dev precision 🌙
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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


class VolatilityThreshold(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade (Moon Dev standard)

    def init(self):
        # Calculate indicators with lunar precision 🌕
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=20)
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=19200)  # 200-day SMA (19200 15m periods)

        # Calculate ATR percentile with expanding cosmic window ✨
        def atr_percentile(series):
            return series.expanding().quantile(0.1)

        self.atr_percentile = self.I(atr_percentile, self.atr)

        self.trailing_high = None  # For tracking trailing stop

    def next(self):
        # Moon Dev progress updates (every 1000 bars)
        if len(self.data) % 1000 == 0:
            print(
                f"🌙 Moon Dev Status: Bar {len(self.data)} | Price: {self.data.Close[-1]:.2f} | ATR: {self.atr[-1]:.2f} | ATR Percentile: {self.atr_percentile[-1]:.2f} ✨"
            )

        # Skip if indicators not ready (cosmic alignment not achieved yet)
        if pd.isna(self.atr[-1]) or pd.isna(self.sma200[-1]):
            return

        # Entry logic (when the stars align 🌟)
        if not self.position:
            if (self.atr[-1] < self.atr_percentile[-1]) and (self.data.Close[-1] > self.sma200[-1]):
                # Calculate position size with Moon Dev risk management
                risk_amount = self.equity * self.risk_per_trade
                stop_distance = 2 * self.atr[-1]
                position_size = int(round(risk_amount / stop_distance))  # Ensuring whole units

                if position_size > 0:
                    self.buy(size=position_size)
                    self.trailing_high = self.data.High[-1]
                    print(
                        f"🚀 MOON DEV ENTRY 🚀 | Size: {position_size} | Price: {self.data.Close[-1]:.2f} | ATR Stop: {stop_distance:.2f} | Equity: {self.equity:.2f} 🌙"
                    )

        # Exit logic with trailing stop (protecting lunar gains)
        if self.position:
            current_high = self.data.High[-1]
            if current_high > self.trailing_high:
                self.trailing_high = current_high
                print(f"✨ New Swing High: {self.trailing_high:.2f} ✨")

            current_stop = self.trailing_high - 2 * self.atr[-1]
            if self.data.Low[-1] <= current_stop:
                self.position.close()
                print(
                    f"🌙 MOON DEV EXIT 🌙 | Stop: {current_stop:.2f} | Price: {self.data.Close[-1]:.2f} | P&L: {self.position.pl_pct:.2%} 🛑"
                )


# Run backtest with Moon Dev settings (1M lunar credits)
bt = Backtest(data, VolatilityThreshold, cash=1_000_000, margin=1.0)
stats = bt.run()

# Print full Moon Dev analytics
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST RESULTS:")
print(stats)
print("\nSTRATEGY METRICS:")
print(stats._strategy)
print("🌙 Lunar Mission Complete! 🚀")
