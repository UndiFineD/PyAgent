# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_final\ContrarianGapfill_BTFinal_v3.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and clean data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Convert datetime and set index properly
data["Datetime"] = pd.to_datetime(data["datetime"])
data = data.drop("datetime", axis=1)

# Ensure proper column mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Set datetime as index
data = data.set_index("Datetime")
print(f"🌙 Moon Dev Data Loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]} ✨")


class ContrarianGapfill(Strategy):
    gap_threshold = 0.04  # 4% gap down
    rsi_oversold = 30
    volume_multiplier = 1.5
    sl_pct = 0.05  # 5% stop loss
    tp_pct = 0.15  # 15% take profit
    risk_pct = 0.01  # 1% portfolio risk per trade
    vol_period = 20
    rsi_period = 14

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=self.vol_period)
        self.gap_level = None
        print("🌙 Moon Dev ContrarianGapfill Strategy Initialized! Scanning for gaps... ✨")
        print(f"   Indicators ready: RSI period={self.rsi_period}, Vol SMA period={self.vol_period} 🌕")

    def next(self):
        if len(self.data) < max(self.rsi_period, self.vol_period) + 1:
            return

        # If in position, check for gap fill exit
        if self.position:
            if self.gap_level is not None and self.data.Close[-1] >= self.gap_level:
                self.position.close()
                print(f"🌕 Moon Dev Exit: Gap filled at {self.data.Close[-1]:.2f}! Profits secured. 🚀")
            return  # Early return after position check to avoid entry logic

        # Entry logic if no position
        prev_close = self.data.Close[-2]
        curr_open = self.data.Open[-1]
        gap_pct = (prev_close - curr_open) / prev_close

        # Debug print for potential small gaps
        if gap_pct > 0.02:
            vol_ratio = (
                self.data.Volume[-1] / self.volume_sma[-1]
                if not pd.isna(self.volume_sma[-1]) and self.volume_sma[-1] != 0
                else 0
            )
            print(
                f"🌙 Potential Gap Alert: {gap_pct * 100:.2f}% down | RSI: {self.rsi[-1]:.1f} | Vol ratio: {vol_ratio:.2f} | Threshold: {self.gap_threshold * 100:.0f}% ✨"
            )

        # Debug print for potential gaps
        if gap_pct > self.gap_threshold:
            vol_ratio = (
                self.data.Volume[-1] / self.volume_sma[-1]
                if not pd.isna(self.volume_sma[-1]) and self.volume_sma[-1] != 0
                else 0
            )
            print(
                f"🌙 Moon Dev Gap Detected: {gap_pct * 100:.2f}% down | RSI: {self.rsi[-1]:.1f} | Vol ratio: {vol_ratio:.2f} | Threshold met! ✨"
            )

        if (
            gap_pct > self.gap_threshold
            and not pd.isna(self.rsi[-1])
            and self.rsi[-1] < self.rsi_oversold
            and not pd.isna(self.volume_sma[-1])
            and self.data.Volume[-1] > self.volume_sma[-1] * self.volume_multiplier
        ):
            # Additional debug for met conditions
            print(f"🌙 All Entry Conditions Met! Proceeding to calculate size... 🚀")

            self.gap_level = prev_close
            entry = self.data.Close[-1]
            equity = self._broker.getvalue()
            risk_amount = self.risk_pct * equity
            risk_per_unit = entry * self.sl_pct
            size = risk_amount / risk_per_unit
            size = int(round(size))

            print(
                f"   Calculated size: {size} units | Equity: {equity:.2f} | Risk: {risk_amount:.2f} | Entry assumed: {entry:.2f}"
            )

            if size > 0:
                sl_price = entry * (1 - self.sl_pct)
                tp_price = entry * (1 + self.tp_pct)
                self.buy(size=size, sl=sl_price, tp=tp_price)
                print(
                    f"🚀 Moon Dev Entry Alert: {gap_pct * 100:.1f}% gap down on BTC! RSI: {self.rsi[-1]:.1f}, Volume spike detected. Buying {size} units at {entry:.2f} 🌙✨"
                )
            else:
                print(f"   Size calculated as {size} - Skipping trade due to insufficient size 🌙")


# Run backtest
bt = Backtest(data, ContrarianGapfill, cash=1000000, commission=0.001, exclusive_orders=True)
stats = bt.run()
print(stats)
total_trades = stats.get("# Trades", 0)
return_pct = stats.get("Return [%]", 0.0)
print(f"🌙 Moon Dev Backtest Complete! Total Trades: {total_trades} | Return: {return_pct:.2f}% ✨")
