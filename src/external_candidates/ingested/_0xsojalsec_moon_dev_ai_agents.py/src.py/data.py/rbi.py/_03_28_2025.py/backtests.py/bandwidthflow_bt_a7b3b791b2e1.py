# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\BandwidthFlow_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data 🌙
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
data.set_index(pd.to_datetime(data["datetime"]), inplace=True)
data = data[["Open", "High", "Low", "Close", "Volume"]]


class BandwidthFlow(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Bollinger Bandwidth Calculation ✨
        self.upper_band = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            position=0,
        )
        self.lower_band = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            position=2,
        )
        self.mid_band = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            position=1,
        )
        self.bandwidth = self.I(
            lambda u, l, m: (u - l) / m, self.upper_band, self.lower_band, self.mid_band
        )

        # Volatility Contraction Detection 🌗
        self.bandwidth_low = self.I(talib.MIN, self.bandwidth, timeperiod=20)

        # Money Flow Confirmation 💰
        self.cmf = self.I(
            talib.CMF,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            timeperiod=20,
        )

        # Volatility Expansion Signal 🌊
        self.bandwidth_sma10 = self.I(talib.SMA, self.bandwidth, timeperiod=10)

        self.trailing_high = None

    def next(self):
        price = self.data.Close[-1]

        # Entry Logic 🚀
        if not self.position:
            if self.bandwidth[-1] <= self.bandwidth_low[-1] and crossover(self.cmf, 0):

                # Risk Management Calculation 🌙
                risk_amount = self.equity * self.risk_per_trade
                risk_per_share = price * 0.05  # 5% stop
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size)
                    self.trailing_high = price
                    print(
                        f"🌙✨ MOON DEV ENTRY: Long {position_size} units at {price:.2f}! "
                        f"Volatility squeeze + CMF bullish crossover detected! 🚀"
                    )

        # Exit Logic 🛑
        else:
            # Update trailing high 🌕
            self.trailing_high = max(self.trailing_high, self.data.High[-1])

            # Trailing Stop Check 🔒
            if price < self.trailing_high * 0.95:
                self.position.close()
                print(
                    f"🌙🛑 TRAILING STOP TRIGGERED: Exiting at {price:.2f} "
                    f"({(self.trailing_high - price)/self.trailing_high:.1%} retracement)!"
                )

            # Volatility Expansion Check 🌪️
            elif self.bandwidth[-1] > self.bandwidth_sma10[-1]:
                self.position.close()
                print(
                    f"🌙💨 VOLATILITY EXPANSION: Exiting at {price:.2f}! "
                    f"Bandwidth {self.bandwidth[-1]:.4f} > SMA10 {self.bandwidth_sma10[-1]:.4f}"
                )


# Launch Backtest 🚀🌙
bt = Backtest(data, BandwidthFlow, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
