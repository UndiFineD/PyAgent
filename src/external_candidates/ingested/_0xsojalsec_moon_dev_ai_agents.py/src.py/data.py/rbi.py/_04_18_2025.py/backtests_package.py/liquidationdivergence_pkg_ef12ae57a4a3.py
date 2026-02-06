# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests_package\LiquidationDivergence_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


# Moon Dev Data Preparation 🌙
def load_data(path):
    data = pd.read_csv(path, parse_dates=["datetime"])
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

    # Column mapping with Moon Dev precision ✨
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

    data.set_index("datetime", inplace=True)
    return data


class LiquidationDivergence(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙
    position_size = 1_000_000  # Base equity amount

    def init(self):
        # Liquidation Spike Detection 🌊
        self.long_liq = self.data["long_liq"]  # Assuming liquidation data exists
        self.liq_spike = self.I(talib.MAX, self.long_liq, 96, name="24h Liq Spike")

        # 4h RSI Calculation using Moon Dev Temporal Magic ⏳
        self.rsi_4h = self.I(talib.RSI, self.data.Close, 224, name="4h RSI")

        # Swing Detection System 🌙
        self.swing_high = self.I(talib.MAX, self.data.High, 20, name="Swing High")
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="Swing Low")

        self.last_signal = None

    def next(self):
        # Moon Dev Safety Checks 🌙
        if len(self.data) < 224:
            return

        # Liquidation Spike Condition 🔥
        liq_condition = (
            self.long_liq[-1] > self.liq_spike[-2] * 1.5
            and self.data.Close[-1] < self.data.Close[-96]
        )

        # RSI Divergence Detection 🌗
        rsi_bull_div = (
            self.swing_low[-1] < self.swing_low[-2]
            and self.rsi_4h[-1] > self.rsi_4h[-2]
            and self.rsi_4h[-1] < 30
        )

        # Moon Dev Entry Logic 🚀
        if not self.position and liq_condition and rsi_bull_div:
            # Fibonacci Calculations 🌙
            fib_high = self.swing_high[-96:-1].max()
            fib_low = self.swing_low[-96:-1].min()
            fib_50 = (fib_high + fib_low) * 0.5

            # Risk Management 🌙
            stop_loss = fib_low * 0.995
            risk_amount = self.equity * self.risk_per_trade
            risk_per_unit = self.data.Close[-1] - stop_loss
            units = int(round(risk_amount / risk_per_unit))

            if units > 0:
                self.buy(size=units, sl=stop_loss, tp=fib_50)
                print(
                    f"🌙 MOON DEV LONG SIGNAL 🌙\n"
                    f"Entry: {self.data.Close[-1]:.2f} | "
                    f"Size: {units} | "
                    f"SL: {stop_loss:.2f} | "
                    f"TP: {fib_50:.2f}"
                )

        # Moon Dev Auto-Exit via TP/SL handled by backtesting.py


# Load Moon Dev Market Data 🌙
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
ohlc_data = load_data(data_path)

# Execute Moon Dev Backtest 🌙
bt = Backtest(ohlc_data, LiquidationDivergence, cash=1_000_000)
stats = bt.run()

# Print Full Moon Dev Analytics 🌙
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST RESULTS:")
print(stats)
print(stats._strategy)
print("🌕🌖🌗🌘🌑🌒🌓🌔🌕\n")
