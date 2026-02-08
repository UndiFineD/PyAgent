# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_27_2025\backtests_package\VolumetricBreakout_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolumetricBreakout(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Bollinger Bands indicators
        def bb_upper(close):
            upper, _, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return upper

        self.upper_band = self.I(bb_upper, self.data.Close, name="Upper BB")

        def bb_middle(close):
            _, middle, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return middle

        self.middle_band = self.I(bb_middle, self.data.Close, name="Middle BB")

        # Volume SMA
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20, name="Volume SMA")

        # RSI
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14, name="RSI")

        self.entry_bar = 0  # To track time-based exits

    def next(self):
        if len(self.data) < 20:  # Wait for indicators to warm up
            return

        # Moon Dev Entry Logic 🌙✨
        if not self.position:
            price_break = self.data.Close[-1] > self.upper_band[-1]
            volume_spike = self.data.Volume[-1] >= 2 * self.volume_sma[-1]

            if price_break and volume_spike:
                entry_price = self.data.Close[-1]
                stop_price = self.middle_band[-1]

                if entry_price <= stop_price:
                    self._print(f"🌑 Aborted: Stop {stop_price:.2f} ≥ Entry {entry_price:.2f}")
                    return

                risk_amount = self.equity * self.risk_percent
                risk_per_share = entry_price - stop_price
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_price)
                    self.entry_bar = len(self.data)
                    self._print(f"🚀 LIFTOFF! {position_size} units @ {entry_price:.2f}")
                else:
                    self._print("🌑 Aborted: Position size ≤ 0")

        # Moon Dev Exit Logic 🌙💫
        else:
            # RSI exit (using array comparison instead of crossover)
            rsi_exit = self.rsi[-1] < 70 and self.rsi[-2] >= 70

            # Bollinger Band re-entry exit
            price_exit = self.data.Close[-1] < self.upper_band[-1]

            # Time-based exit (5 days = 480 *15m bars)
            time_exit = (len(self.data) - self.entry_bar) >= 480

            if rsi_exit or price_exit or time_exit:
                self.sell()
                self._print(f"🌕 LANDING! Exit @ {self.data.Close[-1]:.2f}")

    def _print(self, msg):
        print(f"🌙 Moon Dev: {msg}")


# Data preparation 🌙📊
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean and format columns
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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

# Convert index to datetime
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# Launch backtest 🌙🚀
bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
