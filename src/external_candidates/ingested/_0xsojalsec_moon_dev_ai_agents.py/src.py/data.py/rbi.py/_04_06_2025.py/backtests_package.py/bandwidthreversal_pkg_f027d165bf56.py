# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_06_2025\backtests_package\BandwidthReversal_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandwidthReversal(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    stop_loss_pct = 0.03  # 3% stop loss
    take_profit_pct = 0.05  # 5% take profit

    def init(self):
        # Calculate Bollinger Band Width (BBW)
        def calculate_bbw(close):
            upper, middle, lower = talib.BBANDS(
                close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
            )
            return (upper - lower) / middle

        self.bbw = self.I(calculate_bbw, self.data.Close)

        # 20-day low of BBW
        self.bbw_low = self.I(talib.MIN, self.bbw, timeperiod=20)

        # 10-day SMA of BBW
        self.bbw_sma10 = self.I(talib.SMA, self.bbw, timeperiod=10)

        # RSI 14-period
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)

        print("🌙✨ MOON DEV INDICATORS READY FOR LIFTOFF! ✨")

    def next(self):
        price = self.data.Close[-1]

        # Entry logic
        if not self.position:
            # Check BBW at 20-day low (with floating point tolerance)
            bbw_at_low = abs(self.bbw[-1] - self.bbw_low[-1]) < 1e-5

            # Check RSI crosses above 30 (replaced crossover with direct comparison)
            rsi_cross = self.rsi[-2] < 30 and self.rsi[-1] > 30

            if bbw_at_low and rsi_cross:
                # Calculate position size
                risk_amount = self.equity * self.risk_per_trade
                stop_loss_price = price * (1 - self.stop_loss_pct)
                risk_per_share = price - stop_loss_price
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        sl=stop_loss_price,
                        tp=price * (1 + self.take_profit_pct),
                    )
                    print(
                        f"🌙🚀 MOONSHOT ENTRY! 🚀 | Size: {position_size} | Price: {price:.2f} | RSI: {self.rsi[-1]:.2f}"
                    )

        # Exit logic
        else:
            # Volatility expansion exit
            if self.bbw[-1] > self.bbw_sma10[-1]:
                self.position.close()
                print(
                    f"🌑🌊 VOLATILITY TSUNAMI EXIT! | Price: {price:.2f} | BBW: {self.bbw[-1]:.4f}"
                )


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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
data["DateTime"] = pd.to_datetime(data["datetime"])
data = data.set_index("DateTime").drop(columns=["datetime"])

# Launch backtest
bt = Backtest(data, BandwidthReversal, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full moon stats
print("\n🌕🌖🌗🌘🌑 MOON DEV FINAL STATS 🌑🌒🌓🌔🌕")
print(stats)
print("\n🌌 STRATEGY DETAILS 🌌")
print(stats._strategy)
