# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests_final\LiquidationReversal_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class LiquidationReversal(Strategy):
    def init(self):
        data = self.data
        self.swing_period = 20

        # Calculate indicators using TA-Lib with self.I()
        self.swing_high = self.I(
            talib.MAX, data.High, timeperiod=self.swing_period, name="Swing High"
        )
        self.swing_low = self.I(
            talib.MIN, data.Low, timeperiod=self.swing_period, name="Swing Low"
        )

        # Calculate Bollinger Bands
        upper, middle, lower = talib.BBANDS(
            data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.bb_upper = self.I(lambda: upper, name="BB Upper")
        self.bb_lower = self.I(lambda: lower, name="BB Lower")
        bb_width = (upper - lower) / middle
        self.bb_width = self.I(lambda: bb_width, name="BB Width")

        # Calculate rolling percentile
        rolling_percentile = bb_width.rolling(672).quantile(0.2)
        self.bb_percentile = self.I(lambda: rolling_percentile, name="BB Percentile")

    def next(self):
        if len(self.data) < 672 or self.bb_percentile[-1] is None:
            return

        price = self.data.Close[-1]
        swing_high = self.swing_high[-1]
        swing_low = self.swing_low[-1]
        bb_width = self.bb_width[-1]
        bb_percentile = self.bb_percentile[-1]

        if not self.position:
            # Long entry logic
            if (
                self.data.Low[-1] < swing_low
                and price > swing_low
                and bb_width < bb_percentile
            ):

                risk_amount = self.equity * 0.01
                sl = swing_low - 0.0001
                risk_per_unit = price - sl
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl, tp=price + 3 * (price - sl))
                    print(
                        f"🌙✨ MOON DEV LONG SIGNAL! Entry: {price:.5f} | Size: {position_size} | SL: {sl:.5f} 🚀"
                    )

            # Short entry logic
            elif (
                self.data.High[-1] > swing_high
                and price < swing_high
                and bb_width < bb_percentile
            ):

                risk_amount = self.equity * 0.01
                sl = swing_high + 0.0001
                risk_per_unit = sl - price
                position_size = int(round(risk_amount / risk_per_unit))

                if position_size > 0:
                    self.sell(size=position_size, sl=sl, tp=price - 3 * (sl - price))
                    print(
                        f"🌙✨ MOON DEV SHORT SIGNAL! Entry: {price:.5f} | Size: {position_size} | SL: {sl:.5f} 🚀"
                    )


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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
data["datetime"] = pd.to_datetime(data["datetime"])
data = data.set_index("datetime")

# Run backtest
bt = Backtest(data, LiquidationReversal, cash=1_000_000, commission=0.002)
stats = bt.run()
print("🌙✨ MOON DEV BACKTEST COMPLETE! ✨🌙")
print(stats)
print(stats._strategy)
