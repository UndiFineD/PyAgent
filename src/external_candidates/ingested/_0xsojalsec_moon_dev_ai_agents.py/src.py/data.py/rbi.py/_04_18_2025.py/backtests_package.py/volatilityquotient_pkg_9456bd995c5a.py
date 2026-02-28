# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests_package\VolatilityQuotient_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean column names
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Proper column mapping
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

# Convert datetime and set index
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VolatilityQuotient(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    stop_loss_pct = 0.02  # 2% stop loss
    time_exit_bars = 960  # 10 days in 15m intervals (96 bars/day)

    def init(self):
        # Calculate 1-period returns
        self.returns = self.I(talib.ROCP, self.data.Close, timeperiod=1)

        # 10-period volatility (STDDEV of returns)
        self.hv_10 = self.I(talib.STDDEV, self.returns, timeperiod=10, nbdev=1)

        # 20-period MA of volatility
        self.ma_hv_20 = self.I(talib.SMA, self.hv_10, timeperiod=20)

        # 5-period RSI
        self.rsi_5 = self.I(talib.RSI, self.data.Close, timeperiod=5)

        self.entry_bar = None

    def next(self):
        current_close = self.data.Close[-1]

        # Moon-themed debug prints
        if len(self.hv_10) > 20:
            print(
                f"🌙 Volatility Update | HV_10: {self.hv_10[-1]:.4f} vs MA_20: {self.ma_hv_20[-1]:.4f} | RSI_5: {self.rsi_5[-1]:.2f}"
            )

        # Entry logic: HV crosses below MA(HV)
        if not self.position:
            # Replaced crossover with direct comparison
            if (
                self.ma_hv_20[-2] > self.hv_10[-2]
                and self.ma_hv_20[-1] < self.hv_10[-1]
            ):
                risk_amount = self.equity * self.risk_percent
                stop_loss_price = current_close * (1 - self.stop_loss_pct)
                risk_per_share = current_close - stop_loss_price

                if risk_per_share <= 0:
                    print("🌑 ABORT! Invalid risk calculation")
                    return

                position_size = int(round(risk_amount / risk_per_share))
                if position_size == 0:
                    print("🌑 ABORT! Position size too small")
                    return

                # Execute buy with stop loss
                self.buy(
                    size=position_size,
                    sl=stop_loss_price,
                    tag="🌙 Volatility Breakout Entry",
                )
                self.entry_bar = len(self.data)
                print(
                    f"🚀 LIFTOFF! Long {position_size} units at {current_close:.2f} | SL: {stop_loss_price:.2f}"
                )

        # Exit logic
        else:
            # RSI exit condition - replaced crossover
            if self.rsi_5[-2] < 70 and self.rsi_5[-1] > 70:
                self.position.close()
                print(f"🌑 RSI OVERBOUGHT! Exiting at {current_close:.2f}")
                self.entry_bar = None

            # Time-based exit
            elif self.entry_bar and (
                len(self.data) - self.entry_bar >= self.time_exit_bars
            ):
                self.position.close()
                print(f"⏰ MISSION TIME LIMIT! Exiting at {current_close:.2f}")
                self.entry_bar = None


# Run backtest
bt = Backtest(data, VolatilityQuotient, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
