# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\BandedReversion_BTFinal_WORKING.py
import pandas as pd
import talib
from backtesting import Strategy


class BandedReversion(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade
    atr_multiplier = 2
    bb_period = 20
    bb_dev = 2
    atr_period = 14
    rsi_period = 14
    rsi_threshold = 30

    def init(self):
        # Calculate indicators
        self.ma = self.I(talib.SMA, self.data.Close, timeperiod=self.bb_period)
        upper, middle, lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=self.bb_dev,
            nbdevdn=self.bb_dev,
        )
        self.upper_band = upper
        self.lower_band = lower
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)

    def next(self):
        if len(self.data.Close) < max(self.bb_period, self.atr_period, self.rsi_period) + 1:
            return

        current_price = self.data.Close[-1]
        lower_band = self.lower_band[-1]
        ma = self.ma[-1]
        atr = self.atr[-1]
        rsi = self.rsi[-1]

        # Moon Dev debug prints 🌙
        print(
            f"🌙 Moon Dev Debug: Price={current_price:.2f}, LowerBand={lower_band:.2f}, MA={ma:.2f}, ATR={atr:.2f}, RSI={rsi:.2f}"
        )

        # Entry condition
        if (current_price <= lower_band) and (rsi < self.rsi_threshold):
            if not self.position:
                risk_amount = self.equity * self.risk_per_trade
                stop_loss = current_price - (self.atr_multiplier * atr)
                position_size = risk_amount / (current_price - stop_loss)
                position_size = int(round(position_size))

                print(f"🚀 Moon Dev Entry Signal: BUY at {current_price:.2f}, Size={position_size}, SL={stop_loss:.2f}")
                self.buy(size=position_size, sl=stop_loss)

        # Exit conditions
        if self.position:
            if current_price >= ma:
                print(f"✨ Moon Dev Partial Exit: Closing half position at MA {ma:.2f}")
                self.position.close(0.5)

            if current_price <= (self.trades[-1].entry_price - (self.atr_multiplier * atr)):
                print(f"🌑 Moon Dev Stop Loss Hit: Closing full position at {current_price:.2f}")
                self.position.close()

            if (current_price > ma) and (rsi > 70):
                print(f"🌕 Moon Dev Take Profit: Closing full position at {current_price:.2f}")
                self.position.close()


if __name__ == "__main__":
    from backtesting import Backtest

    data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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
    data["Datetime"] = pd.to_datetime(data["datetime"])
    data = data.set_index("Datetime")

    # Moon Dev warning: Increased initial cash to handle BTC prices 🌙
    bt = Backtest(data, BandedReversion, commission=0.002, exclusive_orders=True, cash=100000)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
