# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests\VolumetricMomentum_BT.py
import pandas as pd
import talib
from backtesting import Strategy
from backtesting.lib import crossover, crossunder


class VolumetricMomentum(Strategy):
    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(
            columns=[col for col in self.data.df.columns if "unnamed" in col.lower()]
        )

        # Calculate indicators
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )
        self.vwap = self.I(
            talib.SMA,
            (self.data.High + self.data.Low + self.data.Close) / 3 * self.data.Volume,
            timeperiod=20,
        )

        # Custom BILDI calculation (simplified for backtesting)
        self.bildi_bullish = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.bildi_bearish = self.I(talib.MAX, self.data.High, timeperiod=20)

        # Volume moving average for confirmation
        self.vol_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # Track trade information
        self.trade_count = 0
        self.risk_per_trade = 0.01  # 1% risk per trade
        self.size = 1000000  # Fixed size

    def next(self):
        current_price = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # Moon Dev debug prints 🌙
        if len(self.data.Close) % 100 == 0:
            print(
                f"🌙 Moon Dev Update: Current Price={current_price}, ADX={self.adx[-1]}, VWAP={self.vwap[-1]}"
            )

        # Only trade when ADX confirms trend
        if self.adx[-1] < 25:
            return

        # Calculate position size based on risk
        stop_distance = 0.02 * current_price  # 2% stop distance
        position_size = int(round((self.size * self.risk_per_trade) / stop_distance))

        # Long entry conditions
        if (
            current_price > self.bildi_bullish[-1]
            and crossover(self.data.Close, self.vwap)
            and current_volume > self.vol_ma[-1]
        ):

            stop_loss = min(self.data.Low[-20:])
            take_profit = current_price + 2 * (current_price - stop_loss)

            print(
                f"🚀 Moon Dev LONG Signal! Price={current_price}, Size={position_size}"
            )
            self.buy(size=position_size, sl=stop_loss, tp=take_profit)
            self.trade_count += 1

        # Short entry conditions
        elif (
            current_price < self.bildi_bearish[-1]
            and crossunder(self.data.Close, self.vwap)
            and current_volume > self.vol_ma[-1]
        ):

            stop_loss = max(self.data.High[-20:])
            take_profit = current_price - 2 * (stop_loss - current_price)

            print(
                f"🌑 Moon Dev SHORT Signal! Price={current_price}, Size={position_size}"
            )
            self.sell(size=position_size, sl=stop_loss, tp=take_profit)
            self.trade_count += 1

        # Exit if trend weakens
        for trade in self.trades:
            if self.adx[-1] < 20:
                print(f"✨ Moon Dev Exit: ADX weakening, closing trade")
                trade.close()


# Backtest execution
if __name__ == "__main__":
    from backtesting import Backtest

    data = pd.read_csv(
        "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
    )
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

    # Ensure proper column mapping
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    bt = Backtest(data, VolumetricMomentum, commission=0.002)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
