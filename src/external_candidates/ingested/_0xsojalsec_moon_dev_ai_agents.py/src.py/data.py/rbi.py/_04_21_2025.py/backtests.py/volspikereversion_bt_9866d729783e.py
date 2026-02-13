# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests\VolSpikeReversion_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Load and preprocess data
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


class VolSpikeReversion(Strategy):
    def init(self):
        # VVIX Bollinger Bands
        def bb_upper(data):
            upper, _, _ = talib.BBANDS(
                data, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
            )
            return upper

        self.vvix_upper = self.I(bb_upper, self.data.vvix)

        # VVIX SMA
        self.vvix_sma = self.I(talib.SMA, self.data.vvix, 20)

        # Volume averages
        self.vix_vol_avg = self.I(talib.SMA, self.data.vix_volume, 20)
        self.spx_vol_avg = self.I(talib.SMA, self.data.spx_volume, 20)

        # SPX low
        self.spx_low = self.I(talib.MIN, self.data.spx_close, 20)

        self.entry_bar = None

    def next(self):
        price = self.data.Close[-1]
        print(f"🌙 Moon Dev Debug | Bar: {len(self.data)-1} | Price: {price:.2f} ✨")

        if not self.position:
            # Entry conditions
            term_structure = self.data.vix_front[-1] > self.data.vix_second[-1]
            vvix_breakout = self.data.vvix[-1] > self.vvix_upper[-1]
            vol_spike = self.data.vix_volume[-1] > 1.2 * self.vix_vol_avg[-1]
            spx_safe = self.data.spx_close[-1] > self.spx_low[-1]

            if term_structure and vvix_breakout and vol_spike and spx_safe:
                # Position sizing
                risk_amount = self.equity * 0.02
                position_size = int(round(risk_amount / price))

                self.sell(size=position_size)
                self.entry_bar = len(self.data) - 1
                print(f"🌙 MOON DEV SHORT ENTRY | Size: {position_size} 🚀🔥")

        else:
            # Exit conditions
            days_in_trade = (len(self.data) - 1 - self.entry_bar) / (24 * 4)
            vvix_below_sma = self.data.vvix[-1] < self.vvix_sma[-1]
            term_contango = self.data.vix_front[-1] < self.data.vix_second[-1]
            vol_exit = self.data.vix_volume[-1] > 1.1 * self.vix_vol_avg[-1]

            # Stop checks
            vvix_5d_high = self.data.vvix[-1] == max(self.data.vvix[-5 * 24 * 4 :])
            time_exit = days_in_trade >= 5

            if (
                (vvix_below_sma and term_contango and vol_exit)
                or vvix_5d_high
                or time_exit
            ):
                self.position.close()
                print(
                    f"🌙 MOON DEV EXIT | Reason: {'Signal' if not vvix_5d_high else 'Stop'} 🌟"
                )


# Run backtest
bt = Backtest(data, VolSpikeReversion, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
