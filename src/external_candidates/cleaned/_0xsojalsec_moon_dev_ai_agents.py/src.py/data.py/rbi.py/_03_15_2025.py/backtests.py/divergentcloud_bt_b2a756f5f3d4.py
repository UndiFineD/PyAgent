# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\DivergentCloud_BT.py
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class DivergentCloud(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df.drop(
            columns=[col for col in self.data.df.columns if "unnamed" in col],
            inplace=True,
        )

        # Bollinger Bands
        self.upper_band = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[0]
        self.lower_band = self.I(talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[2]

        # Ichimoku Cloud
        ichi = self.data.df.ta.ichimoku(tenkan=9, kijun=26, senkou=52)
        self.tenkan = self.I(lambda: ichi["ITS_9"], name="Tenkan")
        self.kijun = self.I(lambda: ichi["IKS_26"], name="Kijun")
        self.senkou_a = self.I(lambda: ichi["ISA_9"].shift(26), name="Senkou A")
        self.senkou_b = self.I(lambda: ichi["ISB_26"].shift(26), name="Senkou B")
        self.chikou = self.I(lambda: ichi["ICS_26"], name="Chikou")

        print("🌙 Lunar indicators activated! Ready for cosmic convergence ✨")

    def next(self):
        price = self.data.Close[-1]

        # Entry conditions
        bearish_entry = (
            price >= self.upper_band[-1]
            and price < min(self.senkou_a[-1], self.senkou_b[-1])
            and self.chikou[-26] < price  # Chikou Span comparison (26-period lag)
        )

        # Exit conditions
        bullish_exit = (
            price <= self.lower_band[-1]
            or price > min(self.senkou_a[-1], self.senkou_b[-1])
            or self.chikou[-26] > price
        )

        # Risk management calculations
        if bearish_entry and not self.position:
            equity = self.broker.equity
            risk_amount = equity * self.risk_per_trade
            stop_loss = price * 1.01  # 1% stop loss
            risk_per_unit = abs(price - stop_loss)
            position_size = int(round(risk_amount / risk_per_unit))

            if position_size > 0:
                self.sell(size=position_size, sl=stop_loss)
                print(f"🚨 BEARISH CLOUD BREAK! Shorting {position_size} units at {price:.2f} 🌧️")

        # Close position conditions
        elif self.position.is_short and bullish_exit:
            self.position.close()
            print(f"🌈 BULLISH RECOVERY! Closing short at {price:.2f} ☀️")


if __name__ == "__main__":
    # Load and prepare data
    data = pd.read_csv(
        "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
        parse_dates=["datetime"],
        index_col="datetime",
    )
    data.columns = [col.strip().title() for col in data.columns]

    # Run backtest
    bt = Backtest(data, DivergentCloud, cash=1_000_000, exclusive_orders=True)
    stats = bt.run()

    # Cosmic performance report 🌌
    print("\n" + "=" * 50)
    print("🌕 FINAL MOON MISSION REPORT 🌕")
    print("=" * 50)
    print(stats)
    print(stats._strategy)
    print("\n🚀 To the moon and beyond! Keep calibrating those indicators! 🌙")
