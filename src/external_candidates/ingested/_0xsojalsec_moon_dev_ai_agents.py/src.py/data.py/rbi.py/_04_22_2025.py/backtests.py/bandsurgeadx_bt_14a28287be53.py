# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_22_2025\backtests\BandSurgeADX_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preprocessing
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


class BandSurgeADX(Strategy):
    def init(self):
        self.upper_band = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2)[0],
            self.data.Close,
            name="Upper BB",
        )
        self.middle_band = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2)[1],
            self.data.Close,
            name="Middle BB",
        )
        self.lower_band = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2)[2],
            self.data.Close,
            name="Lower BB",
        )
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, 14, name="ADX"
        )

    def next(self):
        if len(self.data.Close) < 20:
            return

        current_close = self.data.Close[-1]
        prev_close = self.data.Close[-2] if len(self.data.Close) >= 2 else current_close
        current_upper = self.upper_band[-1]
        prev_upper = self.upper_band[-2] if len(self.upper_band) >= 2 else current_upper
        current_lower = self.lower_band[-1]
        prev_lower = self.lower_band[-2] if len(self.lower_band) >= 2 else current_lower
        current_adx = self.adx[-1]
        prev_adx = self.adx[-2] if len(self.adx) >= 2 else current_adx

        if not self.position:
            risk_percent = 0.01
            risk_amount = self.equity * risk_percent

            # Long entry logic
            if (
                current_close > current_upper
                and prev_close <= prev_upper
                and current_adx > 25
                and current_adx > prev_adx
            ):

                stop_loss = self.middle_band[-1]
                risk_per_share = current_close - stop_loss

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        tp_price = current_close + 2 * risk_per_share
                        print(
                            f"🚀🌙 LONG SURGE! Entry: {current_close:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | TP: {tp_price:.2f}"
                        )
                        self.buy(size=position_size, sl=stop_loss, tp=tp_price)

            # Short entry logic
            elif (
                current_close < current_lower
                and prev_close >= prev_lower
                and current_adx > 25
                and current_adx > prev_adx
            ):

                stop_loss = self.middle_band[-1]
                risk_per_share = stop_loss - current_close

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        tp_price = current_close - 2 * risk_per_share
                        print(
                            f"🌙🚀 SHORT SURGE! Entry: {current_close:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | TP: {tp_price:.2f}"
                        )
                        self.sell(size=position_size, sl=stop_loss, tp=tp_price)


bt = Backtest(
    data, BandSurgeADX, cash=1_000_000, commission=0.002, exclusive_orders=True
)
stats = bt.run()
print(stats)
print(stats._strategy)
