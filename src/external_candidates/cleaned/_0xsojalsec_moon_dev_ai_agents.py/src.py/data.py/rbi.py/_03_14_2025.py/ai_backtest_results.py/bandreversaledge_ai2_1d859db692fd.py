# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\BandReversalEdge_AI2.py
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "datetime": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)


class BandReversalEdge(Strategy):
    risk_percentage = 0.01
    atr_period = 14
    bb_period_20 = 20
    bb_std_20 = 2
    bb_period_50 = 50
    bb_std_50 = 2
    exit_bars = 15

    def init(self):
        # 🌙 Moon Dev Indicators Setup
        close = pd.Series(self.data.Close)
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)

        # 20-period Bollinger Bands
        sma20 = close.rolling(self.bb_period_20).mean()
        std20 = close.rolling(self.bb_period_20).std()

        self.bb_upper_20 = self.I(lambda: sma20 + self.bb_std_20 * std20)
        self.bb_lower_20 = self.I(lambda: sma20 - self.bb_std_20 * std20)

        # 50-period Bollinger Bands
        sma50 = close.rolling(self.bb_period_50).mean()
        std50 = close.rolling(self.bb_period_50).std()

        self.bb_lower_50 = self.I(lambda: sma50 - self.bb_std_50 * std50)

        # ATR for stop loss
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        self.atr = self.I(lambda: tr.rolling(self.atr_period).mean())

        self.entry_bar = 0
        self.stop_loss_price = 0

        print("🌙✨ Moon Dev BandReversalEdge Indicators Activated! 🚀")

    def next(self):
        if not self.position:
            # Entry conditions
            price = self.data.Close[-1]
            bb_l20 = self.bb_lower_20[-1] if not np.isnan(self.bb_lower_20[-1]) else price
            bb_l50 = self.bb_lower_50[-1] if not np.isnan(self.bb_lower_50[-1]) else price
            atr_value = self.atr[-1] if not np.isnan(self.atr[-1]) else 100

            if (price <= bb_l20 * 1.005) and (price <= bb_l50 * 1.005) and atr_value > 0:
                # Calculate position size
                equity = self.equity
                risk_amount = equity * self.risk_percentage
                sl_distance = 1.5 * atr_value
                risk_per_share = sl_distance

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size)
                        self.entry_bar = len(self.data)
                        self.stop_loss_price = price - sl_distance
                        print(
                            f"🌙 Moon Dev Entry Signal 🚀 | Price: {price:.2f} | Size: {position_size} | SL: {self.stop_loss_price:.2f} | Equity: {equity:.2f}"
                        )
        else:
            # Exit conditions
            current_bar = len(self.data)
            bb_u20 = self.bb_upper_20[-1] if not np.isnan(self.bb_upper_20[-1]) else self.data.Close[-1]

            # Profit target check
            if self.data.High[-1] >= bb_u20:
                self.position.close()
                print(f"🎯 Moon Dev Profit Target Hit! | Close: {self.data.Close[-1]:.2f}")
                return

            # Stop loss check
            if self.data.Low[-1] <= self.stop_loss_price:
                self.position.close()
                print(f"🛑 Moon Dev Stop Loss Triggered! | Close: {self.data.Close[-1]:.2f}")
                return

            # Time-based exit
            if current_bar - self.entry_bar >= self.exit_bars:
                self.position.close()
                print(
                    f"⌛ Moon Dev Time Exit | Bars Held: {current_bar - self.entry_bar} | Close: {self.data.Close[-1]:.2f}"
                )


# 🌙🚀 Moon Dev Backtest Execution
print("🌙🚀 Starting BandReversalEdge Backtest...")
bt = Backtest(data, BandReversalEdge, cash=1000000, commission=0.002)
stats = bt.run()
print("\n" + "=" * 60)
print("🌙✨ BAND REVERSAL EDGE STRATEGY RESULTS ✨🌙")
print("=" * 60)
print(stats)
print("\n🚀 Strategy Details:")
print(stats._strategy)
print("=" * 60)
