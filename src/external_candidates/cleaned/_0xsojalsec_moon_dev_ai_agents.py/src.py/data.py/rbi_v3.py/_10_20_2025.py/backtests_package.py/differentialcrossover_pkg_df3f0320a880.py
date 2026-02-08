# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_package\DifferentialCrossover_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(path, parse_dates=["datetime"], index_col="datetime")
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


class DifferentialCrossover(Strategy):
    ema20_period = 20
    sma50_period = 50
    sma200_period = 200
    swing_window = 10
    risk_percent = 0.01
    rr_ratio = 2
    sl_percent_swing = 0.015  # 1.5% below swing low
    sl_percent_sma = 0.01  # 1% below 200 SMA

    def init(self):
        close = self.data.Close
        self.sma50 = self.I(talib.SMA, close, timeperiod=self.sma50_period)
        self.sma200 = self.I(talib.SMA, close, timeperiod=self.sma200_period)
        self.diff = self.sma50 - self.sma200
        self.ema_diff = self.I(lambda: talib.EMA(self.diff.array, timeperiod=self.ema20_period))
        self.ema20p = self.I(talib.EMA, close, timeperiod=self.ema20_period)
        self.trailing_active = False
        self.initial_risk = 0
        print("🌙 Moon Dev: Initialized DifferentialCrossover Strategy ✨")

    def next(self):
        if len(self.data) < self.sma200_period:
            return

        # Exit logic first
        if self.position:
            # Signal exit: Diff crosses below EMA_diff
            if self.diff[-1] < self.ema_diff[-1] and self.diff[-2] >= self.ema_diff[-2]:
                self.position.close()
                print(f"🚀 Moon Dev: Exit on momentum reversal at {self.data.Close[-1]} 🌙")
                self.trailing_active = False

            # Trailing stop logic
            if self.position.pl > self.initial_risk and not self.trailing_active:
                self.trailing_active = True
                print("✨ Moon Dev: Trailing stop activated 🚀")

            if self.trailing_active:
                new_sl = self.ema20p[-1]
                if new_sl > self.position.sl:
                    self.position.sl = new_sl
                    print(f"🌙 Moon Dev: Trailing SL updated to {new_sl:.2f} ✨")

        # Entry logic
        if not self.position:
            if (
                self.sma50[-1] < self.sma200[-1]
                and self.diff[-1] > self.ema_diff[-1]
                and self.diff[-2] <= self.ema_diff[-2]
            ):
                entry_price = self.data.Close[-1]
                print(f"🌙 Moon Dev: Potential entry signal at {entry_price} 🚀")

                # Calculate swing low (past 10 bars, excluding current)
                past_lows = self.data.Low[-self.swing_window - 1 : -1]
                if len(past_lows) == 0:
                    return
                recent_swing_low = past_lows.min()

                # Candidate stops
                sl_swing = recent_swing_low * (1 - self.sl_percent_swing)
                sl_sma = self.sma200[-1] * (1 - self.sl_percent_sma)

                # Choose the one with smaller risk (higher SL price)
                risk_swing = entry_price - sl_swing
                risk_sma = entry_price - sl_sma
                if risk_swing < risk_sma:
                    sl = sl_swing
                else:
                    sl = sl_sma

                if sl >= entry_price:
                    print("⚠️ Moon Dev: Invalid SL (above entry), skipping 🌙")
                    return

                risk = entry_price - sl
                equity = self._broker.get_equity()
                risk_amount = equity * self.risk_percent
                size = risk_amount / risk
                size = int(round(size))

                if size <= 0:
                    print("⚠️ Moon Dev: Position size too small, skipping 🚀")
                    return

                tp = entry_price + self.rr_ratio * risk

                self.buy(size=size, sl=sl, tp=tp)
                self.initial_risk = size * risk
                self.trailing_active = False
                print(
                    f"🌙 Moon Dev: LONG Entry! Price: {entry_price}, Size: {size}, SL: {sl:.2f}, TP: {tp:.2f}, Risk: {risk:.2f} ✨🚀"
                )


bt = Backtest(data, DifferentialCrossover, cash=1000000, commission=0.001)
stats = bt.run()
print(stats)
