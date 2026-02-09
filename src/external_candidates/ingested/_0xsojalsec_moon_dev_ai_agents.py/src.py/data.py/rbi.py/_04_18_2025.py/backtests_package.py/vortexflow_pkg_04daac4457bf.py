# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests_package\VortexFlow_PKG.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and format data
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class VortexFlow(Strategy):
    def init(self):
        # Calculate indicators with self.I() wrapper
        high, low, close = self.data.High, self.data.Low, self.data.Close

        # Vortex Indicator
        vi = ta.vortex(high=high, low=low, close=close, length=14)
        self.vi_plus = self.I(lambda: vi["VORTEX_14U"], name="VI+")
        self.vi_minus = self.I(lambda: vi["VORTEX_14D"], name="VI-")

        # MFI and Volume MA
        self.mfi = self.I(talib.MFI, high, low, close, self.data.Volume, timeperiod=14)
        self.volume_ma5 = self.I(talib.SMA, self.data.Volume, timeperiod=5)

        # Trend filter and risk management
        self.ma200 = self.I(talib.SMA, close, timeperiod=200)
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=14)

    def next(self):
        # Moon Dev debug prints 🌙
        if len(self.data.Close) < 2:
            return

        current_close = self.data.Close[-1]
        moon_emoji = "🌑🌒🌓🌔🌕🌖🌗🌘"[len(self.data) % 8]

        # Entry logic
        if not self.position:
            # Replaced crossover with direct comparison
            vi_bullish = (self.vi_plus[-2] < self.vi_minus[-2]) and (
                self.vi_plus[-1] > self.vi_minus[-1]
            )
            mfi_bullish = (self.mfi[-2] < 30) and (self.mfi[-1] > 30)
            volume_spike = self.data.Volume[-1] > self.volume_ma5[-1]
            trend_up = current_close > self.ma200[-1]

            if all([vi_bullish, mfi_bullish, volume_spike, trend_up]):
                risk_amount = self.equity * 0.01
                atr_value = self.atr[-1]
                stop_price = current_close - 2 * atr_value
                risk_per_share = current_close - stop_price

                if risk_per_share > 0:
                    size = int(round(risk_amount / risk_per_share))
                    self.buy(size=size, sl=stop_price)
                    print(
                        f"{moon_emoji}✨🚀 MOON ENTRY: {current_close:.2f} | Size: {size} | Risk: {2*atr_value:.2f}"
                    )

        # Exit logic
        else:
            # Replaced crossunder with direct comparison
            bearish_flip = (self.vi_plus[-2] > self.vi_minus[-2]) and (
                self.vi_plus[-1] < self.vi_minus[-1]
            )
            overbought = self.mfi[-1] > 70

            if bearish_flip or overbought:
                self.position.close()
                print(
                    f"{moon_emoji}✨🌑 MOON EXIT: {current_close:.2f} | P&L: {self.position.pl:.2f}"
                )


# Execute backtest
bt = Backtest(data, VortexFlow, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
