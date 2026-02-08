# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\BandedRSI_Trend_BTFinal_v1.py
import pandas as pd
import talib
from backtesting import Strategy


class BandedRSITrend(Strategy):
    rsi_period = 14
    bb_period = 20
    bb_stddev = 2
    ma_period = 50
    risk_per_trade = 0.01

    def init(self):
        close = self.data.Close

        # Calculate indicators
        self.rsi = self.I(talib.RSI, close, self.rsi_period)
        self.ma = self.I(talib.SMA, close, self.ma_period)

        # Calculate Bollinger Bands on RSI
        self.rsi_upper, self.rsi_mid, self.rsi_lower = self.I(
            talib.BBANDS,
            self.rsi,
            timeperiod=self.bb_period,
            nbdevup=self.bb_stddev,
            nbdevdn=self.bb_stddev,
            matype=0,
        )

        # Track previous RSI for crossover detection
        self.prev_rsi = None

    def next(self):
        if len(self.data.Close) < max(self.rsi_period, self.bb_period, self.ma_period):
            return

        price = self.data.Close[-1]
        rsi = self.rsi[-1]
        ma = self.ma[-1]
        rsi_upper = self.rsi_upper[-1]
        rsi_lower = self.rsi_lower[-1]

        # Calculate position size based on risk
        if self.position:
            current_risk = abs(self.trades[-1].entry_price - self.trades[-1].sl) / self.trades[-1].entry_price
            position_size = int(round((self.equity * self.risk_per_trade) / (current_risk * price)))
        else:
            position_size = int(round(self.equity * 0.1 / price))  # Default size if no position

        # Moon Dev debug prints 🌙
        print(f"🌙 Moon Dev Debug: Price={price:.2f}, RSI={rsi:.2f}, MA={ma:.2f}")
        print(f"✨ RSI Bands: Upper={rsi_upper:.2f}, Lower={rsi_lower:.2f}")

        # Trend direction
        uptrend = price > ma
        downtrend = price < ma

        # Entry conditions
        if not self.position:
            if uptrend and (self.rsi[-2] < self.rsi_lower[-2] and self.rsi[-1] > self.rsi_lower[-1]):
                sl = self.data.Low[-20:-1].min()  # Swing low stop
                print(f"🚀 Moon Dev LONG Signal! Price={price:.2f}, RSI={rsi:.2f}")
                self.buy(size=position_size, sl=sl)

            elif downtrend and (self.rsi[-2] > self.rsi_upper[-2] and self.rsi[-1] < self.rsi_upper[-1]):
                sl = self.data.High[-20:-1].max()  # Swing high stop
                print(f"🌑 Moon Dev SHORT Signal! Price={price:.2f}, RSI={rsi:.2f}")
                self.sell(size=position_size, sl=sl)

        # Exit conditions
        else:
            if self.position.is_long:
                if (self.rsi[-2] > self.rsi_lower[-2] and self.rsi[-1] < self.rsi_lower[-1]) or price < ma:
                    print(f"🌕 Moon Dev Closing LONG: RSI={rsi:.2f}, Price={price:.2f}")
                    self.position.close()
            elif self.position.is_short:
                if (self.rsi[-2] < self.rsi_upper[-2] and self.rsi[-1] > self.rsi_upper[-1]) or price > ma:
                    print(f"🌖 Moon Dev Closing SHORT: RSI={rsi:.2f}, Price={price:.2f}")
                    self.position.close()


if __name__ == "__main__":
    from backtesting import Backtest

    # Load and prepare data
    data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

    # Map columns to backtesting.py format
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    data["Open"] = pd.to_numeric(data["Open"])
    data["High"] = pd.to_numeric(data["High"])
    data["Low"] = pd.to_numeric(data["Low"])
    data["Close"] = pd.to_numeric(data["Close"])
    data["Volume"] = pd.to_numeric(data["Volume"])
    data.index = pd.to_datetime(data["datetime"])

    # Run backtest
    bt = Backtest(data, BandedRSITrend, commission=0.002, exclusive_orders=True)
    stats = bt.run()
    print(stats)
    print(stats._strategy)
