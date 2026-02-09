# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests\VolSpikeBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# Clean column names and format
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


class VolSpikeBreakout(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # Bollinger Bands Upper (20,2)
        def bb_upper(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
            upper, _, _ = talib.BBANDS(
                close,
                timeperiod=timeperiod,
                nbdevup=nbdevup,
                nbdevdn=nbdevdn,
                matype=matype,
            )
            return upper

        self.upper_bb = self.I(
            bb_upper, self.data.Close, timeperiod=20, nbdevup=2, name="UPPER_BB"
        )

        # 20-period SMA for exit
        self.sma = self.I(talib.SMA, self.data.Close, 20, name="SMA_20")

        # 20-period average volume
        self.avg_volume = self.I(talib.SMA, self.data.Volume, 20, name="AVG_VOL")

    def next(self):
        if len(self.data) < 20:
            return  # Skip early bars

        # Moon Dev debug prints 🌙
        if len(self.data) % 100 == 0:
            print(
                f"🌙 Current Bar: {self.data.index[-1]} | Close: {self.data.Close[-1]:.2f} | Upper BB: {self.upper_bb[-1]:.2f} | SMA: {self.sma[-1]:.2f} | Volume: {self.data.Volume[-1]:.2f}"
            )

        # Entry logic ✨
        if not self.position:
            if len(self.data) < 2:
                return

            # Check previous bar's conditions
            prev_close = self.data.Close[-2]
            prev_upper = self.upper_bb[-2]
            prev_vol = self.data.Volume[-2]
            prev_avg_vol = self.avg_volume[-2]

            if prev_close > prev_upper and prev_vol >= 2 * prev_avg_vol:
                entry_price = self.data.Open[-1]
                sl_price = self.data.Low[-2]

                risk_per_share = entry_price - sl_price
                if risk_per_share <= 0:
                    return

                position_size = (self.risk_per_trade * self.equity) / risk_per_share
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    print(
                        f"🌙✨🚀 MOON DEV ENTRY | Size: {position_size} | Entry: {entry_price:.2f} | SL: {sl_price:.2f} | Equity: {self.equity:.2f}"
                    )

        # Exit logic 🌑
        else:
            if self.data.Low[-1] <= self.sma[-1]:
                self.sell()
                print(
                    f"🌙✨🌑 MOON DEV EXIT | Price: {self.data.Close[-1]:.2f} | SMA: {self.sma[-1]:.2f} | PnL: {self.position.pl:.2f}"
                )


# Run backtest with Moon Dev parameters 🌕
bt = Backtest(data, VolSpikeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
